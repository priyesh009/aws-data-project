# orm/path_registry.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
"""Path tracking utilities, representing mapper graph traversals.

"""

from itertools import chain
import logging

from .base import class_mapper
from .. import exc
from .. import inspection
from .. import util
from ..sql import visitors
from ..sql.traversals import HasCacheKey

log = logging.getLogger(__name__)


def _unreduce_path(path):
    return PathRegistry.deserialize(path)


_WILDCARD_TOKEN = "*"
_DEFAULT_TOKEN = "_sa_default"


class PathRegistry(HasCacheKey):
    """Represent query load paths and registry functions.

    Basically represents structures like:

    (<User mapper>, "orders", <Order mapper>, "items", <Item mapper>)

    These structures are generated by things like
    query options (joinedload(), subqueryload(), etc.) and are
    used to compose keys stored in the query._attributes dictionary
    for various options.

    They are then re-composed at query compile/result row time as
    the query is formed and as rows are fetched, where they again
    serve to compose keys to look up options in the context.attributes
    dictionary, which is copied from query._attributes.

    The path structure has a limited amount of caching, where each
    "root" ultimately pulls from a fixed registry associated with
    the first mapper, that also contains elements for each of its
    property keys.  However paths longer than two elements, which
    are the exception rather than the rule, are generated on an
    as-needed basis.

    """

    __slots__ = ()

    is_token = False
    is_root = False

    _cache_key_traversal = [
        ("path", visitors.ExtendedInternalTraversal.dp_has_cache_key_list)
    ]

    def __eq__(self, other):
        try:
            return other is not None and self.path == other.path
        except AttributeError:
            util.warn(
                "Comparison of PathRegistry to %r is not supported"
                % (type(other))
            )
            return False

    def __ne__(self, other):
        try:
            return other is None or self.path != other.path
        except AttributeError:
            util.warn(
                "Comparison of PathRegistry to %r is not supported"
                % (type(other))
            )
            return True

    def set(self, attributes, key, value):
        log.debug("set '%s' on path '%s' to '%s'", key, self, value)
        attributes[(key, self.natural_path)] = value

    def setdefault(self, attributes, key, value):
        log.debug("setdefault '%s' on path '%s' to '%s'", key, self, value)
        attributes.setdefault((key, self.natural_path), value)

    def get(self, attributes, key, value=None):
        key = (key, self.natural_path)
        if key in attributes:
            return attributes[key]
        else:
            return value

    def __len__(self):
        return len(self.path)

    def __hash__(self):
        return id(self)

    @property
    def length(self):
        return len(self.path)

    def pairs(self):
        path = self.path
        for i in range(0, len(path), 2):
            yield path[i], path[i + 1]

    def contains_mapper(self, mapper):
        for path_mapper in [self.path[i] for i in range(0, len(self.path), 2)]:
            if path_mapper.is_mapper and path_mapper.isa(mapper):
                return True
        else:
            return False

    def contains(self, attributes, key):
        return (key, self.path) in attributes

    def __reduce__(self):
        return _unreduce_path, (self.serialize(),)

    @classmethod
    def _serialize_path(cls, path):
        return list(
            zip(
                [m.class_ for m in [path[i] for i in range(0, len(path), 2)]],
                [path[i].key for i in range(1, len(path), 2)] + [None],
            )
        )

    @classmethod
    def _deserialize_path(cls, path):
        p = tuple(
            chain(
                *[
                    (
                        class_mapper(mcls),
                        class_mapper(mcls).attrs[key]
                        if key is not None
                        else None,
                    )
                    for mcls, key in path
                ]
            )
        )
        if p and p[-1] is None:
            p = p[0:-1]
        return p

    @classmethod
    def serialize_context_dict(cls, dict_, tokens):
        return [
            ((key, cls._serialize_path(path)), value)
            for (key, path), value in [
                (k, v)
                for k, v in dict_.items()
                if isinstance(k, tuple) and k[0] in tokens
            ]
        ]

    @classmethod
    def deserialize_context_dict(cls, serialized):
        return util.OrderedDict(
            ((key, tuple(cls._deserialize_path(path))), value)
            for (key, path), value in serialized
        )

    def serialize(self):
        path = self.path
        return self._serialize_path(path)

    @classmethod
    def deserialize(cls, path):
        if path is None:
            return None
        p = cls._deserialize_path(path)
        return cls.coerce(p)

    @classmethod
    def per_mapper(cls, mapper):
        if mapper.is_mapper:
            return CachingEntityRegistry(cls.root, mapper)
        else:
            return SlotsEntityRegistry(cls.root, mapper)

    @classmethod
    def coerce(cls, raw):
        return util.reduce(lambda prev, next: prev[next], raw, cls.root)

    def token(self, token):
        if token.endswith(":" + _WILDCARD_TOKEN):
            return TokenRegistry(self, token)
        elif token.endswith(":" + _DEFAULT_TOKEN):
            return TokenRegistry(self.root, token)
        else:
            raise exc.ArgumentError("invalid token: %s" % token)

    def __add__(self, other):
        return util.reduce(lambda prev, next: prev[next], other.path, self)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.path)


