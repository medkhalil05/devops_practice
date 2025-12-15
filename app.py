from flask import Flask, render_template_string, jsonify
import speedtest
import threading
import time
import os

app = Flask(__name__)

# Variables pour stocker les résultats du test de vitesse
speedtest_results = {
    'download': 0,
    'upload': 0,
    'ping': 0,
    'is_testing': False,
    'last_test': None,
    'error': None
}

def run_speedtest():
    """Fonction pour exécuter un test de vitesse"""
    try:
        speedtest_results['is_testing'] = True
        speedtest_results['error'] = None
        
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # Test de téléchargement
        speedtest_results['download'] = st.download() / 1_000_000  # Convertir en Mbps
        # Test de téléversement
        speedtest_results['upload'] = st.upload() / 1_000_000  # Convertir en Mbps
        # Ping
        speedtest_results['ping'] = st.results.ping
        
        speedtest_results['last_test'] = time.strftime('%H:%M:%S')
        
    except Exception as e:
        speedtest_results['error'] = str(e)
        print(f"Erreur lors du test de vitesse: {e}")
    finally:
        speedtest_results['is_testing'] = False

@app.route('/')
def home():
    # Template HTML simplifié pour Docker
    html_template = '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test de Débit Internet - Docker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .results {
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                flex-wrap: wrap;
            }
            .result-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                min-width: 200px;
                margin: 10px;
            }
            .download { border-left: 4px solid #4CAF50; }
            .upload { border-left: 4px solid #2196F3; }
            .ping { border-left: 4px solid #FF9800; }
            .value {
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }
            .button {
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                display: block;
                margin: 20px auto;
            }
            .button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .error {
                color: #f44336;
                text-align: center;
                margin: 20px 0;
            }
            .info {
                text-align: center;
                color: #666;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Test de Débit Internet</h1>
            <p style="text-align: center;">Version Docker</p>
            
            <div class="results">
                <div class="result-card download">
                    <h3>⬇️ Téléchargement</h3>
                    <div class="value">{{ "%.2f"|format(speedtest_results.download) }}</div>
                    <p>Mbps</p>
                </div>
                <div class="result-card upload">
                    <h3>⬆️ Téléversement</h3>
                    <div class="value">{{ "%.2f"|format(speedtest_results.upload) }}</div>
                    <p>Mbps</p>
                </div>
                <div class="result-card ping">
                    <h3>📡 Ping</h3>
                    <div class="value">{{ "%.0f"|format(speedtest_results.ping) }}</div>
                    <p>ms</p>
                </div>
            </div>
            
            {% if speedtest_results.error %}
            <div class="error">
                Erreur: {{ speedtest_results.error }}
            </div>
            {% endif %}
            
            <button class="button" onclick="startTest()" id="testBtn">
                {% if speedtest_results.is_testing %}
                ⏳ Test en cours...
                {% else %}
                🚀 Tester le débit
                {% endif %}
            </button>
            
            {% if speedtest_results.last_test %}
            <div class="info">
                Dernier test: {{ speedtest_results.last_test }}
            </div>
            {% endif %}
            
            <div class="info">
                Conteneur Docker | Port 5000
            </div>
        </div>
        
        <script>
            function startTest() {
                const btn = document.getElementById('testBtn');
                btn.disabled = true;
                btn.innerHTML = '⏳ Test en cours...';
                
                fetch('/start-test')
                    .then(response => response.json())
                    .then(data => {
                        // Attendre 3 secondes avant de recharger
                        setTimeout(() => {
                            location.reload();
                        }, 3000);
                    })
                    .catch(error => {
                        console.error('Erreur:', error);
                        btn.disabled = false;
                        btn.innerHTML = '🚀 Tester le débit';
                    });
            }
            
            // Recharger toutes les 60 secondes
            setTimeout(() => {
                location.reload();
            }, 60000);
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, speedtest_results=speedtest_results)

@app.route('/start-test')
def start_test():
    """Démarrer un test de vitesse dans un thread séparé"""
    if not speedtest_results['is_testing']:
        thread = threading.Thread(target=run_speedtest)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'Test démarré', 'message': 'Le test peut prendre 30-60 secondes'})
    return jsonify({'status': 'Un test est déjà en cours'})

@app.route('/health')
def health():
    """Endpoint de santé pour Docker/Kubernetes"""
    return jsonify({
        'status': 'healthy',
        'service': 'speedtest-web',
        'last_test': speedtest_results['last_test']
    })

if __name__ == '__main__':
    # Démarrer un test initial au lancement
    thread = threading.Thread(target=run_speedtest)
    thread.daemon = True
    thread.start()
    
    # Utiliser le port défini par l'environnement ou 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)