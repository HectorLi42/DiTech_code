### the second version of dcp
### Previous version is ungly, so I prefer to rewrite this 
### script instead of mend the first version of dcp.py

### Define more functions, Add more comments
### write python like a professional programmer >_<

import numpy as np
import pandas as pd
import datetime
import os
import time

def datelist(start,end):
    ''' 
    Generate a list of date strings in required form.
    from time*start to time*end
    start and end should be a tuple like (2016,2,21)

    '''
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
<<<<<<< HEAD
    return result

def hash2id(district_hash,id_map):
    '''
    convert district_hash to district_id
    id_map should be a DataFrame, where the first column
    is hash, the second column is corresponding id.    
    Recomended column name of id_map is     
    ['district_hash','district_id']    
    Return:    
        if input hash is valid,    
        return district_id (integer)    
        if input hash is incorrect,    
        return 'invalidhash'    
    '''
=======
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result

def hash2id(district_hash,id_map):
	'''
	convert district_hash to district_id
	id_map should be a DataFrame, where the first column
	is hash, the second column is corresponding id.
	Recomended column name of id_map is 
	['district_hash','district_id']
	Return:
	    if input hash is valid,
	    return district_id (integer)
	    if input hash is incorrect,
	    return 'invalidhash'
	'''
>>>>>>> origin/master
    location = (id_map.iloc[:,0] == district_hash)
    if sum(location):
        return int(id_map[location].iloc[0,1])
    else:
        return 'invalidhash'

def time2slot(time_sample):
<<<<<<< HEAD
    '''
    Calculate which time_slot a specific time record belongs to.
=======
    '''Calculate which time_slot a specific time record belongs to.
