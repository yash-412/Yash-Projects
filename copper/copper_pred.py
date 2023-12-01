import streamlit as st
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from xgboost import XGBRegressor

# Load your trained regression model

# Get the absolute path to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the absolute path to the pickle file
final_model_path = os.path.join(script_dir, "final_model.pkl")

# Check if the file exists before attempting to load it
if os.path.exists(final_model_path):
    # Load the model
    with open(final_model_path, 'rb') as file:
        final_model = pickle.load(file)
    st.success("Model loaded successfully.")
else:
    st.error("Error: 'final_model.pkl' not found. Please check the file path.")

# Load your saved scaler
# scaler_path = "path/to/your/scaler.joblib"
# scaler = joblib.load(scaler_path)

# Function to apply transformations to input data
def transform_input(input_data):
    transformed_data = input_data.copy()

    # Standardize 'selling_price'
    transformed_data['selling_price'] = scaler.transform(input_data[['selling_price']])

    # Log1p transformation for 'quantity_tons_log'
    transformed_data['quantity_tons_log'] = np.log1p(input_data['quantity_tons_log'])

    # Log2 transformation for 'width_log' and 'thickness_log'
    transformed_data['width_log'] = np.log2(input_data['width_log'])
    transformed_data['thickness_log'] = np.log2(input_data['thickness_log'])

    # Standardize 'width_log' and 'thickness_log'
    transformed_data[['width_log', 'thickness_log']] = scaler.transform(
        input_data[['width_log', 'thickness_log']]
    )

    return transformed_data

# Function to reverse transformations on predicted values
def reverse_transform(predicted_value):
    # Reverse standardization for 'selling_price'
    reversed_value = scaler.inverse_transform(np.array([[predicted_value]]))[0][0]

    return reversed_value

# Streamlit App
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Regression", "Classifier"])

    if page == "Regression":
        st.title("Regression Page")

        # Collect user inputs
        application = st.text_input("Enter Application:")
        width = st.number_input("Enter Width:")
        thickness_log = st.number_input("Enter Thickness (log2 transformed):")
        selling_price = st.number_input("Enter Selling Price:")
        quantity_tons_log = st.number_input("Enter Quantity Tons (log1p transformed):")
        month = st.number_input("Enter Month:")
        year = st.number_input("Enter Year:")

        # Create a DataFrame from user input
        input_data = pd.DataFrame({
            'application': [application],
            'width': [width],
            'thickness_log': [thickness_log],
            'selling_price': [selling_price],
            'quantity_tons_log': [quantity_tons_log],
            'month': [month],
            'year': [year]
        })

        # Transform input data
        transformed_data = transform_input(input_data)

        if st.button("Enter"):
            # Predict using the model
            predicted_value = final_model.predict(transformed_data)[0]

            # Reverse transformations
            actual_selling_price = reverse_transform(predicted_value)

            # Display results
            st.write("Predicted Selling Price:", predicted_value)
            st.write("Actual Selling Price (after reverse transformation):", actual_selling_price)

    elif page == "Classifier":
        st.title("Classifier Page")
        # Add code for the classifier page here

if __name__ == "__main__":
    main()

# streamlit run D:\VSCodium\Guvi-Projects\copper\copper_pred.py