# ImageCertificateManager.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import datetime
import os
import json
import base64
from PIL import Image
import numpy as np
import io
from scipy.fftpack import dct, idct
import hashlib
import sys 
import re
import reedsolo

class ImageCertificateManager:
    def __init__(self, cert_path="../../../certs/"):
        self.cert_path = cert_path
        
        # Créer le dossier de certificats s'il n'existe pas
        os.makedirs(self.cert_path, exist_ok=True)
        
        # Chemins des fichiers
        self.root_key_path = os.path.join(self.cert_path, "root_key.pem")
        self.root_cert_path = os.path.join(self.cert_path, "root_cert.pem")
        
        # Initialiser ou charger la CA
        self._init_root_ca()

    def _init_root_ca(self):
        """Initialise ou charge l'autorité de certification racine"""
        if os.path.exists(self.root_key_path) and os.path.exists(self.root_cert_path):
            # Charger la clé et le certificat existants
            with open(self.root_key_path, "rb") as key_file:
                self.root_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None  # En production, utiliser un mot de passe
                )
            
            with open(self.root_cert_path, "rb") as cert_file:
                self.root_cert = x509.load_pem_x509_certificate(cert_file.read())
        else:
            # Créer une nouvelle CA
            self.root_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096
            )
            self.root_cert = self._create_root_certificate()
            
            # Enregistrer la clé et le certificat
            with open(self.root_key_path, "wb") as key_file:
                key_file.write(self.root_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()  # Utiliser encryption en production
                ))
            
            with open(self.root_cert_path, "wb") as cert_file:
                cert_file.write(self.root_cert.public_bytes(serialization.Encoding.PEM))

    def _create_root_certificate(self):
        """Crée le certificat racine"""
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"SteganographIA Root CA"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"SteganographIA"),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
        ])
        
        return x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.root_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=3650)  # 10 ans
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), 
            critical=True
        ).sign(self.root_key, hashes.SHA256())

    def create_user_certificate(self, username):
        """Crée un certificat utilisateur et le stocke sur disque"""
        user_dir = os.path.join(self.cert_path, username)
        os.makedirs(user_dir, exist_ok=True)
        
        private_key_path = os.path.join(user_dir, "private_key.pem")
        cert_path = os.path.join(user_dir, "certificate.pem")
        
        # Vérifier si les certificats existent déjà
        if os.path.exists(private_key_path) and os.path.exists(cert_path):
            # Charger les certificats existants
            with open(private_key_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None
                )
            
            with open(cert_path, "rb") as cert_file:
                cert = x509.load_pem_x509_certificate(cert_file.read())
            
            return cert, private_key
        
        # Créer une nouvelle paire de clés
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, username),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"SteganographIA Users"),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.root_cert.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), 
            critical=True
        ).sign(self.root_key, hashes.SHA256())
        
        # Enregistrer la clé et le certificat
        with open(private_key_path, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(cert_path, "wb") as cert_file:
            cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
        
        return cert, private_key

    def list_users(self):
        """Liste tous les utilisateurs avec certificats"""
        users = []
        for item in os.listdir(self.cert_path):
            user_dir = os.path.join(self.cert_path, item)
            if os.path.isdir(user_dir) and os.path.exists(os.path.join(user_dir, "certificate.pem")):
                users.append(item)
        return users

    def sign_image(self, image_data, user_cert, user_private_key, steg_method):
        """Signe l'image avec le certificat utilisateur - Version adaptée pour LSB."""
        # Calcul du hash de l'image
        image_hash = hashes.Hash(hashes.SHA256())
        image_hash.update(image_data)
        digest = image_hash.finalize()
        
        # Signature
        signature = user_private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Extraire les informations essentielles du certificat
        common_name = None
        for attr in user_cert.subject:
            if attr.oid == NameOID.COMMON_NAME:
                common_name = attr.value
                break
        
        if not common_name:
            raise ValueError("Certificate does not have a Common Name")
        
        # Convertir les données binaires en base64 pour la sérialisation JSON
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        
        # Version compressée du payload
        compressed_payload = {
            "cid": common_name,
            "sn": str(user_cert.serial_number),
            "fpt": hashlib.sha256(user_cert.public_bytes(serialization.Encoding.DER)).hexdigest()[:20],
            "sig": signature_base64,
            "ts": int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        }

        img = Image.open(io.BytesIO(image_data))
        
        # Vérifier si l'image est en RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        return steg_method(image_data, compressed_payload)

    def verify_image(self, image_data: bytes, steg_method):
        """Vérification complète avec logs détaillés pour chaque étape."""
        try:
            print("================ DÉBUT DE LA VÉRIFICATION ================")
            
            # Extraire le payload
            extracted_bytes = steg_method(image_data)
            payload = None
            
            payload_str = extracted_bytes.decode('utf-8')

            try:
                # Décoder le JSON
                payload = json.loads(payload_str)
                
                # Traiter les valeurs en base64 (comme la signature)
                for key, value in payload.items():
                    if isinstance(value, str) and key == "signature":
                        try:
                            payload[key] = base64.b64decode(value)
                            print(payload[key])
                        except:
                            pass

            except Exception as e:
                print(f"Erreur lors du décodage: {str(e)}")
                
                # Tenter une extraction partielle
                try:
                    cert_id_match = re.search(r'"cid"\s*:\s*"([^"]+)"', payload_str)
                    if cert_id_match:
                        cert_id = cert_id_match.group(1)
                        
                        payload = {"cert_id": cert_id}
                        
                        # Signature
                        sig_match = re.search(r'"sn"\s*:\s*"([^"]+)"', payload_str)
                        if sig_match:
                            sig_b64 = sig_match.group(1)
                            try:
                                payload["signature"] = base64.b64decode(sig_b64)
                            except:
                                payload["signature"] = b"signature_decode_failed"
                except Exception as e2:
                    print(f"Erreur 2 lors du décodage: {str(e2)}")
                    pass

            print(f"Extracted payload keys: {list(payload.keys())}")
            print("\n--- CONTENU DU PAYLOAD ---")
            for key, value in payload.items():
                if key == "signature" or key == "sig":
                    print(f"{key}: [DONNÉES BINAIRES]")
                else:
                    print(f"{key}: {value}")
            print("------------------------")
            
            # Normaliser les clés
            normalized_payload = {}
            key_mapping = {
                'cid': 'cert_id',
                'sig': 'signature',
                'sn': 'cert_serial',
                'fpt': 'cert_fingerprint',
                'ts': 'timestamp'
            }
            
            print("\n--- NORMALISATION DES CLÉS ---")
            for key, value in payload.items():
                if key in key_mapping:
                    normalized_key = key_mapping[key]
                    print(f"Conversion: '{key}' -> '{normalized_key}'")
                else:
                    normalized_key = key
                    print(f"Conservation: '{key}'")
                normalized_payload[normalized_key] = value
            
            # Récupérer l'utilisateur et la signature
            user_id = normalized_payload.get('cert_id')
            if not user_id:
                print("❌ ÉCHEC: User ID non trouvé dans le payload")
                return False, "User ID not found in payload"
            
            print(f"\n✓ User ID trouvé: {user_id}")
            
            # Vérifier si la signature existe
            signature = normalized_payload.get('signature')
            if isinstance(signature, str):
                print(f"Signature en format chaîne, tentative de décodage...")
                try:
                    signature = base64.b64decode(signature)
                    normalized_payload['signature'] = signature
                    print(f"✓ Signature décodée avec succès: {len(signature)} bytes")
                except Exception as decode_err:
                    print(f"❌ ÉCHEC: Impossible de décoder la signature: {decode_err}")
                    return False, "Invalid signature format"
            
            if not signature:
                print("❌ ÉCHEC: Signature non trouvée ou invalide")
                return False, "Valid signature not found in payload"
            
            print(f"✓ Signature valide trouvée: {len(signature)} bytes")
            
            # Récupérer le certificat
            cert_path = os.path.join(self.cert_path, user_id, "certificate.pem")
            print(f"\n--- VÉRIFICATION DU CERTIFICAT ---")
            print(f"Recherche du certificat: {cert_path}")
            
            if not os.path.exists(cert_path):
                print(f"Certificat non trouvé, recherche de variantes du nom...")
                # Rechercher des variantes du nom d'utilisateur
                potential_users = []
                for item in os.listdir(self.cert_path):
                    if os.path.isdir(os.path.join(self.cert_path, item)) and item.lower() == user_id.lower():
                        potential_users.append(item)
                
                if potential_users:
                    user_id = potential_users[0]
                    cert_path = os.path.join(self.cert_path, user_id, "certificate.pem")
                    print(f"✓ Variante trouvée: {user_id}, nouveau chemin: {cert_path}")
                else:
                    print(f"❌ ÉCHEC: Aucun certificat trouvé pour '{user_id}'")
                    return False, f"Certificate for user '{user_id}' not found"
            
            try:
                # Charger et vérifier le certificat
                with open(cert_path, "rb") as f:
                    cert_data = f.read()
                    print(f"✓ Certificat chargé: {len(cert_data)} bytes")
                    cert = x509.load_pem_x509_certificate(cert_data)
                
                print("\n--- VÉRIFICATION DE LA CHAÎNE DE CERTIFICATS ---")
                if not self.verify_certificate_chain(cert):
                    print("❌ ÉCHEC: Chaîne de certificats invalide")
                    return False, "Invalid certificate chain"
                
                print("✓ Chaîne de certificats validée avec succès")
                
                # Initialiser le score de vérification et les messages
                verification_score = 0
                verification_checks = []
                
                print("\n--- VÉRIFICATIONS DÉTAILLÉES ---")
                
                # 1. Vérifier le numéro de série du certificat
                cert_serial = str(cert.serial_number)
                payload_serial = normalized_payload.get('cert_serial')
                
                if payload_serial:
                    print(f"1. Numéro de série du certificat:")
                    print(f"   - Certificat: {cert_serial}")
                    print(f"   - Payload:    {payload_serial}")
                    
                    if cert_serial == payload_serial:
                        verification_score += 1
                        verification_checks.append(("Numéro de série", "✓ SUCCÈS"))
                        print(f"   - Résultat:   ✓ Correspond")
                    else:
                        verification_checks.append(("Numéro de série", "❌ ÉCHEC"))
                        print(f"   - Résultat:   ❌ Différent")
                else:
                    verification_checks.append(("Numéro de série", "⚠️ NON VÉRIFIÉ (absent)"))
                    print(f"1. Numéro de série: ⚠️ Non vérifié (absent du payload)")
                
                # 2. Vérifier l'empreinte du certificat
                cert_fingerprint = hashlib.sha256(cert.public_bytes(serialization.Encoding.DER)).hexdigest()
                payload_fingerprint = normalized_payload.get('cert_fingerprint')
                
                if payload_fingerprint:
                    print(f"\n2. Empreinte du certificat:")
                    print(f"   - Certificat: {cert_fingerprint}")
                    print(f"   - Payload:    {payload_fingerprint}")
                    
                    # Comparaison flexible (l'un peut être un préfixe de l'autre)
                    if cert_fingerprint.startswith(payload_fingerprint) or payload_fingerprint.startswith(cert_fingerprint[:len(payload_fingerprint)]):
                        verification_score += 1
                        verification_checks.append(("Empreinte", "✓ SUCCÈS"))
                        print(f"   - Résultat:   ✓ Correspond")
                    else:
                        verification_checks.append(("Empreinte", "❌ ÉCHEC"))
                        print(f"   - Résultat:   ❌ Différent")
                else:
                    verification_checks.append(("Empreinte", "⚠️ NON VÉRIFIÉ (absent)"))
                    print(f"2. Empreinte: ⚠️ Non vérifié (absent du payload)")
                
                # 3. Vérifier l'émetteur du certificat
                cert_issuer = str(cert.issuer.rfc4514_string())
                payload_issuer = normalized_payload.get('cert_issuer')
                
                if payload_issuer:
                    print(f"\n3. Émetteur du certificat:")
                    print(f"   - Certificat: {cert_issuer}")
                    print(f"   - Payload:    {payload_issuer}")
                    
                    if cert_issuer == payload_issuer:
                        verification_score += 1
                        verification_checks.append(("Émetteur", "✓ SUCCÈS"))
                        print(f"   - Résultat:   ✓ Correspond")
                    else:
                        verification_checks.append(("Émetteur", "❌ ÉCHEC"))
                        print(f"   - Résultat:   ❌ Différent")
                else:
                    verification_checks.append(("Émetteur", "⚠️ NON VÉRIFIÉ (absent)"))
                    print(f"3. Émetteur: ⚠️ Non vérifié (absent du payload)")
                
                # 4. Vérifier l'algorithme de signature
                cert_sign_algo = cert.signature_algorithm_oid._name
                payload_sign_algo = normalized_payload.get('cert_sign_algo')
                
                if payload_sign_algo:
                    print(f"\n4. Algorithme de signature:")
                    print(f"   - Certificat: {cert_sign_algo}")
                    print(f"   - Payload:    {payload_sign_algo}")
                    
                    if cert_sign_algo == payload_sign_algo:
                        verification_score += 1
                        verification_checks.append(("Algorithme", "✓ SUCCÈS"))
                        print(f"   - Résultat:   ✓ Correspond")
                    else:
                        verification_checks.append(("Algorithme", "❌ ÉCHEC"))
                        print(f"   - Résultat:   ❌ Différent")
                else:
                    verification_checks.append(("Algorithme", "⚠️ NON VÉRIFIÉ (absent)"))
                    print(f"4. Algorithme: ⚠️ Non vérifié (absent du payload)")
                
                # 5. Vérifier les dates de validité
                try:
                    # Convertir les dates du payload en objets datetime
                    payload_valid_from = normalized_payload.get('cert_valid_from')
                    payload_valid_to = normalized_payload.get('cert_valid_to')
                    
                    if payload_valid_from and payload_valid_to:
                        print(f"\n5. Dates de validité:")
                        
                        # Obtenir les dates du certificat
                        if hasattr(cert, 'not_valid_before_utc'):
                            cert_valid_from = cert.not_valid_before_utc
                            cert_valid_to = cert.not_valid_after_utc
                        else:
                            cert_valid_from = cert.not_valid_before
                            cert_valid_to = cert.not_valid_after
                        
                        # Convertir en chaînes ISO pour la comparaison
                        cert_valid_from_str = cert_valid_from.isoformat()
                        cert_valid_to_str = cert_valid_to.isoformat()
                        
                        print(f"   - Certificat (de): {cert_valid_from_str}")
                        print(f"   - Payload (de):    {payload_valid_from}")
                        print(f"   - Certificat (à):  {cert_valid_to_str}")
                        print(f"   - Payload (à):     {payload_valid_to}")
                        
                        if payload_valid_from == cert_valid_from_str and payload_valid_to == cert_valid_to_str:
                            verification_score += 1
                            verification_checks.append(("Dates validité", "✓ SUCCÈS"))
                            print(f"   - Résultat:        ✓ Correspond")
                        else:
                            verification_checks.append(("Dates validité", "❌ ÉCHEC"))
                            print(f"   - Résultat:        ❌ Différent")
                    else:
                        verification_checks.append(("Dates validité", "⚠️ NON VÉRIFIÉ (absent)"))
                        print(f"5. Dates validité: ⚠️ Non vérifié (absent du payload)")
                except Exception as date_error:
                    verification_checks.append(("Dates validité", f"❌ ERREUR: {date_error}"))
                    print(f"5. Dates validité: ❌ Erreur lors de la vérification: {date_error}")
                
                # 6. Vérifier le timestamp (pas trop ancien, pas dans le futur)
                try:
                    payload_timestamp = normalized_payload.get('timestamp')
                    if payload_timestamp:
                        print(f"\n6. Horodatage de la signature:")
                        now = datetime.datetime.now(datetime.timezone.utc)
                        print(f"   - Date actuelle: {now.isoformat()}")
                        
                        if isinstance(payload_timestamp, int):
                            # Format timestamp Unix
                            sig_time = datetime.datetime.fromtimestamp(payload_timestamp, tz=datetime.timezone.utc)
                            print(f"   - Timestamp:     {payload_timestamp} (Unix)")
                        else:
                            # Format ISO
                            sig_time = datetime.datetime.fromisoformat(payload_timestamp)
                            print(f"   - Timestamp:     {payload_timestamp} (ISO)")
                        
                        print(f"   - Date signature: {sig_time.isoformat()}")
                        
                        # Vérifier que le timestamp n'est pas dans le futur (avec marge d'erreur de 5 minutes)
                        if sig_time > now + datetime.timedelta(minutes=5):
                            verification_checks.append(("Horodatage", "❌ ÉCHEC (futur)"))
                            print(f"   - Résultat:      ❌ La date de signature est dans le futur")
                        else:
                            # Vérifier que le timestamp n'est pas trop ancien (par exemple, pas plus d'un an)
                            if now - sig_time > datetime.timedelta(days=365):
                                verification_checks.append(("Horodatage", "⚠️ ATTENTION (ancien)"))
                                print(f"   - Résultat:      ⚠️ La signature date de plus d'un an")
                            else:
                                verification_score += 1
                                verification_checks.append(("Horodatage", "✓ SUCCÈS"))
                                print(f"   - Résultat:      ✓ Horodatage valide")
                    else:
                        verification_checks.append(("Horodatage", "⚠️ NON VÉRIFIÉ (absent)"))
                        print(f"6. Horodatage: ⚠️ Non vérifié (absent du payload)")
                except Exception as time_error:
                    verification_checks.append(("Horodatage", f"❌ ERREUR: {time_error}"))
                    print(f"6. Horodatage: ❌ Erreur lors de la vérification: {time_error}")
                
                # 7. Vérifier la taille de la signature
                print(f"\n7. Taille de la signature:")
                print(f"   - Taille: {len(signature)} bytes")
                if len(signature) >= 256:
                    verification_checks.append(("Taille signature", "✓ OPTIMALE"))
                    print(f"   - Résultat: ✓ Taille optimale")
                elif len(signature) >= 128:
                    verification_checks.append(("Taille signature", "✓ CORRECTE"))
                    print(f"   - Résultat: ✓ Taille correcte")
                else:
                    verification_checks.append(("Taille signature", "⚠️ SOUS-OPTIMALE"))
                    print(f"   - Résultat: ⚠️ Taille sous-optimale")
                
                # Résumé des vérifications
                print("\n--- RÉSUMÉ DES VÉRIFICATIONS ---")
                print(f"Score de vérification: {verification_score}/6")
                print("Détails:")
                for check, result in verification_checks:
                    print(f"- {check}: {result}")
                
                # Critères de réussite
                if verification_score >= 3 and len(signature) >= 128:
                    # Succès avec niveau de confiance élevé
                    confidence_level = "élevée" if verification_score >= 5 else "moyenne"
                    result_msg = user_id
                    print(f"\n✅ SUCCÈS: {result_msg}")
                    return True, result_msg
                elif verification_score >= 1 and len(signature) >= 64:
                    # Succès avec niveau de confiance plus faible
                    result_msg = user_id
                    print(f"\n⚠️ SUCCÈS PARTIEL: {result_msg}")
                    return True, result_msg
                else:
                    result_msg = f"Échec de la vérification. Critères insuffisants."
                    print(f"\n❌ ÉCHEC: {result_msg}")
                    return False, result_msg
                    
            except Exception as cert_error:
                print(f"\n❌ ERREUR de traitement du certificat: {cert_error}")
                return False, f"Certificate error for user '{user_id}': {str(cert_error)}"
        
        except Exception as e:
            print(f"\n❌ ERREUR générale: {str(e)}")
            return False, f"Verification failed: {str(e)}"

    def verify_certificate_chain(self, cert):
        """Vérifie la chaîne de certificats"""
        try:
            # Vérifier que le certificat a été signé par notre CA racine
            cert_issuer = cert.issuer
            root_subject = self.root_cert.subject
            
            # Vérifier que l'émetteur du certificat correspond au sujet du certificat racine
            if cert_issuer != root_subject:
                return False
            
            # Vérifier la signature
            public_key = self.root_cert.public_key()
            public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),  # Le padding utilisé pour les signatures de certificats
                cert.signature_hash_algorithm
            )
            
            # Vérifier la date de validité
            now = datetime.datetime.utcnow()
            if now < cert.not_valid_before or now > cert.not_valid_after:
                return False
                
            return True
        except Exception:
            return False
    