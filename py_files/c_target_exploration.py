import pandas as pd
import datetime as dt
import pytz
import os

def mod_concat_NEMDE(file_path):
    '''
    load modified df of concatenated pkl chunks after clean_filter_concat_pkl func application
    '''
    df = pd.read_pickle(file_path)
    df.drop(columns=["BandNo","RRNBandPrice","BandCost"], inplace=True)
    df = df.set_index('PeriodID', drop=True)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df[["Price", "Increase"]] = df[["Price", "Increase"]].astype(float)
    df.rename(columns={"Unit":"DUID"}, inplace=True)
    df.sort_index(inplace=True, ascending=False)
    df.index = df.index - dt.timedelta(minutes = 5)
    df.rename(columns={"Unit":"DUID"}, inplace=True)
    
    assert df["Price"].dtype == float
    assert df["Increase"].dtype == float
    assert not df.isna().any().any()
    
    return df

    
def df_groupby_period(df, path_destination):
    '''
    Groups df by its period and returns arithmetic mean of prices
    df=dataframe varibale of interest
    path_destination="path + desired filename for grouped df to be saved to pickle"
    '''
    df_group_period = df.groupby("PeriodID").agg({"Price":"mean"}).sort_values(by="PeriodID",ascending=False)
    pd.to_pickle(df_group_period, path_destination)
    
    return df_group_period


def load_MMSDM_dispatch(file_path):
    df_dispatch = pd.read_csv(file_path, index_col = 0, parse_dates=True)
    df_dispatch.sort_index(ascending=False, inplace=True)
    
    assert df_dispatch["RRP SA1"].dtype == float
    
    return df_dispatch
    
    
def join_NEMDE_MMSDM(NEMDE_df, MMSDM_df, how="inner"):
    '''
    The inner join guarantees same max and min datetime in index; function will fail if they are unequal
    joins two dataframes on index
    how="string"
    '''
    
    MMSDM_df = MMSDM_df.loc[(MMSDM_df.index <= NEMDE_df.index.max()) &
                                  (MMSDM_df.index >= NEMDE_df.index.min()), :][['RRP SA1']]
    
    assert MMSDM_df.index.min() == NEMDE_df.index.min()
    assert MMSDM_df.index.max() == NEMDE_df.index.max()
    
    df_join = NEMDE_df.join(MMSDM_df, how=how)
    
    assert not df_join.all().all()
    
    print("The percentage of mismatching dispatch prices from MMSDM and NEMDE is {} %.".format(round(((sum(abs((df_join["Price"] - df_join["RRP SA1"])\
                                                                                  /df_join["RRP SA1"]) > 0.000001)/df_join.shape[0])*100),2)))
    
    return df_join


def adjust_NEMDE_MMSDM(NEMDE_MMSDM_join_df):
    '''
    Any dispatch price differences between NEMDE and MMSDM should be scrutinised; use this function if you evaluate them negligible
    '''
    df_join_mismatch = NEMDE_MMSDM_join_df.loc[abs((NEMDE_MMSDM_join_df["Price"] - NEMDE_MMSDM_join_df["RRP SA1"])/NEMDE_MMSDM_join_df["RRP SA1"]) > 0.000001, :]
    NEMDE_MMSDM_join_df.drop(df_join_mismatch.index, inplace=True)
    
    assert (abs(((NEMDE_MMSDM_join_df["Price"] - NEMDE_MMSDM_join_df["RRP SA1"])/NEMDE_MMSDM_join_df["RRP SA1"])) > 0.000001).any() == False
    
    print("The percentage of mismatching dispatch prices from MMSDM and NEMDE changed to {} %.".format(round(((sum(abs((NEMDE_MMSDM_join_df["Price"]\
                                                                                                                        - NEMDE_MMSDM_join_df["RRP SA1"])\
                                                                                  /NEMDE_MMSDM_join_df["RRP SA1"]) > 0.000001)/NEMDE_MMSDM_join_df.shape[0])*100),2)))
    
    return NEMDE_MMSDM_join_df