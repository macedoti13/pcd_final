import plotly.graph_objects as go

def create_question_5_plot(input_df):
    df = input_df.copy()
    real_data = df[df.simulation==False].tail(10)
    simulation_data = df[df.simulation==True]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=real_data.timestamp, y=real_data.reservoir_level_percentage, mode='lines+markers', name='Nivel do Reservatorio Real', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=simulation_data.timestamp, y=simulation_data.reservoir_level_percentage, mode='lines+markers', name='Nivel do Reservatorio Simulado', line=dict(color='red')))
    fig.update_layout(title={'text': 'Simulacao de Esvaziamento do Reservatorio em Queda de Energia', 'x': 0.5, 'xanchor': 'center'},xaxis_title='Horarion', yaxis_title='Porcentagem do Reservatorio',legend_title='Type')
    plot_html = fig.to_html(full_html=False)
    return plot_html
