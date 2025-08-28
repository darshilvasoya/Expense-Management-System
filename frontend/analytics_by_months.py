import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:8000"

def analytics_months_tab():

    st.markdown(
        "<p style='color: #4B5563;'>Analyze your expenses month-wise for the year.</p>",
        unsafe_allow_html=True
    )


    try:
        response = requests.get(f"{API_URL}/monthly_summary/")
        monthly_summary = response.json()
    except:
        st.error("Failed to fetch monthly summary.")
        return

    if not monthly_summary:
        st.warning("No monthly data available.")
        return


    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)


    df_sorted = df.sort_values(by="Month Number", ascending=True).reset_index(drop=True)


    st.markdown(
        "<div style='text-align: center; color: #2C3E50; font-weight: bold; font-size:20px; margin-bottom:4px;'>Monthly Expense Breakdown</div>",
        unsafe_allow_html=True
    )
    chart = alt.Chart(df_sorted).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X('Month Name:N', sort=None, title="Month"),
        y=alt.Y('Total:Q', title="Total Amount"),
        color=alt.Color('Total:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=['Month Name', 'Total']
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)


    df_sorted["Total"] = df_sorted["Total"].astype(float).map("{:.2f}".format)

    table_styles = [
        {"selector": "thead", "props": [("background-color", "#2563EB"), ("color", "white"), ("font-weight", "bold")]},
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F3F4F6")]},
        {"selector": "tbody tr:nth-child(odd)", "props": [("background-color", "white")]}
    ]

    st.markdown("<h4 style='color: #2C3E50;'>Monthly Expense Details</h4>", unsafe_allow_html=True)
    st.dataframe(
        df_sorted[["Month Name", "Total"]].style.set_table_styles(table_styles),
        hide_index=True
    )
