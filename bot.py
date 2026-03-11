import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os

# Ambil URI dari secret GitHub
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['hnp_database']
collection = db['videos_global']

def gas_nyolong():
    # Contoh target awal (nanti kita ganti ke target asli yang lebih ganas)
    url = "https://www.google.com" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Robot HNP mulai memantau target...")
        
        # Test simpan satu data ke MongoDB buat mastiin koneksi lancar
        data_test = {
            "title": "HNP Digital Test", 
            "link": "https://hnp-production.com/test", 
            "status": "ready_to_cuan"
        }
        
        # Cek dlu biar gak double
        if not collection.find_one({"title": "HNP Digital Test"}):
            collection.insert_one(data_test)
            print("Berhasil! Data test masuk ke MongoDB Atlas.")
        else:
            print("Data test udah ada di gudang.")
            
    except Exception as e:
        print(f"Error pas nyoba konek: {e}")

if __name__ == "__main__":
    gas_nyolong()
  
