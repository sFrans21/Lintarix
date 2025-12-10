import streamlit as st
import plotly.graph_objects as go
from src.market_data import MarketFetcher
from src.news_scraper import NewsFetcher
from src.llm_engine import LLMEngine
from src.pdf_generator import create_pdf

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Lintarix AI",
    page_icon="📈",
    layout="wide"
)

# Judul & Header
st.title("🤖 Lintarix: AI Investment Analyst")
st.markdown("---")

# --- SIDEBAR (Input User) ---
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    ticker = st.text_input("Masukkan Ticker Saham", value="BBRI.JK").upper()
    analyze_btn = st.button("🚀 Mulai Analisis", type="primary")
    
    st.info("Tips: Gunakan .JK untuk saham Indonesia (contoh: BBRI.JK). Gunakan kode langsung untuk US (contoh: NVDA).")

# --- LOGIKA UTAMA (Menggunakan Session State) ---

# 1. JIKA TOMBOL DIKLIK -> AMBIL DATA & SIMPAN KE MEMORI
if analyze_btn:
    news_engine = NewsFetcher()
    llm_engine = LLMEngine()
    
    with st.status("🔍 Sedang bekerja...", expanded=True) as status:
        # A. Data Pasar
        st.write("📊 Mengambil data pasar...")
        market_fetcher = MarketFetcher(ticker)
        summary, hist_df, err = market_fetcher.get_market_data()
        
        if err:
            status.update(label="❌ Terjadi Kesalahan", state="error")
            st.error(err)
            st.stop()
            
        # B. Berita
        st.write("📰 Membaca berita & sentimen...")
        news_data = news_engine.get_news(ticker)
        
        # C. AI Analysis
        st.write("🧠 Lintarix AI sedang berpikir...")
        analysis_result = llm_engine.analyze(ticker, summary, news_data)
        
        status.update(label="✅ Analisis Selesai!", state="complete", expanded=False)

    # --- PENTING: SIMPAN KE SESSION STATE AGAR TIDAK HILANG ---
    st.session_state['data'] = {
        'ticker': ticker,
        'summary': summary,
        'hist_df': hist_df,
        'news_data': news_data,
        'analysis_result': analysis_result
    }

# 2. JIKA ADA DATA DI MEMORI -> TAMPILKAN DASHBOARD
if 'data' in st.session_state:
    # Ambil data dari memori
    data = st.session_state['data']
    
    # --- TAMPILAN DASHBOARD ---
    
    # Kolom 1: Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Harga Terakhir", f"{data['summary']['current_price']:,}")
    col2.metric("RSI (14)", data['summary']['rsi'], delta="Oversold" if data['summary']['rsi'] < 30 else "Normal")
    col3.metric("Trend (vs SMA5)", data['summary']['trend'], delta_color="normal")
    col4.metric("Volume", f"{data['summary']['volume']:,}")

    # Kolom 2: Grafik & Analisis
    row2_col1, row2_col2 = st.columns([2, 1])

    with row2_col1:
        st.subheader("📈 Pergerakan Harga")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data['hist_df'].index,
                        open=data['hist_df']['Open'], high=data['hist_df']['High'],
                        low=data['hist_df']['Low'], close=data['hist_df']['Close'], name='Market Data'))
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with row2_col2:
        st.subheader("🤖 Analisis AI")
        st.info(data['analysis_result'])

    # Kolom 3: Sumber Berita
    with st.expander("📚 Lihat Sumber Berita & Data Pendukung"):
        if data['news_data']:
            for item in data['news_data']:
                st.markdown(f"**[{item['source']}] {item['title']}**")
                st.caption(item['snippet'])
                st.markdown(f"[Baca Selengkapnya]({item['link']})")
                st.markdown("---")
        else:
            st.write("Tidak ada berita spesifik ditemukan.")

    # --- FITUR EXPORT PDF ---
    st.markdown("---")
    st.subheader("📥 Export Laporan")
    
    # Tombol ini sekarang AMAN karena data diambil dari st.session_state
    if st.button("📄 Generate PDF Report"):
        with st.spinner("Sedang membuat PDF... (Grafik sedang dirender)"):
            try:
                pdf_bytes = create_pdf(
                    data['ticker'], 
                    data['summary'], 
                    data['analysis_result'], 
                    fig
                )
                
                st.download_button(
                    label="⬇️ Download PDF Sekarang",
                    data=pdf_bytes,
                    file_name=f"Lintarix_Report_{data['ticker']}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                st.success("PDF berhasil dibuat! Klik tombol di atas untuk mengunduh.")
                
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")

else:
    st.write("👈 Masukkan kode saham di sidebar dan klik tombol untuk memulai.")