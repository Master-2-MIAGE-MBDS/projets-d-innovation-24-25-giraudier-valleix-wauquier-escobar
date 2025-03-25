# SteganographyService.py
from ..manager import ImageCertificateManager, f5SteganoManager, LsbSteganoManager
import io

class ImageSignatureRequest:
    def __init__(self, image_data: bytes, user_id: str, format: str):
        self.image_data = image_data
        self.user_id = user_id
        self.format = format

class ImageSignatureResponse:
    def __init__(self, signed_image: bytes, success: bool, message: str):
        self.signed_image = signed_image
        self.success = success
        self.message = message

class ImageVerificationRequest:
    def __init__(self, signed_image: bytes, format: str):
        self.signed_image = signed_image
        self.format = format

class ImageVerificationResponse:
    def __init__(self, is_valid: bool, message: str):
        self.is_valid = is_valid
        self.message = message

class SteganographyService:
    def __init__(self, cert_path="../certs/"):
        self.cert_manager = ImageCertificateManager(cert_path=cert_path)

    def sign_image(self, request: ImageSignatureRequest):
        """Signe l'image avec le certificat de l'utilisateur"""
        try:
            
            if request.format == "PNG" or request.format == "JPG" or request.format == "JPEG":
                image = f5SteganoManager.sign_image(request.image_data, request.user_id)
                image_stream = io.BytesIO()
                image.save(image_stream, format=request.format)

                return ImageSignatureResponse(
                    signed_image=image_stream.getvalue(),
                    success=True,
                    message=f"Image successfully signed by {request.user_id}"
                )

            elif request.format == "BMP":
                cert, private_key = self.cert_manager.create_user_certificate(request.user_id)

                # Signer l'image
                signed_image_data = self.cert_manager.sign_image(
                    request.image_data, 
                    cert, 
                    private_key,
                    LsbSteganoManager.embed_in_dct
                )
            
                return ImageSignatureResponse(
                    signed_image=signed_image_data,
                    success=True,
                    message=f"Image successfully signed by {request.user_id}"
                )
        
        except Exception as e:
            return ImageSignatureResponse(
                signed_image=None,
                success=False,
                message=f"Failed to sign image: {str(e)}"
            )

    def verify_image(self, request: ImageVerificationRequest):
        """Vérifie la signature d'une image"""

        stegMethod = None
        if request.format == "PNG" or request.format == "JPG" or request.format == "JPEG":
            strData = f5SteganoManager.verify_image(request.signed_image)
            return ImageVerificationResponse(
                is_valid=True,
                message=strData
            )

        elif request.format == "BMP":
            is_valid, message = self.cert_manager.verify_image(request.signed_image, LsbSteganoManager.extract_from_dct)
        
            return ImageVerificationResponse(
                is_valid=is_valid,
                message=message
            )

    def list_users(self):
        """Liste tous les utilisateurs avec certificats"""
        return self.cert_manager.list_users()