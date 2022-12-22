import mysql.connector
import pandas as pd
import os


def connector():
    conn = mysql.connector.connect(host=os.getenv('MYSQL_HOST'),
                    user=os.getenv('MYSQL_USER'),
                    password=os.getenv('MYSQL_PASSWORD'))
    return conn

class ClientMysql:
    def __init__(self, log:object, table:str = None, df:pd.DataFrame = None):
        self.conn = connector()
        self.df = df
        self.log = log
        self.table = table

    def infering_columns(self) -> list:
        cursor2 = self.conn.cursor()
        query = f"describe challenge.{self.table}"
        cursor2.execute(query)
        records = cursor2.fetchall()
        df = pd.DataFrame(records)
        self.log.info(f'Infered colums:{list(df[0])}')
        return list(df[0])

    def generating_fields(self) -> str:
        self.log.info(f'Generating fields:{self.infering_columns()}')
        return ','.join(self.infering_columns())

    def generating_values(self) -> str:
        self.log.info('Generating Values')
        return ','.join(['%s' for _ in range(len(self.df.keys()))])

    def insert_query(self) -> str:
        query = f"""INSERT into challenge.{self.table} ({self.generating_fields()})
                                        VALUES ({self.generating_values()})"""
        self.log.info(f'Generating Query: {query}')
        return query

    def batch_insert(self) -> list:
        records_to_insert:list = []
        self.log.info(f'Inserting Batch')
        for values in self.df.values:
            records_to_insert.append(tuple(values))
        return records_to_insert

    def inserting_rows(self) -> None:
        insert_query = self.insert_query()
        records_to_insert = self.batch_insert()
        cursor = self.conn.cursor()
        self.log.info(f'Inserting records')
        while records_to_insert:
            if 30000 < len(records_to_insert):
                cursor.executemany(insert_query, records_to_insert[0:30000])
                records_to_insert = records_to_insert[30000:]
            else:
                cursor.executemany(insert_query, records_to_insert)
                records_to_insert = []
        self.conn.commit()
        cursor.close()
        self.conn.close()
    
    def read_query(self) -> str:
        query = f"""select * from challenge.{self.table}"""
        self.log.info(f'Generating Query: {query}')
        return query
    
    def reading_rows(self) -> dict:
        cursor = self.conn.cursor()
        query = self.read_query()
        self.log.info(f'Reading records')
        cursor.execute(query)
        records = cursor.fetchall()
        self.log.info(f'Total records read :{len(records)}')
        cursor.close()
        self.conn.close()
        return records

    def delete_query(self,) -> str:
        query = f"""delete from challenge.{self.table}"""
        self.log.info(f'Generating Query: {query}')
        return query

    def deleting_table(self) -> None:
        cursor = self.conn.cursor()
        query = self.delete_query()
        self.log.info(f'Deleting records')
        cursor.execute(query)
        self.conn.commit()


    def restore_backup(self) -> None:
        self.deleting_table()
        self.inserting_rows()
        self.log.info(f'Restoring Table from Backup')
        

    def df_setter(self, df:pd.DataFrame) -> None:
        self.df = df

    def metrics_queries(self, query:str) -> pd.DataFrame:
        cursor = self.conn.cursor()
        self.log.info(f'Reading records')
        cursor.execute(query)
        records = cursor.fetchall()
        self.log.info(f'Total records read :{len(records)}')
        cursor.close()
        self.conn.close()
        return records
