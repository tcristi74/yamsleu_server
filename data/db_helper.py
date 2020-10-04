from typing import List,Dict
Strings = List[str]
recordset = List[tuple]

class DbHelper:
    
    @staticmethod
    def dic_to_string(dic:Dict, skip_keys:Strings) -> Strings:
        """Converts a dictionary into an array of condtitions
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

    @staticmethod
    def recordset_to_dic(columns:List,records:recordset,start_at=0)->list:
        rows = []
        for r in records:
            # r is a tuple
            row = {}
            for i in range(len(r)):
                if i<start_at:
                    continue
                if i-start_at>=len(columns):
                    break
                # we clean column name prefix 
                clean_column = columns[i-start_at] if len(columns[i-start_at].split("."))==1 else columns[i-start_at].split(".")[1] 
                #we clean column name use with " as"
                clean_column = clean_column.split(" as ")[1]if len(clean_column.split(" as "))>1 else clean_column
                row[clean_column]=r[i]
            rows.append(row)
        return rows