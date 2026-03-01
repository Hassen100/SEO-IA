import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RecommendationsEngine:
    """Moteur de recommandations SEO basé sur les données analytics"""
    
    def __init__(self):
        self.rules = {
            'high_bounce_rate': self._check_high_bounce_rate,
            'low_ctr_good_position': self._check_low_ctr_good_position,
            'high_impressions_low_clicks': self._check_high_impressions_low_clicks,
            'low_engagement': self._check_low_engagement,
            'traffic_opportunities': self._check_traffic_opportunities
        }
    
    def generate_recommendations(self, ga4_data=None, gsc_data=None):
        """Génère des recommandations basées sur les données disponibles"""
        recommendations = []
        
        if ga4_data:
            recommendations.extend(self._analyze_ga4_data(ga4_data))
        
        if gsc_data:
            recommendations.extend(self._analyze_gsc_data(gsc_data))
        
        if ga4_data and gsc_data:
            recommendations.extend(self._analyze_combined_data(ga4_data, gsc_data))
        
        # Trier par priorité
        recommendations.sort(key=lambda x: x.get('priority', 3))
        
        return {
            'total_recommendations': len(recommendations),
            'high_priority': len([r for r in recommendations if r.get('priority') == 1]),
            'medium_priority': len([r for r in recommendations if r.get('priority') == 2]),
            'low_priority': len([r for r in recommendations if r.get('priority') == 3]),
            'recommendations': recommendations[:20]  # Top 20 recommandations
        }
    
    def _analyze_ga4_data(self, data):
        """Analyse les données GA4 pour générer des recommandations"""
        recommendations = []
        
        if not data:
            return recommendations
        
        kpi = data.get('kpi', {})
        top_pages = data.get('top_pages', [])
        
        # Règle 1: Taux de rebond élevé
        if kpi.get('avg_bounce_rate', 0) > 70:
            recommendations.append({
                'type': 'high_bounce_rate',
                'title': 'Taux de rebond élevé détecté',
                'description': f'Le taux de rebond moyen est de {kpi.get("avg_bounce_rate", 0):.1f}%, ce qui est au-dessus du seuil recommandé de 70%.',
                'recommendation': 'Améliorez la pertinence du contenu, optimisez la vitesse de chargement et assurez-vous que les pages répondent aux attentes des visiteurs.',
                'priority': 1,
                'impact': 'high',
                'effort': 'medium',
                'data': {
                    'bounce_rate': kpi.get('avg_bounce_rate', 0),
                    'threshold': 70
                }
            })
        
        # Règle 2: Pages spécifiques avec taux de rebond élevé
        high_bounce_pages = [page for page in top_pages if page.get('bounce_rate', 0) > 80]
        if high_bounce_pages:
            for page in high_bounce_pages[:3]:  # Top 3 pages problématiques
                recommendations.append({
                    'type': 'page_high_bounce_rate',
                    'title': f'Page avec taux de rebond élevé: {page.get("page", "")}',
                    'description': f'La page {page.get("page", "")} a un taux de rebond de {page.get("bounce_rate", 0):.1f}% avec {page.get("pageviews", 0)} pages vues.',
                    'recommendation': 'Révisez le contenu de cette page, ajoutez des appels à l\'action clairs et améliorez l\'expérience utilisateur.',
                    'priority': 1,
                    'impact': 'high',
                    'effort': 'medium',
                    'data': {
                        'page': page.get('page', ''),
                        'bounce_rate': page.get('bounce_rate', 0),
                        'pageviews': page.get('pageviews', 0)
                    }
                })
        
        # Règle 3: Faible engagement
        if kpi.get('avg_engagement_rate', 0) < 50:
            recommendations.append({
                'type': 'low_engagement',
                'title': 'Taux d\'engagement faible',
                'description': f'Le taux d\'engagement moyen est de {kpi.get("avg_engagement_rate", 0):.1f}%, ce qui est en dessous du seuil recommandé de 50%.',
                'recommendation': 'Enrichissez le contenu avec des éléments interactifs, des vidéos et des liens internes pertinents.',
                'priority': 2,
                'impact': 'medium',
                'effort': 'medium',
                'data': {
                    'engagement_rate': kpi.get('avg_engagement_rate', 0),
                    'threshold': 50
                }
            })
        
        return recommendations
    
    def _analyze_gsc_data(self, data):
        """Analyse les données Search Console pour générer des recommandations"""
        recommendations = []
        
        if not data:
            return recommendations
        
        kpi = data.get('kpi', {})
        top_queries = data.get('top_queries', [])
        page_performance = data.get('page_performance', {})
        
        # Règle 1: CTR global faible
        if kpi.get('avg_ctr', 0) < 2:
            recommendations.append({
                'type': 'low_global_ctr',
                'title': 'CTR global faible',
                'description': f'Le CTR moyen est de {kpi.get("avg_ctr", 0):.1f}%, ce qui est en dessous de la moyenne recommandée de 2%.',
                'recommendation': 'Optimisez les titres et meta descriptions pour les rendre plus attractifs dans les résultats de recherche.',
                'priority': 1,
                'impact': 'high',
                'effort': 'low',
                'data': {
                    'ctr': kpi.get('avg_ctr', 0),
                    'threshold': 2
                }
            })
        
        # Règle 2: Position moyenne faible
        if kpi.get('avg_position', 0) > 15:
            recommendations.append({
                'type': 'low_avg_position',
                'title': 'Position moyenne faible',
                'description': f'La position moyenne est de {kpi.get("avg_position", 0):.1f}, ce qui indique une visibilité limitée.',
                'recommendation': 'Travaillez sur le SEO on-page, créez du contenu de qualité et obtenez des backlinks pertinents.',
                'priority': 1,
                'impact': 'high',
                'effort': 'high',
                'data': {
                    'position': kpi.get('avg_position', 0),
                    'threshold': 15
                }
            })
        
        # Règle 3: Requêtes avec bon positionnement mais CTR faible
        low_ctr_queries = [q for q in top_queries if 4 <= q.get('position', 0) <= 10 and q.get('ctr', 0) < 2]
        if low_ctr_queries:
            for query in low_ctr_queries[:3]:  # Top 3 requêtes problématiques
                recommendations.append({
                    'type': 'low_ctr_good_position',
                    'title': f'CTR faible pour la requête: "{query.get("query", "")}"',
                    'description': f'La requête "{query.get("query", "")}" est en position {query.get("position", 0):.1f} mais n\'a qu\'un CTR de {query.get("ctr", 0):.1f}%.',
                    'recommendation': 'Optimisez le titre et la meta description de la page concernée pour augmenter le CTR.',
                    'priority': 1,
                    'impact': 'high',
                    'effort': 'low',
                    'data': {
                        'query': query.get('query', ''),
                        'position': query.get('position', 0),
                        'ctr': query.get('ctr', 0),
                        'impressions': query.get('impressions', 0)
                    }
                })
        
        # Règle 4: Opportunités d'amélioration
        opportunities = page_performance.get('improvement_opportunities', [])
        if opportunities:
            for opp in opportunities[:3]:  # Top 3 opportunités
                recommendations.append({
                    'type': 'improvement_opportunity',
                    'title': f'Opportunité d\'amélioration: {opp.get("page", "")}',
                    'description': f'La page {opp.get("page", "")} a {opp.get("impressions", 0)} impressions mais seulement {opp.get("ctr", 0):.1f}% de CTR. {opp.get("issue", "")}',
                    'recommendation': 'Optimisez le contenu, les balises title et meta description pour améliorer la performance.',
                    'priority': 2,
                    'impact': 'medium',
                    'effort': 'medium',
                    'data': opp
                })
        
        return recommendations
    
    def _analyze_combined_data(self, ga4_data, gsc_data):
        """Analyse combinée des données GA4 et GSC"""
        recommendations = []
        
        # Pages avec fort trafic organique mais faible engagement
        ga4_pages = {page.get('page'): page for page in ga4_data.get('top_pages', [])}
        gsc_pages = {page.get('page'): page for page in gsc_data.get('top_pages', [])}
        
        for page_url, gsc_page in gsc_pages.items():
            if page_url in ga4_pages:
                ga4_page = ga4_pages[page_url]
                
                # Page avec beaucoup de trafic organique mais fort taux de rebond
                if (gsc_page.get('clicks', 0) > 50 and 
                    ga4_page.get('bounce_rate', 0) > 75):
                    
                    recommendations.append({
                        'type': 'organic_traffic_high_bounce',
                        'title': f'Trafic organique élevé mais rebond important: {page_url}',
                        'description': f'La page reçoit {gsc_page.get("clicks", 0)} clics organiques mais a un taux de rebond de {ga4_page.get("bounce_rate", 0):.1f}%.',
                        'recommendation': 'Le contenu attire les visiteurs mais ne les retient pas. Améliorez la pertinence et l\'expérience utilisateur.',
                        'priority': 1,
                        'impact': 'high',
                        'effort': 'medium',
                        'data': {
                            'page': page_url,
                            'organic_clicks': gsc_page.get('clicks', 0),
                            'bounce_rate': ga4_page.get('bounce_rate', 0)
                        }
                    })
        
        return recommendations
    
    def _check_high_bounce_rate(self, data):
        """Vérifie le taux de rebond élevé"""
        pass  # Implémenté dans _analyze_ga4_data
    
    def _check_low_ctr_good_position(self, data):
        """Vérifie les requêtes avec bon positionnement mais CTR faible"""
        pass  # Implémenté dans _analyze_gsc_data
    
    def _check_high_impressions_low_clicks(self, data):
        """Vérifie les pages avec beaucoup d'impressions mais peu de clics"""
        pass  # Implémenté dans _analyze_gsc_data
    
    def _check_low_engagement(self, data):
        """Vérifie le faible engagement"""
        pass  # Implémenté dans _analyze_ga4_data
    
    def _check_traffic_opportunities(self, data):
        """Vérifie les opportunités de trafic"""
        pass  # Implémenté dans _analyze_gsc_data