>>>>>>> origin/master
    Args:
        time_sample: a string, takes the format '2010-01-21 19:03:43'
    Returns:
        time_slot from 1 to 144,
        if input time_sample is Null, return np.nan
     '''
    if len(time_sample) != 0:
        time_refer = time_sample[:-8]+'00:00:00'
        time_sample_struct = time.strptime(time_sample,'%Y-%m-%d %H:%M:%S')
        time_refer_struct = time.strptime(time_refer,'%Y-%m-%d %H:%M:%S')
        time_interval = time.mktime(time_sample_struct) - time.mktime(time_refer_struct)
        return int(np.ceil(time_interval/600.0))
    else:
        return np.nan

def get_week_day(date):
    """
    A function to get the week day of a particular date. I'll simply use the 
    actual week day of the dates to obtain the week days for the different 
    order transactions
    Args:
        date: a string,the date of the particular order being processed
        takes the form '2015-02-21'
    Returns:
        week_day: The week day of that particular order being processed
    """
    date_datetime = datetime.datetime.strptime(date, '%Y-%m-%d')
    week_day = date_datetime.weekday()
    return week_day

def num2str(num):
<<<<<<< HEAD
    ''' convert a num, float is OK to a string,
     for exmaple, 1.0 to '1'
     It is used before apply One-Hot-Encoding to Weather type
     '''
=======
	''' convert a num, float is OK to a string,
	 for exmaple, 1.0 to '1'
	 It is used before apply One-Hot-Encoding to Weather type
	 '''
>>>>>>> origin/master
    return str(int(num))

def OneHotEncoding(X):
    '''
    apply OHE to string features
    Args:
        X, a DataFrame, possibly have catagorical features
    Returns:
        output, a DataFrame, all features are numerical
    '''
    # Initialize new output DataFrame
    output = pd.DataFrame(index = X.index)

    # Investigate each feature column for the data
    for col, col_data in X.iteritems():

        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            # Example: 'Weather' => 'Weather_1' to 'Weather_9'
            col_data = pd.get_dummies(col_data, prefix = col)  
        
        # Collect the revised columns
        output = output.join(col_data)
    
    return output


def add_nearby_gaps2features(data_tmp):
    '''
    add previous 3 gaps as new features
    Args:
        data_tmp, a DataFrame, need to contain a column
        named 'gaps'
    Return:
        data_tmp, with three new columns 
        ['gaps_pre_1','gaps_pre_2',''gaps_pre_3'']
        added
    '''
    data_tmp = data_tmp.reset_index(drop = True)
    gaps_pre_1 = data_tmp['gaps'].shift(1)
    gaps_pre_2 = data_tmp['gaps'].shift(2)
    gaps_pre_3 = data_tmp['gaps'].shift(3)
    data_tmp['gaps_pre_1'] = gaps_pre_1
    data_tmp['gaps_pre_2'] = gaps_pre_2
    data_tmp['gaps_pre_3'] = gaps_pre_3
    data_tmp= data_tmp.fillna({'gaps_pre_1':0,'gaps_pre_2':0,'gaps_pre_3':0})

    return data_tmp

<<<<<<< HEAD
def add_nearby_prices2features(data_tmp):
    '''
    add previous 3 pricess as new features,then remove present prices
    since we don't know temp prices in test data
    Args:
        data_tmp, a DataFrame, need to contain a column
        named 'prices'
    Return:
        data_tmp, with three new columns 
        ['prices_pre_1','prices_pre_2',''prices_pre_3'']
        added
    '''
    data_tmp = data_tmp.reset_index(drop = True)
    for i in np.arange(3)+1:
        prices_pre = data_tmp['prices'].shift(i)
        data_tmp['prices_pre_'+str(i)] = prices_pre
    data_tmp= data_tmp.fillna({'prices_pre_1':0,'prices_pre_2':0,'prices_pre_3':0})
    #data_tmp.drop(['prices'],axis = 1,inplace = True)

    return data_tmp

def add_nearby_counts2features(data_tmp):
    '''
    add previous 3 counts as new features,then remove present prices
    since we don't know temp prices in test data
    Args:
        data_tmp, a DataFrame, need to contain a column
        named 'counts'
    Return:
        data_tmp, with three new columns 
        ['counts_pre_1','counts_pre_2',''counts_pre_3'']
        added
    '''
    data_tmp = data_tmp.reset_index(drop = True)
    for i in np.arange(3)+1:
        prices_pre = data_tmp['counts'].shift(i)
        data_tmp['counts_pre_'+str(i)] = prices_pre
    data_tmp = data_tmp.fillna({'counts_pre_1':0,'counts_pre_2':0,'counts_pre_3':0})
    #data_tmp.drop(['counts'],axis = 1,inplace = True)

    return data_tmp

=======
>>>>>>> origin/master
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


def load_data(datapath,filename,datatype):
<<<<<<< HEAD
    '''
    load data table as a DataFrame.
    Args:
        datapath, path to load a data file
        filename, exact filename ,order data should be
        like 'order_data_2015_02_21'
        datatype, a string,takes value from
        ['cluster','order','weather','traffic']
    Return:
       DataFrame with correct column names
    '''

    dataset_path = os.path.join(datapath, filename)
    if datatype == 'cluster':
        col_name = ['district_hash','district_id']

    if datatype == 'order':
        col_name = ['order_id','driver_id','passenger_id',\
    'start_district_hash','dest_district_hash','Price','Time']

    if datatype == 'weather':
        col_name = ['Time','Weather','temperature','PM2.5']

    if datatype == 'traffic':
        col_name = ['district_hash','tj_level_1','tj_level_2','tj_level_3','tj_level_4','tj_time']

    ### load data
    data = pd.read_table(dataset_path,header = None, names = col_name)
    #print datatype+' data set read successfully!'
    #print len(data)

    return data

def aligncols(data,col_list):
    '''
    rearange columns in data following order in col_list
    Arg:
        data,a dataframe, whose column names are the same as col_list,
        only orders are different.
    Returns:
        rearanged data
    '''
    output = pd.DataFrame(index = data.index)
    for col in col_list:
        col_data = data[col]
        output = output.join(col_data)
        
    return output

def process_order_data(order_data,date_string,id_map):
    '''
    clean and apply feature transformation on order_data
    '''
=======
	'''
	load data table as a DataFrame.
	Args:
	    datapath, path to load a data file
	    filename, exact filename ,order data should be
	    like 'order_data_2015_02_21'
	    datatype, a string,takes value from
	    ['cluster','order','weather','traffic']
	Return:
	   DataFrame with correct column names
	'''

	dataset_path = os.path.join(path, filename)
	if datatype == 'cluster':
		col_name = ['district_hash','district_id']

	if datatype == 'order':
		col_name = ['order_id','driver_id','passenger_id',\
    'start_district_hash','dest_district_hash','Price','Time']

    if datatype = 'weather':
    	col_name = ['Time','Weather','temperature','PM2.5']

    if datatype = 'traffic':
    	col_name = ['district_hash','tj_level_1','tj_level_2','tj_level_3','tj_level_4','tj_time']

    ### load data
    data = pd.read_table(dataset_path,header = None, names = feature_name)
    print datatype+' data set read successfully!'
    print len(data)

    return data

def process_order_data(order_data,date_string,id_map):
	'''
	clean and apply feature transformation on order_data
	'''
>>>>>>> origin/master

    ### generate a standard time series, from 1 to 144, for later use
    time_standard = pd.DataFrame(data = np.arange(144)+1,columns = ['time'])
    ###
<<<<<<< HEAD
    district_number = 66
    order_data['no_response'] = order_data['driver_id'].isnull()
=======

	order_data['no_response'] = order_data['driver_id'].isnull()
>>>>>>> origin/master

    #order_data_refined = order_data.copy()
    order_data_refined = order_data
    #order_data_refined = order_data_refined[:500]
<<<<<<< HEAD
    useless_col = ['passenger_id','dest_district_hash']
    order_data_refined.drop(useless_col, axis = 1,inplace = True)

    order_data_refined['start_district_hash'] = \
    order_data_refined['start_district_hash'].apply(hash2id,id_map = id_map)
    order_data_refined['Time'] = order_data_refined['Time'].apply(time2slot)
    
    ## calculate gaps
    '''
    gaps = order_data_refined['no_response'].groupby(
        [order_data_refined['start_district_hash'], order_data_refined['Time']]).sum()
    gaps = gaps.reset_index()

    ## calculate average prices
    prices = order_data_refined['Price'].groupby(
        [order_data_refined['start_district_hash'], order_data_refined['Time']]).mean()
    prices = prices.reset_index()

    ## calculate total order number
    counts = order_data_refined['order_id'].groupby(
        [order_data_refined['start_district_hash'], order_data_refined['Time']]).count()
    counts = counts.reset_index()
    ## merge three pieces into order_data_refined
    order_data_refined = pd.merge(gaps,prices,how = 'outer', on = ['start_district_hash','Time'])
    order_data_refined = pd.merge(order_data_refined,counts, how = 'outer', on = ['start_district_hash','Time'])
    '''

    ## new method to calculate gaps
    group_count = order_data_refined.groupby(['start_district_hash','Time'])
    #gaps = group_count['no_response'].sum()
    gaps = group_count['order_id'].count() - group_count['driver_id'].count()
    #print gaps_2
    gaps = gaps.reset_index()
    gaps.columns = ['start_district_hash', 'Time','no_response']


    prices = group_count['Price'].mean()
    prices = prices.reset_index()

    counts = group_count['order_id'].count()
    counts = counts.reset_index()

    ## merge three pieces into order_data_refined
    order_data_group = pd.merge(gaps,prices,how = 'outer', on = ['start_district_hash','Time'])
    order_data_group = pd.merge(order_data_group,counts, how = 'outer', on = ['start_district_hash','Time'])


    ###sort gaps by time and district_id
    order_data_group = order_data_group.sort_values(by = ['start_district_hash', 'Time'])

    cols_name = ['start_district_hash','Time','no_response','Price','order_id']
    order_data_group = aligncols(order_data_group,cols_name)
    order_data_group.columns = ['district_id','time','gaps','prices','counts']
    order_data_group['weekday'] = get_week_day(date_string)  ###add a column indicate weekdays,take value from 1 to 7

    ### Warning, the above process has a drawback ####
    ### If in a paticular time slot there is no passenger request, this time slot won't appear in above dataframe
    ### But according to problem statement, such a data point should be marked as 'gaps = 0'
    ### Fix this problem before further analysis

    order_data_filled = pd.DataFrame(columns = order_data_group.columns)

    for iid in np.arange(district_number)+1:
        order_data_tmp = order_data_group[order_data_group['district_id'] == iid]
        order_data_tmp_fixed = pd.merge(time_standard,order_data_tmp,how = 'outer', on = ['time']) ### add missing time-slot
        order_data_tmp_fixed = order_data_tmp_fixed.fillna({'district_id':iid,'gaps':0,'weekday':get_week_day(date_string)})
        order_data_filled = pd.concat([order_data_filled, order_data_tmp_fixed], ignore_index=True)

    return order_data_filled

def processing_traffic_data(traffic_data,id_map):
    '''
    '''
    level_list = ['tj_level_1','tj_level_2','tj_level_3','tj_level_4']
=======
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
    gaps['weekday'] = get_week_day(date_string)  ###add a column indicate weekdays,take value from 1 to 7

    ### Warning, the above process has a drawback ####
    ### If in a paticular time slice there is no passenger request, this time slice won't appear in above dataframe
    ### But according to problem statement, such a data point should be marked as 'gaps = 0'
    ### Fix this problem before further analysis

    gaps_filled = pd.DataFrame(columns = gaps.columns)

    for iid in np.arange(district_number)+1:
        gaps_tmp = gaps[gaps['district_id'] == iid]
        gaps_tmp_fixed = pd.merge(time_standard,gaps_tmp,how = 'outer', on = ['time']) ### add missing time-slice
        gaps_tmp_fixed = gaps_tmp_fixed.fillna({'district_id':iid,'gaps':0,'weekday':get_week_day(date_string)})
        gaps_filled = pd.concat([gaps_filled, gaps_tmp_fixed], ignore_index=True)

    return gaps_filled

def processing_traffic_data(order_data,id_map):
	'''
	'''
	level_list = ['tj_level_1','tj_level_2','tj_level_3','tj_level_4']
>>>>>>> origin/master
    for level in level_list:
        traffic_data[level] = traffic_data[level].apply(level2num)

    traffic_data['district_hash'] = traffic_data['district_hash'].apply(hash2id,id_map = id_map)
<<<<<<< HEAD
    traffic_data['tj_time'] = traffic_data['tj_time'].apply(time2slot)
    traffic_data = traffic_data.fillna(method ='pad')
    traffic_data = traffic_data.fillna(method = 'bfill')
=======
    traffic_data['tj_time'] = traffic_data['tj_time'].apply(time2slice)
    traffic_data = traffic_data.fillna(method =' pad')
    traffic_data = traffic_data_fillna(method = 'bfill')
>>>>>>> origin/master

    ## change column names into ['district_id','tj_level_1','tj_level_2',
    ##'tj_level_3','tj_level_4','time'])
    traffic_data.columns = ['district_id','tj_level_1',\
    'tj_level_2','tj_level_3','tj_level_4','time']

    return traffic_data

<<<<<<< HEAD
def processcing_weather_data(weather_data):
    '''
    '''
    ### sort weather_data by time
    ### remove repeated weather information
    ### fill missing values with weather data with previous data point
    ### generate a standard time series, from 1 to 144, for later use
    time_standard = pd.DataFrame(data = np.arange(144)+1,columns = ['time'])

    weather_data['Time'] = weather_data['Time'].apply(time2slot)
=======
def processcing_weather_data(weather_data,id_map):
	'''
	'''
	### sort weather_data by time
    ### remove repeated weather information
    ### fill missing values with weather data with previous data point
    weather_data['Time'] = weather_data['Time'].apply(time2slice)
>>>>>>> origin/master
    weather_data = weather_data.sort_values(by = ['Time'])
    weather_data = weather_data.drop_duplicates(['Time'])

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

<<<<<<< HEAD
    return weather_data_filled

=======
>>>>>>> origin/master
def clean_and_save(datapath, id_map, date_string,save_or_not = True):
    '''This is main function of this script
    load in original data for each day, do data cleaning
    then merge these three tables into a DataFrame named data_train
