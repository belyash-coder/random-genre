from flask import Flask, jsonify
import requests
import re
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/everynoise')
def everynoise():
    try:
        r = requests.get('https://everynoise.com/engenremap.html', 
                         headers={'User-Agent': 'Mozilla/5.0'})
        # Ищем жанры в ссылках
        genres = re.findall(r'href="\?genre=[^"]*"[^>]*>(.*?)<', r.text)
        # Чистим от HTML тегов
        genres = [re.sub(r'<.*?>', '', g).strip() for g in genres]
        # Фильтруем мусор
        genres = [g for g in genres if g and len(g) > 1 and len(g) < 80]
        genres = list(set(genres))
        
        if not genres:
            return jsonify({"error": "жанры не найдены"})
            
        genre = random.choice(genres)
        return jsonify({"genre": genre, "total": len(genres)})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/musicmap')
def musicmap():
    try:
        r = requests.get('https://musicmap.info/',
                         headers={'User-Agent': 'Mozilla/5.0'})
        
        # Находим текст всех ссылок
        raw_genres = re.findall(r'<a[^>]*>(.*?)</a>', r.text)
        
        # Чистим от HTML
        raw_genres = [re.sub(r'<.*?>', '', g).strip() for g in raw_genres]
        
        # Фильтруем мусор
        blacklist = [
            'wikipedia', 'list of', '2016', 'copyright', '©', 'http',
            'privacy', 'cookie', 'contact', 'about', 'home', 'menu',
            'search', 'previous', 'next', 'more', 'click', 'here',
            'musicmap', 'info', 'general', 'the music', 'legend',
            'super-genre', 'sub-genre', 'derivative', 'preference',
            'facebook', 'twitter', 'share', 'email'
        ]
        
        genres = []
        for g in raw_genres:
            g_lower = g.lower()
            # Пропускаем если содержит запрещённые слова
            if any(bad in g_lower for bad in blacklist):
                continue
            # Пропускаем слишком длинные/короткие
            if len(g) < 3 or len(g) > 50:
                continue
            # Пропускаем если много заглавных (служебный текст)
            if g.isupper() and len(g) > 10:
                continue
            # Пропускаем чисто цифровые
            if g.isdigit():
                continue
            genres.append(g)
        
        genres = list(set(genres))
        
        if not genres:
            return jsonify({"error": "жанры не найдены"})
            
        genre = random.choice(genres)
        return jsonify({"genre": genre, "total": len(genres)})
    except Exception as e:
        return jsonify({"error": str(e)})
