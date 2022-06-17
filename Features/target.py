import pandas as pd
from dateutil.relativedelta import relativedelta


def get_labels(df, start_dates, lookahead, periodicity):
    dfs = []
    for start_date in start_dates:
        dfs.append(get_labels_once(df, start_date, lookahead, periodicity))
    return pd.concat(dfs)


def get_labels_once(df, start_date, lookahead, periodicity):
    """ Flag clients who who took loan in next 'lookahead' months (or, more generally, periodicity) counting from 'start_date'
    Args:
        df_clients: dataframe containing client data
        df_loans: dataframe containing loans data
        start_date: date from which flags begin. This date should be of type int
        lookahead: in months (or periodicity), time ahead to check if a client contracted loan
        periodicity: week, month or quarter
    Returns:
        a dataframe with client id and a column with 0 for clients who did not contract any loans in given perio and 1 otherwise
    """

    # TODO: add other periodicities (e.g. week, quarter)
    df.date_order = pd.to_datetime(df.date_order, format='%Y-%m-%d')
    all_client_ids = df["client_id"].to_frame()

    if (periodicity == "m") or (periodicity == "month"):
        # month = lookahead % 100
        # year = lookahead // 100

        start_date_int = start_date

        # Ones
        start_date = pd.to_datetime(start_date, format="%Y%m")
        end_date = start_date + relativedelta(months=lookahead)

        df = df[["client_id", "date_order"]]
        df = df[df["date_order"] >= start_date]
        df = df[df["date_order"] <= end_date]
        df["DWP"] = start_date_int
        df["TARGET"] = 1
        df.drop("date_order", axis=1, inplace=True)

        # Zeros
        ones = df["client_id"]
        all_client_ids.drop_duplicates(inplace=True)
        zeros = all_client_ids[~all_client_ids.client_id.isin(ones.copy())].copy()
        zeros["DWP"] = start_date_int
        zeros["TARGET"] = 0
        return pd.concat([df, zeros], sort=False)
    else:
        raise Exception("Not yet implemented")