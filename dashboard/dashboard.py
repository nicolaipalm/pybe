import streamlit as st
import pandas as pd
import plotly.express as px
from pybe.benchmark import Benchmark

######
# Meta
######
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.header('Benchmark Results')

########
# Header
########

#######################
# Sidebar configuration
#######################
st.sidebar.header('PyBe Benchmark visualization `v1.0.0`')

###############
# Create upload
###############
uploaded_files = st.sidebar.file_uploader('', accept_multiple_files=True)

# TODO error handling if not yaml

if uploaded_files:
    benchmarks = []
    for uploaded_file in uploaded_files:
        benchmarks.append(Benchmark(uploaded_file))
else:
    benchmarks = [Benchmark('../examples/benchmark.csv')]
benchmark = pd.concat([benchmark_i.result for benchmark_i in benchmarks])

# Append Inputs
with st.sidebar.expander('Inputs'):
    text = ''
    for input in benchmarks[0].inputs:
        text += f'- {input} \n'
    st.markdown(text)

# Append name of outputs
with st.sidebar.expander('Outputs'):
    text = ''
    for name_output in benchmarks[0].name_outputs:
        text += f'- {name_output} \n'
    st.markdown(text)

#
st.sidebar.markdown('contact, My links linkedin etc')

#########
# Graphs
#########


# Bar chart of benchmarked means

means = pd.concat([benchmark_i.means for benchmark_i in benchmarks])

# bar charts
bar_charts_means = [px.bar(means,
                           x='Input',
                           y=name_output,
                           color='Name',
                           barmode='group') for name_output in benchmarks[0].name_outputs]

columns_bar_charts_mean = st.columns(len(bar_charts_means))
for i, bar_chart in enumerate(bar_charts_means):
    with columns_bar_charts_mean[i]:
        st.plotly_chart(bar_chart, use_container_width=True)


# Box plots for benchmark results
name_output_box_chart = st.selectbox(
    'Which output do you want to visualize?',
    benchmarks[0].name_outputs)
st.plotly_chart(px.box(benchmark,
                       x='Input',
                       y=name_output_box_chart,
                       color='Name', ),
                use_container_width=True)


# plot all
x_container, y_container, color_container = st.columns(3)
options = ['Input'] + ['Name'] + benchmarks[0].name_outputs
with x_container:
    x = st.radio(
        'x-Label',
        options,
        index=0
    )

with y_container:
    y = st.radio(
        'y-Label',
        options,
        index=2
    )

with color_container:
    color = st.radio(
        'color-Label',
        options,
        index=1
    )

st.plotly_chart(px.scatter(benchmark,
                           x=x,
                           y=y,
                           color=color, ),
                use_container_width=True)


# Table of results
with st.expander('Table of results'):
    # Show data frame
    st.dataframe(benchmark)
