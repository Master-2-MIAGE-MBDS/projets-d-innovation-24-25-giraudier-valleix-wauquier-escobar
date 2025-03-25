import sys
from PIL import Image
from steganography_f5 import SteganographyF5

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("  Pour encoder avec un fichier:")
        print("    python test_steganography.py image.png fichier.txt")
        print("  Pour encoder avec une chaîne de caractères:")
        print('    python test_steganography.py image.png "votre message"')
        sys.exit(1)

    # Récupération des arguments
    carrier_path = sys.argv[1]
    message_source = sys.argv[2]

    try:
        # Chargement de l'image porteuse
        carrier_image = Image.open(carrier_path).convert("RGB")
        
        # Détermine si le second argument est un fichier ou une chaîne
        try:
            with open(message_source, 'r', encoding='utf-8') as f:
                secret_message = f.read()
                print(f"Message lu depuis le fichier: {message_source}")
        except IOError:
            # Si ce n'est pas un fichier, traite comme une chaîne directe
            secret_message = message_source
            print("Message lu depuis la ligne de commande")
        
        # Création de l'instance de stéganographie
        steg = SteganographyF5()
        
        # Encodage du message
        encoded_image = steg.encode(carrier_image, secret_message)
        
        # Sauvegarde de l'image stégo
        stego_path = "stego_image.png"
        encoded_image.save(stego_path)
        
        print(f"\nMessage caché avec succès dans '{stego_path}'")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()