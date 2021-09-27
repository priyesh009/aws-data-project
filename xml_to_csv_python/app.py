import xmltodict
import requests
import pandas as pd

xml_filename = 'sample.xml'

def normalize_json(data):
    "Planning to use this in future"
    "This function is used for Normalizing the nested json data"
    new_data = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            new_data[key] = value
        else:
            for k, v in value.items():
                new_data[key + "_" + k] = v

    return new_data

#Get data from URL using request module
try:
    res = requests.get('https://www.europarl.europa.eu/rss/doc/top-stories/en.xml')
    if not res:
        raise Exception
    str_data = res.text
except  Exception as e:
    print('error while retriving data from URL: ' , e , e.__class__)

#Writng XML file in local
try:
    with open(xml_filename, 'w') as file:
        file.write(str_data)
except OSError:
    print ("Could not write file:", xml_filename)
# reading XML file and converting it in to Dict type
try:
    with open("sample.xml", 'r') as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
except OSError:
    print ("Could not open/read file:", xml_filename)


#Reading data under item key and creating Dataframe and appending 'item_'  before column names
df_items = pd.DataFrame(data_dict["rss"]["channel"]["item"]).add_prefix('item_')
#Reading data under channel key and creating Dataframe
df_channel = pd.DataFrame(data_dict["rss"]["channel"])
df_channel.drop(columns='item',inplace=True)
df_channel.dropna(inplace=True,axis=1) # Dropping null columns in our case it is columns description

#merging the two data frame and writing data in csv file in local
result = pd.concat([df_channel, df_items],axis=1, sort=False ,)
try:
    result.to_csv('output.csv' , index=False)
    print('File write sucessful')
except  Exception as e:
    print('error writing Dataframe: ' , e , e.__class__)