# # Ngambil berita dari DDGS: DuckDuckGo Search karna gratis dna powerful untuk ngambil snippet berita

# # ga perlu full article text karena sering kena paywall/bot detection. Buat analisis LLM nya, kasih judul + Snippet ringkasan 2 kalimat aja dari 5 sumber berbeda udah cukup untuk nangkap sentimen pasar

# from duckduckgo_search import DDGS
# from datetime import datetime

# class NewsFetcher:
#     def __init__(self):
#         self.ddgs = DDGS()

#     def get_news(self, query, max_results=5):
#         """
#         Mencari berita terbaru menggunakan DuckDuckGo.
#         Query otomatis ditambah kata kunci finansial.
#         """
#         search_query = f"{query} stock news finance business"
#         news_list = []

#         try:
#             # Menggunakan DDGS untuk mencari berita (timelimit='w' artinya minggu ini)
#             results = self.ddgs.text(search_query, max_results=max_results, timelimit='w')
            
#             if not results:
#                 return []

#             for res in results:
#                 news_item = {
#                     "title": res['title'],
#                     "source": res['href'], # Link sumber
#                     "snippet": res['body'], # Ringkasan konten
#                     "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M")
#                 }
#                 news_list.append(news_item)
            
#             return news_list

#         except Exception as e:
#             print(f"Error fetching news: {e}")
#             return []

# # Test block
# if __name__ == "__main__":
#     fetcher = NewsFetcher()
#     berita = fetcher.get_news("BBRI Bank Rakyat Indonesia")
#     for b in berita:
#         print(f"[{b['title']}]\n{b['snippet']}\n")

import json
import os
from datetime import datetime, timedelta
from GoogleNews import GoogleNews
from termcolor import colored

class NewsFetcher:
    def __init__(self):
        # Konfigurasi Google News
        self.googlenews = GoogleNews(lang='en', region='US', period='7d')
        
        # Konfigurasi Cache
        self.cache_dir = "data"
        self.cache_file = os.path.join(self.cache_dir, "news_cache.json")
        self.cache_duration_hours = 4  # Cache berlaku 4 jam
        
        # Buat folder data jika belum ada
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _load_cache(self):
        """Membaca file JSON cache."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self, data):
        """Menyimpan data ke file JSON."""
        with open(self.cache_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_news(self, query, max_results=5):
        clean_query = query.replace(".JK", "") # Key untuk cache (misal: BBRI)
        
        # 1. CEK CACHE DULU
        cache_data = self._load_cache()
        
        if clean_query in cache_data:
            entry = cache_data[clean_query]
            cached_time = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
            
            # Cek apakah cache masih valid (belum kadaluarsa)
            if datetime.now() - cached_time < timedelta(hours=self.cache_duration_hours):
                print(colored(f"   [CACHE HIT] Menggunakan data tersimpan ({entry['timestamp']})", "cyan"))
                return entry['data']
            else:
                print(colored("   [CACHE EXPIRED] Data lama kadaluarsa, mengambil baru...", "yellow"))
        
        # 2. AMBIL DARI GOOGLE (Jika cache tidak ada/expired)
        try:
            search_query = f"{clean_query} stock financial news"
            self.googlenews.clear()
            self.googlenews.search(search_query)
            
            results = self.googlenews.result()
            news_list = []
            
            for item in results[:max_results]:
                if len(item['title']) > 5: 
                    news_item = {
                        "title": item['title'],
                        "source": item['media'],
                        "snippet": item['desc'],
                        "link": item['link'],
                        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    news_list.append(news_item)
            
            # 3. SIMPAN KE CACHE
            if news_list:
                cache_data[clean_query] = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": news_list
                }
                self._save_cache(cache_data)
                print(colored("   [API CALL] Berhasil mengambil data baru dari Google.", "green"))
            
            return news_list

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

if __name__ == "__main__":
    fetcher = NewsFetcher()
    berita = fetcher.get_news("BBRI")
    print(f"Jumlah berita: {len(berita)}")