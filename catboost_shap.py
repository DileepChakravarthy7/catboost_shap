# -*- coding: utf-8 -*-
"""Catboost_shap.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_YGuMiTJidXyvd9JamSU9WYd9I1XNvyt
"""

!pip install shap
!pip install catboost

import pandas as pd
from imblearn.under_sampling import ClusterCentroids
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from catboost import CatBoostClassifier

import shap

df = pd.read_csv('/content/drive/MyDrive/Catboost_shap/WA_Fn-UseC_-HR-Employee-Attrition.csv',index_col=9)

df.info()

df.head(5)

yes_no_to_0_1 = {"Yes":1, "No":0}

business_travel_dict = {'Non_Travel':0,
                        'Travel_Rarely':1,
                        'Travel_Frequently':2}

df=df.replace({'Attrition':yes_no_to_0_1})
df = df.replace({'OverTime':yes_no_to_0_1})
df=df.replace({'BusinessTravel':business_travel_dict})

df

df.columns[df.nunique ()==1]

df = df.drop(["EmployeeCount","StandardHours","Over18"], axis=1)

df = pd.get_dummies(df)
# This instruction can be used before and after the use of
# get_dummies to see changes on the dataset
df.filter(like="Marital").sample(10, random_state=22)

df["Attrition"].value_counts()

"""**MODEL_ROUND_1**"""

x = df.drop("Attrition",axis=1)
y = df['Attrition']

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=22)

model = CatBoostClassifier(iterations=500,verbose=100,eval_metric="Recall")

model.fit(x_train,y_train)

print("TRAIN PERFORMANCE:\n")

confusion_matrix_train = confusion_matrix(y_train, model.predict(x_train))
confusion_matrix_train=pd.DataFrame(confusion_matrix_train,
                                    index = ['Actual_No','Actual_Yes'],
                                    columns=["Predicted_No","Predicted_Yes"])

display(confusion_matrix_train)

recall_resignation_train  = confusion_matrix_train.iloc[1,1] / confusion_matrix_train.iloc[1,:].sum()

print("Train score:{}".format(round(model.score(x_train,y_train),3)))

print("Recall Train:{}".format(round(recall_resignation_train,3)))

print("\n*******************************************************\n")

print('TEST PREFORMANCE:\n')

confusion_matrix_test = confusion_matrix(y_test,model.predict(x_test))

confusion_matrix_test = pd.DataFrame(confusion_matrix_test,
                                     index = ['Actual_No','Actual_Yes'],
                                    columns=["Predicted_No","Predicted_Yes"])

display(confusion_matrix_test)

recall_resignation_test = confusion_matrix_test.iloc[1,1] / confusion_matrix_test.iloc[1,:].sum()
print("Train Score: {}".format(round(model.score(x_test,y_test),3)))
print("Recall Train: {}".format(round(recall_resignation_test,3)))

"""**MODEL_ROUND_2(using class weights)**"""

class_weights = dict({0:1, 1:5})
model = CatBoostClassifier(iterations=500,
                           verbose=100,
                           eval_metric="Recall",
                           class_weights=class_weights)
model.fit(x_train,y_train);

print("TRAIN PERFORMANCE:\n")

confusion_matrix_train = confusion_matrix(y_train, model.predict(x_train))
confusion_matrix_train=pd.DataFrame(confusion_matrix_train,
                                    index = ['Actual_No','Actual_Yes'],
                                    columns=["Predicted_No","Predicted_Yes"])

display(confusion_matrix_train)

recall_resignation_train  = confusion_matrix_train.iloc[1,1] / confusion_matrix_train.iloc[1,:].sum()

print("Train score:{}".format(round(model.score(x_train,y_train),3)))

print("Recall Train:{}".format(round(recall_resignation_train,3)))

print("\n*******************************************************\n")

print('TEST PREFORMANCE:\n')

confusion_matrix_test = confusion_matrix(y_test,model.predict(x_test))

confusion_matrix_test = pd.DataFrame(confusion_matrix_test,
                                     index = ['Actual_No','Actual_Yes'],
                                    columns=["Predicted_No","Predicted_Yes"])

display(confusion_matrix_test)

cc = ClusterCentroids()
x_cc, y_cc = cc.fit_resample(x, y)
x_train, x_test, y_train, y_test = train_test_split(x_cc, y_cc)

print("TRAIN PERFORMANCE:\n")

confusion_matrix_train = confusion_matrix(y_train, model.predict(x_train))
confusion_matrix_train=pd.DataFrame(confusion_matrix_train,
                                    index = ['Actual_No','Actual_Yes'],
                                    columns=["Predicted_No","Predicted_Yes"])

display(confusion_matrix_train)

recall_resignation_train  = confusion_matrix_train.iloc[1,1] / confusion_matrix_train.iloc[1,:].sum()

print("Train score:{}".format(round(model.score(x_train,y_train),3)))

print("Recall Train:{}".format(round(recall_resignation_train,3)))

print("\n*******************************************************\n")

print('TEST PREFORMANCE:\n')

confusion_matrix_test = confusion_matrix(y_test,model.predict(x_test))

confusion_matrix_test = pd.DataFrame(confusion_matrix_test,
                                     index = ['Actual_No','Actual_Yes'],
                                    columns=["Predicted_No","Predicted_Yes"])

display(confusion_matrix_test)

feat_imp = pd.DataFrame(model.feature_importances_, index=x.columns, columns=["Importance"])
feat_imp.sort_values(by="Importance", ascending=False).head(15)

# Overall calculation of the SHAP model and values
shap_explainer = shap.TreeExplainer(model)
shap_values = shap_explainer.shap_values(x)
#
Employee_ID = 1
shap.initjs()
index_choice = df.index.get_loc(Employee_ID)
shap.force_plot(shap_explainer.expected_value, shap_values[index_choice], x.iloc[index_choice])

# Overall calculation of the SHAP model and values
shap_explainer = shap.TreeExplainer(model)
shap_values = shap_explainer.shap_values(x)
#
Employee_ID = 2
shap.initjs()
index_choice = df.index.get_loc(Employee_ID)
shap.force_plot(shap_explainer.expected_value, shap_values[index_choice], x.iloc[index_choice])

shap.initjs()
shap.force_plot(shap_explainer.expected_value, shap_values, x)

shap.summary_plot(shap_values, x, x.columns)

