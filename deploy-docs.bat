@echo off
echo ====================================
echo   DEPLOIEMENT GITHUB PAGES - METHODE DOCS
echo ====================================
echo.

cd /d "C:\Users\VIP INFO\Desktop\magasin-jeux"

echo [1/6] Build pour GitHub Pages...
ng build --configuration production

echo [2/6] Initialisation de Git...
git init

echo [3/6] Ajout des fichiers...
git add .

echo [4/6] Creation du commit...
git commit -m "Deploy SEO-IA to GitHub Pages"

echo [5/6] Connexion au repository GitHub...
git remote add origin https://github.com/Hassen100/SEO-IA.git

echo [6/6] Push sur GitHub...
git push -u origin main --force

echo.
echo ====================================
echo   TERMINE !
echo ====================================
echo.
echo Votre site sera disponible sur:
echo https://hassen100.github.io/SEO-IA/
echo.
echo ETAPE SUIVANTE:
echo 1. Allez sur https://github.com/Hassen100/SEO-IA
echo 2. Settings > Pages
echo 3. Source: Deploy from a branch
echo 4. Branch: main
echo 5. Folder: /docs
echo 6. Save
echo.
pause
