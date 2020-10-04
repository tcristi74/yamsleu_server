import json
import logging

class Tabel:
    
    @staticmethod
    def __calculate_tabel(self,tabel:dict) ->dict:
        """Calculate the table

        Keyword arguments:
        dic -- input dictionary

        returns the calculated tabel
        """
        logging.debug("calculate tabel")
        return tabel