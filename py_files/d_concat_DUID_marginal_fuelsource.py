import pandas as pd

def DUID_items(NEMDE_market_df, CO2_generators_df):
    '''
    The function needs dataframes with the generator ID columns named "DUID" in each case.
    A list variable is returned
    '''
    lst1 = []
    for i in set(NEMDE_market_df.DUID):
        if i in set(CO2_generators_df.DUID):
            lst1.append(i)
    print('The NEMDE_market_table uses {} DUID items from the DUID CO2_generator column.'.format(len(lst1)))
    
    lst2 = []
    for i in set(NEMDE_market_df.DUID):
        if i in set(CO2_generators_df.GENSETID):
            lst2.append(i)
    print('The NEMDE_market_table uses {} DUID items from the GENSETID CO2_generator column.'.format(len(lst2)))
    
    lst_diff =[]
    for i in lst2:
        if i not in lst1:
            lst_diff.append(i)
    print('The items {} from the GENSETID column should be added to the DUID column.'.format(lst_diff))
    return lst_diff


def merge_DUID_GENSETID(CO2_generators_df, lst_diff):
    '''
    This function takes care of the mismatch output by DUID_items. Note that .groupby("DUID").mean() is applied to the
    CO2_generators table. Hence, only numerical columns are returned.
    The mismatch list lst_diff must be the output from DUID_items
    '''
    CO2_generators_grouped = CO2_generators_df.groupby("DUID").mean().reset_index()
    count = -1
    for i in CO2_generators_df.GENSETID:
        count += 1
        if i in lst_diff:
            CO2_generators_grouped = pd.concat([CO2_generators_grouped, CO2_generators_df.iloc[[count],:]\
                                                .loc[:,["GENSETID","CO2E_EMISSIONS_FACTOR"]].rename(columns={"GENSETID":"DUID"})],)
    CO2_generators_grouped = CO2_generators_grouped.sort_values(by="DUID").reset_index(drop=True)
    return CO2_generators_grouped