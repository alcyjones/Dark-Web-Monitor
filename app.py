from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import threading
from datetime import datetime
import requests
import re
from urllib.parse import urljoin
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TorCrawler:
    def __init__(self):
        self.session = requests.Session()
        # Proxy TOR padrão (localhost:9050)
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.visited_urls = set()
        self.max_depth = 2

    def is_tor_running(self):
        try:
            # httpbin.org é acessível pela clearnet via TOR, útil pra testar IP
            response = self.session.get('http://httpbin.org/ip', timeout=10)
            return response.status_code == 200
        except:
            return False

    def extract_links(self, html, base_url):
        links = []
        # Extrai href="..."
        link_pattern = r'href=[\"\']([^\"\']+)[\"\']'
        matches = re.findall(link_pattern, html, re.IGNORECASE)

        for match in matches:
            if match.startswith('http'):
                links.append(match)
            elif match.startswith('/'):
                links.append(urljoin(base_url, match))
        return links

    def search_keywords(self, html, keywords):
        found_keywords = []
        html_lower = html.lower()
        for keyword in keywords:
            if keyword.lower() in html_lower:
                found_keywords.append(keyword)
        return found_keywords

    def crawl_url(self, url, keywords, depth=0):
        if depth > self.max_depth or url in self.visited_urls:
            return []

        self.visited_urls.add(url)
        results = []

        try:
            logger.info(f"Crawling: {url}")
            response = self.session.get(url, timeout=30)

            if response.status_code == 200:
                html = response.text
                found_keywords = self.search_keywords(html, keywords)

                if found_keywords:
                    result = {
                        'url': url,
                        'keywords': found_keywords,
                        'timestamp': datetime.now().isoformat(),
                        'title': self.extract_title(html)
                    }
                    results.append(result)
                    self.save_result(result)

                # Segue links .onion
                if '.onion' in url and depth < self.max_depth:
                    links = self.extract_links(html, url)
                    for link in links[:5]:  # limita a 5 por página
                        if '.onion' in link:
                            results.extend(self.crawl_url(link, keywords, depth + 1))

        except Exception as e:
            logger.error(f"Erro ao crawl {url}: {str(e)}")

        return results

    def extract_title(self, html):
        m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return m.group(1).strip() if m else "Sem título"

    def save_result(self, result):
        conn = sqlite3.connect('darkweb_monitor.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO results (url, keywords, timestamp, title)
            VALUES (?, ?, ?, ?)
            ''',
            (result['url'], ','.join(result['keywords']), result['timestamp'], result['title'])
        )
        conn.commit()
        conn.close()

crawler = TorCrawler()

def init_db():
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            keywords TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/keywords')
def keywords():
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM keywords ORDER BY created_at DESC')
    keywords_list = cursor.fetchall()
    conn.close()
    return render_template('keywords.html', keywords=keywords_list)

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    keyword = request.form.get('keyword', '').strip()
    if keyword:
        conn = sqlite3.connect('darkweb_monitor.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO keywords (keyword) VALUES (?)', (keyword,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()
    return redirect(url_for('keywords'))

@app.route('/delete_keyword/<int:keyword_id>')
def delete_keyword(keyword_id):
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM keywords WHERE id = ?', (keyword_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('keywords'))

@app.route('/urls')
def urls():
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM urls ORDER BY created_at DESC')
    urls_list = cursor.fetchall()
    conn.close()
    return render_template('urls.html', urls=urls_list)

@app.route('/add_url', methods=['POST'])
def add_url():
    url = request.form.get('url', '').strip()
    if url and '.onion' in url:
        conn = sqlite3.connect('darkweb_monitor.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()
    return redirect(url_for('urls'))

@app.route('/toggle_url/<int:url_id>')
def toggle_url(url_id):
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE urls SET active = NOT active WHERE id = ?', (url_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('urls'))

@app.route('/results')
def results():
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM results ORDER BY created_at DESC LIMIT 100')
    results_list = cursor.fetchall()
    conn.close()
    return render_template('results.html', results=results_list)

@app.route('/start_monitoring')
def start_monitoring():
    if not crawler.is_tor_running():
        return jsonify({'error': 'TOR não está rodando. Inicie o TOR primeiro.'}), 400

    thread = threading.Thread(target=run_monitoring, daemon=True)
    thread.start()
    return jsonify({'message': 'Monitoramento iniciado!'})

def run_monitoring():
    conn = sqlite3.connect('darkweb_monitor.db')
    cursor = conn.cursor()

    cursor.execute('SELECT keyword FROM keywords')
    keywords = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT url FROM urls WHERE active = 1')
    urls = [row[0] for row in cursor.fetchall()]

    conn.close()

    if not keywords or not urls:
        logger.warning("Nenhuma palavra-chave ou URL configurada")
        return

    logger.info(f"Iniciando monitoramento com {len(keywords)} palavras-chave e {len(urls)} URLs")

    for url in urls:
        try:
            crawler.crawl_url(url, keywords)
        except Exception as e:
            logger.error(f"Erro no monitoramento de {url}: {str(e)}")

@app.route('/status')
def status():
    return jsonify({'tor_running': crawler.is_tor_running()})

@app.route('/upload_urls', methods=['GET', 'POST'])
def upload_urls():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and file.filename.endswith('.txt'):
            urls_added = 0
            urls_skipped = 0
            
            conn = sqlite3.connect('darkweb_monitor.db')
            cursor = conn.cursor()
            
            for line in file.readlines():
                url = line.decode('utf-8').strip()
                if url and '.onion' in url:
                    try:
                        cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
                        urls_added += 1
                    except sqlite3.IntegrityError:
                        urls_skipped += 1 # URL já existe
                else:
                    urls_skipped += 1 # URL inválida ou não .onion
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'message': f'{urls_added} URLs adicionadas, {urls_skipped} URLs ignoradas.',
                'added': urls_added,
                'skipped': urls_skipped
            }), 200
        else:
            return jsonify({'error': 'Formato de arquivo inválido. Apenas .txt é permitido.'}), 400
            
    return render_template('upload_urls.html') # Vamos criar este template

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
