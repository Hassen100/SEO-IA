# Installation et Déploiement du Dashboard SEO/IA

## 🚀 Installation rapide

### 1. Prérequis
- Python 3.9+
- Node.js 16+ (optionnel pour le frontend)
- Compte Google Cloud avec accès à Analytics et Search Console

### 2. Configuration Google Cloud

#### a) Créer un projet Google Cloud
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet (ex: "seo-ia-dashboard")

#### b) Activer les API requises
Dans votre projet, activez les API suivantes :
- Google Analytics Data API
- Google Search Console API

#### c) Créer un compte de service
1. IAM & Admin > Comptes de service
2. Créez un compte de service
3. Téléchargez la clé JSON
4. Renommez le fichier en `service-account.json` et placez-le dans `backend/`

#### d) Configurer les permissions
1. **Google Analytics 4** :
   - Allez dans votre propriété GA4
   - Administration > Gestion des accès
   - Ajoutez l'email du compte de service comme "Lecteur"

2. **Google Search Console** :
   - Allez dans votre propriété GSC
   - Paramètres > Utilisateurs et permissions
   - Ajoutez l'email du compte de service comme "Utilisateur" avec permissions complètes

### 3. Configuration Backend

```bash
cd backend

# Installation des dépendances
pip install -r requirements.txt

# Configuration des variables d'environnement
cp .env.example .env
# Éditez .env avec vos identifiants :
# GA4_PROPERTY_ID=properties/35RSYRP4HD
# GSC_SITE_URL=https://seo-ia123.vercel.app
# GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# Lancement du serveur
python app.py
```

Le backend sera disponible sur http://localhost:5000

### 4. Configuration Frontend

```bash
cd frontend

# Option 1: Serveur local simple
python -m http.server 8000

# Option 2: Serveur Node.js (si installé)
npx serve .

# Option 3: Déploiement direct sur Vercel
# Importez le dossier frontend sur Vercel
```

Le frontend sera disponible sur http://localhost:8000

## 🌐 Déploiement en production

### Backend sur Render

1. **Créez un repo GitHub** avec votre code
2. **Connectez Render** à votre repo GitHub
3. **Configurez le service Web** :
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment Variables: ajoutez toutes les variables de .env
4. **Déployez** automatiquement

### Frontend sur Vercel

1. **Importez le dossier frontend** sur Vercel
2. **Configurez les variables d'environnement** si nécessaire
3. **Modifiez l'URL de l'API** dans `script.js` :
   ```javascript
   const API_BASE_URL = 'https://votre-backend.onrender.com/api';
   ```
4. **Déployez** automatiquement

## 🔗 Configuration requise

### Variables d'environnement (.env)

```env
# Chemin vers la clé du compte de service
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# ID de la propriété Google Analytics 4
GA4_PROPERTY_ID=properties/35RSYRP4HD

# URL du site dans Search Console
GSC_SITE_URL=https://seo-ia123.vercel.app

# Configuration Flask
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000

# Cache
CACHE_TIMEOUT=300
```

### ID de propriété GA4

Pour trouver votre GA4 Property ID :
1. Allez dans Google Analytics
2. Administration > Paramètres de la propriété
3. L'ID est au format "properties/XXXXXXXXXXXX"

## 📊 Utilisation

### Accès au dashboard

1. **Local** : http://localhost:8000
2. **Production** : https://votre-domaine.vercel.app

### Fonctionnalités

- **KPI en temps réel** : Visiteurs, pages vues, taux de rebond
- **Graphiques interactifs** : Évolution du trafic, pages populaires
- **Recommandations IA** : Suggestions SEO personnalisées
- **Export de données** : CSV pour analyse externe

### API Endpoints

- `GET /api/health` : Vérification de santé
- `GET /api/analytics` : Données GA4
- `GET /api/searchconsole` : Données Search Console
- `GET /api/recommendations` : Recommandations SEO
- `GET /api/dashboard` : Toutes les données

## 🐛 Dépannage

### Erreurs communes

1. **"Permission denied"**
   - Vérifiez que le compte de service a les bonnes permissions dans GA4 et GSC

2. **"Property not found"**
   - Vérifiez que le GA4_PROPERTY_ID est correct

3. **"Site not found"**
   - Vérifiez que le GSC_SITE_URL correspond exactement à votre propriété GSC

4. **"No data available"**
   - Les données peuvent prendre 24-48h pour apparaître dans GA4
   - Vérifiez que votre site reçoit du trafic

### Logs et monitoring

- **Backend logs** : Disponibles dans la console Render
- **Frontend errors** : Console du navigateur (F12)
- **API responses** : Onglet Network des outils de développement

## 🔄 Maintenance

### Mises à jour

1. **Backend** : `pip install -r requirements.txt --upgrade`
2. **Frontend** : Déployez automatiquement via Git
3. **API Google** : Vérifiez les quotas et limites

### Monitoring

- **Performance** : Temps de réponse des API
- **Erreurs** : Taux d'erreur des requêtes
- **Usage** : Volume de données traitées

## 📈 Optimisations

### Cache

Les données sont mises en cache pendant 5 minutes pour éviter les appels excessifs aux API Google.

### Limitation

- Maximum 1000 lignes par requête API
- 100 requêtes par jour par projet
- Cache de 5 minutes entre les requêtes

## 🤝 Support

Pour toute question :
1. Vérifiez les logs d'erreur
2. Consultez la documentation Google API
3. Testez les endpoints API directement
4. Vérifiez la configuration des permissions
