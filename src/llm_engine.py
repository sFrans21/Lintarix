import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load API Key dari file .env
load_dotenv()

class LLMEngine:
    def __init__(self):
        # Ambil key dari lingkungan sistem
        self.api_key = os.getenv("GROQ_API_KEY")
        
        # Cek apakah key ada
        if not self.api_key:
            raise ValueError("❌ API Key Groq tidak ditemukan! Pastikan file .env sudah benar.")
        
        # Inisialisasi Client Groq
        self.client = Groq(api_key=self.api_key)
        
        # Kita pakai model Llama-3.3
        self.model = "llama-3.3-70b-versatile" 

    def analyze(self, ticker, market_data, news_data):
        """
        Fungsi utama untuk mengirim data ke AI dan meminta analisis.
        """
        
        # Format Berita agar rapi dibaca AI
        news_context = ""
        if news_data:
            for i, n in enumerate(news_data, 1):
                news_context += f"{i}. [{n['source']}] {n['title']}\n   Snippet: {n['snippet']}\n"
        else:
            news_context = "Tidak ada berita terkini yang ditemukan."

        # --- PROMPT ENGINEERING (Jantung dari New Quant) ---
        
        system_prompt = """
        You are Lintarix, a professional 'New Quant' Investment Analyst AI.
        Your goal is to synthesize Technical Data (Numbers) with Sentiment Data (News) to provide a reasoning-based verdict.
        Bahasa: Please answer in Indonesian (Bahasa Indonesia).
        Style: Professional, Objective, Analytical.
        """

        user_prompt = f"""
        Tolong analisis saham berikut: {ticker}

        [DATA TEKNIKAL]
        - Harga Saat Ini: {market_data['current_price']}
        - RSI (14): {market_data['rsi']} (Note: <30 Oversold, >70 Overbought)
        - Trend (vs SMA5): {market_data['trend']}
        
        [BERITA & SENTIMEN TERBARU]
        {news_context}

        [TUGAS ANDA]
        Berikan analisis terstruktur:
        1. **Sentimen Pasar:** (Ringkasan singkat dari berita yang ada)
        2. **Perspektif Teknikal:** (Apa arti dari RSI dan Trend saat ini?)
        3. **New Quant Insight (Reasoning):** (Gabungkan keduanya. Apakah ada konflik antara harga dan berita? Apa pemicu utamanya?)
        4. **Kesimpulan:** (Pilih satu: BULLISH / BEARISH / NEUTRAL / WAIT AND SEE, beserta alasannya).
        """

        try:
            # Kirim request ke Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.6, # Kreativitas moderat
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ Error pada LLM Engine: {str(e)}"

# --- BLOCK TESTING ---
# Kode di bawah ini hanya jalan kalau file ini di-run langsung
if __name__ == "__main__":
    print("⏳ Sedang menghubungi Otak AI (Groq)...")
    
    # Kita buat Data Palsu (Dummy) untuk ngetes logika AI
    dummy_market = {"current_price": 5000, "rsi": 25, "trend": "Bearish"}
    dummy_news = [
        {"source": "CNBC", "title": "Laba Perusahaan Melonjak 50%", "snippet": "Laporan keuangan Q3 menunjukkan kenaikan laba bersih yang signifikan melebihi ekspektasi analis."},
        {"source": "Bloomberg", "title": "CEO Optimis Target Tahunan Tercapai", "snippet": "Dalam wawancara, CEO menegaskan ekspansi bisnis berjalan lancar."}
    ]
    
    # Panggil Engine
    engine = LLMEngine()
    hasil = engine.analyze("TEST.JK", dummy_market, dummy_news)
    
    print("\n=== HASIL ANALISIS AI ===")
    print(hasil)