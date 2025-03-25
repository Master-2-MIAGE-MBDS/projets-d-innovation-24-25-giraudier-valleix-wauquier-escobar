import React from 'react';
import "./Home.css";

import mainLogo from '../assets/images/mainLogo.svg';

const Home: React.FC = () => {
  return (
    <div className='home'>
      <img className='home-main-logo' src={mainLogo} alt="Pic'Sign main logo" />

      <p className='home-text'>
          📌 Bienvenue sur Pic'sign !
          <br/>
          <br/>

          Pic’sign est l’outil idéal pour signer et authentifier vos images en toute simplicité. Que ce soit pour protéger vos créations, certifier l’origine d’un visuel ou garantir son intégrité, notre application vous permet d’ajouter une signature unique à vos fichiers PNG, JPG et BMP.
          <br/>
          <br/>
          🔹 Signez vos images en quelques clics
          <br/>
          🔹 Vérifiez l’authenticité d’une image signée
          <br/>
          🔹 Sécurisez vos fichiers avec une technologie fiable et efficace
          <br/>
          <br/>
          📷 Protégez vos images, assurez leur authenticité !
          <br/>
          <br/>
          Prêt à commencer ? Importez votre première image et signez-la dès maintenant dans l’onglet Signature ! 🚀
      </p>

    </div>
  );
};


export default Home;