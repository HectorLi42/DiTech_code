###import several moduel used in data cleaning

import numpy as np
import pandas as pd
import datetime
import os
import time

#### functions for data preparation ####

def datelist(start,end):
    ''' Generate a list of date strings in required form'''
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    return result

def hash2id(district_hash,id_map):
    location = (id_map.iloc[:,0] == district_hash)
    if sum(location):
        return int(id_map[location].iloc[0,1])
    else:
        return 'invalidhash'

def time2slice(time_sample):
    '''Calculate which time slice a specific time record belongs to'''
    if len(time_sample) != 0:
        time_refer = time_sample[:-8]+'00:00:00'
        time_sample_struct = time.strptime(time_sample,'%Y-%m-%d %H:%M:%S')
        time_refer_struct = time.strptime(time_refer,'%Y-%m-%d %H:%M:%S')
        time_interval = time.mktime(time_sample_struct) - time.mktime(time_refer_struct)
        return int(np.ceil(time_interval/600.0))
    else:
        return np.nan

def num2str(num):
    return str(int(num))

def OneHotEncoding(X):
    '''apply OHE to string features'''
    # Initialize new output DataFrame
    output = pd.DataFrame(index = X.index)

    # Investigate each feature column for the data
    for col, col_data in X.iteritems():

        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            # Example: 'school' => 'school_GP' and 'school_MS'
            col_data = pd.get_dummies(col_data, prefix = col)  
        
        # Collect the revised columns
        output = output.join(col_data)
    
    return output
def add_nearby_gaps2features(data_tmp):
    '''add previous 3 gaps as new features'''
    data_tmp = data_tmp.reset_index(drop = True)
    gaps_pre_1 = data_tmp['gaps'].shift(1)
    gaps_pre_2 = data_tmp['gaps'].shift(2)
    gaps_pre_3 = data_tmp['gaps'].shift(3)
    data_tmp['gaps_pre_1'] = gaps_pre_1
    data_tmp['gaps_pre_2'] = gaps_pre_2
    data_tmp['gaps_pre_3'] = gaps_pre_3
    data_tmp= data_tmp.fillna({'gaps_pre_1':0,'gaps_pre_2':0,'gaps_pre_3':0})
    return data_tmp

def level2num(rawlevel):
    ''' turn tj_level into integers '''
    if str(rawlevel) != 'nan':
        try:
            raw = rawlevel.split(':')
            return int(raw[1])
        except:
            print rawlevel
            return np.nan
    else:
        return np.nan

