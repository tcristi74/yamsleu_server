import psycopg2
from psycopg2 import pool
from psycopg2 import extras
import logging
from .db_config import DbConfig
from typing import Tuple
import numbers

query_response = Tuple[object, str]

class DbExecuter:
    '''
    Writes data to postgres 
    '''

    def __init__(self,  db_config_instance:DbConfig):
        '''
        initializes db configuration and postgres connection pool
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

    def get_query(self, query,args=None) ->query_response:
        """
        execute query
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

    # def get_query2(self, tableName,columns,conditions) -> query_response:
    #     '''
    #     get info from table
    #     '''
    #     # get postgres connection
       
    #     logging.info(f"querying table {tableName}")
    #     ps_connection = self.get_connection()
    #     try:
    #         if ps_connection:
    #             logging.info("successfully received connection from connection pool ")
    #             ps_cursor = ps_connection.cursor()
    #             columns_as_string = ",".join(map(str,columns))
    #             fields_names   = list(fields.keys())
    #             conditions_names = list(conditions.keys())
    #             #vaa = ','.join(map(str,[self.nullable_db_string()  for i in range(len(fields))]))
    #             query = f"select {columns_as_string} public.{tableName} set " + \
    #                 ",".join(map(str, [fields_names[i]+ " = %s " for i in range(len(fields_names))]))
    #             args_list = list(fields.values())
    #             if conditions is not None and len(conditions)>0:
    #                 query+=" where " + \
    #                      " and ".join(map(str, [conditions_names[i]+ " = %s " for i in range(len(conditions_names))]))
    #                 args_list+=list(conditions.values())

    #             ps_cursor.execute(query,tuple(args_list))

    #             ps_connection.commit()
    
    #             logging.info("result committed returning ps_connection to pool")
    #             return (None,None)
                
                        
    #     except Exception as ex:
    #         logging.error(ex)
    #         return (None,str(ex))

    #     finally:
    #         self.postgreSQL_pool.putconn(ps_connection)  


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

    #             # ps_cursor = ps_connection.cursor()
    #             #     #query = f"INSERT INTO public.{tableName} (time, CID, api_name,value) VALUES %s"
    #             #     query = f"INSERT INTO public.{tableName} VALUES(%s,%s,%s,%s)"
    #             #     # write batch
    #             #     psycopg2.extras.execute_batch(ps_cursor, query, results)
    #             #     ps_connection.commit()
                
                        
    #     except Exception as ex:
    #         logging.error(ex)
    #         return (None,str(ex))

    #     finally:
    #         self.postgreSQL_pool.putconn(ps_connection)   

    def insert_one_record(self, results, tableName:str, return_column:str=None) -> query_response:
        '''
        write information to db
        :param results: array of rows to be written to databse
        :return:
        '''
        # get postgres connection
       
        logging.info("inserting {0} recs into postgres".format(len(results)))
        ps_connection = self.get_connection()
        ret_val=None
        try:
            if ps_connection:
                logging.info("successfully received connection from connection pool ")
                ps_cursor = ps_connection.cursor()

                columns = ",".join(map(str, results.keys()))
                vaa = ','.join(map(str,['%s' for i in range(len(results))]))
                query = f"INSERT INTO public.{tableName} ( {columns}) VALUES ({vaa})"
                if return_column:
                    query+=f" RETURNING {return_column};"
                ps_cursor.execute(query,tuple(results.values()))
                if return_column:
                    ret_val= ps_cursor.fetchone()[0]
                ps_connection.commit()
                logging.info("result committed returning ps_connection to pool")
                return (ret_val,None)
                
                        
        except Exception as ex:
            logging.error(ex)
            return (None,str(ex))

        finally:
            self.postgreSQL_pool.putconn(ps_connection)    

    def update_records(self, tableName,fields,conditions) -> query_response:
        '''
        write information to db
        :param results: array of rows to be written to databse
        :return:
        '''
        # get postgres connection
       
        logging.info(f"updating table {tableName}")
        ps_connection = self.get_connection()
        try:
            if ps_connection:
                logging.info("successfully received connection from connection pool ")
                ps_cursor = ps_connection.cursor()

                fields_names   = list(fields.keys())
                conditions_names = list(conditions.keys())
                #vaa = ','.join(map(str,[self.nullable_db_string()  for i in range(len(fields))]))
                query = f"update public.{tableName} set " + \
                    ",".join(map(str, [fields_names[i]+ " = %s " for i in range(len(fields_names))]))
                args_list = list(fields.values())
                if conditions is not None and len(conditions)>0:
                    query+=" where " + \
                         " and ".join(map(str, [conditions_names[i]+ " = %s " for i in range(len(conditions_names))]))
                    args_list+=list(conditions.values())

                ps_cursor.execute(query,tuple(args_list))

                ps_connection.commit()
    
                logging.info("result committed returning ps_connection to pool")
                return (None,None)
                
                        
        except Exception as ex:
            logging.error(ex)
            return (None,str(ex))

        finally:
            self.postgreSQL_pool.putconn(ps_connection)    

    def execute(self, query, args,fetch = False) -> query_response:
        '''
        execute query
        :return:
        '''
        # get postgres connection
       
        logging.info("execute query postgres")
        ps_connection = self.get_connection()
        ret_val=None
        try:
            if ps_connection:
                logging.info("successfully received connection from connection pool ")
                ps_cursor = ps_connection.cursor()

                ps_cursor.execute(query,args)
                if fetch:
                    ret_val= ps_cursor.fetchone()[0]
                ps_connection.commit()
                logging.info("result committed returning ps_connection to pool")
                return (ret_val,None)
                
                        
        except Exception as ex:
            logging.error(ex)
            return (None,str(ex))

        finally:
            self.postgreSQL_pool.putconn(ps_connection)        

    def close_resources(self):
        if self.postgreSQL_pool:
            logging.info("closing all db resources!!")
            self.postgreSQL_pool.closeall()

    def nullable_db_val(self,val :str):

        if val is None or val=="":
            return None
        elif (isinstance(val, numbers.Number)):
            return float(val)
        else:
            return val.replace("'","''") 