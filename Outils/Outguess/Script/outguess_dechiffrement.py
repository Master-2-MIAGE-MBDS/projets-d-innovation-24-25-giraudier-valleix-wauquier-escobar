import os
import subprocess
import tempfile

def outguess_dechiffrement(image_path, cle, afficher_images=True):
    # Créer un dossier temporaire pour les fichiers
    temp_dir = tempfile.mkdtemp()

    # Chemins des fichiers
    img_stegano_path = image_path
    msg_extrait_path = os.path.join(temp_dir, "extrait.txt")

    # 1. Extraire le message
    subprocess.run(['outguess', '-k', cle, '-r', img_stegano_path, msg_extrait_path], check=True)
    print(f"Message extrait de: {img_stegano_path}")

    # Lire le message extrait
    with open(msg_extrait_path, 'r') as f:
        message_recupere = f.read()

    # Résultats
    resultats = {
        "success": message_recupere != '',
        "message_extrait": message_recupere,
        "image_stegano": img_stegano_path
    }

    return resultats
