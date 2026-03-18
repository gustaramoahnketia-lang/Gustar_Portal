import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Gustar Student Portal", layout="centered")

# Custom Styling: Times New Roman, Size 14
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: "Times New Roman", Times, serif;
        font-size: 14px;
    }
    table {
        border: 2px solid black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA STORAGE ---
# This creates a CSV file to store student information permanently
DATA_FILE = "student_records.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Student Name", "Age", "Sex", "Index Number"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- INTERFACE ---
st.title("🎓 Gustar Student Information Portal")
st.write("Please fill in your details below to register.")

# Form for Students
with st.form("student_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    index_no = st.text_input("Index Number")
    
    submit_button = st.form_submit_button("Submit Details")

if submit_button:
    if name and index_no:
        df = load_data()
        new_entry = pd.DataFrame([[name, age, sex, index_no]], 
                                 columns=["Student Name", "Age", "Sex", "Index Number"])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.success(f"Thank you, {name}! Your information has been received.")
    else:
        st.error("Please fill in all required fields.")

# --- ADMIN SECTION (Hidden by default) ---
st.divider()
if st.checkbox("Admin: View Arranged Records"):
    password = st.text_input("Enter Admin Password", type="password")
    if password == "admin123":  # You can change this password
        st.subheader("Student Records (Arranged by Age)")
        
        df = load_data()
        if not df.empty:
            # Sorting the information by Age
            df_sorted = df.sort_values(by="Age")
            st.table(df_sorted)
            
            # Option to download the arranged list
            csv = df_sorted.to_csv(index=False).encode('utf-8')
            st.download_button("Download Excel/CSV", csv, "students_by_age.csv", "text/csv")
        else:
            st.info("No records found yet.")