# init.py
from flask import Flask, jsonify, Blueprint, request, send_file
import io
from ..core.services.SteganographyService import SteganographyService, ImageSignatureRequest, ImageVerificationRequest

def init_routes(app):
    @app.route('/api/ping')
    def ping():
        return jsonify({"message": "Pong ! API is working!"})
    
    # Créer le blueprint pour la stéganographie
    stegano_bp = Blueprint('steganography', __name__)
    stegano_service = SteganographyService(cert_path="../certs/")
    
    @stegano_bp.route('/sign', methods=['POST'])
    def sign_image():
        """
        Route pour signer une image
        ---
        Paramètres:
          - image: fichier image à signer
          - user_id: identifiant de l'utilisateur
        """
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image provided"}), 400
            
        if 'user_id' not in request.form:
            return jsonify({"success": False, "message": "No user_id provided"}), 400
        
        if 'format' not in request.form:
            return jsonify({"success": False, "message": "No format provided"}), 400
            
        image = request.files['image']
        user_id = request.form['user_id']
        format = request.form['format']
        
        # Lire l'image
        image_data = image.read()
        
        # Créer la requête
        sign_request = ImageSignatureRequest(
            image_data=image_data,
            user_id=user_id,
            format=format
        )
        
        # Signer l'image
        response = stegano_service.sign_image(sign_request)
        
        if not response.success:
            return jsonify({
                "success": False,
                "message": response.message
            }), 500
        
        # Retourner l'image signée
        return send_file(
            io.BytesIO(response.signed_image),
            mimetype=image.content_type,
            as_attachment=True,
            download_name=f"signed_{image.filename}"
        )

    @stegano_bp.route('/verify', methods=['POST'])
    def verify_image():
        """
        Route pour vérifier une image signée
        ---
        Paramètres:
          - image: fichier image à vérifier
        """
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image provided"}), 400
        
        if 'format' not in request.form:
            return jsonify({"success": False, "message": "No format provided"}), 400
            
        image = request.files['image']
        format = request.form['format']
        
        # Lire l'image
        image_data = image.read()
        
        # Créer la requête
        sign_request = ImageVerificationRequest(
            signed_image=image_data,
            format=format
        )

        # Vérifier l'image
        response = stegano_service.verify_image(sign_request)
        
        return jsonify({
            "valid": response.is_valid,
            "message": response.message
        })

    @stegano_bp.route('/users', methods=['GET'])
    def list_users():
        """
        Route pour lister les utilisateurs avec certificats
        """
        users = stegano_service.list_users()
        
        return jsonify({
            "success": True,
            "users": users
        })
    
    # Enregistrer le blueprint avec le préfixe
    app.register_blueprint(stegano_bp, url_prefix='/api/steganography')