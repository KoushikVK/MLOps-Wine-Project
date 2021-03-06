##Read params
#Process #Copy the data to Raw  #Return the data frame
import os
import yaml
import pandas as pd
import argparse

def read_params(config_path):
    with open(config_path) as yaml_file:   #params will be loaded as yaml's
        config = yaml.safe_load(yaml_file)  #params and their datatype

    return config    

#Getting the data from source 
def get_data(config_path):
    config = read_params(config_path)
    data = config["data_source"]["s3_source"] #Data source mentioned in params.yaml
    df = pd.read_csv(data,sep=",",encoding = 'utf-8')
    return df


if __name__ =='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config",default = "params.yaml")
    parsed_args = args.parse_args()
    get_data(config_path = parsed_args.config)
    