import psycopg2
from psycopg2 import pool
from psycopg2 import extras
import logging
from .db_config import DbConfig
from typing import Tuple

query_response = Tuple[object, str]

class DbExecuter:
    '''
    Writes data to postgres 
    '''

    def __init__(self,  db_config_instance:DbConfig):
        '''
        initializes db configuration and postgres connection pool
        :param logger: logger for writing logs
        '''
        db_config= db_config_instance.get_config()
        # initialize connection pool
        self.postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 2,
                                                                  user=db_config['username'],
                                                                  password=db_config['password'],
                                                                  host=db_config['host'],
                                                                  port=int(db_config['port']),
                                                                  database=db_config['database'])
        logging.info("Connection pool from pgserver created")                                                          

    def get_connection(self):
        '''
        get postgres connection from pool
        :return:
        '''
        if self.postgreSQL_pool:
            ps_connection = self. postgreSQL_pool.getconn()
            if ps_connection:
                logging.info("connection established successfully")
                return ps_connection
            else:
                logging.error("failed to connect to timescale db")
                raise Exception("failed to establish connection to timescale db")

    def get_query(self, query,args,fetch_results = False) ->query_response:
        """
        execute query
        :param results: array of rows to be written to databse
        :return: a collection
        """
        
        # get postgres connection
        
        logging.info("executing query")
        ps_connection = self.get_connection()
        try:
            if ps_connection:
                logging.info("successfully received connection from connection pool ")
                ps_cursor = ps_connection.cursor()
                
                #query = f"INSERT INTO public.{tableName} VALUES(%s,%s,%s,%s)"
                # write batch
                #result = psycopg2.extras.execute_values(ps_cursor, query, args, fetch=fetch_results)
                ps_cursor.execute(query,args)
                records = ps_cursor.fetchall()
                # ps_connection.commit()
                logging.info(f"{len(records)} records returned")
                logging.info("returning ps_connection to pool")
                return (records,None)           
                        
        except Exception as ex:
            logging.error(ex)
            return (None,str(ex)) 
        finally:
            self.postgreSQL_pool.putconn(ps_connection)    


    # def insert_many(self, results, tableName) -> query_response:
    #     """
    #     write multiple records to db using exzecte values
    #     :param results: array of rows to be written to databse
    #     :return:
    #     """
    #     # get postgres connection
       
    #     logging.info("inserting {0} recs into postgres".format(len(results)))
    #     ps_connection = self.get_connection()
    #     try:
    #         if ps_connection:
    #             logging.info("successfully received connection from connection pool ")
    #             ps_cursor = ps_connection.cursor()

    #             columns = ",".join(map(str, results.keys()))
    #             query = f"INSERT INTO public.{tableName} ( {columns}) VALUES %s"

    #             psycopg2.extras.execute_values(ps_cursor,query,  [tuple(results.values())] )      
    #             res = ps_connection.commit()
    #             logging.info("result committed returning ps_connection to pool")
    #             return (res,None)
                
                        
    #     except Exception as ex:
    #         logging.error(ex)
    #         return (None,str(ex))

    #     finally:
    #         self.postgreSQL_pool.putconn(ps_connection)   

    def insert_one_record(self, results, tableName) -> query_response:
        '''
        write information to db
        :param results: array of rows to be written to databse
        :return:
        '''
        # get postgres connection
       
        logging.info("inserting {0} recs into postgres".format(len(results)))
        ps_connection = self.get_connection()
        try:
            if ps_connection:
                logging.info("successfully received connection from connection pool ")
                ps_cursor = ps_connection.cursor()

                columns = ",".join(map(str, results.keys()))
                vaa = ','.join(map(str,['%s' for i in range(len(results))]))
                query = f"INSERT INTO public.{tableName} ( {columns}) VALUES ({vaa})"
                ps_cursor.execute(query,tuple(results.values()))
                ps_connection.commit()
                # val1 = ps_cursor.fetchall()
                # #val = [t[0] for t in ps_cursor.fetchall()]
                logging.info("result committed returning ps_connection to pool")
                return (None,None)
                
                        
        except Exception as ex:
            logging.error(ex)
            return (None,str(ex))

        finally:
            self.postgreSQL_pool.putconn(ps_connection)    

    def execute(self, query, args) -> query_response:
        '''
        execute query
        :return:
        '''
        # get postgres connection
       
        logging.info("execute query postgres")
        ps_connection = self.get_connection()
        try:
            if ps_connection:
                logging.info("successfully received connection from connection pool ")
                ps_cursor = ps_connection.cursor()

                ps_cursor.execute(query,args)
                ps_connection.commit()
                logging.info("result committed returning ps_connection to pool")
                return (None,None)
                
                        
        except Exception as ex:
            logging.error(ex)
            return (None,str(ex))

        finally:
            self.postgreSQL_pool.putconn(ps_connection)        

    def close_resources(self):
        if self.postgreSQL_pool:
            logging.info("closing all db resources!!")
            self.postgreSQL_pool.closeall()
