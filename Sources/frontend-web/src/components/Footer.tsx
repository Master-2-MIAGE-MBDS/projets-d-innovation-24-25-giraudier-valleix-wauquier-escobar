import "./Footer.css"

import univLogo from '../assets/images/univ.jpg';
import whiteLogo from '../assets/images/icon-white.svg';

const Footer: React.FC = () => {
  
    return (
      <div className="footer desktop">

          <div className="footer-section footer-sec1">
            <img className="footer-logo" src={whiteLogo} alt="" />
            © Copyright 2025
            </div>
          <div className="footer-sep"></div>
          <div className="footer-section footer-section-middle">
            
            <div className="footer-half">
              Projet réalisé par
              <div className="footer-section-middle-under">
                <div>
                  <li><b>Augustin Giraudier</b></li>
                  <li><b>Benjamin Valleix</b></li>
                </div>
                <div>
                  <li><b>Guillaume Wauquier</b></li>
                  <li><b>Quentin Escobar</b></li>
                </div>
              </div>
            </div>
            <div className="footer-half">
              Et encadré par<br />
              <b>M. Gregory Galli</b>
              <b>& M. Michel Syska</b>
            </div>

          </div>
          <div className="footer-sep"></div>
          <div className="footer-section footer-sec1">
            <img className="footer-univ-logo" src={univLogo} alt="" />
            <div>
              Projet réalisé dans le cadre des TPI <br />
              de la promotion <b>MIAGE MBDS</b> <br />
              à l'<b>université Nice Côte d'Azur</b> <br />
            </div>
          </div>


      </div>
    );
  };
  
  export default Footer;