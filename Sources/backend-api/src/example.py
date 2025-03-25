# example.py
# Exemple d'utilisation directe des classes (sans passer par l'API Flask)

from .core.manager import ImageCertificateManager
from .core.services import SteganographyService, ImageSignatureRequest
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python example.py [sign|verify] [image_path] [user_id (pour sign)]")
        return
    
    action = sys.argv[1]
    image_path = sys.argv[2]
    
    if not os.path.exists(image_path):
        print(f"Image {image_path} non trouvée")
        return
    
    # Créer le service
    service = SteganographyService(cert_path="../certs/")
    
    if action == "sign":
        if len(sys.argv) < 4:
            print("Pour signer, spécifiez l'ID utilisateur")
            return
            
        user_id = sys.argv[3]
        
        # Lire l'image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Créer la requête
        request = ImageSignatureRequest(
            image_data=image_data,
            user_id=user_id
        )
        
        # Signer l'image
        response = service.sign_image(request)
        
        if response.success:
            # Sauvegarder l'image signée
            output_path = f"signed_{os.path.basename(image_path)}"
            with open(output_path, "wb") as f:
                f.write(response.signed_image)
            print(f"Image signée sauvegardée sous {output_path}")
            print(f"Message: {response.message}")
        else:
            print(f"Erreur: {response.message}")
            
    elif action == "verify":
        # Lire l'image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Vérifier l'image
        response = service.verify_image(image_data)
        
        print(f"Valide: {response.is_valid}")
        print(f"Message: {response.message}")
        
    elif action == "list-users":
        users = service.list_users()
        if users:
            print("Utilisateurs avec certificats:")
            for user in users:
                print(f"- {user}")
        else:
            print("Aucun utilisateur avec certificat trouvé")
    else:
        print(f"Action inconnue: {action}")

if __name__ == "__main__":
    main()