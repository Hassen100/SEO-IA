// Configuration
const API_BASE_URL = 'http://localhost:5000/api'; // À modifier pour le déploiement

// Variables globales
let dashboardData = null;
let charts = {};

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadDashboardData();
});

// Initialisation des écouteurs d'événements
function initializeEventListeners() {
    // Bouton d'actualisation
    document.getElementById('refresh-btn').addEventListener('click', function() {
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Actualisation...';
        loadDashboardData().finally(() => {
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-sync-alt"></i> Actualiser';
        });
    });

    // Sélecteur de période
    document.getElementById('period-select').addEventListener('change', function() {
        loadDashboardData();
    });

    // Boutons des graphiques
    document.querySelectorAll('.chart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const chartType = this.dataset.chart;
            const metric = this.dataset.metric;
            
            // Mettre à jour les boutons actifs
            document.querySelectorAll(`[data-chart="${chartType}"]`).forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            // Mettre à jour le graphique
            updateChart(chartType, metric);
        });
    });
}

// Chargement des données du dashboard
async function loadDashboardData() {
    showLoading();
    hideError();
    
    try {
        const period = document.getElementById('period-select').value;
        
        // Récupération des données
        const [analyticsResponse, searchConsoleResponse, recommendationsResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/analytics?days=${period}`),
            fetch(`${API_BASE_URL}/searchconsole?days=${period}`),
            fetch(`${API_BASE_URL}/recommendations`)
        ]);
        
        const analytics = await analyticsResponse.json();
        const searchConsole = await searchConsoleResponse.json();
        const recommendations = await recommendationsResponse.json();
        
        if (analytics.success && searchConsole.success && recommendations.success) {
            dashboardData = {
                analytics: analytics.data,
                searchConsole: searchConsole.data,
                recommendations: recommendations.data
            };
            
            updateDashboard();
            hideLoading();
        } else {
            throw new Error('Erreur dans les données reçues');
        }
        
    } catch (error) {
        console.error('Erreur de chargement:', error);
        showError('Impossible de charger les données. Veuillez vérifier que le backend est en cours d\'exécution.');
        hideLoading();
    }
}

// Mise à jour du dashboard
function updateDashboard() {
    if (!dashboardData) return;
    
    updateKPIs();
    updateCharts();
    updateRecommendations();
    updateTables();
    
    // Afficher le contenu
    document.getElementById('dashboard-content').style.display = 'block';
}

// Mise à jour des KPIs
function updateKPIs() {
    const analytics = dashboardData.analytics;
    const searchConsole = dashboardData.searchConsole;
    
    // KPIs GA4
    if (analytics && analytics.kpi) {
        const kpi = analytics.kpi;
        
        document.getElementById('total-users').textContent = formatNumber(kpi.total_users);
        document.getElementById('total-pageviews').textContent = formatNumber(kpi.total_pageviews);
        document.getElementById('bounce-rate').textContent = formatPercentage(kpi.avg_bounce_rate);
        document.getElementById('engagement-rate').textContent = formatPercentage(kpi.avg_engagement_rate);
        
        // Ajouter des indicateurs de changement (simulés pour l'instant)
        updateKPIChange('users-change', 5.2, true);
        updateKPIChange('pageviews-change', 3.8, true);
        updateKPIChange('bounce-change', -2.1, false);
        updateKPIChange('engagement-change', 4.5, true);
    }
    
    // KPIs Search Console
    if (searchConsole && searchConsole.kpi) {
        const kpi = searchConsole.kpi;
        
        document.getElementById('total-clicks').textContent = formatNumber(kpi.total_clicks);
        document.getElementById('total-impressions').textContent = formatNumber(kpi.total_impressions);
        document.getElementById('avg-ctr').textContent = formatPercentage(kpi.avg_ctr);
        document.getElementById('avg-position').textContent = kpi.avg_position.toFixed(1);
        
        // Ajouter des indicateurs de changement
        updateKPIChange('clicks-change', 8.3, true);
        updateKPIChange('impressions-change', 6.7, true);
        updateKPIChange('ctr-change', 1.2, true);
        updateKPIChange('position-change', -3.4, false);
    }
}

// Mise à jour des indicateurs de changement
function updateKPIChange(elementId, change, isPositive) {
    const element = document.getElementById(elementId);
    const icon = isPositive ? '↑' : '↓';
    const className = isPositive ? 'positive' : 'negative';
    
    element.innerHTML = `${icon} ${Math.abs(change)}%`;
    element.className = `kpi-change ${className}`;
}

// Mise à jour des graphiques
function updateCharts() {
    updateTrafficChart();
    updatePagesChart();
    updateSourcesChart();
    updateQueriesChart();
}

// Graphique d'évolution du trafic
function updateTrafficChart() {
    const ctx = document.getElementById('traffic-chart').getContext('2d');
    
    if (charts.traffic) {
        charts.traffic.destroy();
    }
    
    const dailyData = dashboardData.analytics?.daily_data || [];
    
    charts.traffic = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dailyData.map(d => formatDate(d.date)),
            datasets: [{
                label: 'Visiteurs',
                data: dailyData.map(d => d.users),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Pages Vues',
                data: dailyData.map(d => d.pageviews),
                borderColor: '#764ba2',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                tension: 0.4,
                fill: true,
                hidden: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Graphique des pages les plus consultées
function updatePagesChart() {
    const ctx = document.getElementById('pages-chart').getContext('2d');
    
    if (charts.pages) {
        charts.pages.destroy();
    }
    
    const topPages = dashboardData.analytics?.top_pages || [];
    const topPagesGSC = dashboardData.searchConsole?.top_pages || [];
    
    // Utiliser les données GA4 par défaut
    const pages = topPages.slice(0, 10);
    
    charts.pages = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: pages.map(p => truncateText(p.page, 30)),
            datasets: [{
                label: 'Pages Vues',
                data: pages.map(p => p.pageviews),
                backgroundColor: '#667eea',
                borderColor: '#667eea',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Graphique des sources de trafic
function updateSourcesChart() {
    const ctx = document.getElementById('sources-chart').getContext('2d');
    
    if (charts.sources) {
        charts.sources.destroy();
    }
    
    const sources = dashboardData.analytics?.traffic_sources || [];
    
    charts.sources = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: sources.map(s => s.source),
            datasets: [{
                data: sources.map(s => s.sessions),
                backgroundColor: [
                    '#667eea',
                    '#764ba2',
                    '#28a745',
                    '#ffc107',
                    '#dc3545',
                    '#17a2b8'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Graphique des mots-clés
function updateQueriesChart() {
    const ctx = document.getElementById('queries-chart').getContext('2d');
    
    if (charts.queries) {
        charts.queries.destroy();
    }
    
    const topQueries = dashboardData.searchConsole?.top_queries || [];
    const queries = topQueries.slice(0, 10);
    
    charts.queries = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: queries.map(q => truncateText(q.query, 25)),
            datasets: [{
                label: 'Clics',
                data: queries.map(q => q.clicks),
                backgroundColor: '#667eea',
                borderColor: '#667eea',
                borderWidth: 1
            }, {
                label: 'Impressions',
                data: queries.map(q => q.impressions),
                backgroundColor: '#764ba2',
                borderColor: '#764ba2',
                borderWidth: 1,
                hidden: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Mise à jour des graphiques (changement de métrique)
function updateChart(chartType, metric) {
    switch (chartType) {
        case 'traffic':
            updateTrafficChartMetric(metric);
            break;
        case 'pages':
            updatePagesChartSource(metric);
            break;
        case 'queries':
            updateQueriesChartMetric(metric);
            break;
    }
}

// Mise à jour du graphique de trafic par métrique
function updateTrafficChartMetric(metric) {
    const dailyData = dashboardData.analytics?.daily_data || [];
    const chart = charts.traffic;
    
    if (metric === 'users') {
        chart.data.datasets[0].hidden = false;
        chart.data.datasets[1].hidden = true;
    } else {
        chart.data.datasets[0].hidden = true;
        chart.data.datasets[1].hidden = false;
    }
    
    chart.update();
}

// Mise à jour du graphique des pages par source
function updatePagesChartSource(source) {
    const ctx = document.getElementById('pages-chart').getContext('2d');
    
    if (charts.pages) {
        charts.pages.destroy();
    }
    
    let pages = [];
    
    if (source === 'gsc') {
        pages = dashboardData.searchConsole?.top_pages || [];
    } else {
        pages = dashboardData.analytics?.top_pages || [];
    }
    
    pages = pages.slice(0, 10);
    
    charts.pages = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: pages.map(p => truncateText(p.page || p.page, 30)),
            datasets: [{
                label: source === 'gsc' ? 'Clics' : 'Pages Vues',
                data: pages.map(p => p.clicks || p.pageviews),
                backgroundColor: source === 'gsc' ? '#28a745' : '#667eea',
                borderColor: source === 'gsc' ? '#28a745' : '#667eea',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Mise à jour du graphique des requêtes par métrique
function updateQueriesChartMetric(metric) {
    const chart = charts.queries;
    
    if (metric === 'clicks') {
        chart.data.datasets[0].hidden = false;
        chart.data.datasets[1].hidden = true;
    } else {
        chart.data.datasets[0].hidden = true;
        chart.data.datasets[1].hidden = false;
    }
    
    chart.update();
}

// Mise à jour des recommandations
function updateRecommendations() {
    const recommendations = dashboardData.recommendations?.recommendations || [];
    const container = document.getElementById('recommendations-list');
    const countElement = document.getElementById('recommendations-count');
    
    countElement.textContent = recommendations.length;
    
    container.innerHTML = '';
    
    recommendations.forEach(rec => {
        const item = createRecommendationItem(rec);
        container.appendChild(item);
    });
}

// Création d'un élément de recommandation
function createRecommendationItem(recommendation) {
    const div = document.createElement('div');
    div.className = `recommendation-item ${recommendation.priority}-priority`;
    
    const priorityClass = recommendation.priority === 1 ? 'high' : 
                         recommendation.priority === 2 ? 'medium' : 'low';
    
    div.innerHTML = `
        <div class="recommendation-title">${recommendation.title}</div>
        <div class="recommendation-description">${recommendation.description}</div>
        <div class="recommendation-action">${recommendation.recommendation}</div>
        <div class="recommendation-meta">
            <span class="priority-badge ${priorityClass}">Priorité ${recommendation.priority}</span>
            <span>Impact: ${recommendation.impact}</span>
            <span>Effort: ${recommendation.effort}</span>
        </div>
    `;
    
    return div;
}

// Mise à jour des tableaux
function updateTables() {
    updatePagesTable();
    updateQueriesTable();
}

// Mise à jour du tableau des pages
function updatePagesTable() {
    const tbody = document.getElementById('pages-table-body');
    const pages = dashboardData.analytics?.top_pages || [];
    
    tbody.innerHTML = '';
    
    pages.slice(0, 10).forEach(page => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${truncateText(page.page, 40)}</td>
            <td>${formatNumber(page.pageviews)}</td>
            <td>${formatNumber(page.users)}</td>
            <td>${formatPercentage(page.bounce_rate)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Mise à jour du tableau des requêtes
function updateQueriesTable() {
    const tbody = document.getElementById('queries-table-body');
    const queries = dashboardData.searchConsole?.top_queries || [];
    
    tbody.innerHTML = '';
    
    queries.slice(0, 10).forEach(query => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${truncateText(query.query, 30)}</td>
            <td>${formatNumber(query.clicks)}</td>
            <td>${formatNumber(query.impressions)}</td>
            <td>${formatPercentage(query.ctr)}</td>
            <td>${query.position.toFixed(1)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Fonctions utilitaires
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatPercentage(num) {
    return num.toFixed(1) + '%';
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', { day: 'short', month: 'short' });
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Gestion des états de chargement
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('dashboard-content').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    const messageElement = document.getElementById('error-message');
    
    messageElement.textContent = message;
    errorDiv.style.display = 'block';
    document.getElementById('dashboard-content').style.display = 'none';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

// Export des données
function exportData(type) {
    let data = [];
    let filename = '';
    let headers = [];
    
    switch (type) {
        case 'pages':
            data = dashboardData.analytics?.top_pages || [];
            filename = 'pages-analytics';
            headers = ['Page', 'Pages Vues', 'Visiteurs', 'Taux de Rebond'];
            break;
        case 'queries':
            data = dashboardData.searchConsole?.top_queries || [];
            filename = 'queries-search-console';
            headers = ['Requête', 'Clics', 'Impressions', 'CTR', 'Position'];
            break;
    }
    
    // Création du CSV
    let csv = headers.join(',') + '\n';
    
    data.forEach(item => {
        if (type === 'pages') {
            csv += `"${item.page}",${item.pageviews},${item.users},${item.bounce_rate}\n`;
        } else {
            csv += `"${item.query}",${item.clicks},${item.impressions},${item.ctr},${item.position}\n`;
        }
    });
    
    // Téléchargement
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename}-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Auto-rafraîchissement (optionnel)
setInterval(() => {
    if (document.visibilityState === 'visible') {
        loadDashboardData();
    }
}, 5 * 60 * 1000); // 5 minutes
