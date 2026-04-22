import streamlit as st
import pandas as pd
import time
import os
from sqlalchemy import create_engine
from datetime import datetime

# Пытаемся импортировать Plotly
try:
    import plotly.graph_objects as go
except ImportError:
    os.system('pip install plotly')
    import plotly.graph_objects as go

# --- 1. КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(
    page_title="Потоковая сегментация надводных объектов",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Параметры подключения
DB_URI = "postgresql://ruslan:marine_pass@marine_db:5432/marine_pipeline"
engine = create_engine(DB_URI)
STREAM_URL = "http://localhost:5000/video_feed"

# Инициализация сессии (строго 25 точек)
if 'history_counts' not in st.session_state:
    st.session_state.history_counts = []
if 'last_total' not in st.session_state:
    st.session_state.last_total = 0

# --- 2. СТИЛИЗАЦИЯ (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .video-container {
        display: flex; justify-content: center; align-items: center;
        background-color: #000; border: 2px solid #00ff00;
        border-radius: 12px; box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        overflow: hidden; margin: 0 auto 10px auto; max-width: 480px; 
    }
    .status-badge {
        padding: 4px 12px; border-radius: 15px;
        background-color: #00ff00; color: black;
        font-weight: bold; font-size: 0.75rem;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; font-size: 1.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- 3. БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.title("Marine Segmentation")
    st.markdown('<span class="status-badge">VIDEO STREAM</span>', unsafe_allow_html=True)
    st.divider()
    
    st.subheader("Заполнение базы данных")
    chart_placeholder = st.empty()
    
    st.divider()
    st.caption("Окно: последние 25 записей.")

# --- 4. ОСНОВНОЙ КОНТЕНТ ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.header("Визуализация сегментации")
    st.markdown(f'<div class="video-container"><img src="{STREAM_URL}" style="width: 100%;"></div>', unsafe_allow_html=True)

with col_right:
    st.header("Аналитика базы данных")
    metric_placeholder = st.empty()
    table_placeholder = st.empty()

chart_iteration = 0

# --- 5. ЦИКЛ ОБНОВЛЕНИЯ ДАННЫХ ---
while True:
    try:
        # 1. Запрос общего количества
        count_df = pd.read_sql("SELECT count(*) as total FROM marine_analytics", engine)
        total_records = int(count_df.iloc[0, 0])
        
        # 2. Логика СКОЛЬЗЯЩЕГО ОКНА (строго 25 точек)
        if total_records != st.session_state.last_total or not st.session_state.history_counts:
            current_time = datetime.now().strftime("%H:%M:%S")
            st.session_state.history_counts.append({"Время": current_time, "Записей": total_records})
            st.session_state.last_total = total_records
            
            if len(st.session_state.history_counts) > 25:
                st.session_state.history_counts.pop(0)
            
        # 3. Запрос данных для таблицы
        df_table = pd.read_sql("SELECT event_id, filename, mask_file, processed_at FROM marine_analytics ORDER BY processed_at DESC LIMIT 15", engine)
        
        # --- ОТРИСОВКА ---
        metric_placeholder.metric(label="Всего записей в базе", value=total_records)
        
        if len(st.session_state.history_counts) > 1:
            df_history = pd.DataFrame(st.session_state.history_counts)
            
            # Определяем границы Y для зума
            y_min = df_history["Записей"].min()
            y_max = df_history["Записей"].max()
            
            fig = go.Figure()
            # Возвращаем маркеры (mode='lines+markers')
            fig.add_trace(go.Scatter(
                x=df_history["Время"], 
                y=df_history["Записей"], 
                mode='lines+markers', 
                line=dict(color='#00ff00', width=2),
                marker=dict(
                    size=6, 
                    color='#00ff00', 
                    symbol='circle',
                    line=dict(color='#0e1117', width=1) # Контур точек для четкости
                ),
                fill='none'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='#333',
                    side='right',
                    range=[y_min - 0.5, y_max + 0.5], # Плотно прижимаем шкалу к точкам
                    autorange=False 
                ),
                height=180,
                showlegend=False
            )
            
            chart_iteration += 1
            chart_placeholder.plotly_chart(
                fig, 
                use_container_width=True, 
                key=f"final_iter_{chart_iteration}_{time.time()}" 
            )
        
        if not df_table.empty:
            table_placeholder.dataframe(
                df_table[['event_id', 'filename', 'mask_file', 'processed_at']], 
                hide_index=True, 
                width="stretch"
            )
            
    except Exception as e:
        if "multiple elements" not in str(e).lower():
            st.sidebar.error(f"Sync Error: {e}")
    
    time.sleep(1)