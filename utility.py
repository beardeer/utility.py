import csv
import data_path
from datetime import datetime
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from scipy import stats


def build_dict_from_csv(csv_file_name, key_column=1, has_header=True, duplicated=False):
    ## open the csv file
    input_file = open(csv_file_name, 'rb')
    csv_reader = csv.reader(input_file)

    data_dict = {}

    ## get header information
    if has_header:
        header = csv_reader.next()
        header.pop(key_column)
        value_names = header

    ## read data from the csv file
    for row in csv_reader:
        key = row.pop(key_column)

        if duplicated == False:
            if has_header:
                value_dict = {}
                ## build the value dict
                for i,value in enumerate(row):
                    value_name = value_names[i]
                    value_dict[value_name] = value
                    data_dict[key] = value_dict
            else:
                #row.pop(key_column)
                data_dict[key] = row

        elif duplicated == True:
            if has_header:
                if data_dict.has_key(key):
                    pass
                else:
                    data_dict[key] = []
                value_dict = {}
                for i,value in enumerate(row):
                    value_name = value_names[i]
                    value_dict[value_name] = value
                data_dict[key].append(value_dict)
            else:
                pass

    input_file.close()
    return data_dict

def get_file_name_with_time(folder, file_name_prefix, file_name_extension):
    return folder + file_name_prefix + \
           datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + file_name_extension

class QueryProcessor(object):

    def __init__(self):
        pass

    def get_header_from_query(self, query):
        return [item.strip()
            for item in query.upper().split("FROM")[0].split("SELECT")[-1].split(",")]

    def run_query(self, query, db):
        print query
        return db.bind.execute(query).fetchall()

    def run_query_to_csv(self, query, db, output_file_path = None):

        if output_file_path == None:
            output_file_path = get_file_name_with_time(data_path.DROPBOX_DATA_FOLDER, "query_result_", ".csv")
            
        output_file = open(output_file_path, "wb")
        csv_writer = csv.writer(output_file)

        header = self.get_header_from_query(query)
        csv_writer.writerow(header)

        result = self.run_query(query, db)
        for item in result:
            row = [value for value in item]
            csv_writer.writerow(row)

        output_file.close()
        print output_file_name

    def get_value_by_header(self, values, headers, header_name):
        pos = headers.index(header_name.upper())
        return values[pos]

class CsvProcessor(object):

    def __init__(self, file_name, has_header = True, in_memory = True):
        self.has_header = has_header
        self.in_memory = in_memory

        if self.in_memory:
            self.data = []
            input_file = open(file_name, 'rb')
            csv_reader = csv.reader(input_file)
            if self.has_header:
                self.header = csv_reader.next()

            for row in csv_reader:
                self.data.append(row)

    def get_data_from_csv(self, file_name, has_header=True):
        pass

    def get_histogram_plot(self):
        pass

    def get_two_data_from_two_cols(self, col_x, col_y):
        data_x = []
        data_y = []
        if self.in_memory:
            for row in self.data:
                data_x.append(float(row[col_x]))
                data_y.append(float(row[col_y]))
        return data_x, data_y

    def get_r_squared(self, col_x, col_y):
        data_x, data_y = self.get_two_data_from_two_cols(col_x, col_y)
        slope, intercept, r_value, p_value, std_err = stats.linregress(data_x,data_y)
        return float(r_value**2)

    def get_auc(self, col_x, col_y):
        data_x, data_y = self.get_two_data_from_two_cols(col_x, col_y)
        auc = roc_auc_score(data_x, data_y)
        return auc

class DataCache(object):

	def __init__(self, func):
		self.func = func
		self.cache = {}

	def get(self, arg_str):
		if self.cache.has_key(arg_str):
			return self.cache[arg_str]
		else:
			args = arg_str.split(',')
			result = self.func(*args)
			self.cache[arg_str] = result
			return result


if __name__ == "__main__":

    try:
        processor = QueryProcessor()

        query = """ SELECT id, student_reassessment_record_id, reassessment_level, delay_days,
       repeated_time, mastery_speed, adaptive_mode
       FROM student_reassessment_adjustment_records where reassessment_level = 1 and adaptive_mode = 1
       order by repeated_time;"""

        processor.run_query_to_csv(query)
    except:
        pass
