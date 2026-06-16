import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="KOSPI AI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── 데이터 로드 ──────────────────────────────
@st.cache_data
def load_data():
    # ⚠️ 경로를 본인 프로젝트 구조에 맞게 수정하세요!
    # 예: "data/kospi_5years_combined.csv"
    df = pd.read_csv("data/kospi_5years_combined.csv")
    df["Date"]   = pd.to_datetime(df["Date"])
    df["Symbol"] = df["Symbol"].astype(str).str.zfill(6)
    df = df[df["Date"].dt.dayofweek < 5]  # 주말 제거
    return df

# ── 모델 로드 ──────────────────────────────
@st.cache_resource
def load_models():
    # ⚠️ 경로를 본인 models/ 폴더 위치에 맞게 수정하세요!
    return {
        "Linear Regression": joblib.load("models/lr_model.pkl"),
        "Random Forest":     joblib.load("models/rf_model.pkl"),
        "XGBoost":           joblib.load("models/xgb_model.pkl"),
        "LightGBM":          joblib.load("models/lgbm_model.pkl"),
    }

# 종목 리스트 (필요에 따라 추가/수정 가능)
ticker_map = {
    "005930":"삼성전자", "000660":"SK하이닉스",
    "005380":"현대차",   "373220":"LG에너지솔루션",
    "329180":"HD현대중공업"
}

# 사이드바 종목 선택
with st.sidebar:
    st.title("📊 종목")
    for code, name in ticker_map.items():
        if st.button(name, use_container_width=True):
            st.session_state.symbol = code

# 차트 컨트롤 (봉·기간·거래량)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    timeframe = st.radio("봉", ["일봉", "주봉", "월봉"], horizontal=True)
with col2:
    period = st.radio("기간", ["3개월", "6개월", "1년", "3년", "전체"],
                      horizontal=True, index=2)
with col3:
    show_volume = st.toggle("거래량", value=False)

# 캔들스틱 차트 (한국 색상: 빨간=상승, 파란=하락)
fig.add_trace(go.Candlestick(
    x=stock_df["Date"], open=stock_df["Open"],
    high=stock_df["High"], low=stock_df["Low"],
    close=stock_df["Close"],
    increasing_line_color='#FF3B30',   # 빨간 = 상승
    decreasing_line_color='#007AFF',   # 파란 = 하락
))
