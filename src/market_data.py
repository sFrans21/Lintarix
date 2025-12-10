import yfinance as yf
import pandas as pd
# import requests <-- Dihapus karena yfinance terbaru melarang session manual

class MarketFetcher:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        
        # --- UPDATE MINGGU 3 ---
        # Kita hapus session manual. 
        # Biarkan yfinance menangani anti-blocking secara internal (via curl_cffi).
        self.stock = yf.Ticker(self.ticker)

    def get_market_data(self, period="1mo"):
        """
        Mengambil data historis dan menghitung indikator teknikal dasar.
        Return: (Summary Dict, DataFrame History, Error Message)
        """
        try:
            # 1. Ambil History
            # auto_adjust=True penting untuk data harga yang bersih
            hist = self.stock.history(period=period, auto_adjust=True)
            
            if hist.empty:
                return None, None, f"Data kosong untuk {self.ticker}. Coba cek koneksi atau ganti ticker."

            # 2. Hitung Indikator (Manual dengan Pandas)
            # SMA 5
            hist['SMA_5'] = hist['Close'].rolling(window=5).mean()
            
            # RSI 14
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            loss = loss.replace(0, 0.00001) # Hindari pembagian nol
            rs = gain / loss
            hist['RSI'] = 100 - (100 / (1 + rs))

            # 3. Ambil data terakhir
            latest = hist.iloc[-1]
            
            summary = {
                "current_price": round(latest['Close'], 2),
                "volume": int(latest['Volume']),
                "rsi": round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else 0,
                "trend": "Bullish" if latest['Close'] > latest['SMA_5'] else "Bearish"
            }
            
            return summary, hist, None

        except Exception as e:
            # Print error ke terminal untuk debugging, tapi return pesan user-friendly
            print(f"DEBUG ERROR: {e}")
            return None, None, f"Gagal mengambil data: {str(e)}"