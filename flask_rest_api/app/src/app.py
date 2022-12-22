from flask import Flask, jsonify, request
from flask_rest_api.app.clients.ClientSessionMysql import *
from flask_rest_api.app.clients.ClientLogger import *
from setting_config import data_migration_and_creation
import pandavro as pdx
from validations import *
import pandas as pd
import os
import traceback

app = Flask(__name__)
conn = connector()
log = ClientLogger('./api.log', 'api')
log = log.get_log()


@app.route('/migration', methods=['GET'])
def generating_data_migration():
    try:
        log.info('DataBase generated and loaded')
        data_migration_and_creation()
        return jsonify({'message': "Database, tables and Data Migrated", 'Success': True})
    except:
        return jsonify({'message': "Database, tables and Data Could not be created and migrated", 'Success': False})


@app.route('/insert_rows', methods=['POST'])
def insert_data():
    data = request.json
    print(data['messages'])
    df = pd.DataFrame(data['messages'])
    validator_object = Validations(df=df, log=log)
    df_to_be_inserted = validator_object.filtering_data()
    validator_object.doesnt_pass_data_rules()
    if data:
        if not len(data) > 1000 and not len(data) == 0:
            try:
                mysql_object = ClientMysql(df=df_to_be_inserted, log=log, table=data['table'])
                mysql_object.inserting_rows() 
                return jsonify({'message': "Data Inserted.", 'Success': True})
            
            except Exception:
                return jsonify({'message': "Error", 'Success': False})
        
        else:
            return jsonify({'message': "Total Rows sent not allowed. Range Accepted between 1 and 1000", 'Success': False})
    
    else:
        return jsonify({'message': "Invalid Parameters...", 'Success': False})


@app.route('/backup_table', methods=['GET'])
def backup_data():
    if request.args['table']:
        args = request.args
        log.info(f'Args received :{args}')
        table = args['table']
        df = pd.DataFrame()
        try:
            mysql_object = ClientMysql(log=log, table=table)
            data_dict = mysql_object.reading_rows()
            df = pd.DataFrame(data_dict)
            pdx.to_avro(f'.//flask_rest_api//utils//backups//{table}//{table}_bkup.avro', df)
            return jsonify({'message': "Data Backuped.", 'success': True})

        except Exception:
            return jsonify({'message': "Error", 'success': False})

    else:
        return jsonify({'message': "Invalid Parameters...", 'success': False})


@app.route('/restore_table', methods=['GET'])
def restore_data():
    if request.args['table']:
        args = request.args
        table = args['table']
        log.info(f'Args received: {args}')
        if len(os.listdir(f'.//flask_rest_api//utils//backups//{table}')) > 0:
            df = pdx.read_avro(f'.//flask_rest_api//utils//backups//{table}//{table}_bkup.avro')
            log.info(f'Backup found for table :{table}')
            log.info(f'Backup found for table :{df}')
            try:
                mysql_object = ClientMysql(df=df, log=log, table=table)
                mysql_object.restore_backup()
                return jsonify({'message': "Data Restored.", 'success': True})

            except Exception:
                return jsonify({'message': "Error", 'success': False})
        else:
            return jsonify({'message': "No backup file found", 'success': False})
    else:
        return jsonify({'message': "Invalid Parameters...", 'success': False})


@app.route('/hired_by_qs', methods=['GET'])
def hired_by_qs_metrics():
    try:
        with open(".//flask_rest_api//utils//Queries//ETL-hired_by_qs.sql") as file:
            data = file.read()
        query = data.split(';')[0]
        log.info(f'Query for mettrics :{query}')
        mysql_object = ClientMysql(log=log)
        results = mysql_object.metrics_queries(query)
        results_dict = {'department': [], 'job': [], 'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
        for result in results:
            for i, key in enumerate(results_dict.keys()):
                results_dict[key].append(str(result[i]))
        log.info(f'Result obtained :{results_dict}')
        return results_dict
    except Exception:
        return jsonify({'message': f"Error: {traceback.format_exc()}", 'success': False})


@app.route('/hired_over_the_mean', methods=['GET'])
def hired_over_the_mean_metrics():
    try:
        with open(".//flask_rest_api//utils//Queries//ETL-hired_over_the_mean.sql") as file:
            data = file.read()
        query = data.split(';')[0]
        log.info(f'Query for mettrics :{query}')
        mysql_object = ClientMysql(log=log)
        results = mysql_object.metrics_queries(query)
        results_dict = {'id': [], 'department': [], 'hired': []}
        for result in results:
            for i, key in enumerate(results_dict.keys()):
                results_dict[key].append(str(result[i]))
        log.info(f'Result obtained :{results_dict}')
        return results_dict
    except Exception:
        return jsonify({'message': f"Error: {traceback.format_exc()}", 'success': False})


def page_not_found(error):
    return f"<h1>Page not found, error: {error}</h1>", 404


if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.run(port='5001', debug=True)
