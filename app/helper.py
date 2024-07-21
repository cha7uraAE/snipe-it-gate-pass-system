import pandas as pd
import streamlit as st
import glob
import os


# Function to load company names from CSV
def load_company_names(csv_path):
    try:
        df = pd.read_csv(csv_path)
        company_names = df['company_name'].tolist()
        company_names.sort()
        return company_names, df
    except Exception as e:
        st.error(f"Error loading company names: {e}")
        return [], pd.DataFrame()

# Function to add a new company name to the CSV
def add_company_name(csv_path, new_company_name):
    try:
        df = pd.read_csv(csv_path)
        if new_company_name not in df['company_name'].values:
            df_new = pd.DataFrame({'company_name': [new_company_name]})
            df = pd.concat([df, df_new])
            df.to_csv(csv_path, index=False)
            st.success(f"Company '{new_company_name}' added successfully!")
        else:
            st.warning(f"Company '{new_company_name}' already exists in the list.")
    except Exception as e:
        st.error(f"Error adding company name: {e}")

# Function to delete a company name from the CSV
def delete_company_name(csv_path, company_name):
    try:
        df = pd.read_csv(csv_path)
        if company_name in df['company_name'].values:
            df = df[df['company_name'] != company_name]
            df.to_csv(csv_path, index=False)
            st.success(f"Company '{company_name}' deleted successfully!")
        else:
            st.warning(f"Company '{company_name}' not found in the list.")
    except Exception as e:
        st.error(f"Error deleting company name: {e}")


def load_historical_data(csv_path):
    all_files = glob.glob(os.path.join(csv_path, "*.csv"))
    df_list = []
    for filename in all_files:
        df = pd.read_csv(filename)
        df_list.append(df)
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()