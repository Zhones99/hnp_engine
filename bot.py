import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import random

# 1. Koneksi ke Gudang Data HNP
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['hnp_database']
collection = db['videos_global']

def hnp_hunter():
    # DAFTAR TARGET (Bisa lu tambah terus di sini)
    targets = [
        {"name": "XV", "url": "https://www.xvideos.com/", "selector": "div.mozaique div.thumb-block"},
        {"name": "XN", "url": "https://www.xnxx.com/", "selector": "div.thumb-block"},
    ]

    # Biar gak ketauan Bot (Nyamar jadi Chrome/Safari)
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]

    for site in targets:
        try:
            print(f"[*] HNP Hunter sedang memantau target: {site['name']}")
            headers = {'User-Agent': random.choice(user_agents)}
            
            response = requests.get(site['url'], headers=headers, timeout=20)
            if response.status_code != 200:
                print(f"[!] Gagal akses {site['name']}, Status: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari kotak video berdasarkan selector
            video_blocks = soup.select(site['selector'])
            count_new = 0

            for block in video_blocks:
                try:
                    # Ambil Link & Judul (Logika umum tag <a> di dalem div video)
                    link_tag = block.find('a', href=True)
                    img_tag = block.find('img', src=True)

                    if link_tag and img_tag:
                        raw_link = link_tag['href']
                        # Pastikan link lengkap
                        full_link = raw_link if raw_link.startswith('http') else site['url'].rstrip('/') + raw_link
                        
                        title = img_tag.get('alt') or link_tag.get('title') or "No Title"
                        thumb = img_tag.get('data-src') or img_tag.get('src') # Kadang pake lazy load

                        # SIMPAN KE MONGODB (Cek duplikat pake Link)
                        if not collection.find_one({"link": full_link}):
                            collection.insert_one({
                                "title": title,
                                "link": full_link,
                                "thumbnail": thumb,
                                "source": site['name'],
                                "status": "active",
                                "created_at": "2026-03-11" # Tanggal hari ini
                            })
                            count_new += 1
                except:
                    continue

            print(f"[+] Berhasil setor {count_new} link baru dari {site['name']} ke MongoDB.")

        except Exception as e:
            print(f"[!] Error di {site['name']}: {e}")

if __name__ == "__main__":
    hnp_hunter()
            
