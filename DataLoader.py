import pandas as pd

class DataLoader():

    def __init__(self):
        self.data_train = None
        self.data_train_edited = None

    def load_data(self):
        self.data_train = pd.read_csv('data_train/train.csv', sep = ';')
        self.data_train_edited = self.data_train
        df_dt_ord = pd.to_datetime(self.data_train_edited['date_order'], format='%Y-%m-%d')
        self.data_train_edited['date_order_dwp'] = df_dt_ord.map(lambda x: x.year * 100 + x.month)
        df_dt_invoice = pd.to_datetime(self.data_train_edited['date_invoice'], format='%Y-%m-%d')
        self.data_train_edited['date_invoice_dwp'] = df_dt_invoice.map(lambda x: x.year * 100 + x.month)
