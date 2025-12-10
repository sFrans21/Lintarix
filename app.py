import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.market_data import MarketFetcher
from src.news_scraper import NewsFetcher
from src.llm_engine import LLMEngine
from src.pdf_generator import create_pdf

# --- 1. SETUP PAGE ---
st.set_page_config(
    page_title="Lintarix Terminal",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. THE DESIGN SYSTEM (CSS INJECTION) ---
st.markdown("""
<style>
    /* IMPORTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* --- ROOT VARIABLES (The Brand Palette) --- */
    :root {
        --bg-color: #050505; /* Almost Pure Black */
        --card-bg: #0A0A0A;
        --border-color: #262626;
        --accent-primary: #8B5CF6; /* Violet Glow */
        --accent-secondary: #3B82F6; /* Blue Glow */
        --text-primary: #EDEDED;
        --text-secondary: #A1A1AA;
    }

    /* --- GLOBAL RESETS --- */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }
    
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    /* --- TYPOGRAPHY: GRADIENT TITLE --- */
    h1 span {
        background: linear-gradient(90deg, #FFFFFF 0%, #999999 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* --- COMPONENT: METRIC CARDS (The 'Linear' Glow) --- */
    div[data-testid="stMetric"] {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    /* Hover Effect: Glowing Border */
    div[data-testid="stMetric"]:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        font-weight: 700;
        color: #fff;
    }

    /* --- COMPONENT: BUTTONS --- */
    div.stButton > button {
        background: linear-gradient(180deg, #1e1e1e 0%, #0a0a0a 100%);
        color: white;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: var(--text-primary);
        color: #fff;
        box-shadow: 0 0 10px rgba(255,255,255,0.1);
    }
    
    /* Primary Action Button Override */
    div.stButton > button:active {
        background: var(--accent-primary);
        border-color: var(--accent-primary);
    }

    /* --- COMPONENT: INPUTS --- */
    .stTextInput input {
        background-color: #0A0A0A !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 8px;
    }
    .stTextInput input:focus {
        border-color: var(--accent-primary) !important;
    }

    /* --- COMPONENT: TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid #262626;
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER & HERO ---
col_h1, col_h2 = st.columns([0.1, 0.9])
with col_h1:
    st.markdown("<h1 style='font-size: 40px;'>⚡</h1>", unsafe_allow_html=True)
with col_h2:
    st.title("LINTARIX")
    st.markdown("<div style='margin-top: -15px; color: #666; font-family: JetBrains Mono; font-size: 14px;'>INSTITUTIONAL GRADE AI ANALYST</div>", unsafe_allow_html=True)

st.markdown("---")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### CONTROL STATION")
    ticker = st.text_input("ASSET TICKER", value="BBRI.JK").upper()
    
    st.markdown("###")
    analyze_btn = st.button("RUN ANALYSIS MODULE")
    
    st.markdown("---")
    st.info("STATUS: **ONLINE**\n\nAI CORE: **LLAMA-3**\nDATA FEED: **REALTIME**")

# --- 5. MAIN LOGIC ---

if analyze_btn:
    news_engine = NewsFetcher()
    llm_engine = LLMEngine()
    
    # Custom Loader yang minimalis
    with st.status("SYSTEM PROCESS...", expanded=True) as status:
        st.write("Targeting Asset Data...")
        market_fetcher = MarketFetcher(ticker)
        summary, hist_df, err = market_fetcher.get_market_data()
        
        if err:
            status.update(label="CRITICAL ERROR", state="error")
            st.error(err)
            st.stop()
            
        st.write("Synthesizing Global Intel...")
        news_data = news_engine.get_news(ticker)
        
        st.write("Computing Verdict...")
        analysis_result = llm_engine.analyze(ticker, summary, news_data)
        
        status.update(label="COMPUTATION COMPLETE", state="complete", expanded=False)

    st.session_state['data'] = {
        'ticker': ticker,
        'summary': summary,
        'hist_df': hist_df,
        'news_data': news_data,
        'analysis_result': analysis_result
    }

if 'data' in st.session_state:
    data = st.session_state['data']
    
    # --- METRICS GRID (The Glowing Cards) ---
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("ASSET PRICE", f"{data['summary']['current_price']:,}")
    
    # Custom Logic untuk RSI Label
    rsi = data['summary']['rsi']
    rsi_label = "NEUTRAL"
    if rsi < 30: rsi_label = "OVERSOLD (BUY)"
    elif rsi > 70: rsi_label = "OVERBOUGHT (SELL)"
    
    col2.metric("RSI (14)", f"{rsi}", rsi_label)
    col3.metric("MOMENTUM", data['summary']['trend'])
    col4.metric("VOL (24H)", f"{data['summary']['volume']:,}")

    st.markdown("###")

    # --- CHART SECTION (The Cyberpunk Graph) ---
    st.markdown(f"<h4 style='font-family: Inter; font-weight: 800;'>PRICE ACTION: {data['ticker']}</h4>", unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['hist_df'].index,
        open=data['hist_df']['Open'], high=data['hist_df']['High'],
        low=data['hist_df']['Low'], close=data['hist_df']['Close'], 
        name='Price',
        increasing_line_color='#8B5CF6', # Neon Violet
        decreasing_line_color='#525252'  # Dark Grey (Ghost)
    ))
    
    # Chart Styling Ekstrem
    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_rangeslider_visible=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, color='#444'),
        yaxis=dict(gridcolor='#1a1a1a', color='#444', zerolinecolor='#333')
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- ANALYSIS SECTION (Clean Typography) ---
    st.markdown("###")
    
    tab1, tab2 = st.tabs(["INTELLIGENCE REPORT", "DATA SOURCES"])
    
    with tab1:
        # Container khusus untuk Teks AI
        st.markdown(f"""
        <div style="
            background-color: #0A0A0A; 
            border: 1px solid #262626; 
            padding: 25px; 
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #D4D4D8;
        ">
            {data['analysis_result'].replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        if data['news_data']:
            for item in data['news_data']:
                st.markdown(f"""
                <div style="padding: 10px; border-bottom: 1px solid #222;">
                    <div style="font-size: 12px; color: #666; font-family: JetBrains Mono;">{item['source'].upper()}</div>
                    <a href="{item['link']}" style="color: #EDEDED; text-decoration: none; font-weight: 600; font-size: 15px;">{item['title']}</a>
                    <div style="font-size: 13px; color: #888; margin-top: 5px;">{item['snippet']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No external signal detected.")

    # --- EXPORT ---
    st.markdown("---")
    col_x, col_y = st.columns([0.8, 0.2])
    with col_y:
        if st.button("DOWNLOAD PDF"):
            try:
                pdf_bytes = create_pdf(
                    data['ticker'], 
                    data['summary'], 
                    data['analysis_result'], 
                    fig
                )
                st.download_button(
                    label="GET FILE",
                    data=pdf_bytes,
                    file_name=f"LINTARIX_{data['ticker']}.pdf",
                    mime="application/pdf"
                )
            except:
                st.error("Export Failed")

else:
    # Empty State - Minimalist Center
    st.markdown("""
    <div style='text-align: center; margin-top: 100px; color: #333;'>
        <h3 style='color: #222;'>WAITING FOR INPUT</h3>
        <p style='font-family: JetBrains Mono; font-size: 12px;'>SECURE CONNECTION ESTABLISHED</p>
    </div>
    """, unsafe_allow_html=True)