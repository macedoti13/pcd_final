import plotly.graph_objects as go

def create_questions_4_and_7_plot_1(input_df):
    df = input_df.copy()
    real_data = df[df.forecasted==False]
    forecasted_data = df[df.forecasted==True]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=real_data.timestamp, y=real_data.forecasted_output_flow_rate, mode='lines+markers', name='Ultimas 24 horas', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=forecasted_data.timestamp, y=forecasted_data.forecasted_output_flow_rate, mode='lines+markers', name='Previsao Proximas 24 horas sem dados meterologicos', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=forecasted_data.timestamp, y=forecasted_data.weather_forecasted_output_flow_rate, mode='lines+markers', name='Previsao Proximas 24 horas com dados meterologicos', line=dict(color='green')))
    plot_html = fig.to_html(full_html=False)
    return plot_html