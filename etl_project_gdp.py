import requests
import pandas as pd
import sqlite3
import os
from bs4 import BeautifulSoup
import datetime
import numpy as np 


#initialization 

url ='https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ['Country', 'GDP_USD_millions']
db_name ='World_Economies.db'
table_name= 'Countries_by_GDP'
csv_path ='./Countries_by_GDP.csv'


# Code for ETL operations on Country-GDP data

# Importing the required libraries

def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    df = pd.DataFrame(columns = table_attribs)
    tables = soup.find_all('tbody')

    rows = tables[2].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col)!= 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {
                    'Country': col[0].a.contents[0],
                    'GDP_USD_millions':col[2].contents[0]
                }
                df1 = pd.DataFrame(data_dict,index =[0])
                df = pd.concat([df,df1], ignore_index= True)

    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP froml
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    gdp_list = df["GDP_USD_millions"].tolist()
    gdp_list = [float("".join(x.split(','))) for x in gdp_list]
    gdp_list =[np.round(x/1000,2) for x in gdp_list]
    df["GDP_USD_millions"] = gdp_list
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    
    return df

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name,sql_connection, if_existe='replace', index =False)

def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
    
def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''

''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''
df = extract(url, table_attribs)
transform(df)