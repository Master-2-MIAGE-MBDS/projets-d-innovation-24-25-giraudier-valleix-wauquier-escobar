import React, { useState } from 'react';
import "./Oscult.css"


import mainLogo from '../assets/images/mainLogo.svg';
import FilePicker from '../components/FilePicker';

const Oscult: React.FC = () => {

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [name, setName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFilesSelected = (file: File) => {
    setSelectedFile(file);
    setError(null);
    setName(null);
  }

  const onOscultButtonClicked = () => {
    if (!selectedFile) return;
    
    const fileExtension = selectedFile.type.split("/")[1];
    const fileExtensionCode = fileExtension.toLocaleUpperCase();

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('format', fileExtensionCode);
    
    fetch('http://localhost:5000/api/steganography/verify', {
      method: 'POST',
      body: formData,
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Erreur lors de la vérification de l'image");
        }
        return response.json();
      })
      .then(data => {
        if(data.valid == true){
          setName(data.message);
        }
        else{
          setError("Impossible de détecter la signature...");
        }
      })
      .catch(error => {
        console.error('Erreur:', error);
      });
  }

  return (
    <div className='oscult'>

      <img className='oscult-main-logo' src={mainLogo} alt="Pic'sign main logo" />

      <div className='oscult-page-container'>
        <FilePicker
          onFileSelected={handleFilesSelected}
          accept=".jpg,.jpeg,.png,.bmp"
          maxSize={5242880} // 5MB
        />
        <button onClick={onOscultButtonClicked} disabled={selectedFile == null} className="oscult-button" type="button">Osculter l'image</button>

        {name != null &&
          <div className='oscult-own-container'>
            <p className='oscult-own-label'><span>Cette image appartient à</span><div className='oscult-sep'></div></p>
            <p className='oscult-own-name'><span>{name}</span></p>
          </div>
        }

        {error &&(
          <p className='oscult-own-error'><span>{error}</span></p>
        )}

      </div>

    </div>
  );
};

export default Oscult;