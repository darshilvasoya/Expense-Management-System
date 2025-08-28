import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:8000"

def analytics_category_tab():

    st.markdown(
        "<p style='color: #4B5563;'>Analyze your expenses by category within a selected date range.</p>",
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))


    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #2563EB;
            color: white;
            border-radius: 6px;
            height: 40px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1D4ED8;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }


        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload).json()
        except:
            st.error("Failed to fetch analytics data.")
            return

        if not response:
            st.warning("No data available for the selected date range.")
            return


        df = pd.DataFrame({
            "Category": list(response.keys()),
            "Total": [response[c]["total"] for c in response],
            "Percentage": [response[c]["percentage"] for c in response]
        })
        df_sorted = df.sort_values(by="Percentage", ascending=False)


        st.markdown(
            "<div style='text-align: center; color: #2C3E50; font-weight: bold; font-size:20px; margin-bottom:4px;'>Visual Expense Breakdown</div>",
            unsafe_allow_html=True
        )
        chart = alt.Chart(df_sorted).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Total:Q', title="Total Amount"),  # <-- changed from Percentage to Total
            y=alt.Y('Category:N', sort='-x', title=None),
            color=alt.Color('Total:Q', scale=alt.Scale(scheme='blues'), legend=None),  # color by total now
            tooltip=['Category', 'Total', 'Percentage']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)


        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        table_styles = [
            {"selector": "thead", "props": [("background-color", "#2563EB"), ("color", "white"), ("font-weight", "bold")]},
            {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#F3F4F6")]},
            {"selector": "tbody tr:nth-child(odd)", "props": [("background-color", "white")]}
        ]

        st.markdown("<h4 style='color: #2C3E50;'>Expense Details</h4>", unsafe_allow_html=True)
        st.dataframe(df_sorted.style.set_table_styles(table_styles))
