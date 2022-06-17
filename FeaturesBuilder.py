from Features.FeaturesBehaviorLastNMonths import *
from Features.FeaturesFirstLastOrders import *
from Features.FeaturesOrdersPast import *
from Features.target import *
from Features.Events import *
from functools import reduce


class FeaturesBuilder():

    def __init__(self, loader, list_dwp):
        self.MasterTable = None
        self.DataLoader = loader  # must have loaded data
        self.listDwp = list_dwp
        self.list_clients = loader.data_train.client_id.unique()

    def create_all_features(self):
        df1 = last_orderchannel(self.DataLoader.data_train_edited, self.listDwp)
        df2 = last_quantity_ordered(self.DataLoader.data_train_edited, self.listDwp)
        df3 = last_sales_net(self.DataLoader.data_train_edited, self.listDwp)
        df4 = first_quantity_ordered(self.DataLoader.data_train_edited, self.listDwp)
        df5 = first_sales_net(self.DataLoader.data_train_edited, self.listDwp)
        df6 = first_orderchannel(self.DataLoader.data_train_edited, self.listDwp)
        df7 = time_since_first_order(self.DataLoader.data_train_edited, self.listDwp)
        df8 = time_since_last_order(self.DataLoader.data_train_edited, self.listDwp)
        df9 = last_order_difference_OrderInvoice(self.DataLoader.data_train_edited, self.listDwp)
        df10 = first_order_difference_OrderInvoice(self.DataLoader.data_train_edited, self.listDwp)
        df11 = difference_order_invoice_stats_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df12 = quantity_ordered_stats_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df13 = sales_net_stats_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df14 = number_change_region_past(self.DataLoader.data_train_edited, self.listDwp)
        df15 = number_order_channels_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df16 = order_channel_dominant_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df17 = number_products_ordered_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df18 = number_orders_before_dwp(self.DataLoader.data_train_edited, self.listDwp)
        df19 = region_change_past_3_months(self.DataLoader.data_train_edited, self.listDwp)
        df20 = number_products_ordered_last_n_months(self.DataLoader.data_train_edited, self.list_clients, self.listDwp, 7)
        df21 = number_orders_by_channel_last_n_months(self.DataLoader.data_train_edited, self.list_clients, self.listDwp, 7)
        df22 = quantity_ordered_last_n_months(self.DataLoader.data_train_edited, self.list_clients, self.listDwp, 7)
        df23 = number_orders_last_n_months(self.DataLoader.data_train_edited, self.list_clients, self.listDwp, 7)
        df24 = sales_last_n_months(self.DataLoader.data_train_edited, self.list_clients, self.listDwp, 7)
        df25 = number_branchs_used_last_n_months(self.DataLoader.data_train_edited, self.list_clients, self.listDwp, 7)
        df26 = time_left_summer(self.listDwp)
        df27 = time_left_to_christmas(self.listDwp)

        df_target = get_labels(self.DataLoader.data_train_edited, self.listDwp, 3, periodicity='m')
        df_target = df_target.drop_duplicates(['client_id', 'DWP'])
        dfs = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17, df18,
               df19, df20, df21, df22, df23, df24, df25, df26, df27, df_target]

        df_res = reduce(lambda left, right: pd.merge(left, right, on=list({'client_id', 'DWP'} & set(right.columns)),
                                                     how='left'), dfs)

        self.MasterTable = df_res