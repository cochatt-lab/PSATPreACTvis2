
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import scipy.stats

st.title("PSAT/PreACT Score and Benchmark Dashboard")

# Load data
df = pd.read_csv("filtered_psat_preact_2028_2029.csv")

# Sidebar filters
benchmark_options = df["Benchmark"].unique().tolist()
selected_benchmarks = st.sidebar.multiselect("Select Benchmark Status:", benchmark_options, default=benchmark_options)

# Filter data
filtered_df = df[df["Benchmark"].isin(selected_benchmarks)]

# Scatter plots
st.subheader("Scatter Plots")
fig1 = px.scatter(filtered_df, x="ReadingWriting", y="Total", color="Benchmark",
                  title="Reading/Writing vs Total Score by Benchmark")
st.plotly_chart(fig1)

fig2 = px.scatter(filtered_df, x="Math", y="Total", color="Benchmark",
                  title="Math vs Total Score by Benchmark")
st.plotly_chart(fig2)

# Density plots
st.subheader("Density Plots")
density_rw = ff.create_distplot(
    [filtered_df[filtered_df["Benchmark"] == b]["ReadingWriting"] for b in selected_benchmarks],
    group_labels=selected_benchmarks,
    show_hist=False,
    show_rug=False
)
density_rw.update_layout(title="Density Plot of Reading/Writing Scores by Benchmark")
st.plotly_chart(density_rw)

density_math = ff.create_distplot(
    [filtered_df[filtered_df["Benchmark"] == b]["Math"] for b in selected_benchmarks],
    group_labels=selected_benchmarks,
    show_hist=False,
    show_rug=False
)
density_math.update_layout(title="Density Plot of Math Scores by Benchmark")
st.plotly_chart(density_math)

# Heatmap
st.subheader("Heatmap")
heatmap_data = filtered_df.pivot_table(index="Class", columns="Benchmark", values="Total", aggfunc="mean")
heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='Viridis'
))
heatmap.update_layout(title="Heatmap of Average Total Score by Class Year and Benchmark Status",
                      xaxis_title="Benchmark Status", yaxis_title="Class Year")
st.plotly_chart(heatmap)

# Data table
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)
