from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

class trainer():
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=450)
        self.gb_clf = GradientBoostingClassifier(n_estimators=170, learning_rate=0.05, max_features=7 , max_depth=3,
                                            random_state=0)
        self.xgb_clf = XGBClassifier()


    def train(self, df_train):

        features_out = ['Unnamed: 0','client_id','DWP','TARGET']

        df_x = df_train[[col for col in df_train.columns if col not in features_out]]
        x = df_x.values
        y=df_train.TARGET
        self.clf.fit(x,y)

    def train_gbm(self, df_train):
        features_out = ['Unnamed: 0', 'client_id', 'DWP', 'TARGET']

        df_x = df_train[[col for col in df_train.columns if col not in features_out]]
        x = df_x.values
        y = df_train.TARGET
        self.gb_clf.fit(x, y)

    def train_xgb(self, df_train):
        features_out = ['Unnamed: 0', 'client_id', 'DWP', 'TARGET']

        df_x = df_train[[col for col in df_train.columns if col not in features_out]]
        x = df_x.values
        y = df_train.TARGET
        self.xgb_clf.fit(x, y)