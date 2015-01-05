raw_data_file = 'data/consolidated_data/raw_data.mat';

% cleaning parameters
min_number_points = 4000;

% load raw data
load(raw_data_file);

% eliminate symbols with too little info (too rencent)
d = raw_data.adjusted_growth;
T = size(d,1);
total_points_per_symbol = sum(~isnan(d));
best_min = min(total_points_per_symbol(total_points_per_symbol>=min_number_points));
idx_symbols = total_points_per_symbol >= best_min;
fprintf('Symbols Kept: %i/%i \n', sum(idx_symbols), numel(idx_symbols));
fprintf('Time Points: %i\n', best_min);

%eliminate remaining rows with NaN
idx_dates = (T-best_min+1):T;
dates_without_nan = sum(isnan(d(idx_dates,idx_symbols)),2) == 0;
idx_dates = idx_dates(dates_without_nan);
fprintf('Extra rows with NaN removed: %i\n', numel(dates_without_nan)-sum(dates_without_nan));

% filter by new index and save new data
data.open = raw_data.open(idx_dates,idx_symbols);
data.high = raw_data.high(idx_dates,idx_symbols);
data.low = raw_data.low(idx_dates,idx_symbols);
data.close = raw_data.close(idx_dates,idx_symbols);
data.volume = raw_data.volume(idx_dates,idx_symbols);
data.adjusted_close = raw_data.adjusted_close(idx_dates,idx_symbols);
data.adjusted_growth = raw_data.adjusted_growth(idx_dates,idx_symbols);
data.symbols = raw_data.symbols(idx_symbols);
data.dates = raw_data.dates(idx_dates);
save('data.mat', 'data')

