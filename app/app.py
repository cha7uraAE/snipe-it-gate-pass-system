import pandas as pd
import streamlit as st
from pdf_generator import create_gate_pass
from snipe_it_data_generation import search_hardware, check_connection_status, fetch_all_data
import helper as hp
from datetime import datetime

st.set_page_config(page_title="Gate Pass Generator",
                   page_icon="data/favicon.ico",
                   layout="wide")

if __name__ == "__main__":
    st.title('Gate Pass Generator')
    
    with st.sidebar:
        st.header('Configuration')
        api_key = st.text_input('Enter your API Key:', type='password', placeholder='Bearer xxxxxxxxxxxxxxx')
        api_url = st.text_input('Enter your API URL:', placeholder='develop.snipeitapp.com')
        if st.button('Connect'):
            if not api_key or not api_url:
                st.error("API Key and URL must not be empty.")
                st.session_state.connected = False
            else:
                st.session_state.connected = check_connection_status(api_key, api_url)

    if 'connected' not in st.session_state:
        st.session_state.connected = False

    if st.session_state.connected:
        company_names, company_df = hp.load_company_names('data/company_names.csv')
        
        tab1, tab2, tab3, tab4 = st.tabs(["Search Assets", "Manage Companies", "Historical Data", "All Data"])
        
        with tab1:
            col1, col2, col3 = st.columns([6, 1, 2])
            with col1:
                search_text = st.text_input('Enter asset tag to search:', disabled=not st.session_state.connected)
            with col2:
                search_option = st.selectbox('Search by:', ('Asset Tag', 'Serial Number'))
            with col3:
                company = st.selectbox('Select company for handover:', company_names, index=0)
            
            if st.button('Search'):
                new_data = search_hardware(search_option, search_text, company, api_key, api_url)
                if 'df' not in st.session_state:
                    st.session_state.df = pd.DataFrame({'id':[], 'asset_tag':[], 'serial':[], 'company':[], 'model_name':[], 'assigned_to_email':[], 'make':[], 'type':[]})
                st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
                st.session_state.df = st.session_state.df.drop_duplicates()
                st.session_state.df = st.session_state.df.sort_values(['company', 'asset_tag'])
                print(st.session_state.df.columns)
            
            if st.button('Reset'):
                st.session_state.df = pd.DataFrame({'id':[], 'asset_tag':[], 'serial':[], 'company':[], 'model_name':[], 'assigned_to_email':[], 'make':[], 'type':[]})
                st.success("Session data has been reset.")
            
            if 'df' in st.session_state and not st.session_state.df.empty:
                st.write("Extracted Data:")
                st.dataframe(st.session_state.df)
                
                output_data = {
                    'item': [f"{row['make']} {row['type']}" for index, row in st.session_state.df.iterrows()],
                    'serial': st.session_state.df['serial'],
                    'quantity': [1] * len(st.session_state.df),
                    'company': st.session_state.df['company']
                }
                df_output = pd.DataFrame(output_data)

                if st.button('Generate Gate Pass PDF'):
                    pdf_path = create_gate_pass(df_output)
                    with open(pdf_path, "rb") as file:
                        pdf_bytes = file.read()

                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=f"{pdf_path[10:]}.pdf",
                        mime="application/pdf"
                    )
                    
                    # Save to CSV
                    date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                    csv_path = f"historical_data/{date_time}_gate_pass.csv"
                    historical_df_to_save = st.session_state.df.copy()
                    historical_df_to_save['created_date'] = date_time
                    historical_df_to_save['created_by'] = 'user1'
                    historical_df_to_save.to_csv(csv_path, index=False)
                    st.success(f"Data saved to {csv_path}")

        with tab2:
            company_df = company_df.sort_values('company_name', ascending=True).reset_index(drop=True)
            st.dataframe(company_df)

            new_company_name = st.text_input('New Company Name')
            if st.button('Add Company'):
                if new_company_name:
                    hp.add_company_name('data/company_names.csv', new_company_name)
                    st.rerun()
                else:
                    st.error("Company name cannot be empty.")
            
            company_to_delete = st.selectbox('Select company to delete:', company_names)
            if st.button('Delete Company'):
                st.session_state.confirm_delete = company_to_delete
            
            if 'confirm_delete' in st.session_state:
                st.warning(f"Are you sure you want to delete the company '{st.session_state.confirm_delete}'?")
                if st.button('Confirm Delete'):
                    hp.delete_company_name('data/company_names.csv', st.session_state.confirm_delete)
                    del st.session_state.confirm_delete
                    st.rerun()
                if st.button('Cancel'):
                    del st.session_state.confirm_delete
        
        with tab3:
            historical_df = hp.load_historical_data('historical_data')
            if not historical_df.empty:
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    search_column = st.selectbox('Select Column to Search', historical_df.columns)
                with col2:
                    unique_values = historical_df[search_column].unique()
                    selected_value = st.selectbox('Select Value', unique_values)
                
                if st.button('Search Historical Data'):
                    filtered_df = historical_df[historical_df[search_column] == selected_value].reset_index(drop=True)
                    st.dataframe(filtered_df)
                historical_df = historical_df.sort_values('created_date', ascending=False).reset_index(drop=True)
                
                st.write("All historical Records:")
                st.dataframe(historical_df)
            else:
                st.warning("No historical data files found.")

        with tab4:
            if 'all_data' not in st.session_state:
                st.session_state.all_data = fetch_all_data(api_key, api_url)
            
            all_df = st.session_state.all_data
            if not all_df.empty:
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    search_column = st.selectbox('Select Column to Search', all_df.columns)
                with col2:
                    unique_values = all_df[search_column].unique()
                    selected_value = st.selectbox('Select Value', unique_values)
                
                if st.button('Search All Data'):
                    filtered_df = all_df[all_df[search_column] == selected_value]
                    st.dataframe(filtered_df)
                
                st.write("Records view:")
                st.dataframe(all_df)

                if st.button('Reset All Data View'):
                    st.session_state.all_data = fetch_all_data(api_key, api_url)
                    st.success("All data view has been reset to top 20 records.")
            else:
                st.warning("No data available.")

    else:
        st.warning("Please connect to the API using the sidebar.")
