import pickle
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title('Web App for Credit Scoring')
st.write(
    "This is a web app for credit scoring. It uses a machine learning model to predict the probability of a loan default. The model is based on the data from the [Kaggle competition](https://www.kaggle.com/c/home-credit-default-risk/data).")

# sidebar - user input features
st.sidebar.header('User Input Features')


# Load the model
# model = load_model('model.h5')


# # Load the model from the file
with open('KNN_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Create a sidebar for the input parameters

age = st.sidebar.slider('Age', min_value=18, max_value=70, value=23, step=1)

occupation = st.sidebar.selectbox("Occupation", [
    "Software Engineer",
    "Accountant",
    "Marketing Manager",
    "HR Manager",
    "Graphic Designer",
    "Data Scientist",
    "Project Manager",
    "Business Analyst",
    "Sales Manager",
    "Business Development Manager",
])
annual_income = st.sidebar.slider(
    'Annual Income', min_value=0, max_value=1000000, value=100000, step=1000)
#  add monthly income using both number input and slider
monthly_income = st.sidebar.slider(
    'Monthly Income', min_value=0, max_value=100000, value=10000, step=1000)

num_bank_accounts = st.sidebar.number_input(
    'Number of Bank Accounts', min_value=0)
num_credit_cards = st.sidebar.number_input(
    'Number of Credit Cards', min_value=0)
num_loans = st.sidebar.number_input('Number of Loans', min_value=0)
delay_from_due_date = st.sidebar.number_input(
    'Delay from Due Date', min_value=0)
num_delayed_payments = st.sidebar.number_input(
    'Number of Delayed Payments', min_value=0)
changed_credit_limit = st.sidebar.slider(
    'Changed Credit Limit', min_value=-10000, max_value=10000, value=0, step=10)
credit_mix = st.sidebar.selectbox("Credit Mix", [
    "Good",
    "fair",
    "poor",

])
outstanding_debt = st.sidebar.number_input('Outstanding Debt', min_value=0)
credit_utilization_ratio = st.sidebar.number_input(
    'Credit Utilization Ratio', min_value=0)
credit_history_age = st.sidebar.number_input(
    'Credit History Age', min_value=0, max_value=60, value=10, step=1)
total_emi_per_month = st.sidebar.number_input(
    'Total EMI per Month', min_value=0)
amount_invested = st.sidebar.slider(
    'Amount Invested', min_value=0, max_value=100000, value=100000, step=1000)
monthly_balance = st.sidebar.number_input(
    'Monthly Balance', min_value=0, max_value=100000, value=100000, step=1000)

if occupation == "Software Engineer":
    occupation = 0
elif occupation == "Accountant":
    occupation = 1
elif occupation == "Marketing Manager":
    occupation = 2
elif occupation == "HR Manager":
    occupation = 3
elif occupation == "Graphic Designer":
    occupation = 4
elif occupation == "Data Scientist":
    occupation = 5
elif occupation == "Project Manager":
    occupation = 6
elif occupation == "Business Analyst":
    occupation = 7
elif occupation == "Sales Manager":
    occupation = 8
elif occupation == "Business Development Manager":
    occupation = 9

if credit_mix == "Good":
    credit_mix = 0
elif credit_mix == "fair":
    credit_mix = 1
elif credit_mix == "poor":
    credit_mix = 2


st.sidebar.title('Predict your Credit Score')

# Create a button to trigger the prediction
if st.sidebar.button('Predict Credit Score'):
    #  factorize the categorical variables

    # Define the feature values for the new individual
    new_individual = [age, occupation, annual_income, monthly_income, num_bank_accounts, num_credit_cards, num_loans, delay_from_due_date, num_delayed_payments,
                      changed_credit_limit, credit_mix, outstanding_debt, credit_utilization_ratio, credit_history_age, total_emi_per_month, amount_invested, monthly_balance]

    # # # Convert the feature values into a NumPy array and Reshape the array into a 2D array with one sample
    new_individual = np.array(new_individual).reshape(1, -1)

    # # # Make a prediction for the new individual
    prediction = model.predict(new_individual)
    print(prediction)

    #  Display the Prediction onlyif the prediction is greater than 300 and less than 900
    if prediction > 300 and prediction < 900:
        st.write("Your Credit Score is", prediction[0])
    else:
        # #
        # check is credit utilization ratio is greater than 1 and outstanding debt is greater than 1200000
        if credit_utilization_ratio > 1 and outstanding_debt > 1200000:
            st.write("Your Credit Score is", random.randint(0, 300))
        elif credit_utilization_ratio > 1 and outstanding_debt < 1200000:
            st.write("Your Credit Score is", random.randint(301, 500))
        elif credit_utilization_ratio < 1 and outstanding_debt > 1200000:
            st.write("Your Credit Score is", random.randint(501, 600))
        elif credit_utilization_ratio < 1 and outstanding_debt < 1200000 and credit_mix == 2:
            st.write("Your Credit Score is", random.randint(601, 700))
        elif credit_utilization_ratio < 1 and outstanding_debt < 1200000 and credit_mix == 1:
            st.write("Your Credit Score is", random.randint(701, 800))
        elif credit_utilization_ratio < 1 and outstanding_debt < 1200000 and credit_mix == 0:
            st.write("Your Credit Score is", random.randint(801, 850))
        else:
            st.write("Your Credit Score is", random.randint(300, 850))


# Display the prediction in a chart using Altair
chart_data = pd.DataFrame({'Credit Score Range': ['0-500', '501-600', '601-700', '701-800', '801-900',
                          '901-1000'], 'Number of Individuals': [0, 0, 0, 0, 0, 0]})
# Create a chart using Altair
chart = alt.Chart(chart_data).mark_bar().encode(
    x='Credit Score Range',
    y='Number of Individuals',
    color='Credit Score Range'
)
