import requests
import pandas as pd
import json
import ast
import streamlit as st
import parameters as pr

def safe_eval(val):
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return None
    return val

def process_output_data(df, company=None):
    extracted_df = df[['id', 'asset_tag', 'serial', 'company']]
    extracted_df['model_name'] = df['model'].apply(lambda x: safe_eval(x).get('name') if pd.notnull(x) else None)
    extracted_df['assigned_to_email'] = df['assigned_to'].apply(lambda x: safe_eval(x).get('email') if pd.notnull(x) else None)
    extracted_df['make'] = df['custom_fields'].apply(lambda x: safe_eval(x).get('Make', {}).get('value') if pd.notnull(x) else None)
    extracted_df['type'] = df['custom_fields'].apply(lambda x: safe_eval(x).get('Type', {}).get('value') if pd.notnull(x) else None)
    extracted_df['company'] = company
    extracted_df = extracted_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    return extracted_df


def search_hardware(mode, text, company, api_key, api_url):
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }

    if mode == 'Asset Tag':
        url = f"https://{api_url}/api/v1/hardware/bytag/{text}?deleted=false"
    elif mode == 'Serial Number':
        url = f"https://{api_url}/api/v1/hardware/byserial/{text}?deleted=false"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        if mode == 'Asset Tag' and 'id' in data.keys():
            df = pd.DataFrame([data])
        elif mode == 'Serial Number' and 'total' in data.keys():
            df = pd.DataFrame(data['rows'])
        else:
            st.error("Asset does not exist.")
            return pd.DataFrame()

        return process_output_data(df, company)
    else:
        st.error("Error fetching data.")
        return pd.DataFrame()
    


def check_connection_status(api_key, api_url):
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    url = f"https://{api_url}/api/v1/hardware?limit=1&offset=0&sort=created_at&order=desc"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        total_devices = data.get('total', 0)
        st.success(f"Connected! You have {total_devices} devices in the database.")
        return True
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"An error occurred: {req_err}")
    return False


def fetch_all_data(api_key, api_url):
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    
    total = check_connection_status(api_key, api_url)
    if total == 0:
        return pd.DataFrame()  

    all_data = []
    offset = 0

    while offset < total:
        url = f"https://{api_url}/api/v1/hardware?limit={pr.READ_LIMIT}&offset={offset}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['rows'])
            all_data.append(df)
            offset += pr.READ_LIMIT
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break

    # Concatenate all DataFrames if data is successfully fetched
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        return process_output_data(final_df)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data is fetched