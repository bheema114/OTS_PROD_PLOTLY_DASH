import pandas as pd
import cx_Oracle
import json

class db_connect:
    @staticmethod 
    def revenue_data():
        # Initialize Oracle client
        cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_18")
        #cx_Oracle.init_oracle_client(lib_dir=r"/opt/OTS_PROD_DASH_APP/instantclient_19_19")


        # Load configuration
        config = json.load(open('config.yaml'))
        db_username = config['db_username']
        db_password = config['db_password']
        db_host = config['db_host']
        db_port = config['db_port']
        db_service = config['db_service']

        # Connect to the database
        dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service)
        connection = cx_Oracle.connect(db_username, db_password, dsn=dsn)

        # Execute SQL queries
        sqlcursor = connection.cursor()
        query_list = ['Revenue_Cash_NonCash.sql', 'Revenue_Cash.sql', 'Revenue_NonCash.sql']
        dfs = {}
        for query in query_list:
            with open(query, 'r') as file:
                sql_script = file.read()

            sql_statements = sql_script.split(';')

            # Execute each SQL statement
            for statement in sql_statements:
                if statement.strip():
                    sqlcursor.execute(statement)

            result = sqlcursor.fetchall()
            if query == query_list[0]:
                dfs['CashNonCash'] = pd.DataFrame(result, columns=["transaction_date",
                                                                    "mid",
                                                                    "station_name",
                                                                    "transactiontype",
                                                                    "payment_type",
                                                                    "payment_mode",
                                                                    "revenue_type",
                                                                    "equipment_id",
                                                                    "transaction_count",
                                                                    "income",
                                                                    "outgoing",
                                                                    "total"
                                                                ])
            elif query == query_list[1]:
                dfs['Cash'] = pd.DataFrame(result, columns=["transaction_date",
                                                    "mid", "station_name",
                                                    "transactiontype",
                                                    "equipment_id",
                                                    "payment_type",
                                                    "payment_mode",
                                                    "revenue_type",
                                                    "transaction_count",
                                                    "income",
                                                    "outgoing",
                                                    "total"
                                                    ])
            else:
                dfs['NonCash'] = pd.DataFrame(result, columns=["transaction_date",
                                                    "mid", "station_name",
                                                    "transactiontype",
                                                    "equipment_id",
                                                    "payment_type",
                                                    "payment_mode",
                                                    "revenue_type",
                                                    "transaction_count",
                                                    "income",
                                                    "outgoing",
                                                    "total"
                                                    ])
        # Close the database connection
        sqlcursor.close()
        connection.close()
        return dfs
    
    @staticmethod 
    def riderhip_data():
        # Initialize Oracle client
        # cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_18")

        # Load configuration
        config = json.load(open('config.yaml'))
        db_username = config['db_username']
        db_password = config['db_password']
        db_host = config['db_host']
        db_port = config['db_port']
        db_service = config['db_service']

        # Connect to the database
        dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service)
        connection = cx_Oracle.connect(db_username, db_password, dsn=dsn)

        # Execute SQL queries
        sqlcursor = connection.cursor()
        query_list = ['Ridership_all.sql']
        dfr = {}
        for query in query_list:
            with open(query, 'r') as file:
                sql_script = file.read()

            sql_statements = sql_script.split(';')

            # Execute each SQL statement
            for statement in sql_statements:
                if statement.strip():
                    sqlcursor.execute(statement)

            result = sqlcursor.fetchall()
            if query == query_list[0]:
                dfr['Ridership'] = pd.DataFrame(result, columns=['Station',
                                                                'Equip Grp ID',
                                                                'Equip ID',
                                                                'Exit Count',
                                                                'Exit TRX DATE',
                                                                'Entry Count',
                                                                'Entry TRX DATE',
                                                                'TRX TYPE',
                                                                'TRX SEQ NUM',
                                                                'LINE ID',
                                                                'AQUIRER ID',
                                                                'OPERATOR ID',
                                                                'TERMINAL ID',
                                                                'CARD TYPE',
                                                                'PANSHA',
                                                                'PRODUCT TYPE',
                                                                'TRX AMOUNT',
                                                                'CARD BALANCE',
                                                                'PAYTM TID',
                                                                'PAYTM MID',
                                                                'INSERT DATE'
                                                                ])
        # Close the database connection
        sqlcursor.close()
        connection.close()
        return dfr
    
    @staticmethod 
    def stock_data():
        # Initialize Oracle client
        # cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_18")

        # Load configuration
        config = json.load(open('config.yaml'))
        db_username = config['db_username']
        db_password = config['db_password']
        db_host = config['db_host']
        db_port = config['db_port']
        db_service = config['db_service']

        # Connect to the database
        dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service)
        connection = cx_Oracle.connect(db_username, db_password, dsn=dsn)

        # Execute SQL queries
        sqlcursor = connection.cursor()
        query_list = ['stock copy.sql']
        dfst = {}
        for query in query_list:
            with open(query, 'r') as file:
                sql_script = file.read()

            sql_statements = sql_script.split(';')

            # Execute each SQL statement
            for statement in sql_statements:
                if statement.strip():
                    sqlcursor.execute(statement)

            result = sqlcursor.fetchall()
            if query == query_list[0]:
                dfst['stock'] = pd.DataFrame(result,columns=['Category',
                                                             'Count',
                                                             'station_id',
                                                             'product_id'
                                                             ])
        
        sqlcursor.close()   
        connection.close()
        return dfst
       

dfs = db_connect.revenue_data()
dfr = db_connect.riderhip_data()
dfst = db_connect.stock_data()