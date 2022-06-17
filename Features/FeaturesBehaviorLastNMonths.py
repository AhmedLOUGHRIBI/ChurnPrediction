from Utils.utils import compute_variable_unstacked, dwp_3months_ago
from functools import reduce
import pandas as pd

def region_change_past_3_months(df,listDwp):
    """
    captures region changes from where the client orders.
    :param df: pandas DataFrame
    :param listDwp: list of dates at which we wish to calculate the feature
    :return: pandas DataFrame containing client_id, date and a binary variable capturing region changes
    """
    df = df[['client_id','branch_id','date_order_dwp']]
    df_dates = pd.DataFrame(listDwp,columns=['DWP'])
    dffinal = df_dates.assign(temp=1).merge(df.assign(temp=1)).drop("temp", 1)
    dffinal['DWP_3MONTHS_AGO']=dffinal.DWP.map(lambda x:dwp_3months_ago(x))
    dffinal = dffinal[(dffinal.date_order_dwp < dffinal.DWP) & (dffinal.date_order_dwp >= dffinal.DWP_3MONTHS_AGO)]
    dffinal = pd.DataFrame(dffinal.groupby(['client_id', 'DWP'])['branch_id'].nunique().reset_index())
    dffinal['CHANGE_LAST_3_MONTHS']=0
    dffinal.loc[dffinal.branch_id >1,'CHANGE_LAST_3_MONTHS']=1
    return dffinal[['client_id', 'DWP', 'CHANGE_LAST_3_MONTHS']]


def number_products_ordered_last_n_months(df, list_clients, list_dwp, timelag_n):
    """
    number of products ordered in each month for the last n months prior to dwp - elements of list_dwp
    :param df: pandas DataFrame
    :param list_clients: list of client_ids for whom we wish to calculate the feature
    :param list_dwp: list of dates at which we wish to calculate the feature
    :param timelag_n: number of months prior to dwp-elements of lis_dwp at which we want to calculate the number of products ordered
    :return: pandas DataFrame containing client_id, date, and number products ordered in last n months
    """

    df = df[df.client_id.isin(list_clients)]
    df = df[['date_order_dwp', 'client_id', 'product_id']]

    # group and unstack
    transactions_grouped = df.groupby(['date_order_dwp', 'client_id'])[ \
        'product_id'].nunique()

    transactions_unstacked = transactions_grouped.unstack('date_order_dwp').fillna(0)

    # compute last N monthly amounts previous to dwp
    df_res = compute_variable_unstacked(transactions_unstacked, list_dwp, 'NUMBER_PRODUCTS', timelag_n).drop_duplicates(['client_id', 'DWP'])
    return df_res


def number_orders_by_channel_last_n_months(df, list_clients, list_dwp, timelag_n):
    """
    number orders by channel dummified in each month for the last n months prior to dwp - elements of list_dwp
    :param df: pandas DataFrame
    :param list_clients: list of client_ids for whom we wish to calculate the feature
    :param list_dwp: list of dates at which we wish to calculate the feature
    :param timelag_n: number of months prior to dwp-elements of lis_dwp at which we want to calculate the number of orders by channel
    :return: pandas DataFrame containing client_id, date, and number orders by channel in last n months dummified
    """

    df = df[df.client_id.isin(list_clients)]
    df = df[['date_order_dwp', 'client_id', 'order_channel']]
    df = pd.get_dummies(df[['client_id', 'order_channel', 'date_order_dwp']],
                                     columns=['order_channel'])

    # group and unstack
    transactions_unstacked_online = df.groupby(['date_order_dwp', 'client_id'])[ \
        'order_channel_online'].sum().unstack('date_order_dwp').fillna(0)

    transactions_unstacked_phone = df.groupby(['date_order_dwp', 'client_id'])[ \
        'order_channel_by phone'].sum().unstack('date_order_dwp').fillna(0)

    transactions_unstacked_store = df.groupby(['date_order_dwp', 'client_id'])[ \
        'order_channel_at the store'].sum().unstack('date_order_dwp').fillna(0)

    transactions_unstacked_visit = df.groupby(['date_order_dwp', 'client_id'])[ \
        'order_channel_during the visit of a sales rep'].sum().unstack('date_order_dwp').fillna(0)

    transactions_unstacked_other = df.groupby(['date_order_dwp', 'client_id'])[ \
        'order_channel_other'].sum().unstack('date_order_dwp').fillna(0)

    # compute last N monthly amounts previous to dwp
    df_res_online = compute_variable_unstacked(transactions_unstacked_online, list_dwp, 'order_channel_online',
                                                    timelag_n).drop_duplicates(['client_id', 'DWP'])
    df_res_phone = compute_variable_unstacked(transactions_unstacked_phone, list_dwp, 'order_channel_by phone',
                                                   timelag_n).drop_duplicates(['client_id', 'DWP'])
    df_res_store = compute_variable_unstacked(transactions_unstacked_store, list_dwp, 'order_channel_at the store',
                                                   timelag_n).drop_duplicates(['client_id', 'DWP'])
    df_res_visit = compute_variable_unstacked(transactions_unstacked_visit, list_dwp,
                                                   'order_channel_during the visit of a sales rep', timelag_n).drop_duplicates(['client_id', 'DWP'])
    df_res_other = compute_variable_unstacked(transactions_unstacked_other, list_dwp, 'order_channel_other',
                                                   timelag_n).drop_duplicates(['client_id', 'DWP'])

    dfs = [df_res_online, df_res_phone, df_res_store, df_res_visit, df_res_other]
    dffinal = reduce(lambda left, right: pd.merge(left, right, on=list(
        {'client_id', 'DWP'} & set(right.columns)), how='left'), dfs)
    return dffinal


