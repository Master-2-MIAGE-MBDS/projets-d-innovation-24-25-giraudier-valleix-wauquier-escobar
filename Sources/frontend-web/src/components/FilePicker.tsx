import "./Footer.css"
import "./FilePicker.css"
import { useCallback, useEffect, useRef, useState } from "react";


import uploadFileIcon from '../assets/images/upload-file.svg';

interface FilePickerProps {
  onFileSelected: (file: File) => void;
  shouldReset?: boolean;
  accept?: string;
  maxSize?: number; // taille maximale en bytes
}

const FilePicker: React.FC<FilePickerProps> = ({
  shouldReset = false,
  onFileSelected,
  accept = '*',
  maxSize = 10485760, // 10MB par défaut
}) => {
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [currentSelectedFile, setCurrentSelectedFile] = useState<File | null>(null);

  useEffect(()=>{
    setCurrentSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [shouldReset]);

  // Fonction pour gérer la sélection des fichiers
  const handleFileSelection = useCallback(
    (selectedFiles: FileList | null) => {
      setError(null);
      
      if (!selectedFiles || selectedFiles.length === 0) {
        return;
      }
      
      const filesArray = Array.from(selectedFiles);
      
      // Vérification de la taille des fichiers
      const oversizedFiles = filesArray.filter(file => file.size > maxSize);
      if (oversizedFiles.length > 0) {
        const fileNames = oversizedFiles.map(file => file.name).join(', ');
        setError(`Fichier(s) trop volumineux: ${fileNames}`);
        return;
      }
      
      const file: File|null = filesArray[0];
      setCurrentSelectedFile(file);
      // Appel de la fonction de callback avec les fichiers valides
      if(file != null)
        onFileSelected(file);
    },
    [onFileSelected, maxSize]
  );

  // Gestionnaires d'événements de drag and drop
  const handleDragEnter = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDragging) {
      setIsDragging(true);
    }
  }, [isDragging]);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      
      const { files } = e.dataTransfer;
      handleFileSelection(files);
    },
    [handleFileSelection]
  );

  // Gestionnaire pour le clic sur le bouton
  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  // Gestionnaire pour le changement de l'input file
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = e.target;
    handleFileSelection(files);
  };

  return (
    <div className="file-picker-container">
      <div
        className={`file-drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleButtonClick}
      >
        <div className="file-drop-content">
          <img className="upload-icon" src={uploadFileIcon} alt="" />
          
          <p className="desktop">
            {isDragging 
              ? 'Déposez les fichiers ici' 
              : 'Glissez-déposez vos fichiers ici ou cliquez pour parcourir (' + (accept.replace(/\./g, "").split(",").join(" • ")) + ')'}
          </p>
          <p className="mobile">
              Cliquez pour parcourir ({accept.replace(/\./g, "").split(",").join(" • ")})
          </p>

          {currentSelectedFile != null && (
            <p className="filepicker-text">
              Fichier sélectionné : {currentSelectedFile.name}
            </p>
          )}
        </div>
      </div>
      
      {error && <div className="file-error-message">{error}</div>}
      
      <input
        type="file"
        ref={fileInputRef}
        className="file-input"
        accept={accept}
        multiple={false}
        onChange={handleInputChange}
      />
    </div>
  );
};

export default FilePicker;