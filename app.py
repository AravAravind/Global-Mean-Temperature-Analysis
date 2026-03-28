import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Global Temperature Dashboard", layout="wide")

st.title("🌍 Global Mean Temperature Dashboard (1950–2024)")

df = pd.read_csv("archive/temperature-medie-annuali-1950-2024.csv")

baseline = df[(df["year"] >= 1950) & (df["year"] <= 1980)]
baseline_avg = baseline.groupby("country")["mean_temperature"].mean()
df["baseline_temp"] = df["country"].map(baseline_avg)
df["temp_change"] = df["mean_temperature"] - df["baseline_temp"]

st.sidebar.header("Filters")

years = sorted(df["year"].unique())
selected_year = st.sidebar.slider("Select Year", min(years), max(years), max(years))

countries = sorted(df["country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=["India", "United States of America", "China"]
)

metric = st.sidebar.radio("Select Metric", ["Mean Temperature", "Temperature Change"])

filtered_df = df[df["year"] == selected_year]
country_df = df[df["country"].isin(selected_countries)]

value_column = "mean_temperature" if metric == "Mean Temperature" else "temp_change"

st.metric("Global Avg", round(filtered_df[value_column].mean(), 2))

fig_map = px.choropleth(
    filtered_df,
    locations="iso_code",
    color=value_column,
    hover_name="country",
    color_continuous_scale="RdYlBu_r"
)

st.plotly_chart(fig_map, use_container_width=True)

fig_line = px.line(
    country_df,
    x="year",
    y=value_column,
    color="country"
)

st.plotly_chart(fig_line, use_container_width=True)

top10 = filtered_df.sort_values(by=value_column, ascending=False).head(10)

fig_bar = px.bar(
    top10,
    x=value_column,
    y="country",
    orientation="h"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.dataframe(filtered_df)