<p align="center">
<img alt="DataHub" src="https://www.miage.fr/wp-content/uploads/2021/01/MIAGE_50ans_MIAGE-50ans_COULEURS.png" height="150px" />
</p>
<h1 align="center">Projet de Stéganographie avec Outguess</h1>

---

# 🔒 Introduction

La stéganographie est l'art de dissimuler un message dans un autre support (ici une image) de manière à ce que seul le destinataire puisse détecter et extraire ce message. Contrairement au chiffrement qui rend le message illisible mais visible, la stéganographie cache complètement l'existence même du message. 

Ici, nous utilisons l'outil **Outguess**, qui permet de cacher des données dans les bits les moins significatifs d'images JPEG. Ce projet se compose de deux parties principales :
1. Un fichier Jupyter notebook `steganographie-outguess.ipynb` qui montre comment tester et faire fonctionner l'outil Outguess.
2. Un script Python `outguess.py` permettant de crypter et extraire un message secret.

---

## 🖥️ Execution du fichier Jupyter Notebook avec WSL sous Pycharm

1. Ouvrir PyCharm.
2. Aller dans `File > Settings > Project: <nom_du_projet> > Python Interpreter`.
3. Cliquer sur l'icône ⚙ (Settings) puis `Add Interpreter`.
4. Sélectionner `WSL`.
5. Choisir votre distribution (`Ubuntu`) et valider.


## 🏁 Exécution du script python sous Windows PowerShell via WSL

### Pré-requis :

1. **WSL (Windows Subsystem for Linux)** doit être installé avec une distribution Linux comme Ubuntu.
2. **Outguess** et **ImageMagick** doivent être installés sous WSL.

### Étapes pour exécuter le script via PowerShell :

#### 1. Installer les dépendances sous WSL
Dans votre terminal Ubuntu WSL, installez les outils nécessaires pour exécuter le script :

```bash
sudo apt update
sudo apt install python3 python3-pip imagemagick
```

#### 2. Exécuter le script Python
Ouvrez PowerShell sur Windows et utilisez la commande suivante pour exécuter le script Python via WSL 

```bash
wsl python3 /mnt/c/Users/<path>/mbds-steganography-project/Outils/Outguess/outguess.py "/mnt/c/Users/<path>/mbds-steganography-project/ImagesAChiffrer/image_depart.jpg" "La stéganographie j'adore !" "/mnt/c/Users/<path>/mbds-steganography-project/MessageSecret/message_secret.txt" --afficher_images
```

#### 3. Résultat

Voici un exemple de résultat obtenu après l'exécution du script :

```bash
C:\Users\Benja>wsl python3 /mnt/c/Users/Benja/Documents/Mes\ Applications/mbds-steganography-project/Outils/Outguess/outguess.py "/mnt/c/Users/Benja/Documents/Mes Applications/mbds-steganography-project/Outils/Outguess/ImagesAChiffrer/image_depart.jpg" "La stéganographie j'adore" "/mnt/c/Users/Benja/Documents/Mes Applications/mbds-steganography-project/Outils/Outguess/MessageSecret/message_secret.txt" --afficher_images

==== Chiffrement ====
Message créé dans: /tmp/tmp374y2vgc/message.txt
Reading /mnt/c/Users/Benja/Documents/Mes Applications/mbds-steganography-project/Outils/Outguess/ImagesAChiffrer/image_depart.jpg....
JPEG compression quality set to 75
Extracting usable bits:   830476 bits
Correctable message size: 5952 bits, 0.72%
Encoded '/tmp/tmp374y2vgc/message.txt': 224 bits, 28 bytes
Finding best embedding...
    0:   139(54.9%)[62.1%], bias   104(0.75), saved:    -3, total:  0.02%
    1:   126(49.2%)[56.2%], bias   111(0.88), saved:    -1, total:  0.02%
    2:   126(49.2%)[56.2%], bias    96(0.76), saved:    -1, total:  0.02%
    6:   127(49.6%)[56.7%], bias    82(0.65), saved:    -1, total:  0.02%
   16:   137(53.5%)[61.2%], bias    70(0.51), saved:    -3, total:  0.02%
   26:   113(44.5%)[50.4%], bias    76(0.67), saved:     0, total:  0.01%
26, 189: Embedding data: 224 in 830476
Bits embedded: 254, changed: 113(44.5%)[50.4%], bias: 76, tot: 831261, skip: 831007
Foiling statistics: corrections: 63, failed: 0, offset: 77.428571 +- 200.556369
Total bits changed: 189 (change 113 + bias 76)
Storing bitmap into data...
Writing /tmp/tmp374y2vgc/stegano.jpg....
Message caché dans: /tmp/tmp374y2vgc/stegano.jpg

==== Résultats du test de chiffrement ====

Message original: 'La stéganographie j'adore'
Taille du message: 27 caractères

✅ Le message a été correctement caché dans l'image.

==== Déchiffrement ====
Reading /tmp/tmp374y2vgc/stegano.jpg....
Extracting usable bits:   830476 bits
Steg retrieve: seed: 26, len: 28
Message extrait de: /tmp/tmp374y2vgc/stegano.jpg

==== Résultats du test de déchiffrement ====

Message extrait : 'La stéganographie j'adore'

✅ Le message a été correctement extrait.
```

## 📈 Notes

- **Outguess** fonctionne uniquement avec des images au format JPEG.
- Les modifications apportées à l'image sont **invisibles à l'œil nu**.

## ✍️ Auteurs

👤 **VALLEIX Benjamin**

* GitHub: [@B3njaminV](https://github.com/B3njaminV)
* LinkedIn: [@Benjamin VALLEIX](https://www.linkedin.com/in/benjamin-valleix-27115719a)

## 📝 License

Copyright © 2024-2025

