import os
import pandas as pd
from flask_rest_api.app.clients.ClientLogger import ClientLogger
from flask_rest_api.app.clients.ClientSessionMysql import ClientMysql, connector
from flask_rest_api.app.src.validations import *
import os

conn = connector()

def data_migration_and_creation():
    log = ClientLogger('./api.log', 'api')
    log = log.get_log()
    path = ".//flask_rest_api//utils//Data//"
    files = os.listdir(path)
    files = [path + file for file in files]
    tables = ['employes', 'departments', 'jobs']
    cursor = conn.cursor()
    with open(".//flask_rest_api//utils//Queries//DDL-create_tables.sql") as file:
        data = file.read()

    data = data.split(';')[:-1]

    #validates that database doesnt' exist, so it's the first time
    #running the compose, and it doesn't duplicate info
    cursor.execute('show databases')
    databases = list(cursor.fetchall())
    if not ('challenge',) in databases:

        #generates database and creates tables
        for query in data:
            log.info(f'Query ran {query}')

            if query:
                cursor.execute(query)
                conn.commit()

        #fills tables with files info
        if files:
            for file, table in zip(files, tables):
                log.info(f'About to insert file info: {file}')
                df = pd.read_csv(file)
                validator_object = Validations(df=df, log=log)
                df_to_be_inserted = validator_object.filtering_data()
                validator_object.doesnt_pass_data_rules()
                mysql_object = ClientMysql(df=df_to_be_inserted , table=table, log=log)
                mysql_object.inserting_rows() 
