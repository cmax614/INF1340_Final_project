# -*- coding: utf-8 -*-
"""Copy of PythonFinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YYsmgva_lv5zR0uCeaN1OqiqKOn9JLpu
"""

import pandas as pd 
import numpy as np
import io
from google.colab import files
import sklearn
from scipy import stats
import matplotlib.pyplot as plt
import os
import seaborn as sns
 
 
uploaded = files.upload()



 
df = pd.read_csv(io.BytesIO(uploaded['heart.csv']))
print(df)
df.describe()

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score, recall_score, precision_score, average_precision_score, f1_score, classification_report, accuracy_score, plot_roc_curve, plot_precision_recall_curve, plot_confusion_matrix

# print out the correlation matrix and deciding which variables to study
corr_matrix = df.corr()
print(corr_matrix)

# visualizing the correlation matrix
mask = np.triu(np.ones_like(corr_matrix,dtype=bool))
sns.heatmap(corr_matrix,cmap="BuPu",annot=True,mask=mask)

# Group B numerical variables and categorical variables
num_var = ["chol","thalach","age","oldpeak"]
cat_var = ["exng","sex","fbs"]

print(df.head())

df.info()

df.describe()

df.columns

#we’ll remove:
#the columns with many missing values, which are slope, ca, thal.
#the rows with missing values.
#df = df.drop(['slp', 'caa', 'thall'], axis=1)

#df = df.dropna().copy()

#info showing updated columns
df.info()

#we can print out the numeric columns and categorical columns
numeric_cols = ['age','chol', 'thalachh', 'oldpeak']
cat_cols = list(set(df.columns) - set(numeric_cols) - {'output','cp','restecg','thalachh','trtbps','caa','slp','thall'})
cat_cols.sort()

print(numeric_cols)
print(cat_cols)

#To make sure the fitted model can be generalized to unseen data, 
#we always train it using some data while evaluating the model using 
#the holdout data. So we need to split the original dataset into training 
#and test datasets.
random_seed = 888
df_train, df_test = train_test_split(df, test_size=0.2, random_state=random_seed, stratify=df['output'])


print(df_train.shape)
print(df_test.shape)
print()
print(df_train['output'].value_counts(normalize=True))
print()
print(df_test['output'].value_counts(normalize=True))

#performs standardization on the numeric_cols of df to return the new array X_numeric_scaled. 
#transforms cat_cols to a NumPy array X_categorical.
#combines both arrays back to the entire feature array X.
#assigns the target column to y.
scaler = StandardScaler()
scaler.fit(df_train[numeric_cols])

def get_features_and_target_arrays(df, numeric_cols, cat_cols, scaler):
    X_numeric_scaled = scaler.transform(df[numeric_cols])
    X_categorical = df[cat_cols].to_numpy()
    X = np.hstack((X_categorical, X_numeric_scaled))
    y = df['output']
    return X, y

X, y = get_features_and_target_arrays(df_train, numeric_cols, cat_cols, scaler)

#We can fit the logistic regression in Python on our example dataset.

#We first create an instance clf of the class LogisticRegression. 
# logistic regression with no penalty term in the cost function.

clf = LogisticRegression(penalty='none')

#Then we can fit it using the training dataset.

clf.fit(X, y)

LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True, intercept_scaling=1, l1_ratio=None, max_iter=100, multi_class='auto', n_jobs=None, penalty='none', random_state=None, solver='lbfgs', tol=0.0001, verbose=0, warm_start=False)

#scaled test dataset
X_test, y_test = get_features_and_target_arrays(df_test, numeric_cols, cat_cols, scaler)

#prediction results from the test dataset
test_prob = clf.predict_proba(X_test)[:, 1]
test_pred = clf.predict(X_test)

#Using 0.5 as threshold:
#Precision
print('Precision = {:.5f}'.format(precision_score(y_test, test_pred)))

#Using 0.5 as threshold:
#Accuracy
print('Accuracy = {:.5f}'.format(accuracy_score(y_test, test_pred)))

#Interpret the Results

coefficients = np.hstack((clf.intercept_, clf.coef_[0]))
pd.DataFrame(data={'variable': ['intercept'] + cat_cols + numeric_cols, 'coefficient': coefficients})

"""For categorical feature exng, this fitted model says that holding all the other features at fixed values, the log of odds of having heart disease for people who do not have exercised induced angina, is 1.41 times lower when compared to people who have exercise induced angina. 

For categorical feature fbs, this fitted model says that holding all the other features at fixed values, the log of odds of having heart disease for people who have a fasting blood sugar level less 120 mg/dl, is 0.25 times lower when compared to people who have a fasting blood sugar level more than 120 mg/dl.

For categorical feature sex, this fitted model says that holding all the other features at fixed values, the log of odds of having heart disease for females is -1.43 times lower when compared to men. 


"""

#Since the numerical variables are scaled by StandardScaler, we need to think of them in terms of standard deviations. Let’s first print out the list of numeric variable and its sample standard deviation.
pd.DataFrame(data={'variable': numeric_cols, 'unit': np.sqrt(scaler.var_)})

"""For numerical variable chol, holding all other variables fixed, there is a 46% decrease in the odds of having a heart disease for every standard deviation increase in cholesterol (63.470764) since exp(0.380175) = 1.46. 
Calculated as 1(e^.380175)

For numerical variable age, holding all other variables fixed, there is a 20% increase in the odds of having a heart disease for every standard deviation increase in age (63.470764) since exp(0.184601) = 1.20273845173
Calculated as 1(e^.184601)

For numerical variable thalachh, holding all other variables fixed, there is a 100% increase in the odds of having a heart disease for every standard deviation increase in maximum heart rate achieved (63.470764) since exp(0.694858) = 2.00342456745
Caculated as 1(e^.694858)

For numerical variable oldpeak, holding all other variables fixed, there is a 90% increase in the odds of having a heart disease for every standard deviation increase in oldpeak (63.470764) since exp(0.642905) = 1.90199816624
Caculated as 1(e^.642905)
"""