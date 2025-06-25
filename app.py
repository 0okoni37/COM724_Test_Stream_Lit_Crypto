import streamlit as st
from processed_data import processed_crypto_data
import plotly.express as px
import pandas as pd

st.title("Cryptocurrency Data Visualization with Plotly")

# Ensure data is available
if processed_crypto_data is not None and not processed_crypto_data.empty:
    # List of cryptocurrencies
    cryptos = sorted(set(col.split('_')[0] for col in processed_crypto_data.columns))
    metrics = ['Open', 'High', 'Low', 'Close', 'Volume']

    # User selections for scatter plot
    crypto_x_scatter = st.selectbox("Select first cryptocurrency for scatter plot", cryptos)
    crypto_y_scatter = st.selectbox("Select second cryptocurrency for scatter plot", cryptos, index=1)
    metric_scatter = st.selectbox("Select metric for scatter plot", metrics)

    # Columns for scatter plot
    col_x_scatter = f"{crypto_x_scatter}_{metric_scatter}"
    col_y_scatter = f"{crypto_y_scatter}_{metric_scatter}"

    # Plot scatter plot
    if col_x_scatter in processed_crypto_data.columns and col_y_scatter in processed_crypto_data.columns:
        df_scatter = processed_crypto_data.reset_index()
        fig_scatter = px.scatter(
            df_scatter,
            x=col_x_scatter,
            y=col_y_scatter,
            hover_data=['Date'],
            labels={
                col_x_scatter: f"{crypto_x_scatter} {metric_scatter}",
                col_y_scatter: f"{crypto_y_scatter} {metric_scatter}"
            },
            title=f"{crypto_x_scatter} vs {crypto_y_scatter} ({metric_scatter})"
        )
        st.plotly_chart(fig_scatter)
    else:
        st.write("Selected data not available for scatter plot.")

    st.markdown("---")  # Separator

    # User selections for line chart
    crypto_x_line = st.selectbox("Select first cryptocurrency for line chart", cryptos, key='line_x')
    crypto_y_line = st.selectbox("Select second cryptocurrency for line chart", cryptos, index=1, key='line_y')
    metric_line = st.selectbox("Select metric for line chart", metrics, key='line_metric')

    # Columns for line chart
    col_x_line = f"{crypto_x_line}_{metric_line}"
    col_y_line = f"{crypto_y_line}_{metric_line}"

    # Plot line chart over time
    if col_x_line in processed_crypto_data.columns and col_y_line in processed_crypto_data.columns:
        df_time = processed_crypto_data.reset_index()
        df_time['Date'] = pd.to_datetime(df_time['Date'])
        fig_line = px.line(
            df_time,
            x='Date',
            y=[col_x_line, col_y_line],
            labels={'value': metric_line, 'variable': 'Cryptocurrency', 'Date': 'Date'},
            title=f"{metric_line} over Time"
        )
        st.plotly_chart(fig_line)
    else:
        st.write("Selected data not available for line chart.")

else:
    st.write("Processed data not found or empty.")