#### main function ####
def clean_and_save(datapath, id_map, date_string,save_or_not = True):
    '''This is main function of this script
    load in original data for each day, do data cleaning
    then merge these three tables into a DataFrame named data_train
    '''
    ### generate a standard time series, from 1 to 144, for later use
    time_standard = pd.DataFrame(data = np.arange(144)+1,columns = ['time'])
    ###
    district_number = id_map['district_id'].max()  ### total district_number = 66

    #### Step 1, load order_data and turn it into required form
    order_folder_location = datapath + '//order_data'
    file_name = '//order_data_'+ date_string
    feature_name = ['order_id','driver_id','passenger_id',\
    'start_district_hash','dest_district_hash','Price','Time']

    order_data = pd.read_table(order_folder_location + file_name,names = feature_name)
    print 'order data set read successfully!'
    print len(order_data)

    ## According to discussion on forum, problem has been simplified, 
    ##count 'null' record directly
    order_data['no_response'] = order_data['driver_id'].isnull()

    #order_data_refined = order_data.copy()
    order_data_refined = order_data
    #order_data_refined = order_data_refined[:500]
    useless_col = ['order_id','driver_id','dest_district_hash','Price']
    order_data_refined.drop(useless_col,axis = 1,inplace = True)

    order_data_refined['start_district_hash'] = \
    order_data_refined['start_district_hash'].apply(hash2id,id_map = id_map)
    order_data_refined['Time'] = order_data_refined['Time'].apply(time2slice)

    gaps = order_data_refined['no_response'].groupby(
        [order_data_refined['start_district_hash'], order_data_refined['Time']]).sum()
    #gaps = order_data_refined.groupby(['start_district_hash','Time']).sum()
    ### dataframe 'gaps' is exactly what to predict in the problem
    gaps = gaps.reset_index()
    gaps = gaps.sort_values(by = ['start_district_hash', 'Time'])   ###sort gaps by time and district_id
    gaps.columns = ['district_id','time','gaps']

    ### Warning, the above process has a drawback ####
    ### If in a paticular time slice there is no passenger request, this time slice won't appear in above dataframe
    ### But according to problem statement, such a data point should be marked as 'gaps = 0'
    ### Fix this problem before further analysis

    gaps_filled = pd.DataFrame(columns = gaps.columns)

    for iid in np.arange(district_number)+1:
        gaps_tmp = gaps[gaps['district_id'] == iid]
        gaps_tmp_fixed = pd.merge(time_standard,gaps_tmp,how = 'outer', on = ['time']) ### add missing time-slice
        gaps_tmp_fixed = gaps_tmp_fixed.fillna({'district_id':iid,'gaps':0})
        gaps_filled = pd.concat([gaps_filled, gaps_tmp_fixed], ignore_index=True)

        gaps_final = gaps_filled
    ### use gaps_final as 'gaps' dataframe for later merge
    ### Step 1 finished

    ### Step 2 load traffic data and change it into numerical features
    traffic_data_location = datapath + '//traffic_data'
    file_name = '//traffic_data_' + date_string
    feature_name = ['district_hash','tj_level_1','tj_level_2','tj_level_3','tj_level_4','tj_time']
    traffic_data = pd.read_table(traffic_data_location + file_name,names = feature_name)

    print 'traffic data set read successfully!'
    print len(traffic_data)

    level_list = ['tj_level_1','tj_level_2','tj_level_3','tj_level_4']
    for level in level_list:
        traffic_data[level] = traffic_data[level].apply(level2num)

    traffic_data['district_hash'] = traffic_data['district_hash'].apply(hash2id,id_map = id_map)
    traffic_data['tj_time'] = traffic_data['tj_time'].apply(time2slice)
    traffic_data = traffic_data.fillna(method='pad')

    ## change column names into ['district_id','tj_level_1','tj_level_2',
    ##'tj_level_3','tj_level_4','time'])
    traffic_data.columns = ['district_id','tj_level_1',\
    'tj_level_2','tj_level_3','tj_level_4','time']
    traffic_final = traffic_data
    ### use traffic_final as 'traffic' dataframe for later merge
    ### Step 2 finished

    ### Step 3 load weather data and apply One-Hot-Encoding
    weather_data_location = datapath + '//weather_data'
    file_name = '//weather_data_' + date_string
    feature_name = ['Time','Weather','temperature','PM2.5']

    weather_data = pd.read_table(weather_data_location + file_name,names = feature_name)
    print 'weather data set read successfully!'
    print len(weather_data) ### if len(weather_data) != 288, indicates there are missing values

    ### sort weather_data by time
    ### remove repeated weather information
    ### fill missing values with weather data with previous data point
    weather_data['Time'] = weather_data['Time'].apply(time2slice)
    weather_data = weather_data.sort_values(by = ['Time'])
    #weather_data = weather_data[1::2]
    #IsDuplicated = weather_data['Time'].duplicated()
    #weather_data = weather_data[IsDuplicated]
    weather_data = weather_data.drop_duplicates(['Time'])
    #display(weather_data.head(10))
    #print len(weather_data)

    ### change column names for future merge
    weather_col = list(weather_data.columns)
    weather_col[0] = 'time'

    weather_data.columns = weather_col
    ### fill missing values with weather data in previous data point
    weather_data_filled = pd.merge(time_standard,weather_data,how = 'left', on=['time'])
    weather_data_filled = weather_data_filled.fillna(method = 'pad')
    weather_data_filled = weather_data_filled.fillna(method = 'bfill')
    #weather_data_filled = weather_data_filled.fillna(0)

    ### apply one-hot-encoding to feature 'Weather'
    weather_data_filled['Weather'] = weather_data_filled['Weather'].apply(num2str)
    weather_data_filled = OneHotEncoding(weather_data_filled)
    weather_final = weather_data_filled
    ### use weather_final as 'weather' dataframe to merge
    ### Step 3 finished

    ### Step 4 merge gaps_final, traffic_final, weather_final into one dataframe
    ### merge data
    data_train = pd.merge(gaps_final, traffic_final, how='left', on=['district_id', 'time'])
    data_train = pd.merge(data_train,weather_final,how = 'outer', on=['time'])
    data_train = data_train.sort_values(by = ['district_id','time'])

    ### fill missing traffic level values in each district, 
    ### then add previous 3 gaps as new features.
    data_train_fixed = pd.DataFrame(columns = data_train.columns)
    for iid in np.arange(district_number)+1:
        data_tmp = data_train[data_train['district_id'] == iid]
        data_tmp = data_tmp.reset_index(drop = True)
        ### add 3 previous gaps to each points
        data_tmp = add_nearby_gaps2features(data_tmp)
        ### fillna in traffic level
        data_tmp = data_tmp.fillna(method = 'bfill')
        data_tmp = data_tmp.fillna(method = 'pad')
        data_tmp = data_tmp.fillna(data_tmp.mean())
        #if data_tmp['tj_level_1'].count() < 144:
        #    print iid
        #data_tmp = data_tmp.fillna(0)
        data_train_fixed = pd.concat([data_train_fixed, data_tmp], ignore_index=True)

    data_train_fixed = data_train_fixed.fillna(data_train_fixed.mean())
    ### Step 4 finished

    ### make new folder and save to csvfile
    if save_or_not:
        folder_name = 'merged_training_data_' + date_string
        new_path = os.path.join(datapath, folder_name)

        if not os.path.isdir(new_path):
            os.makedirs(new_path)

        data_train_fixed.to_csv(new_path + '//data_train.csv',index = False)
    return data_train_fixed


def run():
    date_list = datelist((2016, 1, 1), (2016, 1, 21))  ### generate time list of training data
    pwd = os.getcwd()
    data_set_type = '//training_data'

    ### Step 0 generate a map between district_hash & district_id
    cluster_folder_location = pwd + data_set_type + '//cluster_map'
    file_name = '//cluster_map'
    col_name = ['district_hash','district_id']

    id_map = pd.read_table(cluster_folder_location + file_name,names = col_name)

    datapath = pwd + data_set_type
    for date_string in date_list:
        start_time = time.time()
        clean_and_save(datapath, id_map, date_string)
        end_time = time.time()
        print 'time needed to convert training data_' + date_string + ':'
        print end_time - start_time

    print 'haha lege ha, data cleaning finished'
    return None






