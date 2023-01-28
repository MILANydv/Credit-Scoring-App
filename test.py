import pickle

import matplotlib.pyplot as plt
import numpy as np  # linear algebra
import pandas as pd
import seaborn as sns
import streamlit as st

# Create function to get user input and make prediction

# ceate a Title
st.title('Web App for Credit Scoring')

with open("xgboost_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)


def predict():
    # Get user input from the sidebar

    person_age = st.sidebar.text_input("Enter person's age:")
    person_income = st.sidebar.text_input("Enter person's income:")
    person_home_ownership = st.sidebar.selectbox("Select person's home ownership:", [
        "Own", "Rent", "Mortgage", "Other"])
    person_emp_length = st.sidebar.text_input(
        "Enter person's employment length:")
    loan_intent = st.sidebar.selectbox("Select loan intent:", [
        'PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT',
        'DEBTCONSOLIDATION'])
    loan_grade = st.sidebar.selectbox("Select loan grade:", [
        "A", "B", "C", "D", "E", "F", "G"])
    loan_amnt = st.sidebar.text_input("Enter loan amount:")
    loan_int_rate = st.sidebar.text_input("Enter loan interest rate:")
    loan_percent_income = st.sidebar.text_input(
        "Enter loan percent of income:")
    cb_person_default_on_file = st.sidebar.selectbox(
        "Select whether person has default on file:", ["yes", "no"])
    cb_person_cred_hist_length = st.sidebar.text_input(
        "Enter person's credit history length:")
#  create a button to predict the loan status
    if st.sidebar.button("Predict"):
        #  show selected and inputted values in rows
        st.subheader("User Input:")
        st.write("Person's age:", person_age)
        st.write("Person's income:", person_income)
        st.write("Person's home ownership:", person_home_ownership)
        st.write("Person's employment length:", person_emp_length)
        st.write("Loan intent:", loan_intent)
        st.write("Loan grade:", loan_grade)
        st.write("Loan amount:", loan_amnt)
        st.write("Loan interest rate:", loan_int_rate)
        st.write("Loan percent of income:", loan_percent_income)
        st.write("Person has default on file:", cb_person_default_on_file)
        st.write("Person's credit history length:", cb_person_cred_hist_length)

        # Make DataFrame for model input
        input_df = pd.DataFrame({'person_age': person_age, 'person_income': person_income,
                                 'person_home_ownership': person_home_ownership, 'person_emp_length': person_emp_length,
                                 'loan_intent': loan_intent, 'loan_grade': loan_grade, 'loan_amnt': loan_amnt,
                                 'loan_int_rate': loan_int_rate, 'loan_percent_income': loan_percent_income,
                                 'cb_person_default_on_file': cb_person_default_on_file, 'cb_person_cred_hist_length': cb_person_cred_hist_length},
                                index=[0])

        # Make prediction
        prediction = loaded_model.predict(input_df)
        print(prediction)
        #  if prediction is 1, then the loan is approved else the loan is not approved
        if prediction == 1:
            prediction = "Approved"
        else:
            prediction = "Not Approved"

        #  if approved, then show in green color else show in red color

        # prediction title
        st.subheader("Prediction:")

        if prediction == "Approved":
            st.success("The loan status is: {}".format(prediction))
        else:
            st.error("The loan status is: {}".format(prediction))

        #  use graph to show the prediction
        st.subheader("Prediction Probability:")
        pred_proba = loaded_model.predict_proba(input_df)
        st.write(pred_proba)

        #  create a bar chart to show the prediction probability
        st.bar_chart(pred_proba)

        #


# Run the app
if __name__ == '__main__':
    predict()
