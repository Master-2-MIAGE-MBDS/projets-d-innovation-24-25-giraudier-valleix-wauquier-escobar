import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Outils.Outguess.Script.outguess_chiffrement import outguess_chiffrement
from Outils.Outguess.Script.outguess_dechiffrement import outguess_dechiffrement

def chiffrer_message(image_path, message, key_path, afficher_images=True):
    print("\n==== Chiffrement ====")
    resultats_chiffre = outguess_chiffrement(image_path, message, key_path, afficher_images=afficher_images)

    print("\n==== Résultats du test de chiffrement ====\n")
    print(f"Message original: '{resultats_chiffre['message_original']}'")
    print(f"Taille du message: {resultats_chiffre['taille_message']} caractères")

    if resultats_chiffre['success']:
        print("\n✅ Le message a été correctement caché dans l'image.")
        return resultats_chiffre['image_stegano']
    else:
        print("\n❌ Test de chiffrement échoué.")
        return None

def dechiffrer_message(image_stegano, key_path, afficher_images=True):
    print("\n==== Déchiffrement ====")
    resultats_dechiffre = outguess_dechiffrement(image_stegano, key_path, afficher_images=afficher_images)

    print("\n==== Résultats du test de déchiffrement ====\n")
    print(f"Message extrait : '{resultats_dechiffre['message_extrait']}'")

    if resultats_dechiffre['success']:
        print("\n✅ Le message a été correctement extrait.")
    else:
        print("\n❌ Test de déchiffrement échoué.")


def main():
    parser = argparse.ArgumentParser(
        description="Chiffrer et déchiffrer un message caché dans une image en utilisant Outguess.")
    parser.add_argument('image', type=str, help="Chemin de l'image à utiliser pour le chiffrement (JPEG).")
    parser.add_argument('message', type=str, help="Message à cacher dans l'image.")
    parser.add_argument('key', type=str, help="Chemin du fichier contenant la clé secrète.")
    parser.add_argument('--afficher_images', action='store_true', help="Affiche les images avant et après chiffrement.")

    args = parser.parse_args()

    image_stegano = chiffrer_message(args.image, args.message, args.key, afficher_images=args.afficher_images)

    if image_stegano:
        dechiffrer_message(image_stegano, args.key, afficher_images=args.afficher_images)


if __name__ == "__main__":
    main()