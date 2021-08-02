'''
The test cases for recursive lambda are under construction
You may use below command in terminal to runt the unittest
Command: python -m unittest test_lambda_handler.py 
'''
from unittest import TestCase
from recursive_lambda import lambda_handler

class  TestFunctions(TestCase):
    def test_for_configFile(self):
        event = 'test'
        context = 'test'
        expected_result = True
        self.assertEqual(lambda_handler(event,context),expected_result)