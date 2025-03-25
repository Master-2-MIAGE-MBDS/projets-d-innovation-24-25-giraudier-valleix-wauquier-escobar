import sys
from PIL import Image
from steganography_f5 import SteganographyF5

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python test_decode.py stego_image.png")
        sys.exit(1)

    try:
        # Chargement de l'image stégo
        stego_path = sys.argv[1]
        stego_image = Image.open(stego_path).convert("RGB")
        
        # Création de l'instance de stéganographie
        steg = SteganographyF5()
        
        # Décodage du message
        hidden_message = steg.decode(stego_image)
        
        if hidden_message:
            # Sauvegarde du message dans un fichier
            output_file = "message_decode.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(hidden_message)
            
            print(f"\nMessage extrait et sauvegardé dans '{output_file}'")
            print(f"Message: {hidden_message}")
        else:
            print("Aucun message valide n'a été trouvé dans l'image")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()