<p align="center">
<img alt="DataHub" src="https://www.miage.fr/wp-content/uploads/2021/01/MIAGE_50ans_MIAGE-50ans_COULEURS.png" height="150px" />
</p>

<h1 align="center">Exemple d'utilisation F5</h1>

---

Ce code implémente une version modifiée de l'algorithme de stéganographie F5, permettant de cacher des messages dans les coefficients DCT d'une image.

## 📝 Installation

Avant d'utiliser ce code, assurez-vous d'avoir installé :

- Python 3.x
- Les bibliothèques Python requises :

```bash
pip install numpy Pillow scipy
```

## 🔹 Structure des fichiers

Le projet contient les fichiers suivants :

- **steganography_f5.py:** L'implémentation principale de l'algorithme
- **test_steganography.py:** Script pour encoder un message dans une image
- **test_decode.py:** Script pour décoder un message depuis une image
- **carrier_image.png:** Image pour porter des messages à cacher
- **hello.txt:** Fichier txt pour pouvoir écrire le message à encoder

## 🚀 Utilisation

### 1. Cacher un message

Vous avez deux options pour cacher un message :

#### Option 1 : À partir d'un fichier texte
```bash
python test_steganography.py image.png message.txt
```
Où :
- `image.png` est votre image porteuse
- `message.txt` est le fichier contenant votre message

#### Option 2 : À partir d'une chaîne de caractères
```bash
python test_steganography.py image.png "Votre message secret"
```

Dans les deux cas, le script générera un fichier `stego_image.png` contenant votre message caché.

### 2. Extraire un message

Pour extraire un message d'une image :
```bash
python test_decode.py stego_image.png
```

Le message décodé sera :
- Sauvegardé dans un fichier `message_decode.txt`
- Affiché dans la console

## ⚠️ Notes importantes

### Format d'image :
- Utilisez de préférence des images PNG comme porteuses
- L'image stégo est toujours sauvegardée en PNG pour éviter la compression

### Capacité :
- La taille du message pouvant être caché dépend de la taille de l'image
- Utilisez des images suffisamment grandes pour vos messages

### Robustesse :
- Ne modifiez pas l'image stégo (redimensionnement, recadrage, etc.)
- Évitez la compression JPEG qui détruirait le message caché

## 🔧 Dépannage

Si vous rencontrez des erreurs :
- Vérifiez que toutes les dépendances sont installées
- Assurez-vous que l'image source existe et est lisible
- Vérifiez que vous avez les droits d'écriture dans le dossier
- Pour les messages depuis des fichiers, vérifiez l'encodage (UTF-8 recommandé)

## 📚 Note technique

Cette implémentation utilise une version modifiée de F5 avec :
- Modifications plus importantes des coefficients DCT pour plus de robustesse
- Utilisation de positions fixes dans les blocs DCT
- Travail sur le canal vert de l'image

## ⚠️ Limitations

- La capacité de stockage est limitée par la taille de l'image
- Les modifications sont plus importantes que dans F5 standard
- Sensible aux modifications de l'image stégo

## 📝 License

Copyright © 2024-2025