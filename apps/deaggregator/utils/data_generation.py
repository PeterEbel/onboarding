import numpy as np
import pandas as pd
import random

def get_invalid_row(data, col_check, true_value):
    """Checks whether specified columns add up to 'Total' column"""
    # sums columns
    sum = data[col_check].sum()
    # checks whether summed column is equal to total column
    compare = true_value == sum
    return compare

def drop_invalid_rows(data,validity):
    """Removes invalid rows from dataframe"""
    # if all rows are valid returns datadframe unchanged 
    if validity is True:
        return data
    # else removes rows with invalid sums from dataframe and returns clean data
    clean = data.drop(validity)
    return clean

def make_valid(dic,n_datapoints):
    """Makes a dictionary valid by adding NaN values to columns that have too few rows due to mismatch in original data"""
    # for each key in dictionary checks whether length of stored array has expected length
    for key in dic.keys():
        # if not then adds nan values to match the length of other arrays in dictionary
        if len(dic[key]) != n_datapoints:
           diff = n_datapoints - len(dic[key])
           dic[key].extend([np.nan]*diff)
    # returns adjusted dictionary
    return dic

def combine_cols(data):
    """Combines data from multiple columns into one, based on one row. 
       i.e. Columns [Small engine, Medium engine, Large engine, Unknown] become [Engine size] with 
       values [small, medium, large, unknown]
    """
    items = list(data.index)
    values = [int(val) for val in data.values]

    ran_col = random.sample(items,counts=values,k = sum(values))
    return ran_col

def binary_col(candidates, total_count,value):
    """Generates a binary column given a set of candidate indices, number of records and 
       total number of vehicles
    """
    if np.isnan(value):
        value = 0
    else:
        value = int(value)
    indices = np.random.choice(candidates,value,replace=False)
    binary_data = np.zeros(total_count)
    binary_data[indices] = 1
    return binary_data.astype(int)

def gen_rows_cars(row,column_dict):
    # number of records to be generated
    total_count = row['Total']
    # remove column total as won't be needed
    row = row.drop('Total')
    # dictionary with generated data
    gen_data = {}
    candidates = np.arange(total_count)
    bin = 0
    for key in column_dict.keys():
        # get col name from original table 
        cols = column_dict[key]
        # get value from key
        value = row[column_dict[key]]
        if key in ['Federal State', 'State District', 'County Code','County','Year', 'Vehicle type']:
            gen_data[key] = [value]*total_count
        elif type(cols) is not str:
            gen_data[key] = combine_cols(data=value)
        elif bin < 2:
            gen_data[key] = binary_col(candidates=candidates,total_count=total_count,value=value)
            if key != 'Fourwheel drive':
                candidates = np.setdiff1d(candidates,np.where(gen_data[key]==1)[0])
            bin = bin + 1 
        else:
            gen_data[key] = binary_col(candidates=candidates,total_count=total_count,value=value)
            candidates = np.setdiff1d(candidates,np.where(gen_data[key]==1)[0])
            bin = bin + 1 
    # makes sure all columns have same length 
    gen_data = make_valid(dic=gen_data,n_datapoints=total_count)
    # creates table from generated data
    gen_rows = pd.DataFrame(gen_data)
    # shuffles the generated data to be more realistic 
    gen_rows = gen_rows.sample(frac = 1).reset_index(drop = True)
    return gen_rows

def gen_rows_motorbikes(row,column_dict):
    """This method generates a DataFrame of records based on a single row of the Motorcycle Registration file.
       It creates a row for each registered vehicle in a given county, district, and state. 
       Columns 'Two wheels', 'Three wheels', 'Four wheels', are combined. 
       Column names in the returned object are as indicated by input: column_dict
    """
    #number of records to be generated
    total_count = row['Total']
    #remove column total as won't be needed
    row = row.drop('Total')
    #dictionary with generated data
    gen_data = {}
    #counter for number of wheels
    wheels = 2
    #iterate through each column in the input row
    for col, value in row.items():
        col_name = column_dict[col]
        #if any of these columns, then we want to copy their data to new table 
        if col in ['Federal State', 'State District', 'County Code','County', 'Year']:
            gen_data[col_name] = [value]*total_count
        #if column is 'Female bike owners', we create a random binary array
        elif col in ['Female bike owners']:
            gen_data[col_name] = binary_col(candidates=np.arange(total_count),total_count=total_count,value=value)
        #if column is 'Two wheels', 'Three wheels', 'Four wheels',  
        #we create an array of length = number of registered motocycles, and number of wheels = counterwheels
        elif wheels == 2:
            gen_data[col_name] = [wheels]*value
            wheels = wheels + 1
        else: 
            gen_data[col_name].extend([wheels]*value)
            wheels = wheels + 1
    #create array for column 'vehicle_type' of length = number of registered motocycles, and values = 'motobike'
    gen_data['vehicle_type'] = ['Motorbike']*total_count
    #makes sure all columns have same length 
    gen_data = make_valid(dic=gen_data,n_datapoints=total_count)
    #creates dataframe from dictionary of generated data
    gen_rows = pd.DataFrame(gen_data)
    #shuffles the generated data to be more realistic 
    gen_rows = gen_rows.sample(frac = 1).reset_index(drop = True)
    return gen_rows

def gen_table (data,column_dict,vehicle_type='motorbike'):
    """Generates a deaggregated dataset for an input table and a given vehicle type"""
    #replaces empty cells with NaN
    data.replace('',np.nan)
    table = pd.DataFrame()
    #given vehicle type, deaggregates data for each each row of input and collect in one table
    match vehicle_type:
        case 'motorbike':
            gen_func = gen_rows_motorbikes
        case 'car':
            gen_func = gen_rows_cars
    for index,row in data.iterrows():
        gen_rows = gen_func(row,column_dict=column_dict) 
        print(f'successfully generated data for row {index}')  
        table = pd.concat([table, gen_rows],ignore_index = True)
    return table

