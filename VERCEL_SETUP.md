# Configuration Vercel pour Magasin de Jeux

## Étape 1: Créer un compte Vercel
1. Allez sur https://vercel.com
2. Créez un compte avec votre email (GitHub recommandé)
3. Connectez-vous avec votre compte GitHub

## Étape 2: Importer votre projet
1. Cliquez sur "Add New Project"
2. Choisissez "Import Git Repository"
3. Sélectionnez votre dépôt: Hassen100/SEO-IA
4. Vercel détectera automatiquement votre projet

## Étape 3: Configuration du build
1. **Framework Preset**: Other
2. **Root Directory**: ./
3. **Build Command**: (laisser vide)
4. **Output Directory**: docs
5. **Install Command**: (laisser vide)

## Étape 4: Variables d'environnement
(Aucune variable nécessaire pour ce projet statique)

## Étape 5: Déployer
1. Cliquez sur "Deploy"
2. Attendez le déploiement (2-3 minutes)
3. Votre site sera disponible sur: https://magasin-jeux-xxxx.vercel.app

## Avantages de Vercel vs GitHub Pages
✅ Déploiement automatique à chaque push
✅ HTTPS gratuit
✅ Domaines personnalisés gratuits
✅ Analytics intégré
✅ Preview URLs pour chaque PR
✅ Edge caching global
✅ Support des SPA (Single Page Applications)

## URL après déploiement
Votre site sera disponible sur: https://magasin-jeux.vercel.app

## Redirection automatique
Le fichier vercel.json configurera automatiquement:
- / → /docs/index.html
- /jeux.html → /docs/jeux.html
- Toutes les autres routes → /docs/

## Commandes utiles
# Pour vérifier la configuration
vercel ls

# Pour déployer manuellement
vercel --prod

# Pour voir les logs
vercel logs
