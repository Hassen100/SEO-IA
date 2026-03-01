from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import os
import logging
from datetime import datetime, timedelta
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)

class GSCClient:
    """Client pour interagir avec Google Search Console API"""
    
    def __init__(self):
        self.site_url = os.getenv('GSC_SITE_URL')
        if not self.site_url:
            raise ValueError("GSC_SITE_URL n'est pas défini dans les variables d'environnement")
        
        # Configuration du client
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError("Fichier de credentials Google non trouvé")
        
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
        
        self.service = build('searchconsole', 'v1', credentials=self.credentials)
        
        # Cache de 5 minutes
        self.cache = TTLCache(maxsize=100, ttl=300)
    
    @cached(lambda self: self.cache)
    def get_search_console_data(self, days=7):
        """Récupère les données principales de Search Console"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            logger.info(f"Récupération GSC du {start_date} au {end_date}")
            
            # Requêtes principales
            queries_data = self._get_queries_data(start_date, end_date)
            pages_data = self._get_pages_data(start_date, end_date)
            
            # Données agrégées
            aggregated = self._get_aggregated_metrics(queries_data + pages_data)
            
            return {
                'kpi': aggregated,
                'top_queries': self._get_top_queries(queries_data),
                'top_pages': self._get_top_pages(pages_data),
                'query_performance': self._get_query_performance(queries_data),
                'page_performance': self._get_page_performance(pages_data),
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'days': days
                }
            }
            
        except HttpError as e:
            logger.error(f"Erreur HTTP GSC: {str(e)}")
            if e.resp.status == 403:
                logger.error("Permissions insuffisantes pour Search Console")
            return None
        except Exception as e:
            logger.error(f"Erreur GSC: {str(e)}")
            return None
    
    def _get_queries_data(self, start_date, end_date):
        """Récupère les données des requêtes"""
        try:
            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['query'],
                'rowLimit': 1000
            }
            
            response = self.service.searchanalytics().query(
                siteUrl=self.site_url,
                body=request
            ).execute()
            
            return response.get('rows', [])
            
        except Exception as e:
            logger.error(f"Erreur requêtes GSC: {str(e)}")
            return []
    
    def _get_pages_data(self, start_date, end_date):
        """Récupère les données des pages"""
        try:
            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['page'],
                'rowLimit': 1000
            }
            
            response = self.service.searchanalytics().query(
                siteUrl=self.site_url,
                body=request
            ).execute()
            
            return response.get('rows', [])
            
        except Exception as e:
            logger.error(f"Erreur pages GSC: {str(e)}")
            return []
    
    def _get_aggregated_metrics(self, data):
        """Calcule les métriques agrégées"""
        if not data:
            return {}
        
        total_clicks = sum(row.get('clicks', 0) for row in data)
        total_impressions = sum(row.get('impressions', 0) for row in data)
        
        # Calcul CTR moyen
        total_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        
        # Calcul position moyenne
        positions = [row.get('position', 0) for row in data if row.get('position')]
        avg_position = sum(positions) / len(positions) if positions else 0
        
        return {
            'total_clicks': int(total_clicks),
            'total_impressions': int(total_impressions),
            'avg_ctr': round(total_ctr, 2),
            'avg_position': round(avg_position, 2)
        }
    
    def _get_top_queries(self, data):
        """Extrait les requêtes les plus performantes"""
        if not data:
            return []
        
        top_queries = []
        for row in sorted(data, key=lambda x: x.get('clicks', 0), reverse=True)[:20]:
            top_queries.append({
                'query': row.get('keys', [''])[0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': round(row.get('clicks', 0) / row.get('impressions', 1) * 100, 2),
                'position': round(row.get('position', 0), 2)
            })
        
        return top_queries
    
    def _get_top_pages(self, data):
        """Extrait les pages les plus performantes"""
        if not data:
            return []
        
        top_pages = []
        for row in sorted(data, key=lambda x: x.get('clicks', 0), reverse=True)[:20]:
            top_pages.append({
                'page': row.get('keys', [''])[0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': round(row.get('clicks', 0) / row.get('impressions', 1) * 100, 2),
                'position': round(row.get('position', 0), 2)
            })
        
        return top_pages
    
    def _get_query_performance(self, data):
        """Analyse la performance des requêtes par position"""
        if not data:
            return {}
        
        performance_by_position = {
            'top_3': {'clicks': 0, 'impressions': 0, 'queries': 0},
            'top_10': {'clicks': 0, 'impressions': 0, 'queries': 0},
            'top_20': {'clicks': 0, 'impressions': 0, 'queries': 0}
        }
        
        for row in data:
            position = row.get('position', 0)
            clicks = row.get('clicks', 0)
            impressions = row.get('impressions', 0)
            
            if position <= 3:
                performance_by_position['top_3']['clicks'] += clicks
                performance_by_position['top_3']['impressions'] += impressions
                performance_by_position['top_3']['queries'] += 1
            elif position <= 10:
                performance_by_position['top_10']['clicks'] += clicks
                performance_by_position['top_10']['impressions'] += impressions
                performance_by_position['top_10']['queries'] += 1
            elif position <= 20:
                performance_by_position['top_20']['clicks'] += clicks
                performance_by_position['top_20']['impressions'] += impressions
                performance_by_position['top_20']['queries'] += 1
        
        # Calcul des CTR
        for pos_data in performance_by_position.values():
            if pos_data['impressions'] > 0:
                pos_data['ctr'] = round(pos_data['clicks'] / pos_data['impressions'] * 100, 2)
            else:
                pos_data['ctr'] = 0
        
        return performance_by_position
    
    def _get_page_performance(self, data):
        """Analyse la performance des pages"""
        if not data:
            return {}
        
        # Pages avec fort potentiel d'amélioration
        improvement_opportunities = []
        
        for row in data:
            position = row.get('position', 0)
            ctr = row.get('clicks', 0) / row.get('impressions', 1) * 100
            impressions = row.get('impressions', 0)
            
            # Pages en position 4-10 avec CTR faible
            if 4 <= position <= 10 and ctr < 2 and impressions > 50:
                improvement_opportunities.append({
                    'page': row.get('keys', [''])[0],
                    'position': position,
                    'ctr': round(ctr, 2),
                    'impressions': impressions,
                    'issue': 'CTR faible malgré bonne position'
                })
            # Pages avec beaucoup d'impressions mais peu de clics
            elif impressions > 100 and ctr < 1:
                improvement_opportunities.append({
                    'page': row.get('keys', [''])[0],
                    'position': position,
                    'ctr': round(ctr, 2),
                    'impressions': impressions,
                    'issue': 'Beaucoup d\'impressions mais peu de clics'
                })
        
        return {
            'improvement_opportunities': sorted(improvement_opportunities, 
                                               key=lambda x: x['impressions'], reverse=True)[:10]
        }
