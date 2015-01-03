__author__ = 'daniel'

import os
import aux

# path & files parameters
data_path = 'data/'
historic_folder = 'historic_data'
historic_path = data_path + historic_folder + '/'
constituents_file = 'SP_constituents.csv'
consolidated_path = data_path + 'consolidated_data/'

# historic data specification
columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'adjusted_close']

# for each of the non-date columns, create a data matrix where each row corresponds
# to a date and each column corresponds to the given column for a symbol. For example,
# a row in the 'volume' matrix corresponds to the volumes of each of the S&P500 companies
# in a given date

# get all symbols
symbols = aux.get_all_symbols(data_path + constituents_file)

# define and initialize data holding structure
all_data = {}  # {column : {date: {symbol : value} } }
for col in columns[1:]:
    all_data[col] = {}
smallest_date = '9999-12-31'
largest_date = '0000-01-01'

# extract data into all_data format
path = './'+data_path+historic_folder
files = [f for f in os.listdir(path) if os.path.isfile(historic_path+f)]
for filename in files:
    with open(historic_path + filename, 'r') as f:
        symbol = filename.split('_', 1)[0]
        next(f)  # skip header
        for line in f:
            date = line.split(',')[0]
            smallest_date = min(smallest_date, date)
            largest_date = max(largest_date, date)
            row_data = line.split(',')[1:]
            for idx, val in enumerate(row_data):
                col = columns[idx+1]
                if date not in all_data[col]:
                    all_data[col][date] = {}
                all_data[col][date][symbol] = val.strip()

# get list of dates
dates = sorted(all_data[columns[1]].keys())

# rewrite data in new format
for col in all_data:
    output_filename = consolidated_path + col + '.csv'
    with open(output_filename, 'w') as f:
        for date in dates:
            first = True;
            for symbol in symbols:
                if symbol in all_data[col][date]:
                    value = all_data[col][date][symbol]
                else:
                    value = 'NaN'
                if first:
                    first = False
                else:
                    f.write(',')
                f.write(value)
            f.write('\n')

# output date list
output_filename = consolidated_path + 'dates.csv'
with open(output_filename, 'w') as f:
    for date in dates:
        f.write(date + '\n')

# output symbols
output_filename = consolidated_path + 'symbols.csv'
with open(output_filename, 'w') as f:
    for symbol in symbols:
        f.write(symbol + '\n')


