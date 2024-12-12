@echo off
REM Définir le nom du fichier de sortie
set OUTPUT_FILE=liste_fichiers.txt

REM Supprimer le fichier existant (si présent)
if exist "%OUTPUT_FILE%" del "%OUTPUT_FILE%"

REM Ajouter la liste des fichiers dans le répertoire courant au fichier texte
dir /b > "%OUTPUT_FILE%"

REM Afficher un message de confirmation
echo La liste des fichiers a été enregistrée dans %OUTPUT_FILE%
pause
