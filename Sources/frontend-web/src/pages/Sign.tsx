import React, { useState } from 'react';
import "./Sign.css"


import mainLogo from '../assets/images/mainLogo.svg';
import FilePicker from '../components/FilePicker';

const Sign: React.FC = () => {

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [currentName, setCurrentName] = useState<string>("");
  const [resetPickerTrigger, setResetPickerTrigger] = useState<boolean>(false);

  const handleFilesSelected = (file: File) => {
    setSelectedFile(file);
  }

  const resetFilePicker = () => {
    setResetPickerTrigger(!resetPickerTrigger);
    setSelectedFile(null);
  }

  const handleNameInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentName(event.target.value.trim());
  }

  const onSignButtonClicked = () => {
    if (!selectedFile || !currentName) return;
    
    const fileExtension = selectedFile.type.split("/")[1];
    const fileExtensionCode = fileExtension.toLocaleUpperCase();
    
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('user_id', currentName);
    formData.append('format', fileExtensionCode);
    
    fetch('http://localhost:5000/api/steganography/sign', {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      if (!response.ok) {
        throw new Error("Erreur lors de la vérification de l'image");
      }
      return response.blob(); // Utiliser blob() au lieu de text() ou json()
    })
    .then(imageBlob => {
      // Créer un URL pour le blob directement
      const url = URL.createObjectURL(imageBlob);
      
      // Créer un élément <a> pour télécharger
      const link = document.createElement('a');
      link.href = url;
      link.download = `signed_${selectedFile.name}`; // Nom du fichier à télécharger
      
      // Ajouter le lien au document, cliquer dessus, puis le supprimer
      document.body.appendChild(link);
      link.click();
      
      // Nettoyer en supprimant le lien et en révoquant l'URL
      setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }, 100);
    })
    .catch(error => {
      console.error('Erreur:', error);
    });

    resetFilePicker();
  }

  return (
    <div className='sign'>

      <img className='sign-main-logo' src={mainLogo} alt="Pic'Sign main logo" />

      <div className='sign-page-container'>
        <FilePicker
          onFileSelected={handleFilesSelected}
          shouldReset={resetPickerTrigger}
          accept=".jpg,.jpeg,.png,.bmp"
          maxSize={5242880} // 5MB
        />

        <input onChange={handleNameInputChange} className="sign-name-inp" type="text" placeholder="Votre nom" id="sign-name-inp" />

        <button onClick={onSignButtonClicked} disabled={selectedFile == null || currentName == ""} className="sign-button" type="button">Signer et télécharger</button>
      </div>

    </div>
  );
};

export default Sign;