__author__ = 'daniel'

import os
import time
import aux
import datetime

# info about data to crawl
start_date = datetime.datetime(1950, 1, 1)     # YYYY,MM,DD
end_date = datetime.datetime(2014, 12, 31)     # YYYY,MM,DD
secs_to_sleep = 10

# path & files parameters
data_path = 'data/'
historic_path = data_path + 'historic_data/'
constituents_file = 'SP_constituents.csv'

# get symbols
symbols = aux.get_all_symbols(data_path + constituents_file)

# for each symbol, get page to extract and extract it
existing = []
failed = []
succeeded = []
for symbol in symbols:
    file_name = historic_path + aux.historic_filename(symbol, start_date, end_date)
    # don't re-extract existing files
    if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:
        existing.append(symbol)
        continue
    # extraction
    web_page = aux.page_to_extract(symbol, start_date, end_date)
    success = aux.extract_page(symbol, web_page, file_name)
    if success:
        succeeded.append(symbol)
    else:
        failed.append(symbol)
    # sleep to avoid making to many requests to server
    time.sleep(secs_to_sleep)
# print report
aux.print_extraction_report(existing, succeeded, failed)