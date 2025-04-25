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
    def __init__(self, ticker, api_key= os.environ.get('api_key')):
        self.ticker= ticker
        self.api_key= api_key
    #load data from api
    def get_data_from_api(self):
        #url
        url= f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.ticker}&outputsize=full&apikey={self.api_key}'
        #send get request
        r= requests.get(url)
        #get the json data
        api_data= r.json()
        #convert to pandas df
        df= pd.DataFrame().from_dict(api_data['Time Series (Daily)'], orient='index')
        #set index col name to 'date'
        df.index.name= 'Date'
        #ensure column names are of approriate format
        df.columns= [col[3:].capitalize() for col in df.columns.to_list()]
        #convert to polars df
        df= pl.from_pandas(df, include_index=True)
        #convert columns to their appropriate data types
        df= df.with_columns(
            pl.col('Date').cast(pl.Date),
            pl.col('Open').cast(pl.Float64),
            pl.col('High').cast(pl.Float64),
            pl.col('Low').cast(pl.Float64),
            pl.col('Close').cast(pl.Float64),
            pl.col('Volume').cast(pl.Float64)
        )
        return df
            
class Db_Repo:
    #setup init values
    def __init__(
        self,
        url_object= URL.create(
    "postgresql+psycopg",
    username=f"{os.environ.get('db_username')}",
    password=f"{os.environ.get('db_password')}",
    host=f"{os.environ.get('db_host')}",
    port=f"{os.environ.get('db_port')}",
    database=f"{os.environ.get('db_name')}"
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


        
