
data_path = 'data/';
files_path = [data_path 'consolidated_data/'];

addpath(data_path);
addpath([files_path]);

kpis_list = {'open', 'high', 'low', 'close', 'volume', 'adjusted_close'};

% load core data
for i = 1:length(kpis_list)
    kpi = kpis_list{i};
    filename = [kpi '.csv'];
    eval(['raw_data.' kpi ' = csvread(''' filename ''')';]);
end

% load metadata
raw_data.symbols = importdata('symbols.csv');
raw_data.dates = importdata('dates.csv');

save([files_path 'raw_data.mat'], 'raw_data');