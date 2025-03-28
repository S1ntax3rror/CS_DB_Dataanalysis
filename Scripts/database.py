import os
import traceback
from argparse import ArgumentError
import connectorx as cx
import pandas as pd

import psycopg

class Database:
    """
    Handles PostgreSQL Database connection and conversation
    """
    def __init__(self, dbname='CSGODatabase', user='postgres', password='postgres', host='localhost', port='5000'):
        self.conn = None
        self.cur = None
        self.connect(dbname, user, password, host, port)

        self.CONNECTION_STRING = "postgresql://postgres:postgres@localhost:5000/CSGODatabase"

    def connect(self, dbname, user, password, host, port):
        """
        Connect to CSGO Database
        """
        self.conn = psycopg.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def close(self):
        """
        Disconnect from CSGO Database
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cur = None

    def init_file(self, file: str):
        """
        Initialise a .sql file into the database
        :param file: File to be initialised
        """
        try:
            if not file.endswith('.sql'):
                raise ArgumentError

            self.cur.execute(open(file, 'r').read())
        except Exception as E:
            self.conn.rollback()
            print(f'Error reading file')
            print(E)
            print(traceback.format_exc())
        self.conn.commit()

    def init_files(self, dir: str):
        """
        Initialise multiple .sql files into the database
        :param dir: Directory containing .sql files
        """
        try:
            for file in os.listdir(dir):
                if file.endswith('.sql'):
                    self.cur.execute(open(f'{dir}/{file}').read())
                    print(f'-- {file} executed')
        except Exception as E:
            self.conn.rollback()
            print(f'Error reading files')
            print(E)
            print(traceback.format_exc())
        self.conn.commit()

    def query(self, query: str) -> pd.DataFrame:
        """
        Execute a query on the database
        Uses the connector-x library for querying. Partitions normally the query on the gameid attribute. If not present, it will just execute the query without partitioning.
        :param query: Query to be executed
        """
        if 'gameid' in query:
            table = cx.read_sql(self.CONNECTION_STRING, query, partition_on="gameid", partition_num=10, return_type="arrow", protocol="binary")
        else:
            table = cx.read_sql(self.CONNECTION_STRING, query, return_type="arrow", protocol="binary")

        df = table.to_pandas(split_blocks = False, date_as_object = False)
        return df

    def dump_database(self):
        tables = self.query("""
            SELECT * FROM pg_tables
            WHERE schemaname = 'public'
        """)
        print("Copying Database to CSV")
        for table_name in tables['tablename']:
            print(f"Copying table {table_name} to CSV")

            # Ensure the output directory exists
            os.makedirs("../Datasets/DataDump/", exist_ok=True)
            with open(f"../Datasets/DataDump/{table_name}.csv", "wb") as f:
                with self.cur.copy(f"COPY {table_name} TO STDOUT WITH DELIMITER ';'") as copy:
                    for data in copy:
                        f.write(data)
        print("Finished copying data")

if __name__ == '__main__':
    db = Database()
   # db.init_files('../SQL/Indexes')
    #db.init_files('../SQL/Tables')
    #db.init_files('../SQL/MarketTables')
    #db.init_files('../SQL/Keys')
    #db.init_files('../SQL/Constraints')
    db.init_file('../SQL/MaterializedViews/GameView.sql')
    db.init_file('../SQL/MaterializedViews/GameFrameView.sql')
    #db.init_file('../SQL/Keys_and_Constrains_steamApi/PrimaryKeys.sql')
    #db.init_file('../SQL/Keys_and_Constrains_steamApi/ForeignKeys.sql')
    #db.dump_database()