<<<<<<< HEAD
    comment added 2016-09-10:
    Relative to previous version, add average prices, total counts as new features
    '''
    ### step1, load order_data and clean
    order_folder_location = os.path.join(datapath, 'order_data')
    file_name = 'order_data_'+ date_string
    order_data = load_data(order_folder_location,file_name,'order')
=======
    '''

    ### step1, load order_data and clean
    order_folder_location = os.path.join(datapath, 'order_data')
    file_name = 'order_data_'+ date_string
    order_data = load_data(order_folder_location,filename,'order')
>>>>>>> origin/master
    gaps_final = process_order_data(order_data,date_string,id_map)

    ### step2, load traffic_data and clean
    traffic_data_location = os.path.join(datapath, 'traffic_data')
    file_name = 'traffic_data_' + date_string
<<<<<<< HEAD
    traffic_data = load_data(traffic_data_location,file_name,'traffic')
    traffic_final = processing_traffic_data(traffic_data,id_map)

    ### step3, load weather_data and clean
    weather_data_location = os.path.join(datapath, 'weather_data')
    file_name = 'weather_data_' + date_string
    weather_data = load_data(weather_data_location,file_name,'weather')
    weather_final = processcing_weather_data(weather_data)

    ### step4, merge and save(?)
    data_train = pd.merge(gaps_final, traffic_final, how = 'left', on=['district_id', 'time'])
