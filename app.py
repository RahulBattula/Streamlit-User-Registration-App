import streamlit as st
import mysql.connector
import pandas as pd
from db import DataBase_HOST, DataBase_USER, DataBase_PASSWORD, DataBase_NAME

st.set_page_config(
    page_icon="5210072_marketing_mobile_social media_icon.ico",
    page_title="User Registration"
)

try:
    mydb = mysql.connector.connect(
        host=DataBase_HOST,
        user=DataBase_USER,
        password=DataBase_PASSWORD,
        database=DataBase_NAME
    )
    if mydb.is_connected():
        mycursor = mydb.cursor()
        st.write("Connected to MySQL database")
except Exception as e:
    st.write("Error connecting to the database:", e)

mycursor.execute("CREATE TABLE IF NOT EXISTS users (name VARCHAR(255), age INT, DOB DATE, phone_number VARCHAR(255), email VARCHAR(255))")

st.title("User Registration Form")

name = st.text_input("Name")
age = st.number_input("Age")
dob = st.date_input("Date of Birth")
phone_number = st.text_input("Phone Number")
email = st.text_input("Email Address")

# Define a function to validate the form data
def validate_form_data(name, age,dob, phone_number, email):
    if not name:
        raise ValueError("Name is required.")
    if not age:
        raise ValueError("Age is required.")
    if not dob:
        raise ValueError("Enter or select your Date of Birth.")
    if not phone_number:
        raise ValueError("Phone Number is required.")
    if not email:
        raise ValueError("Email is required.")

submit_button = st.button("Submit")

if submit_button:
    if not name or not age or not dob or not phone_number or not email:
        st.error("Please fill in all required fields.")
    else:
        try:
            validate_form_data(name, age, dob, phone_number, email)
        except ValueError as e:
            # Display an alert if the form data is invalid
            st.error(e)
        else:
            # Insert the form data into the MySQL table
            mycursor.execute("INSERT INTO users (name, age, DOB, phone_number, email) VALUES (%s, %s, %s, %s, %s)", (name, age, dob, phone_number, email))
            mydb.commit()
            # Display a success message to the user
            st.success("Form submitted successfully!")
            st.experimental_rerun()

fetch_button = st.button("Fetch Records")

if fetch_button:
    mycursor.execute("SELECT * FROM users")
    user_data = mycursor.fetchall()
    df = pd.DataFrame(user_data, columns=["name", "age", "date_of_birth", "phone_number", "email_address"])
    st.table(df)



