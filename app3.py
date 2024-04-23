import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# Function to convert ppm to percentage
def ppm_to_percent(CH4, C2H4, C2H2):
    total = CH4 + C2H4 + C2H2
    if total == 0:
        return 0, 0, 0
    return 100 * CH4 / total, 100 * C2H4 / total, 100 * C2H2 / total

# Define zone checking functions
def check_PD_zone(CH4, C2H4, C2H2):
    return CH4 >= 98 and C2H4 <= 2 and C2H2 <= 2

def check_D1_zone(CH4, C2H4, C2H2):
    return C2H2 >= 13 and C2H4 <= 23

def check_D2_zone(CH4, C2H4, C2H2):
    return (C2H4 >= 23 and C2H2 >= 29) or (C2H4 >= 23 and C2H4 <= 40 and C2H2 >= 13 and C2H2 <= 29)

def check_DT_zone(CH4, C2H4, C2H2):
    return (C2H2 >= 15 and C2H2 <= 29 and C2H4 >= 40) or (C2H2 >= 13 and C2H2 <= 15 and C2H4 >= 40 and C2H4 <= 50) or (C2H4 <= 50 and C2H2 >= 4 and C2H2 <= 13)

def check_T1_zone(CH4, C2H4, C2H2):
    return CH4 >= 76 and CH4 <= 98 and C2H2 <= 4 and C2H4 <= 20

def check_T2_zone(CH4, C2H4, C2H2):
    return CH4 >= 46 and CH4 <= 80 and C2H4 >= 20 and C2H4 <= 50 and C2H2 <= 4

def check_T3_zone(CH4, C2H4, C2H2):
    return CH4 <= 50 and C2H2 <= 15 and C2H4 >= 50 

@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

def main():
    st.title('Duval Triangle for DGA Interpretation')
    
    # Mapping of user-friendly names to file paths
    file_options = {
        "BOSA_T401": r"C:\Users\peter\Documents\Python\Python-ideas\timeseries_transformers\matej\Xfmr-Fault-Type-Prediction-main\gas_data.xlsx",
        "BOSA_T402": r"C:\Users\peter\Documents\Python\Python-ideas\timeseries_transformers\matej\Xfmr-Fault-Type-Prediction-main\gas_data2.xlsx",
        "Additional Gas Data": 'gas_data2.xlsx'
    }
    
    # Dropdown to select the data file
    selected_option = st.selectbox(
        "Select transformer:",
        options=list(file_options.keys())  # Display user-friendly names
    )

    # Load selected data using the file path corresponding to the chosen option
    gas_data = load_data(file_options[selected_option])
    
    # Convert ppm to percentage and apply zone checks
    gas_data[['CH4%', 'C2H4%', 'C2H2%']] = gas_data.apply(
        lambda row: ppm_to_percent(row['CH4_ppm'], row['C2H4_ppm'], row['C2H2_ppm']), axis=1, result_type="expand")
    
    gas_data['Zone'] = gas_data.apply(lambda row: (
        ("PD " if check_PD_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "") +
        ("D1 " if check_D1_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "") +
        ("D2 " if check_D2_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "") +
        ("DT " if check_DT_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "") +
        ("T1 " if check_T1_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "") +
        ("T2 " if check_T2_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "") +
        ("T3 " if check_T3_zone(row['CH4%'], row['C2H4%'], row['C2H2%']) else "")
    ).strip(), axis=1)

    # Prepare the figure
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "ternary"}], [{"type": "table"}]],
        vertical_spacing=0.1
    )
        # Add scatter and line traces for the ternary plot
    traces = [
        go.Scatterternary({
            'a': [98, 1, 98], 'b': [0, 0, 2], 'c': [2, 0, 0], 
            'mode': 'lines', 'fill': 'toself', 'name': 'PD'
        }),
        go.Scatterternary({
            'a': [0, 0, 64, 87], 'b': [1, 77, 13, 13], 'c': [0, 23, 23, 0], 
            'mode': 'lines', 'fill': 'toself', 'name': 'D1'
        }),
                go.Scatterternary({
            'a': [0, 0, 31, 47, 64], 'b': [77, 29, 29, 13, 13], 'c': [23, 71, 40, 40, 23],
            'mode': 'lines', 'fill': 'toself', 'name': 'D2'
        }),
                go.Scatterternary({
            'a': [0, 0, 35, 46, 96, 87, 47, 31], 'b': [29, 15, 15, 4, 4, 13, 13, 29], 'c': [71, 85, 50, 50, 0, 0, 40, 40],
            'mode': 'lines', 'fill': 'toself', 'name': 'DT'
        }),
                go.Scatterternary({
            'a': [76, 80, 98, 98, 96], 'b': [4, 0, 0, 2, 4], 'c': [20, 20, 2, 0, 0],
            'mode': 'lines', 'fill': 'toself', 'name': 'T1'
        }),
                go.Scatterternary({
            'a': [46, 50, 80, 76], 'b': [4, 0, 0, 4], 'c': [50, 50, 20, 20],
            'mode': 'lines', 'fill': 'toself', 'name': 'T2'
        }),
                go.Scatterternary({
            'a': [0, 0, 50, 35], 'b': [15, 0, 0, 15], 'c': [85, 1, 50, 50],
            'mode': 'lines', 'fill': 'toself', 'name': 'T3'
        }),
        # Add other traces as needed
    ]
    # Add zone traces to the plot
    for trace in traces:
        fig.add_trace(trace, row=1, col=1)
    # Example traces (predefined zones)
    # Include your Scatterternary traces here

    # Add scatter traces for individual data points dynamically
    for index, row in gas_data.iterrows():
        color = 'blue'  # Default color, can use different colors based on zone
        fig.add_trace(go.Scatterternary({
            'a': [row['CH4%']], 'b': [row['C2H2%']], 'c': [row['C2H4%']],
            'mode': 'markers', 'marker': {'symbol': 'circle', 'size': 10,'color': row['Color']},
            'name': f"{row['Zone']} - {row['Fault location']}"
        }), row=1, col=1)

    # Table trace for the second row
    fig.add_trace(
        go.Table(
            header=dict(
                values=['Fault Location', 'CH4%', 'C2H4%', 'C2H2%', 'Zone'],
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[
                    gas_data['Fault location'],
                    gas_data['CH4%'].round(2),
                    gas_data['C2H4%'].round(2),
                    gas_data['C2H2%'].round(2),
                    gas_data['Zone']
                ],
                fill_color='lavender',
                align='left'
            )
        ), 
        row=2, col=1
    )

    # Update layout for better presentation
    fig.update_layout(
        title='Duval Triangle Analysis',
        height=1000,
        ternary={
            'sum': 100,
            'aaxis': {'title': 'CH4%','linewidth': 2, 'ticks': 'outside'},
            'baxis': {'title': 'C2H2%','linewidth': 2, 'ticks': 'outside'},
            'caxis': {'title': 'C2H4%','linewidth': 2, 'ticks': 'outside'}
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()