=======
    traffic_data = load_data(traffic_data_location,filename,'traffic')
    traffic_final = processing_traffic_data(traffic_data,date_string,id_map)

    ### step3, load weather_data and clean
    weather_data_location = os.path.join(datapath, 'weather_data')
    filename = 'weather_data' + date_string
    weather_data = load_data(weather_data_location,filename,'weather')
    weather_final = processcing_weather_data(weather_data,date_string)

    ### step4, merge and save(?)
    data_train = pd.merge(gaps_final, traffic_final, how='left', on=['district_id', 'time'])
>>>>>>> origin/master
    data_train = pd.merge(data_train,weather_final,how = 'outer', on=['time'])
    data_train = data_train.sort_values(by = ['district_id','time'])

    ### fill missing traffic level values in each district, 
<<<<<<< HEAD
    ### then add previous 3 gaps,prices,counts as new features.
    district_number = 66
    data_train_fixed = pd.DataFrame(columns = data_train.columns)
    data_train_fixed.drop(['prices','counts'],axis = 1,inplace = True)
    for iid in np.arange(district_number)+1:
        data_tmp = data_train[data_train['district_id'] == iid]
        data_tmp = data_tmp.reset_index(drop = True)
        ### add 3 nearby information to each points
        data_tmp = add_nearby_gaps2features(data_tmp)
        data_tmp = add_nearby_prices2features(data_tmp)
        data_tmp = add_nearby_counts2features(data_tmp)
        data_tmp.drop(['prices','counts'],axis = 1,inplace = True)
