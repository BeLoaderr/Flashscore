import git
import os
import shutil

# CONFIGURA QUI I TUOI DATI
GITHUB_REPO = "https://beloaderr.github.io/Flashscore/"
LOCAL_REPO_PATH = "./my-website"
HTML_FILE = "index.html"

# Se la cartella esiste, rimuovila per evitare conflitti
if os.path.exists(LOCAL_REPO_PATH):
    shutil.rmtree(LOCAL_REPO_PATH)

# Clona il repository GitHub
repo = git.Repo.clone_from(GITHUB_REPO, LOCAL_REPO_PATH)