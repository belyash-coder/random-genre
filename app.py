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
        genres = re.findall(r'href="\?genre=[^"]*"[^>]*>(.*?)<', r.text)
        genres = list(set(genres))
        genre = random.choice(genres)
        return jsonify({"genre": genre, "total": len(genres)})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/musicmap')
def musicmap():
    try:
        r = requests.get('https://musicmap.info/',
                         headers={'User-Agent': 'Mozilla/5.0'})
        genres = re.findall(r'<a[^>]*>(.*?)</a>', r.text)
        genres = list(set([g.strip() for g in genres if 3 < len(g.strip()) < 60]))
        genre = random.choice(genres)
        return jsonify({"genre": genre, "total": len(genres)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