=======
    ### then add previous 3 gaps as new features.
    district_number = 66
    data_train_fixed = pd.DataFrame(columns = data_train.columns)
    for iid in np.arange(district_number)+1:
        data_tmp = data_train[data_train['district_id'] == iid]
        data_tmp = data_tmp.reset_index(drop = True)
        ### add 3 previous gaps to each points
        data_tmp = add_nearby_gaps2features(data_tmp)
>>>>>>> origin/master
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

<<<<<<< HEAD
def train_run():
=======
def run():
>>>>>>> origin/master
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

<<<<<<< HEAD
def concat_train_data():
    '''
    concat all training data
    add 'Weather_6' = 0 for training all data
    drop rows where gaps = 0
    '''
    date_list = datelist((2016, 1, 1), (2016, 1, 21))
    pwd = os.getcwd()
    data_set_type = '//training_data'
    
    ### concat training data
    data_train_all = pd.DataFrame()
    for date_string in date_list:
        folder_name = 'merged_training_data_' + date_string
        new_path = os.path.join(pwd+data_set_type, folder_name)
        data_train = pd.read_csv(new_path+'\\data_train.csv')
        data_train_all = pd.concat([data_train_all,data_train],ignore_index = True)
        print folder_name + ' concat finished'

    data_train_all = data_train_all.fillna(0)

    data_train_all['Weather_6'] = 0
    col_standard = ['district_id','time','gaps', 'gaps_pre_1', 'gaps_pre_2', 'gaps_pre_3',\
                'prices_pre_1','prices_pre_2','prices_pre_3',\
                'counts_pre_1','counts_pre_2','counts_pre_3',\
                'weekday',\
                'PM2.5', 'Weather_1', 'Weather_2', 'Weather_3', \
                'Weather_4', 'Weather_6', 'Weather_8', 'Weather_9','temperature', \
                'tj_level_1', 'tj_level_2', 'tj_level_3', 'tj_level_4']
    data_train_all = aligncols(data_train_all,col_standard)

    valid = data_train_all['gaps'] != 0
    data_train_all = data_train_all[valid]

    data_train_all.to_csv('TrainingData_fixed_4_test_1.csv',index = False)
    return None

