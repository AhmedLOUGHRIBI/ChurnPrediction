import pandas as pd


class Predictor():

    def __init__(self, classifier):
        self.clf = classifier
        self.df_predictions = pd.DataFrame()

    def predict(self, df_test):

        features_out = ['Unnamed: 0', 'client_id', 'DWP', 'TARGET']
        test_x = df_test[[col for col in df_test.columns if col not in features_out]].values
        preds = self.clf.predict_proba(test_x)[:, 1]

        self.df_predictions['client_id']= df_test['client_id']
        self.df_predictions['PREDICTION'] = preds
        self.df_predictions['TARGET'] = df_test['TARGET']