class RootRegistry(PathRegistry):
    """Root registry, defers to mappers so that
    paths are maintained per-root-mapper.

    """

    inherit_cache = True

    path = natural_path = ()
    has_entity = False
    is_aliased_class = False
    is_root = True

    def __getitem__(self, entity):
        return entity._path_registry


PathRegistry.root = RootRegistry()


class PathToken(HasCacheKey, str):
    """cacheable string token"""

    _intern = {}

    def _gen_cache_key(self, anon_map, bindparams):
        return (str(self),)

    @classmethod
    def intern(cls, strvalue):
        if strvalue in cls._intern:
            return cls._intern[strvalue]
        else:
            cls._intern[strvalue] = result = PathToken(strvalue)
            return result


class TokenRegistry(PathRegistry):
    __slots__ = ("token", "parent", "path", "natural_path")

    inherit_cache = True

    def __init__(self, parent, token):
        token = PathToken.intern(token)

        self.token = token
        self.parent = parent
        self.path = parent.path + (token,)
        self.natural_path = parent.natural_path + (token,)

    has_entity = False

    is_token = True

    def generate_for_superclasses(self):
        if not self.parent.is_aliased_class and not self.parent.is_root:
            for ent in self.parent.mapper.iterate_to_root():
                yield TokenRegistry(self.parent.parent[ent], self.token)
        elif (
            self.parent.is_aliased_class
            and self.parent.entity._is_with_polymorphic
        ):
            yield self
            for ent in self.parent.entity._with_polymorphic_entities:
                yield TokenRegistry(self.parent.parent[ent], self.token)
        else:
            yield self

    def __getitem__(self, entity):
        raise NotImplementedError()


class PropRegistry(PathRegistry):
    is_unnatural = False
    inherit_cache = True

    def __init__(self, parent, prop):
        # restate this path in terms of the
        # given MapperProperty's parent.
        insp = inspection.inspect(parent[-1])
        natural_parent = parent

        if not insp.is_aliased_class or insp._use_mapper_path:
            parent = natural_parent = parent.parent[prop.parent]
        elif (
            insp.is_aliased_class
            and insp.with_polymorphic_mappers
            and prop.parent in insp.with_polymorphic_mappers
        ):
            subclass_entity = parent[-1]._entity_for_mapper(prop.parent)
            parent = parent.parent[subclass_entity]

            # when building a path where with_polymorphic() is in use,
            # special logic to determine the "natural path" when subclass
            # entities are used.
            #
            # here we are trying to distinguish between a path that starts
            # on a the with_polymorhpic entity vs. one that starts on a
            # normal entity that introduces a with_polymorphic() in the
            # middle using of_type():
            #
            #  # as in test_polymorphic_rel->
            #  #    test_subqueryload_on_subclass_uses_path_correctly
            #  wp = with_polymorphic(RegularEntity, "*")
            #  sess.query(wp).options(someload(wp.SomeSubEntity.foos))
            #
            # vs
            #
            #  # as in test_relationship->JoinedloadWPolyOfTypeContinued
            #  wp = with_polymorphic(SomeFoo, "*")
            #  sess.query(RegularEntity).options(
            #       someload(RegularEntity.foos.of_type(wp))
            #       .someload(wp.SubFoo.bar)
            #   )
            #
            # in the former case, the Query as it generates a path that we
            # want to match will be in terms of the with_polymorphic at the
            # beginning.  in the latter case, Query will generate simple
            # paths that don't know about this with_polymorphic, so we must
            # use a separate natural path.
            #
            #
            if parent.parent:
                natural_parent = parent.parent[subclass_entity.mapper]
                self.is_unnatural = True
            else:
                natural_parent = parent
        elif (
            natural_parent.parent
            and insp.is_aliased_class
            and prop.parent  # this should always be the case here
            is not insp.mapper
            and insp.mapper.isa(prop.parent)
        ):
            natural_parent = parent.parent[prop.parent]

        self.prop = prop
        self.parent = parent
        self.path = parent.path + (prop,)
        self.natural_path = natural_parent.natural_path + (prop,)

        self._wildcard_path_loader_key = (
            "loader",
            parent.path + self.prop._wildcard_token,
        )
        self._default_path_loader_key = self.prop._default_path_loader_key
        self._loader_key = ("loader", self.natural_path)

    def __str__(self):
        return " -> ".join(str(elem) for elem in self.path)

    @util.memoized_property
    def has_entity(self):
        return hasattr(self.prop, "mapper")

    @util.memoized_property
    def entity(self):
        return self.prop.mapper

    @property
    def mapper(self):
        return self.entity

    @property
    def entity_path(self):
        return self[self.entity]

    def __getitem__(self, entity):
        if isinstance(entity, (int, slice)):
            return self.path[entity]
        else:
            return SlotsEntityRegistry(self, entity)


