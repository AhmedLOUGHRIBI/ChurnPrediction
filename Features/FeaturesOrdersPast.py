import pandas as pd
from functools import reduce

def difference_order_invoice_stats_before_dwp(df, listDwp):
    """
    statistiques of difference between date order and date invoice in tha past (prior to dwp-elements of listDwp)
    :param df: pandas Dataframe
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame containing client_id, date, and statistiques of difference between date_order and date_invoice
    """
    df = df[['client_id', 'date_order', 'date_invoice']]
    df['date_order_dwp'] = pd.to_datetime(df['date_order'], format='%Y-%m-%d').map(
        lambda x: x.year * 10000 + x.month * 100 + x.day)
    df['date_invoice_dwp'] = pd.to_datetime(df['date_invoice'], format='%Y-%m-%d').map(
        lambda x: x.year * 10000 + x.month * 100 + x.day)

    # days not months to be edited
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp // 100 < dffinal.DWP]
    dffinal['difference'] = df['date_invoice_dwp'] - df['date_order_dwp']
    dffinal_mean = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['difference'].mean().reset_index())
    dffinal_mean = dffinal_mean.rename(columns={'difference': 'difference_mean'})
    dffinal_max = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['difference'].max().reset_index())
    dffinal_max = dffinal_max.rename(columns={'difference': 'difference_max'})
    dffinal_min = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['difference'].min().reset_index())
    dffinal_min = dffinal_min.rename(columns={'difference': 'difference_min'})
    dffinal_sum = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['difference'].sum().reset_index())
    dffinal_sum = dffinal_sum.rename(columns={'difference': 'difference_sum'})
    dfs = [dffinal_min, dffinal_max, dffinal_mean, dffinal_sum]
    df_res = reduce(lambda left, right: pd.merge(left, right, on=list(
        {'client_id', 'DWP'} & set(right.columns)), how='left'), dfs)
    # return dffinal_mean
    return df_res


def quantity_ordered_stats_before_dwp(df, listDwp):
    """
    statistiques of quantities ordered in the past (prior to dwp-elements of listDwp)
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame containing client_id, date, and quantity stats prior to date
    """
    df = df[['client_id', 'quantity', 'date_order_dwp', 'date_invoice_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal_mean = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['quantity'].mean().reset_index())
    dffinal_mean = dffinal_mean.rename(columns={'quantity': 'quantity_mean'})
    dffinal_max = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['quantity'].max().reset_index())
    dffinal_max = dffinal_max.rename(columns={'quantity': 'quantity_max'})
    dffinal_min = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['quantity'].min().reset_index())
    dffinal_min = dffinal_min.rename(columns={'quantity': 'quantity_min'})
    dffinal_sum = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['quantity'].sum().reset_index())
    dffinal_sum = dffinal_sum.rename(columns={'quantity': 'quantity_sum'})
    dfs = [dffinal_min, dffinal_max, dffinal_mean, dffinal_sum]
    df_res = reduce(lambda left, right: pd.merge(left, right, on=list(
        {'client_id', 'DWP'} & set(right.columns)), how='left'), dfs)
    return df_res


def sales_net_stats_before_dwp(df, listDwp):
    """
    statistiques of sales net ordered in the past (prior to dwp-elements of listDwp)
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: statistiques of quantities ordered in the past (prior to dwp)
    """
    df = df[['client_id', 'sales_net', 'date_order_dwp', 'date_invoice_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal_mean = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['sales_net'].mean().reset_index())
    dffinal_mean = dffinal_mean.rename(columns={'sales_net': 'sales_net_mean'})
    dffinal_max = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['sales_net'].max().reset_index())
    dffinal_max = dffinal_max.rename(columns={'sales_net': 'sales_net_max'})
    dffinal_min = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['sales_net'].min().reset_index())
    dffinal_min = dffinal_min.rename(columns={'sales_net': 'sales_net_min'})
    dffinal_sum = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['sales_net'].sum().reset_index())
    dffinal_sum = dffinal_sum.rename(columns={'sales_net': 'sales_net_sum'})
    dfs = [dffinal_min, dffinal_max, dffinal_mean,dffinal_sum]
    df_res = reduce(lambda left, right: pd.merge(left, right, on=list(
        {'client_id', 'DWP'} & set(right.columns)), how='left'), dfs)
    return df_res

def number_change_region_past(df,listDwp):
    """
    number of region changes in the past (prior to dwp -> elements of listDwp)
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas Dataframe containing client_id,date,number_changes
    """
    df = df[['client_id','branch_id','date_order_dwp']]
    df_dates = pd.DataFrame(listDwp,columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['branch_id'].nunique().reset_index())
    dffinal = dffinal.rename(columns= {'client_id':'client_id', 'branch_id':'number_regions'})
    return dffinal[['client_id','DWP','number_regions']]


def number_order_channels_before_dwp(df,listDwp):
    """
    number order channels used in the past (prior to dwp -elements of listDwp)
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas Dataframe containing client_id,date,number_order_channels
    """
    df = df[['client_id','order_channel','date_order_dwp']]
    df_dates = pd.DataFrame(listDwp,columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['order_channel'].nunique().reset_index())
    dffinal = dffinal.rename(columns={'order_channel':'number_orderchannels'})
    return dffinal[['client_id', 'DWP', 'number_orderchannels']]

def order_channel_dominant_before_dwp(df,listDwp):
    """
    most used order_channel dummified
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas Dataframe containing client_id,date, order_channel_dominant->dummified
    """
    df = df[['client_id','order_channel','date_order_dwp']]
    df_dates = pd.DataFrame(listDwp,columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = dffinal[['client_id', 'DWP', 'order_channel']]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['order_channel'].agg(lambda x:x.value_counts().index[0]).reset_index())
    dffinal = dffinal.rename(columns={'order_channel': 'most_recurent_orderchannel'})
    dffinal = pd.get_dummies(dffinal, columns=['most_recurent_orderchannel'])
    return dffinal

def number_products_ordered_before_dwp(df,listDwp):
    """
    number of products ordered in the past (prior to dwp - elements of listDwp)
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas Dataframe containing client_id,date, number_products_ordered
    """
    df = df[['client_id','product_id','date_order_dwp']]
    df_dates = pd.DataFrame(listDwp,columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['product_id'].nunique().reset_index())
    dffinal = dffinal.rename(columns={'product_id': 'number_products_ordered'})
    return dffinal[['client_id', 'DWP', 'number_products_ordered']]

def number_orders_before_dwp(df,listDwp):
    """
    number of orders in the past (prior to dwp - elements of listDwp)
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas Dataframe containing client_id,date, number_ordered
    """
    df = df[['client_id','date_order_dwp']]
    df_dates = pd.DataFrame(listDwp,columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].count().reset_index())
    dffinal = dffinal.rename(columns={'date_order_dwp': 'number_orders'})
    return dffinal[['client_id', 'DWP', 'number_orders']]