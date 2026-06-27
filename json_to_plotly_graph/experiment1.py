import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly 
#import chart_studio 
#import plotly.express as px 



# ------------------------------
# 1️⃣ Load the data
# ------------------------------
file_path = "ft_prod_specific_piecewise.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Convert timestamp columns to datetime
df['start_timestamp'] = pd.to_datetime(df['start_timestamp'], unit='ms')
df['end_timestamp'] = pd.to_datetime(df['end_timestamp'], unit='ms')

# Convert local_time to datetime
df['local_time'] = pd.to_datetime(df['local_time'], format='%H:%M:%S').dt.time

# Extracting Date and Time separately for easier analysis
df['date'] = df['start_timestamp'].dt.date
df['start_time'] = df['start_timestamp'].dt.time
df['end_time'] = df['end_timestamp'].dt.time

# ------------------------------
# 2️⃣ Dynamic Plotting Function
# ------------------------------
def dynamic_plot(df, x, y=None, color=None, plot_type='scatter'):
    """
    Function to create dynamic visualizations with Plotly.
    
    Parameters:
    - df: DataFrame
    - x: X-axis feature
    - y: Y-axis feature (None for histograms)
    - color: Column to color by (optional)
    - plot_type: Type of plot ('scatter', 'line', 'bar', 'histogram', 'box')
    """
    
    if plot_type == 'scatter':
        fig = px.scatter(df, x=x, y=y, color=color, 
                         title=f'Scatter Plot: {x} vs {y}', 
                         hover_data=[x, y, color] if color else [x, y])
    
    elif plot_type == 'line':
        fig = px.line(df, x=x, y=y, color=color, 
                      title=f'Line Plot: {x} vs {y}', 
                      markers=True)
    
    elif plot_type == 'bar':
        fig = px.bar(df, x=x, y=y, color=color, 
                     title=f'Bar Plot: {x} vs {y}')
    
    elif plot_type == 'histogram':
        fig = px.histogram(df, x=x, color=color, 
                           title=f'Histogram: {x}', nbins=30)
    
    elif plot_type == 'box':
        fig = px.box(df, x=x, y=y, color=color, 
                     title=f'Box Plot: {x} vs {y}')
    
    else:
        print("Invalid plot type. Choose from: 'scatter', 'line', 'bar', 'histogram', 'box'")
        return

    fig.show()

# ------------------------------
# 3️⃣ Example Usage
# ------------------------------


# Box plot: Cycle time distribution per machine
dynamic_plot(df, x='machineid', y='actual_cycletime', color='machineid', plot_type='box')