class AbstractEntityRegistry(PathRegistry):
    __slots__ = ()

    has_entity = True

    def __init__(self, parent, entity):
        self.key = entity
        self.parent = parent
        self.is_aliased_class = entity.is_aliased_class
        self.entity = entity
        self.path = parent.path + (entity,)

        # the "natural path" is the path that we get when Query is traversing
        # from the lead entities into the various relationships; it corresponds
        # to the structure of mappers and relationships. when we are given a
        # path that comes from loader options, as of 1.3 it can have ac-hoc
        # with_polymorphic() and other AliasedInsp objects inside of it, which
        # are usually not present in mappings.  So here we track both the
        # "enhanced" path in self.path and the "natural" path that doesn't
        # include those objects so these two traversals can be matched up.

        # the test here for "(self.is_aliased_class or parent.is_unnatural)"
        # are to avoid the more expensive conditional logic that follows if we
        # know we don't have to do it.   This conditional can just as well be
        # "if parent.path:", it just is more function calls.
        if parent.path and (self.is_aliased_class or parent.is_unnatural):
            # this is an infrequent code path used only for loader strategies
            # that also make use of of_type().
            if entity.mapper.isa(parent.natural_path[-1].entity):
                self.natural_path = parent.natural_path + (entity.mapper,)
            else:
                self.natural_path = parent.natural_path + (
                    parent.natural_path[-1].entity,
                )
        # it seems to make sense that since these paths get mixed up
        # with statements that are cached or not, we should make
        # sure the natural path is cachable across different occurrences
        # of equivalent AliasedClass objects.  however, so far this
        # does not seem to be needed for whatever reason.
        # elif not parent.path and self.is_aliased_class:
        #     self.natural_path = (self.entity._generate_cache_key()[0], )
        else:
            # self.natural_path = parent.natural_path + (entity, )
            self.natural_path = self.path

    @property
    def entity_path(self):
        return self

    @property
    def mapper(self):
        return inspection.inspect(self.entity).mapper

    def __bool__(self):
        return True

    __nonzero__ = __bool__

    def __getitem__(self, entity):
        if isinstance(entity, (int, slice)):
            return self.path[entity]
        else:
            return PropRegistry(self, entity)


class SlotsEntityRegistry(AbstractEntityRegistry):
    # for aliased class, return lightweight, no-cycles created
    # version
    inherit_cache = True

    __slots__ = (
        "key",
        "parent",
        "is_aliased_class",
        "entity",
        "path",
        "natural_path",
    )


class CachingEntityRegistry(AbstractEntityRegistry, dict):
    # for long lived mapper, return dict based caching
    # version that creates reference cycles

    inherit_cache = True

    def __getitem__(self, entity):
        if isinstance(entity, (int, slice)):
            return self.path[entity]
        else:
            return dict.__getitem__(self, entity)

    def __missing__(self, key):
        self[key] = item = PropRegistry(self, key)

        return item
