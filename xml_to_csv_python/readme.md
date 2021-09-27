#  Solution for reading XML data from URL and storing it to CSV file:
In this readme file, I have shared my experience while creating this project, setup instructions, and thoughts.

## Senario

Challenge Link: https://gist.github.com/Koodoo-Tech/d4bb9e402c266224c13d83f7d0b56cd2

## Answers to the questions
- Does it solve/run for the basic case? Yes. As I am able to write the CSV file with all required information.
- Does it handle different scenarios? Not all. As, I and not written the logic to handling dynamic columns
- How portable is it? Very portable. just needs few python modules
- How does someone run it on any machine? Install python 3 +, requests, pandas and xmltodict modules in your system and then execute the app.py using command: python app.py in cmd. 


## Some important project files.
Inside folder xml_to_csv_python/.
- **app.py:**  the main driving code. I have also added comments in the code to explain the steps
link: https://github.com/priyesh009/aws-data-project/blob/master/xml_to_csv_python/app.py
- **Output.csv file:** The target file where you can find source data in csv form.
- **sample.xml:** The source data in XML file.

## Quick Setup Steps
- If you are running in local then install python in you system and then pip install below modules OR Setup and start t2.micro AWS EC2 instance and install python and below modules.
- Login to the instance via putty and Install python, , pandas, etc
- **Required modules**: requests, pandas and xmltodict. Command pip install pandas/requests/xmltodict.

## Quick Execution Setup Steps
- use command : **python app.py** in cmd to execute the app.py which with create two files output.csv and sample.xml.

## Project Development and Pending Enhancements

In this project I have used python, pandas and xmltodict.  

- I have created app.py where I have coded the login to get XML data form URL and then convert it in to CSV file in same directory.

- I complete this Task in a hurry. If I had more time then I would have made used of json_normalization method to properly normalize the nested xml after converting it to json file.

- Or I could have build a logic in the existing code to dynamically handle the columns by iterating over the key in XML/Json data.

- I would have done a better job in displaying the information for columns item_source, item_category and item_guid

- I would have also further cleaned the data.


