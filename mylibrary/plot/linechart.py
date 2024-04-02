import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio


def plot_line_chart(df, text='', filename=None):
    # Create traces for each sensor
    traces = []
    for sensor_type in df.columns[1:]:  # Skip the first column (DateTime)
        trace = go.Scatter(x=df['DateTime'], y=df[sensor_type], mode='lines', name=sensor_type)
        traces.append(trace)

    # Create layout for the plot
    layout = go.Layout(title='Sensor Value Over Time ' + text, xaxis=dict(title='DateTime'), yaxis=dict(title='Value'))

    # Create and plot the line chart
    fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(template="plotly_white")
    fig.show()
    
    if filename:  
        pio.write_image(fig, filename)
    
