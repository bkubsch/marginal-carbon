import pandas as pd

def bin_sums(df, col, bin_size):
    '''
    table=table_of_interest
    col="col_of_interest"
    bin_size=number of rows (int) over which the function shall sum up values for each bin
    '''
    bin_sums = []
    count = 0
    for i in df.index:
        if count >= len(df):
            break
        j = count + bin_size
        bin_sum = sum(df[col].iloc[count:j])/6
        count += bin_size
        bin_sums.append(bin_sum)
    return bin_sums