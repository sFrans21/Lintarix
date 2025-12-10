import sys
import time
from termcolor import colored
from src.market_data import MarketFetcher
from src.news_scraper import NewsFetcher
from src.llm_engine import LLMEngine

def main():
    print(colored("\n===========================================", "cyan", attrs=['bold']))
    print(colored("   LINTARIX: AI INVESTMENT ANALYST  ", "cyan", attrs=['bold']))
    print(colored("===========================================", "cyan", attrs=['bold']))
    
    # 1. Inisialisasi Engine
    try:
        news_engine = NewsFetcher()
        llm_engine = LLMEngine()
    except Exception as e:
        print(colored(f"❌ Gagal inisialisasi sistem: {e}", "red"))
        return

    # 2. Input User
    while True:
        print(colored("\n-------------------------------------------", "white"))
        ticker = input("Masukkan Ticker Saham (contoh: BBRI.JK, NVDA, atau 'exit'): ").strip().upper()
        
        if ticker.lower() == 'exit':
            print("Sampai jumpa!")
            break
        if not ticker:
            continue

        start_time = time.time()

        # --- TAHAP 1: MATA (Data Pasar) ---
        print(colored(f"\n[1/3] 📊 Mengambil Data Pasar untuk {ticker}...", "yellow"))
        market_fetcher = MarketFetcher(ticker)
        market_data, err = market_fetcher.get_market_data()

        if err:
            print(colored(f"❌ Error: {err}", "red"))
            continue
        
        print(colored(f"   Harga: {market_data['current_price']} | RSI: {market_data['rsi']} | Trend: {market_data['trend']}", "green"))

        # --- TAHAP 2: TELINGA (Berita) ---
        print(colored(f"\n[2/3] 📰 Mencari Berita & Sentimen...", "yellow"))
        news_data = news_engine.get_news(ticker)
        
        if news_data:
            print(colored(f"   Ditemukan {len(news_data)} berita relevan.", "green"))
        else:
            print(colored("   Tidak ada berita ditemukan (Analisis akan murni teknikal).", "white"))

        # --- TAHAP 3: OTAK (Reasoning AI) ---
        print(colored(f"\n[3/3] 🧠 Lintarix AI sedang menganalisis (Reasoning)...", "magenta", attrs=['bold']))
        
        analysis_result = llm_engine.analyze(ticker, market_data, news_data)
        
        # Tampilkan Hasil
        print(colored("\n" + "="*50, "cyan"))
        print(colored(f"HASIL ANALISIS: {ticker}", "white", attrs=['bold']))
        print(colored("="*50, "cyan"))
        print(analysis_result)
        print(colored("="*50, "cyan"))
        
        # Info Durasi
        duration = round(time.time() - start_time, 2)
        print(colored(f"✅ Selesai dalam {duration} detik.", "white", attrs=['dark']))

if __name__ == "__main__":
    main()