def quantity_ordered_last_n_months(df, list_clients, list_dwp, timelag_n):
    """
    quantity ordered in each month for the last n months prior to dwp - elements of list_dwp
    :param df: pandas DataFrame
    :param list_clients: list of client_ids for whom we wish to calculate the feature
    :param list_dwp: list of dates at which we wish to calculate the feature
    :param timelag_n: number of months prior to dwp-elements of lis_dwp at which we want to calculate the quantity ordered
    :return: pandas DataFrame containing client_id, date, and quantity ordered in last n months
    """
    df = df[df.client_id.isin(list_clients)]
    df = df[['date_order_dwp', 'client_id', 'quantity']]

    df = df.rename(columns={'quantity': 'QUANTITY'})

    # group and unstack
    transactions_grouped = df.groupby(['date_order_dwp', 'client_id'])[ \
        'QUANTITY'].sum()

    transactions_unstacked = transactions_grouped.unstack('date_order_dwp').fillna(0)

    # compute last N monthly amounts previous to dwp
    df_res = compute_variable_unstacked(transactions_unstacked, list_dwp, 'QUANTITY', timelag_n).drop_duplicates(['client_id', 'DWP'])

    return df_res


def number_orders_last_n_months(df, list_clients, list_dwp, timelag_n):
    """
    number orders in each month for the last n months prior to dwp - elements of list_dwp
    :param df: pandas DataFrame
    :param list_clients: list of client_ids for whom we wish to calculate the feature
    :param list_dwp: list of dates at which we wish to calculate the feature
    :param timelag_n: number of months prior to dwp-elements of lis_dwp at which we want to calculate the number of orders
    :return: pandas DataFrame containing client_id, date, and number orders in last n months
    """

    df = df[df.client_id.isin(list_clients)]
    df = df[['date_order_dwp', 'client_id', 'sales_net']]

    df = df.rename(columns={'sales_net': 'SALES'})

    # group and unstack
    transactions_grouped = df.groupby(['date_order_dwp', 'client_id'])[ \
        'SALES'].size()

    transactions_unstacked = transactions_grouped.unstack('date_order_dwp').fillna(0)

    # compute last N monthly amounts previous to dwp
    df_res = compute_variable_unstacked(transactions_unstacked, list_dwp, 'NUMBER_ORDERS', timelag_n).drop_duplicates(['client_id', 'DWP'])

    return df_res


def sales_last_n_months(df, list_clients, list_dwp, timelag_n):
    """
    sales net in each month for the last n months prior to dwp - elements of list_dwp
    :param df: pandas DataFrame
    :param list_clients: list of client_ids for whom we wish to calculate the feature
    :param list_dwp: list of dates at which we wish to calculate the feature
    :param timelag_n: number of months prior to dwp-elements of lis_dwp at which we want to calculate the number of orders
    :return: pandas DataFrame containing client_id, date, and sum of sales net in last n months
    """

    df = df[df.client_id.isin(list_clients)]
    df = df[['date_order_dwp', 'client_id', 'sales_net']]

    df = df.rename(columns={'sales_net': 'SALES'})

    # group and unstack
    transactions_grouped = df.groupby(['date_order_dwp', 'client_id'])[ \
        'SALES'].sum()
    transactions_unstacked = transactions_grouped.unstack('date_order_dwp').fillna(0)

    # compute last N monthly amounts previous to dwp
    df_res = compute_variable_unstacked(transactions_unstacked, list_dwp, 'SALES', timelag_n).drop_duplicates(['client_id', 'DWP'])

    return df_res

def number_branchs_used_last_n_months(df, list_clients, list_dwp, timelag_n):
    """
    number branchs used in each month for the last n months prior to dwp - elements of list_dwp
    :param df: pandas DataFrame
    :param list_clients: list of client_ids for whom we wish to calculate the feature
    :param list_dwp: list of dates at which we wish to calculate the feature
    :param timelag_n: number of months prior to dwp-elements of lis_dwp at which we want to calculate the number of branchs used
    :return: pandas DataFrame containing client_id, date, and number branchs used in last n months
    """

    df = df[df.client_id.isin(list_clients)]
    df = df[['date_order_dwp', 'client_id', 'branch_id']]

    # group and unstack
    transactions_grouped = df.groupby(['date_order_dwp', 'client_id'])[ \
        'branch_id'].nunique()

    transactions_unstacked = transactions_grouped.unstack('date_order_dwp').fillna(0)

    # compute last N monthly amounts previous to dwp
    df_res = compute_variable_unstacked(transactions_unstacked, list_dwp, 'NUMBER_BRANCHS', timelag_n).drop_duplicates(['client_id', 'DWP'])
    return df_res