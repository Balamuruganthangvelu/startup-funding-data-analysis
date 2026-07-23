import streamlit as st
import pandas as pd
import plotly.express as px
from chatbot import ai_chatbot
from db_connect import get_connection


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Startup Funding Dashboard",
    layout="wide"
)

st.title("🚀 Startup Funding Analysis Dashboard")


# ---------------- DATABASE ----------------

conn = get_connection()
df = pd.read_sql(
    "SELECT * FROM public.startup_funding_data;",
    conn
)

conn.close()


# Remove duplicate column names
df = df.loc[:, ~df.columns.duplicated()]


# ---------------- DATA PREVIEW ----------------

with st.expander("📋 View Dataset"):
    st.dataframe(df)


st.sidebar.header("🔎 Filters")


# Keep original data
filtered_df = df.copy()


# ---------------- USER FILTER ----------------

filter_column = st.sidebar.selectbox(
    "Select Filter Column",
    df.columns
)


filter_values = st.sidebar.multiselect(
    f"Select {filter_column}",
    df[filter_column].dropna().unique()
)


if filter_values:
    filtered_df = filtered_df[
        filtered_df[filter_column].isin(filter_values)
    ]


# ---------------- KPI ----------------


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Records",
        len(filtered_df)
    )


with col2:
    if "Startup" in filtered_df.columns:
        st.metric(
            "Total Startups",
            filtered_df["Startup"].nunique()
        )


with col3:
    if "Amount" in filtered_df.columns:
        st.metric(
            "Total Funding",
            f"₹ {filtered_df['Amount'].sum():,.0f}"
        )


with col4:
    if "Amount" in filtered_df.columns:
        st.metric(
            "Average Funding",
            f"₹ {filtered_df['Amount'].mean():,.0f}"
        )


# ---------------- INDUSTRY ANALYSIS ----------------


if "Industry" in filtered_df.columns and "Amount" in filtered_df.columns:

    st.subheader("💰 Funding by Industry")


    industry_data = (
        filtered_df
        .groupby("Industry", as_index=False)
        .agg(
            Total_Funding=("Amount", "sum")
        )
        .sort_values(
            "Total_Funding",
            ascending=False
        )
        .head(10)
    )


    fig = px.bar(
    industry_data,
    x="Industry",
    y="Total_Funding",
    title="Top Industries",
    color="Industry"
   )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ---------------- CITY ANALYSIS ----------------


if "City" in filtered_df.columns and "Amount" in filtered_df.columns:

    st.subheader("🏙️ Funding by City")


    city_data = (
        filtered_df
        .groupby("City", as_index=False)
        .agg(
            Total_Funding=("Amount", "sum")
        )
        .sort_values(
            "Total_Funding",
            ascending=False
        )
        .head(10)
    )


    fig = px.bar(
    city_data,
    x="City",
    y="Total_Funding",
    title="Top Cities",
    color="City"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ---------------- STARTUP ANALYSIS ----------------


if "Startup" in filtered_df.columns and "Amount" in filtered_df.columns:


    st.subheader("🏆 Top Funded Startups")


    startup_data = (
        filtered_df
        .groupby("Startup", as_index=False)
        .agg(
            Total_Funding=("Amount", "sum")
        )
        .sort_values(
            "Total_Funding",
            ascending=False
        )
        .head(10)
    )


    fig = px.pie(
    startup_data,
    names="Startup",
    values="Total_Funding",
    color="Startup",
    title="Top Funded Startups"
)


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------- USER CUSTOM ANALYSIS ----------------

# ---------------- USER CUSTOM ANALYSIS ----------------

st.header("📊 Custom Analysis")


categorical_columns = filtered_df.select_dtypes(
    include=["object"]
).columns.tolist()


numeric_columns = filtered_df.select_dtypes(
    include=["int64","float64"]
).columns.tolist()



if len(categorical_columns) > 0 and len(numeric_columns) > 0:


    x_axis = st.selectbox(
        "Select Category",
        categorical_columns
    )


    y_axis = st.selectbox(
        "Select Value",
        numeric_columns
    )


    chart_type = st.selectbox(
        "Chart Type",
        [
            "Bar",
            "Line",
            "Pie"
        ]
    )


    chart_df = (
        filtered_df
        .groupby(x_axis)[y_axis]
        .sum()
        .reset_index()
        .sort_values(
            y_axis,
            ascending=False
        )
        .head(15)
    )


    if chart_type == "Bar":

        fig = px.bar(
            chart_df,
            x=x_axis,
            y=y_axis,
            color=x_axis,
            text=y_axis,
            title=f"{y_axis} by {x_axis}"
        )


    elif chart_type == "Line":

        fig = px.line(
            chart_df,
            x=x_axis,
            y=y_axis,
            markers=True,
            title=f"{y_axis} Trend"
        )


    else:

        fig = px.pie(
            chart_df,
            names=x_axis,
            values=y_axis,
            title=f"{y_axis} Distribution"
        )


    fig.update_layout(
        height=600,
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.error(
        "No categorical or numeric columns found"
    )
# ---------------- DOWNLOAD ----------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇️ Download Filtered Data",
    csv,
    "startup_funding_analysis.csv",
    "text/csv"
)

# ---------------- AI CHATBOT ----------------

st.subheader("🤖 AI Startup Funding Assistant")

question = st.text_input(
    "Ask your question"
)

if question:

    answer = ai_chatbot(
        filtered_df,
        question
    )

    st.write(answer)