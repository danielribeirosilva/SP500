__author__ = 'daniel'

import os
import datetime


# get all constituent symbols
def get_all_symbols(constituents_file_path):
    symbols = []
    with open(constituents_file_path, 'r') as f:
        next(f)  # skip header
        for line in f:
            symbols.append(line.split(',', 1)[0])
    return symbols


# web page for historic data extraction
# dates are datetime
def page_to_extract(symbol, start_date, end_date):
    # yahoo historical data
    command = 'http://real-chart.finance.yahoo.com/table.csv?'
    command += 's=' + symbol
    command += '&a=' + `start_date.day` + '&b=' + `start_date.month` + '&c=' + `start_date.year`
    command += '&d=' + `end_date.day` + '&e=' + `end_date.month` + '&f=' + `end_date.year`
    command += '&g=d&ignore=.csv'
    return command


# name for extracted historic data
# dates are datetime
def historic_filename(symbol, start_date, end_date):
    filename = symbol + '_'
    filename += `start_date.year` + '-' + `start_date.month` + '-' + `start_date.day` + '_'
    filename += `end_date.year` + '-' + `end_date.month` + '-' + `end_date.day`
    filename += '.csv'
    return filename


# extract page
def extract_page(symbol, web_page, output_filename):
    curl_command = 'curl "' + web_page + '" > ' + output_filename
    print('Trying to extract data for ' + symbol + '... '),
    os.system(curl_command)
    if not os.path.isfile(output_filename) or os.stat(output_filename).st_size == 0:
        print('FAILED!')
        return False
    else:
        print('SUCCESS!')
        return True


# print extraction report
def print_extraction_report(existing, succeeded, failed):
    print('\nExtraction Results:')
    print(`len(succeeded)` + ' symbols were extracted successfully:')
    print(succeeded)
    print(`len(failed)` + ' symbols failed to extract:')
    print(failed)
    print(`len(existing)` + ' symbols had already been extracted:')
    print(existing)


# takes a string in the format YYYY-MM-DD and returns the next date in the same format
def next_date(date):
    split = date.split('-')
    dt = datetime.datetime(int(split[0]), int(split[1]), int(split[2]))
    dt = dt + datetime.timedelta(days=1)
    return '-'.join([`dt.year`, `dt.month`, `dt.day`])