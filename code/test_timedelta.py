import pandas as pd

def correct_timedelta(df, time_diff):
    '''
    df.index must be DateTimeIndex
    table=table_of_interest
    col="column_of_interest"
    time_diff=time_diff in seconds as int
    '''
    lst = []
    lst_i = []
    count = 0
    for i in df.index:
        count += 1
        if count >= len(df):
            break
        delta = abs(df.index[count] - df.index[count-1])
        if int(delta.total_seconds()) != int(time_diff):
            lst.append(("from index {} on, it has been {} s or {} h.".format(count-1,int(delta.total_seconds()),(int(delta.total_seconds()/3600)))))
            lst_i.append((count-1,int(delta.total_seconds())))
    return lst, lst_i