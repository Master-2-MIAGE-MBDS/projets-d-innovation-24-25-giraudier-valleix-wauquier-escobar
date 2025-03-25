import os
import subprocess
import tempfile

def outguess_chiffrement(image_path, message, cle, afficher_images=True):

    # Créer un dossier temporaire pour les fichiers
    temp_dir = tempfile.mkdtemp()

    # Fonction pour vérifier si une image est au format JPEG
    def is_jpeg(file_path):
        result = subprocess.run(['file', file_path], capture_output=True, text=True)
        return 'JPEG' in result.stdout

    # Chemins des fichiers
    img_path = image_path
    img_stegano_path = os.path.join(temp_dir, "stegano.jpg")
    msg_path = os.path.join(temp_dir, "message.txt")

    # 1. Vérifier et convertir l'image si nécessaire
    if not is_jpeg(img_path):
        img_conv_path = os.path.join(temp_dir, "convertie.jpg")
        subprocess.run(['convert', img_path, img_conv_path], check=True)
        img_path = img_conv_path
        print(f"Image convertie en JPEG: {img_path}")

    # 2. Créer le fichier message
    with open(msg_path, 'w') as f:
        f.write(message)
    print(f"Message créé dans: {msg_path}")

    # 3. Cacher le message dans l'image
    subprocess.run(['outguess', '-k', cle, '-d', msg_path, img_path, img_stegano_path], check=True)
    print(f"Message caché dans: {img_stegano_path}")

    # Résultats
    resultats = {
        "success": True,
        "message_original": message,
        "image_stegano": img_stegano_path,
        "taille_message": len(message)
    }

    return resultats
