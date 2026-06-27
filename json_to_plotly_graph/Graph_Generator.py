import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

def json_to_dataframe_with_plot(json_result, x_col=None, y_col=None, hue=None, figsize=(12, 6)):
    """
    Parses JSON into DataFrame, applies dynamic type conversion, and creates a plot.
    
    Parameters:
    - json_result: JSON-formatted string (list of dictionaries)
    - x_col: Column for x-axis (optional)
    - y_col: Column for y-axis (optional)
    - hue: Column for color grouping (optional)
    - figsize: Size of the plot
    
    Returns:
    - DataFrame with converted types and displays the plot
    """
    
    # ✅ Parse JSON into DataFrame
    try:
        data = json.loads(json_result)
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing JSON: {e}")
        return pd.DataFrame()

    # ✅ Handle NaN values
    df.replace("NaN", np.nan, inplace=True)

    # ✅ Convert timestamps to datetime
    timestamp_cols = ['start_timestamp', 'end_timestamp']
    for col in timestamp_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col].astype(float) / 1000, unit='s')

    # ✅ Convert date and local_time columns to datetime
    datetime_cols = ['date', 'local_time']
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # ✅ Convert numerical columns
    int_cols = ['tenantid', 'piece_number', 'pieces_produced_life', 'shiftid']
    float_cols = ['actual_cycletime', 'time_between_jobs', 'average_cycletime', 'cutting_time']

    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')

    # ✅ Convert ID and UUID columns to category
    cat_cols = ['v2tenant', 'org_id', 'unit_id', 'department_id', 'machineid', 'edgeid', 'part_id']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # ✅ Automatically detect X and Y columns if not specified
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    category_cols = df.select_dtypes(include=['category', 'object']).columns.tolist()

    if x_col is None:
        x_col = datetime_cols[0] if datetime_cols else (category_cols[0] if category_cols else (numeric_cols[0] if numeric_cols else None))

    if y_col is None:
        y_col = next((col for col in numeric_cols if col != x_col), None)

    if x_col is None or y_col is None:
        print("Error: Unable to find suitable columns for plotting.")
        return df

    # ✅ Determine plot type
    if x_col in datetime_cols:
        plot_type = 'line'
    elif x_col in category_cols and y_col in numeric_cols:
        plot_type = 'bar'
    elif x_col in numeric_cols and y_col in numeric_cols:
        plot_type = 'scatter'
    elif y_col in numeric_cols:
        plot_type = 'hist'
    else:
        plot_type = 'box'

    # ✅ Plotting
    plt.figure(figsize=figsize)

    if plot_type == 'line':
        sns.lineplot(data=df, x=x_col, y=y_col, hue=hue)
    elif plot_type == 'scatter':
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue)
    elif plot_type == 'bar':
        sns.barplot(data=df, x=x_col, y=y_col, hue=hue)
    elif plot_type == 'hist':
        sns.histplot(data=df[y_col], kde=True)
    elif plot_type == 'box':
        sns.boxplot(data=df, x=x_col, y=y_col, hue=hue)

    plt.title(f"{plot_type.capitalize()} Plot: {x_col} vs {y_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    plt.show()

    
