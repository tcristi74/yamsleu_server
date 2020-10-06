import json
import logging

class Tabel():
    
    def calculate_tabel(self,tabel:dict,column_name:str,recalculate:bool) ->dict:
        """Calculate the table

        Keyword arguments:
        dic -- input dictionary

        returns the calculated tabel
        """
        logging.debug("calculate tabel")
        # for column_name in tabel.keys():
        #     if column_name["T"] is not None:

        
        return tabel
    
    def verify_tabel(self,tabel:dict) ->dict:
        """Calculate the table

        Keyword arguments:
        dic -- input dictionary

        returns the calculated tabel
        """
        logging.debug("calculate tabel")
        return tabel
    
    def ___get_one_to_six_sum(self,column:dict)->int:
        rows=["1","2","3","4","5","6"]
        total=0
        # got_X = False
        for row_name in rows:
               if column[row_name] is None:
                   # we have empty spaces, total is not yet to be calculated
                   return None
            #    got_X = True or got_X if column[row_name]=="X" esle got_X
               val+=int(column[row_name]) if  isinstance(column[row_name], int) else 0

        # if got_X:
        #     #we return the value , no extra point added
        #     return val

        # if self.___column_got_X(rows):
        #     #do a simple count 
        #     for row_name in rows:
        #        val+=int(column[row_name]) if  isinstance(column[row_name], int) else 0
        # else:

        return total



     
    def ___column_got_X(self,column:dict,rows:list)->int:
        for row_name in rows:
            if column[row_name]=="X":
                return True
        return False
    
    def ___column_got_X(self,column:dict,rows:list)->int:
        for row_name in rows:
            if column[row_name]=="X":
                return True
        return False

