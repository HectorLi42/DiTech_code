import pandas as pd

def output_required_format(data):
    '''rewirte data into required format'''
    output = pd.DataFrame(index = data.index)
    #row_number = len(data)
    ### add district_id
    output['district_id'] = data['district_id']
    ### add date-time
    date_time_list = []
    for row_id in data.index:
        date_tmp = data.loc[row_id]['date']
        time_tmp = str(int(data.loc[row_id]['time']))
        date_time_list.append(date_tmp + '-' + time_tmp)
        
    output['date-time'] = date_time_list
        
    ### add gaps_pred
    output['gaps_pred'] = data['gaps']
    ### reset index
    output = output.reset_index(drop = True)
    return output

def measure_performance_mae(result_file = 'test_pred_1.csv'):
    my_result = pd.read_csv(result_file)
    my_result.columns = ['depart', 'time', 'gap_pred']
    # load golden result
    golden_result = pd.read_table("test_result_1", sep=',', names=['depart', 'time', 'gap_real'])

    result = pd.merge(my_result, golden_result, on=['depart', 'time'], how='right')
    #result.fillna(0, inplace = True)
    result['gap'] = (result['gap_real'] - result['gap_pred']).abs()
    result['gap'] = result['gap'].astype(float)
    result = result[['depart', 'time', 'gap']]

    mae = result.groupby('depart').mean().mean()

    print mae

    return mae

def measure_performance_mape(result_file = 'test_pred_1.csv'):
    my_result = pd.read_csv(result_file)
    my_result.columns = ['depart', 'time', 'gap_pred']
    # load golden result
    golden_result = pd.read_table("test_result_1", sep=',', names=['depart', 'time', 'gap_real'])

    result = pd.merge(my_result, golden_result, on=['depart', 'time'], how='right')
    #result.fillna(0, inplace = True)
    result['gap'] = (result['gap_real'] - result['gap_pred']).abs()
    result['gap'] = result['gap'].astype(float)/result['gap_real']
    result = result[['depart', 'time', 'gap']]

    mape = result.groupby('depart').mean().mean()

    print mape

    return mape