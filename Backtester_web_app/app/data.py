import requests
import pandas as pd
import polars as pl
from sqlalchemy import create_engine, text,URL 
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

class stock_data_api:
    #setup init variables
    def __init__(self, ticker, api_key= os.environ.get('API_KEY')):
        self.ticker= ticker
        self.api_key= api_key
    #load data from api
    def get_data_from_api(self):
        #extract data from api
        url = f'https://api.twelvedata.com/time_series?symbol={self.ticker}&interval=1day&outputsize=5000&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        #A load and transform data in a pandas dataframe with the following steps
        df= pd.DataFrame().from_dict(data['values']) #1 load the specific json key
        #rename 'datetime' column to 'date'
        df.rename(columns={'datetime':'date'}, inplace=True)
        #capitalize first letter of all column names
        column_list= [column.capitalize() for column in df.columns.to_list()]
        df.columns= column_list
        #set 'date' column as index
        df.set_index('Date', inplace=True)
        #B load pandas dataframe into a polars dataframe with the following steps
        df2= pl.from_pandas(df, include_index=True)
        #convert columns to their appropriate datatypes
        df3= df2.with_columns(
            pl.col('Date').cast(pl.Date),
            pl.col('Open').cast(pl.Float64),
            pl.col('High').cast(pl.Float64),
            pl.col('Low').cast(pl.Float64),
            pl.col('Close').cast(pl.Float64),
            pl.col('Volume').cast(pl.Float64)
        )
        return df3
            
class Db_Repo:
    #setup init values
    def __init__(
        self,
        url_object= URL.create(
    "postgresql+psycopg",
    username=os.environ.get('DB_USERNAME'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT'),
    database=os.environ.get('DB_NAME')
)
    ):
        self.url_object= url_object

    #load data into postgres database
    def insert_data(self, table_name, records):
        #create sqlalchemy engine
        engine= create_engine(self.url_object)
        #setup connection to database
        with engine.connect() as conn:
            n_transactions = records.write_database(table_name=table_name, connection=conn, if_table_exists='replace')
        return n_transactions

    #read data from database
    def read_data(self, table_name):
        #create sqlalchemy engine
        engine= create_engine(self.url_object)
        #sql query to read data from database
        query = f"""
        SELECT * FROM "{table_name}"
        """
        #setup connection to database
        with engine.connect() as conn:
            df = pl.read_database(query, connection=conn)
        return df
