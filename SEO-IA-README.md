# Dashboard SEO/IA pour Analytics & Search Console

## 🎯 Projet
Dashboard interactif collectant automatiquement les données depuis Google Analytics 4 et Google Search Console avec recommandations SEO personnalisées.

## 🌐 Déploiement
- **Backend** : Render (ou service similaire)
- **Frontend** : Vercel : https://seo-ia123.vercel.app
- **Google Analytics 4** : G-35RSYRP4HD

## 📁 Structure du projet
```
seo-ia-dashboard/
├── backend/
│   ├── app.py                 # Application Flask principale
│   ├── requirements.txt        # Dépendances Python
│   ├── .env.example          # Variables d'environnement
│   ├── utils/
│   │   ├── ga4_client.py     # Client Google Analytics 4
│   │   ├── gsc_client.py     # Client Google Search Console
│   │   └── recommendations.py # Générateur de recommandations
│   └── service-account.json  # Clé du compte de service (à créer)
├── frontend/
│   ├── index.html            # Page principale du dashboard
│   ├── style.css             # Styles CSS
│   └── script.js             # JavaScript avec Chart.js
└── README.md                 # Ce fichier
```

## 🚀 Installation rapide

### 1. Configuration Google Cloud
1. Créez un projet sur [Google Cloud Console](https://console.cloud.google.com/)
2. Activez les API :
   - Google Analytics Data API
   - Google Search Console API
3. Créez un compte de service
4. Téléchargez la clé JSON (placez-la dans `backend/service-account.json`)
5. Partagez le compte de service :
   - Dans GA4 : Ajoutez l'email comme "Lecteur"
   - Dans GSC : Ajoutez l'email comme "Utilisateur" avec permissions complètes

### 2. Configuration Backend
```bash
cd backend
cp .env.example .env
# Éditez .env avec vos identifiants
pip install -r requirements.txt
python app.py
```

### 3. Configuration Frontend
```bash
cd frontend
# Déployez sur Vercel ou utilisez un serveur local
python -m http.server 8000
```

## 🔗 Variables d'environnement (.env)
```env
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GA4_PROPERTY_ID=properties/123456789
GSC_SITE_URL=https://seo-ia123.vercel.app
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📊 Fonctionnalités

### API Routes
- `GET /api/analytics` - Données GA4 (visiteurs, pages vues, taux de rebond)
- `GET /api/searchconsole` - Données GSC (clics, impressions, CTR)
- `GET /api/recommendations` - Recommandations SEO personnalisées

### Dashboard
- KPI en temps réel
- Graphiques interactifs (Chart.js)
- Recommandations IA basées sur les données
- Design responsive

## 🎨 Recommandations IA
- Taux de rebond > 70% → Amélioration du contenu
- Position 4-10 avec CTR < 2% → Optimisation meta
- Impressions ↑ mais clics → Enrichissement contenu

## 🚀 Déploiement

### Backend sur Render
1. Connectez votre repo GitHub
2. Configurez les variables d'environnement
3. Déployez automatiquement

### Frontend sur Vercel
1. Importez le dossier frontend
2. Configurez l'URL de l'API backend
3. Déployez

## 📱 Utilisation
1. Accédez au dashboard
2. Visualisez les données en temps réel
3. Consultez les recommandations SEO
4. Suivez l'évolution des performances

## 🔧 Développement
- Backend : Flask + Python 3.9+
- Frontend : HTML5 + CSS3 + JavaScript ES6
- Graphiques : Chart.js
- API Google : google-analytics-data, google-searchconsole

## 📝 Notes
- Assurez-vous que les permissions sont correctes dans GA4 et GSC
- Les données mettent jusqu'à 24h à apparaître dans GA4
- Le cache backend est de 5 minutes pour éviter les appels excessifs
