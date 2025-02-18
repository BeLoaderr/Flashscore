import git
import os

repo_path = "."
repo = git.Repo(repo_path)

file_to_upload = "partite.html"
file_path = os.path.join(repo_path, file_to_upload)

if not os.path.exists(file_path):
    print(f"Errore: {file_path} non trovato!")
    exit()

repo.git.add(file_to_upload)
repo.git.commit("-m", "Upload automatico con Python")
repo.git.push("origin", "main")

print("File caricato con successo su GitHub Pages!")