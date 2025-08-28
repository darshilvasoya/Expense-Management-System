import streamlit as st
from add_update import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_months import analytics_months_tab


st.markdown("""
    <h1 style="
        text-align: center;
        background: linear-gradient(to right, #1E40AF, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    ">
        Expense Tracking System
    </h1>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    /* Center tabs container */
    div[data-baseweb="tab-list"] {
        justify-content: center !important;
    }

    /* Tab labels styling */
    div[data-baseweb="tab"] button {
        font-weight: bold;
        font-size: 16px;
        color: #2563EB;
        border-radius: 6px 6px 0 0;
    }
    div[data-baseweb="tab"] button:hover {
        color: #3B82F6;
    }
    div[data-baseweb="tab"] button[data-selected] {
        background-color: #2563EB !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Months"])

with tab1:
    add_update_tab()

with tab2:
    analytics_category_tab()

with tab3:
    analytics_months_tab()
