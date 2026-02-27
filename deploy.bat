@echo off
echo ====================================
echo   DEPLOIEMENT GITHUB PAGES
echo ====================================
echo.

cd /d "C:\Users\VIP INFO\Desktop\magasin-jeux"

echo [1/8] Initialisation de Git...
git init

echo [2/8] Ajout des fichiers...
git add .

echo [3/8] Creation du commit...
git commit -m "Initial commit - SEO-IA project"

echo [4/8] Connexion au repository GitHub...
git remote add origin https://github.com/Hassen100/SEO-IA.git

echo [5/8] Configuration de la branche main...
git branch -M main

echo [6/8] Premier push sur GitHub...
git push -u origin main

echo.
echo ====================================
echo   TERMINE !
echo ====================================
echo.
echo Votre site sera disponible sur:
echo https://hassen100.github.io/SEO-IA/
echo.
echo N'oubliez pas d'activer GitHub Pages dans:
echo Settings > Pages > Source: Deploy from a branch
echo.
pause
