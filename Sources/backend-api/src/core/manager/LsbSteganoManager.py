
import json
import base64
from PIL import Image
import io
import re

def embed_in_dct(image_data: bytes, payload : dict):
    """Cache des données dans une image en utilisant la méthode LSB (Least Significant Bit)."""
    # Préparer le payload
    payload_json = json.dumps(payload)
    payload_bytes = payload_json.encode('utf-8')
    
    # Ajouter la taille du payload au début pour faciliter l'extraction
    size_bytes = len(payload_bytes).to_bytes(4, byteorder='big')
    data_to_hide = size_bytes + payload_bytes
    
    print(f"Taille du payload : {len(payload_bytes) / 1024:.2f} KB ({len(payload_bytes)} bytes)")
    print(f"Contenu du payload : {payload_json}")
    
    # Charger l'image 
    img = Image.open(io.BytesIO(image_data))
    width, height = img.size
    
    # Convertir en mode RGB si ce n'est pas déjà le cas
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Vérifier si l'image est assez grande pour stocker les données
    max_bytes = (width * height * 3) // 8  # 3 bits par pixel (un par canal RGB)
    if len(data_to_hide) > max_bytes:
        raise ValueError(f"Image trop petite. Maximum {max_bytes} bytes, besoin de {len(data_to_hide)} bytes.")
    
    # Convertir les données en bits
    bits = []
    for byte in data_to_hide:
        for i in range(8):
            bits.append((byte >> i) & 1)
    
    # Créer une nouvelle image pour stocker les données
    stego_img = img.copy()
    pixels = stego_img.load()
    
    # Cacher les bits dans les LSB des pixels
    idx = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Modifier les LSB des 3 canaux de couleur si nécessaire
            if idx < len(bits):
                r = (r & ~1) | bits[idx]
                idx += 1
            
            if idx < len(bits):
                g = (g & ~1) | bits[idx]
                idx += 1
            
            if idx < len(bits):
                b = (b & ~1) | bits[idx]
                idx += 1
            
            pixels[x, y] = (r, g, b)
            
            # Si tous les bits sont cachés, sortir
            if idx >= len(bits):
                break
        if idx >= len(bits):
            break
    
    # Sauvegarder l'image
    img_byte_array = io.BytesIO()
    stego_img.save(img_byte_array, format='PNG')  # PNG est sans perte, important pour la stéganographie
    
    print(f"Données cachées avec succès. Utilisé {idx} bits sur {width * height * 3} disponibles.")
    return img_byte_array.getvalue()


def extract_from_dct(image_data: bytes):
    """Extrait des données cachées dans une image en utilisant la méthode LSB."""
    # Charger l'image
    img = Image.open(io.BytesIO(image_data))
    width, height = img.size
    
    # S'assurer que l'image est en RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = img.load()
    
    # Extraire les bits LSB
    extracted_bits = []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            extracted_bits.append(r & 1)
            extracted_bits.append(g & 1)
            extracted_bits.append(b & 1)
    
    # Convertir les bits en bytes
    extracted_bytes = bytearray()
    for i in range(0, len(extracted_bits), 8):
        if i + 8 <= len(extracted_bits):
            byte = 0
            for j in range(8):
                byte |= extracted_bits[i + j] << j
            extracted_bytes.append(byte)

    if len(extracted_bytes) < 4:
        print("Pas assez de données extraites")
        return {"error": "Données insuffisantes"}
    
    size = int.from_bytes(extracted_bytes[:4], byteorder='big')
    payload_bytes = extracted_bytes[4:4+size]
    
    if len(payload_bytes) < size:
        print(f"Données incomplètes: {len(payload_bytes)}/{size} bytes")
    
    return payload_bytes