import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Finance Analyzer", layout="wide")

st.title("📊 Personal Finance Data Analyzer")
st.markdown("Upload your file to see automated insights.")

uploaded_file = st.file_uploader("Choose your file (CSV or XLSX)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # 1. Handling the Encoding Issue
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)

        # 2. Mapping your specific columns to the app logic
        # We look for your Albanian column names and map them to English for the charts
        column_mapping = {
            'Kategoria': 'Category',
            'Qarkullimi (EUR)': 'Amount'
        }

        # Rename columns if they exist in the uploaded file
        df = df.rename(columns=column_mapping)

        # Check if the needed columns are now present
        if 'Category' in df.columns and 'Amount' in df.columns:
            # Clean 'Amount' column: ensure it's numeric
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df = df.dropna(subset=['Amount'])

            # Display Metrics
            total_spent = df['Amount'].sum()
            st.metric("Total Circulation", f"€{total_spent:,.2f}")

            # Charts
            col1, col2 = st.columns(2)
            with col1:
                fig_pie = px.pie(df, values='Amount', names='Category', title="Spending by Category")
                st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                fig_bar = px.bar(df, x='Category', y='Amount', title="Transaction History", color='Category')
                st.plotly_chart(fig_bar, use_container_width=True)

            st.subheader("Raw Data Preview")
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Column mismatch! Please ensure columns are named 'Kategoria' and 'Qarkullimi (EUR)'.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
