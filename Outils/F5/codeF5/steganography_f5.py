import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

class SteganographyF5:
    def __init__(self):
        self.positions = [(1,2), (2,1), (2,2), (3,1)]
        self.modification_value = 50  # Beaucoup plus grand pour assurer la persistance

    def _prepare_image(self, image):
        """Convertit l'image en RGB et la normalise"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image

    def _dct_block(self, block):
        """Applique la DCT avec normalisation"""
        block_norm = block.astype(np.float32) - 128.0  # Centre les valeurs
        return dct(dct(block_norm.T, norm='ortho').T, norm='ortho')

    def _idct_block(self, block):
        """Applique l'IDCT avec dénormalisation"""
        idct_block = idct(idct(block.T, norm='ortho').T, norm='ortho')
        return idct_block + 128.0  # Restore la plage

    def _get_bit(self, coef):
        """Extrait un bit basé sur un seuil plus élevé"""
        threshold = 25  # Seuil plus élevé pour la détection
        return 1 if abs(coef) >= threshold else 0

    def _modify_coefficient(self, coef, target_bit):
        """Modifie le coefficient avec une plus grande amplitude"""
        if target_bit == 1 and abs(coef) < 25:
            return 50.0 if coef >= 0 else -50.0
        elif target_bit == 0 and abs(coef) >= 25:
            return 0.0
        return coef

    def encode(self, carrier: Image.Image, payload: str) -> Image.Image:
        # Préparation des données
        carrier = self._prepare_image(carrier)
        msg_bytes = payload.encode('utf-8')
        binary_msg = ''.join(format(b, '08b') for b in msg_bytes)
        msg_length = len(binary_msg)
        length_bits = format(msg_length, '016b')
        binary_data = length_bits + binary_msg
        
        print(f"Message: {payload}")
        print(f"Binary message: {binary_msg}")
        print(f"Length bits: {length_bits}")
        print(f"Total binary data: {binary_data}")
        
        # Préparation de l'image
        img = np.array(carrier)
        green = img[:, :, 1].copy()  # Travail sur le canal vert
        h, w = green.shape
        stego = green.copy()
        
        bits_encoded = 0
        modifications = 0
        
        # Traitement par blocs
        for i in range(0, h-8, 8):
            for j in range(0, w-8, 8):
                if bits_encoded >= len(binary_data):
                    break
                    
                block = green[i:i+8, j:j+8]
                dct_block = self._dct_block(block)
                
                if bits_encoded + 4 <= len(binary_data):
                    current_bits = binary_data[bits_encoded:bits_encoded+4]
                    print(f"\nEncoding block at ({i},{j}):")
                    print(f"Current bits: {current_bits}")
                    
                    for bit_idx, (y, x) in enumerate(self.positions):
                        target_bit = int(current_bits[bit_idx])
                        old_coef = dct_block[y,x]
                        new_coef = self._modify_coefficient(old_coef, target_bit)
                        
                        if abs(old_coef - new_coef) > 1.0:
                            modifications += 1
                            print(f"Modified ({y},{x}): {old_coef:.2f} -> {new_coef:.2f} for bit {target_bit}")
                        
                        dct_block[y,x] = new_coef
                    
                    # Vérification immédiate
                    test_block = self._idct_block(dct_block)
                    test_block = np.clip(test_block, 0, 255)
                    test_dct = self._dct_block(test_block)
                    
                    print("Verification after processing:")
                    for y, x in self.positions:
                        print(f"Position ({y},{x}): {test_dct[y,x]:.2f} -> bit {self._get_bit(test_dct[y,x])}")
                    
                    bits_encoded += 4
                
                idct_block = self._idct_block(dct_block)
                stego[i:i+8, j:j+8] = np.clip(idct_block, 0, 255)
        
        print(f"\nEncoded {bits_encoded} bits with {modifications} modifications")
        
        # Finalisation
        img[:, :, 1] = stego.astype(np.uint8)
        return Image.fromarray(img)

    def decode(self, stego_image: Image.Image) -> str:
        # Préparation
        stego_image = self._prepare_image(stego_image)
        img = np.array(stego_image)
        green = img[:, :, 1]
        h, w = green.shape
        
        extracted_bits = []
        blocks_processed = 0
        
        # Extraction
        for i in range(0, h-8, 8):
            for j in range(0, w-8, 8):
                block = green[i:i+8, j:j+8]
                dct_block = self._dct_block(block)
                
                block_bits = []
                for y, x in self.positions:
                    coef = dct_block[y,x]
                    bit = self._get_bit(coef)
                    block_bits.append(bit)
                
                if blocks_processed < 5:
                    print(f"\nDecoding block at ({i},{j}):")
                    for idx, ((y,x), bit) in enumerate(zip(self.positions, block_bits)):
                        print(f"Position ({y},{x}): coef={dct_block[y,x]:.2f}, bit={bit}")
                
                extracted_bits.extend(block_bits)
                blocks_processed += 1
        
        bit_str = ''.join(str(b) for b in extracted_bits)
        print(f"\nFirst 32 extracted bits: {bit_str[:32]}")
        
        try:
            length = int(bit_str[:16], 2)
            print(f"Decoded length: {length} bits")
            
            if length == 0 or length > len(bit_str) - 16:
                raise ValueError(f"Invalid message length: {length}")
            
            message_bits = bit_str[16:16+length]
            
            message_bytes = bytearray()
            for i in range(0, len(message_bits), 8):
                if i + 8 <= len(message_bits):
                    byte_bits = message_bits[i:i+8]
                    message_bytes.append(int(byte_bits, 2))
            
            message = message_bytes.decode('utf-8', errors="replace")
            print(f"Decoded message: {message}")
            return message
            
        except Exception as e:
            print(f"Decoding error: {str(e)}")
            print(f"Raw bits: {bit_str[:100]}")
            return ""