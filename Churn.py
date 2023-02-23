# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gmHcb4dphXNn4yH2Xdpe2AH3iuMRgzDZ
"""

import pandas as pd
import streamlit as st
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Preprocess data
df = df.drop(['customerID'], axis=1) # drop ID column
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce') # convert TotalCharges column to numeric
df = df.dropna() # drop rows with missing values

# Encode categorical features
categorical_features = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
                        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
preprocessor = ColumnTransformer(transformers=[('cat', OneHotEncoder(), categorical_features)], remainder='passthrough')
X = df.drop(['Churn'], axis=1)
y = df['Churn']
X = preprocessor.fit_transform(X)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Define function to predict customer churn
def predict_defection(gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
                  MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
                  TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
                  MonthlyCharges, TotalCharges):
    
    # Create DataFrame with input values
    input_df = pd.DataFrame([[gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
                              MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
                              TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
                              MonthlyCharges, TotalCharges]], 
                            columns=['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
                                     'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                                     'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
                                     'PaymentMethod', 'MonthlyCharges', 'TotalCharges'])

    # Encode categorical features
    input_df = preprocessor.transform(input_df)

    # Predict churn
    prediction = model.predict(input_df)[0]

    return prediction

# Create Streamlit app
st.title('Customer defection Prediction by Suraj Chaudhary')

# Create input fields
gender = st.selectbox('Gender', ['Male', 'Female'])
SeniorCitizen = st.selectbox('Senior Citizen', [0, 1])
Partner = st.selectbox('Partner', ['Yes', 'No'])
Dependents = st.selectbox('Dependents', ['Yes', 'No'])
tenure = st.slider('Tenure (months)', 0, 100, 50)
PhoneService = st.selectbox('Phone Service', ['Yes', 'No'])
MultipleLines = st.selectbox('Multiple Lines', ['No phone service', 'No', 'Yes'])
InternetService = st.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'])
OnlineSecurity = st.selectbox('Online Security', ['No internet service', 'No', 'Yes'])
OnlineBackup = st.selectbox('Online Backup', ['No internet service','No', 'Yes'])
DeviceProtection = st.selectbox('Device Protection', ['No internet service', 'No', 'Yes'])
TechSupport = st.selectbox('Tech Support', ['No internet service', 'No', 'Yes'])
StreamingTV = st.selectbox('Streaming TV', ['No internet service', 'No', 'Yes'])
StreamingMovies = st.selectbox('Streaming Movies', ['No internet service', 'No', 'Yes'])
Contract = st.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'])
PaperlessBilling = st.selectbox('Paperless Billing', ['Yes', 'No'])
PaymentMethod = st.selectbox('Payment Method', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
MonthlyCharges = st.number_input('Monthly Charges', min_value=0.0, max_value=1000.0, value=50.0, step=1.0)
TotalCharges = st.number_input('Total Charges', min_value=0.0, max_value=100000.0, value=5000.0, step=1.0)

# Predict churn
if st.button('Predict defection'):
    prediction = predict_defection(gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
                               MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
                               TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
                               MonthlyCharges, TotalCharges)
    if prediction == 0:
        st.success('Customer is likely to stay.')
    else:
        st.warning('Customer is likely to defect.')

# Display dataset
if st.checkbox('Show dataset'):
    st.write(df)
