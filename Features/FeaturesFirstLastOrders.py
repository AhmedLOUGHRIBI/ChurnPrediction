import pandas as pd

def last_orderchannel(df, listDwp):
    """
    order channel used in last order dummified prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, last order channel dummified
    """
    df = df[['client_id', 'order_channel', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].max().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'order_channel': 'last_order_channel'}).drop("date_order_dwp",1)
    dffinal = pd.get_dummies(dffinal[['client_id', 'DWP', 'last_order_channel']], columns=['last_order_channel'])
    return dffinal


def last_quantity_ordered(df, listDwp):
    """
    quantity ordered in last order prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, quantity in last order
    """
    df = df[['client_id', 'quantity', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].max().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'quantity': 'last_quantity_ordered'}).drop("date_order_dwp",1)

    return dffinal


def last_order_difference_OrderInvoice(df,listDwp):
    """
    difference date_order and date_invoice in last order prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, difference date_order and date_invoice in last order
    """
    df = df[['client_id', 'date_order', 'date_invoice']]
    df['date_order_dwp'] = pd.to_datetime(df['date_order'], format='%Y-%m-%d').map(
        lambda x: x.year * 10000 + x.month * 100 + x.day)
    df['date_invoice_dwp'] = pd.to_datetime(df['date_invoice'], format='%Y-%m-%d').map(
        lambda x: x.year * 10000 + x.month * 100 + x.day)
    df['difference'] = df['date_invoice_dwp'] - df['date_order_dwp']

    # days not months to be edited
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp // 100 < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id','DWP'])['date_order_dwp'].max().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'difference': 'last_difference_ordered'})
    return dffinal[['client_id', 'DWP', 'last_difference_ordered']]

def last_sales_net(df, listDwp):
    """
    sales net in last order prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, sales net in last order
    """
    df = df[['client_id', 'sales_net', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].max().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'sales_net': 'last_sales_net_ordered'})

    return dffinal[['client_id', 'DWP', 'last_sales_net_ordered']]


def first_quantity_ordered(df, listDwp):
    """
    quantity in first order prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, quantity in first order
    """
    df = df[['client_id', 'quantity', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].min().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'quantity': 'first_quantity_ordered'})
    return dffinal[['client_id', 'DWP', 'first_quantity_ordered']]

def first_order_difference_OrderInvoice(df,listDwp):
    """
    difference order invoice in first order prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, difference order invoice in first order
    """
    df = df[['client_id', 'date_order', 'date_invoice']]
    df['date_order_dwp'] = pd.to_datetime(df['date_order'], format='%Y-%m-%d').map(
        lambda x: x.year * 10000 + x.month * 100 + x.day)
    df['date_invoice_dwp'] = pd.to_datetime(df['date_invoice'], format='%Y-%m-%d').map(
        lambda x: x.year * 10000 + x.month * 100 + x.day)
    df['difference'] = df['date_invoice_dwp'] - df['date_order_dwp']

    # days not months to be edited
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp // 100 < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].min().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'difference': 'first_difference_ordered'})
    return dffinal[['client_id', 'first_difference_ordered', 'DWP']]

def first_sales_net(df, listDwp):
    """
    sales net in first order prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, sales net in first order
    """
    df = df[['client_id', 'sales_net', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].min().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'sales_net': 'first_sales_net_ordered'})

    return dffinal[['client_id', 'DWP', 'first_sales_net_ordered']]


def first_orderchannel(df, listDwp):
    """
    order channel used in first order (dummified) prior to dwp -elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame contaning client_id, date, order channel used in first order dummified
    """
    df = df[['client_id', 'order_channel', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['date_order_dwp'].min().reset_index())
    dffinal = dffinal.merge(df, on=['client_id', 'date_order_dwp'], how='inner').drop_duplicates(['client_id', 'DWP'])
    dffinal = dffinal.rename(columns={'order_channel': 'first_order_channel'})
    dffinal = pd.get_dummies(dffinal[['client_id', 'DWP', 'first_order_channel']], columns=['first_order_channel'])
    return dffinal


def time_since_first_order(df,listDwp):
    """
    time since first order prior to dwp - elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas dataFrame containing clients_id, date, and time since first order
    """
    df = df[['client_id', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal['diff_order_dwp'] = dffinal['DWP'] - dffinal['date_order_dwp']
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['diff_order_dwp'].max().reset_index())
    dffinal = dffinal.rename(columns={'diff_order_dwp': 'DURATION_SINCE_FIRST_ORDER'})

    return dffinal


def time_since_last_order(df,listDwp):
    """
    time since last order prior to dwp - elements of listDwp
    :param df: pandas dataFrame
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas dataFrame containing clients_id, date, and time since last order
    """
    df = df[['client_id', 'date_order_dwp']]
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal = dffinal[dffinal.date_order_dwp < dffinal.DWP]
    dffinal['diff_order_dwp'] = dffinal['DWP'] - dffinal['date_order_dwp']
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['diff_order_dwp'].min().reset_index())
    dffinal = dffinal.rename(columns={'diff_order_dwp': 'DURATION_SINCE_LAST_ORDER'})

    return dffinal