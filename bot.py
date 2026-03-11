import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os

# Koneksi ke Gudang HNP
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['hnp_database']
collection = db['videos_global']

def hunter_mode():
    # GANTI URL ini dengan situs target global lu (contoh situs video)
    target_url = "https://www.example-video-site.com/latest-updates" 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print(f"HNP Hunter sedang memantau: {target_url}")
        response = requests.get(target_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Logika mencari kotak video (Sesuaikan class-nya nanti)
        # Biasanya video ada di dalam tag <a> atau <div> tertentu
        count = 0
        for vid in soup.find_all('div', class_='video-block'): # Ini contoh class
            title = vid.find('img')['alt'] # Ambil judul dari alt gambar
            link = vid.find('a')['href']  # Ambil link detail
            thumb = vid.find('img')['src'] # Ambil gambar cover
            
            # Masukin ke database kalau belum ada
            if not collection.find_one({"link": link}):
                collection.insert_one({
                    "title": title,
                    "link": link,
                    "thumbnail": thumb,
                    "source": "Global_Site_1",
                    "status": "active"
                })
                count += 1
        
        print(f"Selesai! Berhasil nyolong {count} link baru hari ini.")
        
    except Exception as e:
        print(f"Hunter gagal operasional: {e}")

if __name__ == "__main__":
    hunter_mode()
    
