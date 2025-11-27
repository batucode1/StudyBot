import json
import os

user_data = {}
DATA_FILE = "study_bot_data.json"


def load_data():
    global user_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            # ÖNEMLİ DEĞİŞİKLİK BURADA:
            # Eşittir (=) yerine .update() kullanıyoruz.
            # Böylece hafızadaki kutuyu değiştirmeden içini dolduruyoruz.
            try:
                data = json.load(f)
                user_data.update(data)
            except json.JSONDecodeError:
                print("JSON dosyası bozuk veya boş, yeni veri tabanı ile başlanıyor.")


def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(user_data, f, indent=4)


def initialize_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "tasks": [],
            "notes": [],
            "study_sessions": [],
            "total_study_minutes": 0
        }
        save_data()