#### code below is for test data

def str2int(string):
    try:
        return int(string)
    except:
        return np.nan

def inlist(slice,llist):
    return (slice in llist)

def run_test():
    pwd = os.getcwd()
    data_set_type = 'test_set_1'
    filepath = os.path.join(pwd, data_set_type)

    with open(filepath + '//read_me_1.txt','rb') as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            listfromline = line.split('-')
            listfromline = map(str2int,listfromline)
            date_tmp = listfromline[:3]
            date_key = "%04d-%02d-%02d" % (date_tmp[0],date_tmp[1],date_tmp[2])
            if date_time_dict.has_key(date_key):
                date_time_dict[date_key].append(listfromline[3])
            else:
                date_time_dict[date_key] = []
                date_time_dict[date_key].append(listfromline[3])

    ### Step 0 generate a map between district_hash & district_id
    cluster_folder_location = filepath + '//cluster_map'
    file_name = '//cluster_map'
    col_name = ['district_hash','district_id']

    ### Step 1 pickup rows to predict, concat test set into a dataframe
    data_test_all = pd.DataFrame()
    for date_string,timelist in date_time_dict.items():
        data_test_tmp = dcp.clean_and_save(filepath, id_map, date_string,save_or_not = False)
        data_test_tmp['date'] = date_string
    
        data_test_tmp_select = data_test_tmp[data_test_tmp['time'].apply(inlist,llist = timelist)]
        data_test_all = pd.concat([data_test_all,data_test_tmp_select],ignore_index=True)
    
    ### add Weather_8 = 0
    data_test_all['Weather_8'] = 0
    data_test_all = data_test_all.fillna(0)

    ### drop dummy gaps in test data
    data_test_all.drop(['gaps'],axis = 1,inplace = True)

    col_standard = ['date','district_id','time',\
                'gaps_pre_1', 'gaps_pre_2', 'gaps_pre_3',\
                'prices_pre_1','prices_pre_2','prices_pre_3',\
                'counts_pre_1','counts_pre_2','counts_pre_3',\
                'weekday',\
                'PM2.5', 'Weather_1', 'Weather_2', 'Weather_3', \
                'Weather_4', 'Weather_6', 'Weather_8', 'Weather_9','temperature', \
                'tj_level_1', 'tj_level_2', 'tj_level_3', 'tj_level_4']
    data_test_all = aligncols(data_test_all,col_standard)

    data_test_all.to_csv('test_data_1.csv',index = False)

    return None



=======
>>>>>>> origin/master


