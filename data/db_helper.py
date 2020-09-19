from typing import List,Dict
Strings = List[str]

class DbHelper:
    
    @staticmethod
    def dic_to_string(dic:Dict, skip_keys:Strings) -> Strings:
        """Converts a distionary into an array of condtitions
        These conditions can be used later to form sql queries

        Keyword arguments:
        dic -- input dictionary
        skip_keys - array of keys which will be skipped
        
        returns an array of strings
        """
        ret_list = list()
        for k in dic.keys():
            if k in skip_keys:
                continue
            if dic[k] is None:
                ret_list.append(f"{k} = null")
            elif isinstance(dic[k],str):
                clear_str = dic[k].replace("'","''")
                ret_list.append(f"{k} = '{clear_str}'")
            elif isinstance(dic[k],(int,float)):
                # str(dic[k]).replace('.','',1).isdigit()
                ret_list.append(f"{k} = {dic[k]}") 
            else: 
                raise TypeError(f"can't find the type for key:{k}, value: {dic[k]}") 
        return ret_list