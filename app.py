import streamlit as st
import plotly.graph_objects as go

# 1. Setup & Title
st.set_page_config(
    page_title="IndiaAQI-360",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💨 IndiaAQI-360 Dashboard")
st.markdown("---")

# 2. User Inputs
st.sidebar.header("Configuration")
selected_city = st.sidebar.selectbox('Select City', ['Delhi', 'Mumbai', 'Bangalore', 'Chennai'])

# 3. Mock Data
# In a real application, these would be fetched dynamically based on the selected_city.
AQI = 156
aqi_history = [120, 145, 160, 135, 170, 156, 148]
days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

# 4. Health Advisory Logic & HTML Styling
if AQI < 50:
    status = "Good"
    bg_color = "#e8f5e9"  # Light green background
    text_color = "#2e7d32"  # Dark green text
    border_color = "#81c784"
    advice = "Air quality is satisfactory, and air pollution poses little or no risk."
elif AQI < 100:
    status = "Moderate"
    bg_color = "#fffde7"  # Light yellow background
    text_color = "#f57f17"  # Dark yellow/orange text
    border_color = "#fff59d"
    advice = "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
elif AQI < 150:
    status = "Unhealthy for Sensitive Groups"
    bg_color = "#fff3e0"  # Light orange background
    text_color = "#e65100"  # Dark orange text
    border_color = "#ffb74d"
    advice = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
else:
    status = "Unhealthy"
    bg_color = "#ffebee"  # Light red background
    text_color = "#c62828"  # Dark red text
    border_color = "#e57373"
    advice = "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."

# Display dynamic layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader(f"Current Status for {selected_city}")
    
    # Render dynamic HTML Health Advisory Card
    card_html = f"""
    <div style="
        background-color: {bg_color};
        color: {text_color};
        border: 2px solid {border_color};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">
        <h3 style="margin-top: 0; color: {text_color}; font-weight: 700;">Status: {status}</h3>
        <p style="font-size: 1.15rem; font-weight: 600; margin: 5px 0;">Current AQI: <span style="font-size: 1.5rem; font-weight: 800;">{AQI}</span></p>
        <hr style="border-color: {border_color}; opacity: 0.5; margin: 10px 0;">
        <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 0;"><strong>Health Advisory:</strong> {advice}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    # 4. Data Visualizations: Plotly Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=AQI,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Air Quality Index (AQI)", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [0, 300], 'tickwidth': 1, 'tickcolor': "#888888"},
            'bar': {'color': text_color},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#dddddd",
            'steps': [
                {'range': [0, 50], 'color': '#e8f5e9'},
                {'range': [50, 100], 'color': '#fffde7'},
                {'range': [100, 150], 'color': '#fff3e0'},
                {'range': [150, 300], 'color': '#ffebee'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': AQI
            }
        }
    ))
    
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=280
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    st.subheader("7-Day AQI Trend")
    
    # 4. Data Visualizations: Plotly Line Chart
    fig_line = go.Figure()
    
    fig_line.add_trace(go.Scatter(
        x=days,
        y=aqi_history,
        mode='lines+markers',
        name='AQI',
        line=dict(color='#2196f3', width=3),
        marker=dict(size=8, color='#0d47a1', symbol='circle'),
        hovertemplate='<b>%{x}</b><br>AQI: %{y}<extra></extra>'
    ))
    
    # Add target safety line
    fig_line.add_hline(
        y=100, 
        line_dash="dash", 
        line_color="#e65100", 
        annotation_text="Moderate AQI Limit (100)", 
        annotation_position="top left"
    )
    
    fig_line.update_layout(
        xaxis_title="Timeline",
        yaxis_title="AQI Value",
        yaxis=dict(range=[50, 200]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        hovermode="x unified"
    )
    
    fig_line.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    
    st.plotly_chart(fig_line, use_container_width=True)
