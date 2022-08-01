import pandas as pd

def time_left_summer(listDwp):
    """
    number of months left to juin
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame containing dates and timeleft_to_juin
    """
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    df_dates.loc[df_dates.DWP % 100 <= 6, 'timeleft_to_juin'] = 6 - df_dates.DWP % 100
    df_dates.loc[df_dates.DWP % 100 > 6, 'timeleft_to_juin'] = 18 - df_dates.DWP % 100
    return df_dates[['DWP', 'timeleft_to_juin']]


def time_left_to_christmas(listDwp):
    """
    number of months left to december
    :param listDwp: list of dates at which we want to calculate the feature
    :return: pandas DataFrame containing dates and timeleft_to_december
    """
    df_dates = pd.DataFrame(listDwp, columns=['DWP'])
    df_dates['timeleft_to_december'] = 12 - df_dates.DWP % 100
    return df_dates[['DWP', 'timeleft_to_december']]



