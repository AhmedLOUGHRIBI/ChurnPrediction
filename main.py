import DataLoader
import FeaturesBuilder
import Trainer
import Predictor
import Evaluator


loader = DataLoader.DataLoader()
loader.load_data()

ratio = 0.5
list_clients = loader.data_train_edited['client_id'].drop_duplicates().sample(frac=ratio)
loader.data_train_edited = loader.data_train_edited[loader.data_train_edited.client_id.isin(list_clients)]

builder = FeaturesBuilder.FeaturesBuilder(loader, [201803, 201806, 201809, 201812, 201903])
builder.create_all_features()

builder.MasterTable.to_csv('results/Mastertable.csv', index=False)
dfMasterTable = builder.MasterTable.fillna(-1000000)

date_prediction_dwp = 201903
df_train = dfMasterTable[dfMasterTable.DWP < date_prediction_dwp]
df_test = dfMasterTable[dfMasterTable.DWP == date_prediction_dwp]

trainer = Trainer.trainer()
trainer.train_gbm(df_train)
predictor = Predictor.Predictor(trainer.gb_clf)
predictor.predict(df_test)

predictor.df_predictions.to_csv('results/df_predictions_gbm.csv', index=False)

evaluate = Evaluator.Evaluator()
evaluate.show_results(predictor.df_predictions)





