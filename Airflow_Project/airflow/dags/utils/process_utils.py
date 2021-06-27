from StringIO import StringIO
import os
import pandas as pd
from datetime import datetime

def process_json(src_dir,tgt_dir,arc_dir=None):
    "This function process JSON data"
    df_list = []
    if os.listdir(src_dir):
        for file in os.listdir(src_dir):
            date = file.split('_')[1][:8]
            with open(src_dir + file,'r') as rawdata:
                filedata= [i.strip() for i in rawdata.readlines()]
            df_file_level =[]
            for row in filedata:
                series = pd.read_json(StringIO(row), typ='series')
                df = pd.DataFrame(series)
                new=df.transpose()
                new['date'] = date
                df_file_level.append(new)
                #df_list.append(new)
            df_file=pd.concat(df_file_level)
            if arc_dir:
                archive_data_parquet(df_file, arc_dir, file)
            df_list.extend(df_file_level)
        final=pd.concat(df_list)
        final['shares'] = final['shares'].apply(lambda x: x.get('count') if type(x) != type(1.1) else 0)
        write_data_csv(final,tgt_dir,'json_processed_' + f'{datetime.now().date()}.csv')
        return True
    else:
        raise FileNotFoundError


def process_csv(src_dir,tgt_dir,arc_dir=None):
    "This function process CSV data"
    df_list=[]
    if os.listdir(src_dir):
        for file in os.listdir(src_dir):
            date = file.split('_')[1][:8]
            df = pd.read_csv(src_dir + file)
            if arc_dir:
                archive_data_parquet(df, arc_dir, file)
            df['date'] = date
            df_list.append(df)
        final=pd.concat(df_list)
        write_data_csv(final,tgt_dir,'csv_processed_' + f'{datetime.now().date()}.csv')
        return True
    else:
        raise FileNotFoundError


def read_csv(src_dir):
    "This function reads CSV data and return DataFrame"
    df_list = []
    for file in os.listdir(src_dir):
        df = pd.read_csv(src_dir + file)
        df_list.append(df)
    final = pd.concat(df_list)
    return final


def archive_data_parquet(dataframe,archive_dir,filename):
    "This function writes dataframe in parquet format"
    dataframe.to_parquet(archive_dir + filename.split('.')[0] + '.parquet', index=False)


def write_data_csv(dataframe,write_dir,filename):
    "This function writes dataframe in CSV format"
    dataframe.to_csv(write_dir + filename.split('.')[0] + '.csv', index=False)


def merge_csv_json_data(json_path,csv_path,merge_dir):
    "This function merge CSV and JSON data"
    df_json = read_csv(json_path)
    df_csv = read_csv(csv_path)
    final = pd.merge(df_csv, df_json, how='inner', on=['post_id', 'date'])
    write_data_csv(final,merge_dir,'merged_' +  f'{datetime.now().date()}.csv')


def delete_files(dir):
    "This function deletes files under a directory"
    file_list = []
    for file in os.listdir(dir):
        file_list.append(file)
        os.remove(dir + file)

