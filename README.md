# ChurnPrediction
Predict future churners

## Introduction:
In this project, we aim to detect future churner (peoples who won’t make any further orders in the next 3 months).  
To do so, we will use a dataset containing orders of clients in the last 2 years.  

<img width="481" alt="1" src="https://user-images.githubusercontent.com/55580735/182121010-ec85c9cd-f286-4298-b1e3-83d935b67ab1.png">  

The dataset is clean with no missing values, thus the first step of the pipeline will be features engineering.  

## Features Engineering:  
We need to construct features from which the model will learn if a client will churn or not, all features constructed will be calculated based on 2 key variables (client_id, DWP). DWP refer to time  
Exemple: if we need to calculate age of a client, this feature should be calculated for the client “client_id” in the time “DWP”.  
The output will be a dataframe containing 3 variables (client_id, DWP, age of client in DWP).  
After constructing all features we will need to merge the features based on the two key variables (client_id, DWP).  
The last step will be to create the Target feature, this will be a binary variable which takes 0 if the client doesn’t make any order in the next 3 months after DWP and 1 if he does.  

## Features families:  
Based on the data we dispose it seems that we can construct 4 families of features:  
The folder “features” contain 5 files, the target and 4 other files containing each features.  

<img width="227" alt="2" src="https://user-images.githubusercontent.com/55580735/182121079-a4f9c58d-2c3c-4e5a-9f1f-054b33c5c775.png">  
 
1.	The first family of features will capture the client behavior in the past (before DWP).  
2.	The second will capture the client behavior in the last N months before DWP (I used 6 months).  
3.	The third will capture features relative to the first and the last orders of the client before DWP.  
4.	The fourth will capture special events like the approach of Christmas and the approach of summer.  

## Target:
Represent if the client was a churner or not, this is a binary variable which takes 0 if the client doesn’t make any order in the next 3 months after DWP and 1 if he does.  

## Merging features:  
After constructing features and the target, we will need to merge features on the two key variables (client_id, DWP).  
This step enabled us to create a Master table regrouping all features and target, this will be used to train and test a model.  

## Filling NA values:  
While creating features some NAs was created in the process (That’s because some clients weren’t client yet before some specific value of DWP).  
In this project I used tree based models (RandomForest and GradientBoosting), for this type of models using some aberrant value to fill NAs is a good practice.  
Filling with outliers is pretty common when you work with trees or forests (you imputatte missing values with the value that differs much from other values to perform better splitting).  

## Training/Testing:  
I used The Master Table values prior to Mars 2019 as training data, and values after this date as test data.  
This is also called BackTesting.  
We will predict churners in the 3 months after Mars 2019.  
We also know the real churners because we have data until juin 2019.  

## Evaluating model performance:  
Having the predicted and real churners we can evaluate our model using auc score.  
AUC is an abbrevation for area under the curve. It is used in classification analysis in order to determine which of the used models predicts the classes best.  
In general, an AUC of 0.5 suggests no discrimination (i.e., ability to diagnose patients with and without the disease or condition based on the test), 0.7 to 0.8 is considered acceptable, 0.8 to 0.9 is considered excellent, and more than 0.9 is considered outstanding.  

![3](https://user-images.githubusercontent.com/55580735/182121131-e5da7453-60eb-424f-8baa-89f8807e901f.png)  

 
Auc score = 0.95 is considered a good result.  

## Project structure:  

<img width="239" alt="4" src="https://user-images.githubusercontent.com/55580735/182121210-204bf203-4d2a-46ca-93d3-3c59ca5f05dc.png">  
 
Each file plays a specific role in the pipeline.  
The file Dataloader is a class having method “load_data()” this class enable us to load data from the folder data_train.  
The file FeaturesBuilder is a class having the method “create_features()” this method call functions from the files contained in the subfolder Features, create all the features and merge them. The output of calling this method is a Mastertable that will be used to train and test the model.  
The file Trainer has a method “train_gbm()” it takes as argument a Dataframe containing train data and fit a gradient boosting model.  
The file Predictor takes as argument the fitted classifier and have a method “predict()” this method makes predictions on test DataFrame given as argument.  
The file Evaluator calculate the auc score and plot the area under curve courbe.  
The file main is the file that calls all the pipeline from Loading data to evaluating the fitted model.  

## NB:  
Due to complexity reasons:  
I used a parameter ratio in the file main.py which enable us to work with just a proportion of data; for 16go RAM a ratio of 0.5 works just fine.  
The data available in this repo is just a sample of the original data used in reality.  
