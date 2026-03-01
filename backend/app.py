from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
from datetime import datetime, timedelta
from utils.ga4_client import GA4Client
from utils.gsc_client import GSCClient
from utils.recommendations import RecommendationsEngine

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Configuration
app.config['CACHE_TIMEOUT'] = 300  # 5 minutes de cache

# Clients Google
ga4_client = GA4Client()
gsc_client = GSCClient()
recommendations_engine = RecommendationsEngine()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifie que l'API fonctionne"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Récupère les données Google Analytics 4"""
    try:
        # Paramètres optionnels
        days = request.args.get('days', 7, type=int)
        
        logger.info(f"Récupération des données GA4 pour les {days} derniers jours")
        
        # Récupération des données
        data = ga4_client.get_analytics_data(days=days)
        
        if not data:
            return jsonify({
                'error': 'Aucune donnée disponible',
                'message': 'Vérifiez que la propriété GA4 est correctement configurée'
            }), 404
        
        return jsonify({
            'success': True,
            'data': data,
            'period': f'{days} jours',
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données GA4: {str(e)}")
        return jsonify({
            'error': 'Erreur serveur',
            'message': str(e)
        }), 500

@app.route('/api/searchconsole', methods=['GET'])
def get_search_console():
    """Récupère les données Google Search Console"""
    try:
        # Paramètres optionnels
        days = request.args.get('days', 7, type=int)
        
        logger.info(f"Récupération des données GSC pour les {days} derniers jours")
        
        # Récupération des données
        data = gsc_client.get_search_console_data(days=days)
        
        if not data:
            return jsonify({
                'error': 'Aucune donnée disponible',
                'message': 'Vérifiez que la propriété GSC est correctement configurée'
            }), 404
        
        return jsonify({
            'success': True,
            'data': data,
            'period': f'{days} jours',
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données GSC: {str(e)}")
        return jsonify({
            'error': 'Erreur serveur',
            'message': str(e)
        }), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Génère des recommandations SEO basées sur les données"""
    try:
        # Récupération des données
        ga4_data = ga4_client.get_analytics_data(days=7)
        gsc_data = gsc_client.get_search_console_data(days=7)
        
        if not ga4_data and not gsc_data:
            return jsonify({
                'error': 'Données insuffisantes',
                'message': 'Impossible de générer des recommandations sans données'
            }), 404
        
        # Génération des recommandations
        recommendations = recommendations_engine.generate_recommendations(
            ga4_data=ga4_data,
            gsc_data=gsc_data
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'data_sources': {
                'ga4': bool(ga4_data),
                'gsc': bool(gsc_data)
            },
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération des recommandations: {str(e)}")
        return jsonify({
            'error': 'Erreur serveur',
            'message': str(e)
        }), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Récupère toutes les données pour le dashboard"""
    try:
        # Récupération parallèle des données
        ga4_data = ga4_client.get_analytics_data(days=7)
        gsc_data = gsc_client.get_search_console_data(days=7)
        recommendations = recommendations_engine.generate_recommendations(
            ga4_data=ga4_data,
            gsc_data=gsc_data
        )
        
        return jsonify({
            'success': True,
            'data': {
                'analytics': ga4_data,
                'search_console': gsc_data,
                'recommendations': recommendations
            },
            'period': '7 jours',
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données du dashboard: {str(e)}")
        return jsonify({
            'error': 'Erreur serveur',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
