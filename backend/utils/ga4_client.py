from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account
import os
import logging
from datetime import datetime, timedelta
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)

class GA4Client:
    """Client pour interagir avec Google Analytics 4 Data API"""
    
    def __init__(self):
        self.property_id = os.getenv('GA4_PROPERTY_ID')
        if not self.property_id:
            raise ValueError("GA4_PROPERTY_ID n'est pas défini dans les variables d'environnement")
        
        # Configuration du client
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError("Fichier de credentials Google non trouvé")
        
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
        
        self.client = BetaAnalyticsDataClient(credentials=self.credentials)
        
        # Cache de 5 minutes
        self.cache = TTLCache(maxsize=100, ttl=300)
    
    @cached(lambda self: self.cache)
    def get_analytics_data(self, days=7):
        """Récupère les données principales de GA4"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            logger.info(f"Récupération GA4 du {start_date} au {end_date}")
            
            # Requête principale pour les KPI
            request = RunReportRequest(
                property=f"properties/{self.property_id.split('/')[-1]}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                dimensions=[
                    Dimension(name="date"),
                    Dimension(name="pagePath"),
                    Dimension(name="sessionSource")
                ],
                metrics=[
                    Metric(name="activeUsers"),
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="bounceRate"),
                    Metric(name="engagementRate")
                ],
                limit=10000
            )
            
            response = self.client.run_report(request)
            
            # Traitement des données
            data = self._process_report_response(response)
            
            # Ajout des données agrégées
            aggregated = self._get_aggregated_metrics(data)
            
            return {
                'kpi': aggregated,
                'daily_data': self._get_daily_trends(data),
                'top_pages': self._get_top_pages(data),
                'traffic_sources': self._get_traffic_sources(data),
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'days': days
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur GA4: {str(e)}")
            return None
    
    def _process_report_response(self, response):
        """Traite la réponse de l'API GA4"""
        rows = []
        for row in response.rows:
            row_data = {}
            for i, dimension_value in enumerate(row.dimension_values):
                dimension_name = response.dimensions[i].name
                row_data[dimension_name] = dimension_value.value
            
            for i, metric_value in enumerate(row.metric_values):
                metric_name = response.metrics[i].name
                row_data[metric_name] = float(metric_value.value)
            
            rows.append(row_data)
        
        return rows
    
    def _get_aggregated_metrics(self, data):
        """Calcule les métriques agrégées"""
        if not data:
            return {}
        
        total_users = sum(row.get('activeUsers', 0) for row in data)
        total_sessions = sum(row.get('sessions', 0) for row in data)
        total_pageviews = sum(row.get('screenPageViews', 0) for row in data)
        
        # Calcul du taux de rebond moyen
        bounce_rates = [row.get('bounceRate', 0) for row in data if row.get('bounceRate')]
        avg_bounce_rate = sum(bounce_rates) / len(bounce_rates) if bounce_rates else 0
        
        # Calcul du taux d'engagement moyen
        engagement_rates = [row.get('engagementRate', 0) for row in data if row.get('engagementRate')]
        avg_engagement_rate = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        
        return {
            'total_users': int(total_users),
            'total_sessions': int(total_sessions),
            'total_pageviews': int(total_pageviews),
            'avg_bounce_rate': round(avg_bounce_rate, 2),
            'avg_engagement_rate': round(avg_engagement_rate, 2),
            'pages_per_session': round(total_pageviews / total_sessions, 2) if total_sessions > 0 else 0
        }
    
    def _get_daily_trends(self, data):
        """Extrait les tendances quotidiennes"""
        if not data:
            return []
        
        daily_data = {}
        for row in data:
            date = row.get('date', '')
            if date:
                if date not in daily_data:
                    daily_data[date] = {
                        'date': date,
                        'users': 0,
                        'sessions': 0,
                        'pageviews': 0
                    }
                
                daily_data[date]['users'] += row.get('activeUsers', 0)
                daily_data[date]['sessions'] += row.get('sessions', 0)
                daily_data[date]['pageviews'] += row.get('screenPageViews', 0)
        
        return sorted(daily_data.values(), key=lambda x: x['date'])
    
    def _get_top_pages(self, data):
        """Extrait les pages les plus consultées"""
        if not data:
            return []
        
        page_data = {}
        for row in data:
            page = row.get('pagePath', '')
            if page:
                if page not in page_data:
                    page_data[page] = {
                        'page': page,
                        'pageviews': 0,
                        'users': 0,
                        'bounce_rate': 0
                    }
                
                page_data[page]['pageviews'] += row.get('screenPageViews', 0)
                page_data[page]['users'] += row.get('activeUsers', 0)
                page_data[page]['bounce_rate'] = max(page_data[page]['bounce_rate'], row.get('bounceRate', 0))
        
        # Top 10 pages
        return sorted(page_data.values(), key=lambda x: x['pageviews'], reverse=True)[:10]
    
    def _get_traffic_sources(self, data):
        """Extrait les sources de trafic"""
        if not data:
            return []
        
        source_data = {}
        for row in data:
            source = row.get('sessionSource', 'direct')
            if source:
                if source not in source_data:
                    source_data[source] = {
                        'source': source,
                        'sessions': 0,
                        'users': 0
                    }
                
                source_data[source]['sessions'] += row.get('sessions', 0)
                source_data[source]['users'] += row.get('activeUsers', 0)
        
        # Top 10 sources
        return sorted(source_data.values(), key=lambda x: x['sessions'], reverse=True)[:10]
