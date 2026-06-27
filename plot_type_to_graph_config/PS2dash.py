import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load your data
df = pd.read_csv('ft_prod_specific_piecewise.csv')

# Convert timestamps to datetime if needed
df['start_timestamp'] = pd.to_datetime(df['start_timestamp'])
df['end_timestamp'] = pd.to_datetime(df['end_timestamp'])
df['local_time'] = pd.to_datetime(df['local_time'])

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Interactive Machine Data Visualization"),
    
    # Dropdowns for dynamic axis selection
    html.Div([
        html.Label("Select X-axis:"),
        dcc.Dropdown(
            id='x-axis',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='local_time'
        ),

        html.Label("Select Y-axis:"),
        dcc.Dropdown(
            id='y-axis',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='actual_cycletime'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    # Machine ID filter
    html.Div([
        html.Label("Filter by Machine ID:"),
        dcc.Dropdown(
            id='machine-filter',
            options=[{'label': str(m), 'value': str(m)} for m in df['machineid'].unique()],
            multi=True
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    # Graph output
    dcc.Graph(id='interactive-plot')
])

# Callback to update the plot
@app.callback(
    Output('interactive-plot', 'figure'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('machine-filter', 'value')]
)
def update_plot(x_axis, y_axis, machine_filter):
    filtered_df = df.copy()
    if machine_filter:
        filtered_df = filtered_df[filtered_df['machineid'].isin(machine_filter)]
    
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color='machineid', title=f'{y_axis} vs {x_axis}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

