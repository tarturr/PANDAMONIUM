<style>
@font-face {
    font-family: 'ArchivoBlack';
    src: url('assets/font/ArchivoBlack-Regular.ttf');
}
.cookie-higher-part {
    height: 60%;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}
.cookie-container {
    top: 25vh;
    left: 20vw;
    height: 50vh;
    width: 60vw;
    display: flex;
    justify-content: space-evenly;
    flex-direction: column;
    align-items: center;
    position: fixed;
    z-index: 10;
    background-color: #EEE;
    border-radius: 25px;
    overflow: hidden;
}
.cookie-buttons {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}
.cookie-image {
    width: 10vw;
}
.cookie-text-main {
    width: 40vw;
    font-size: 30px;
    font-family: 'ArchivoBlack';
}
.cookie-text {
    font-family: 'ArchivoBlack';
    font-size: 25px;
}
.cookie-link {
    text-decoration: none;
    font-family: 'ArchivoBlack';
    font-size: 15px;
}
#privacy-policy {
    color: #b62000;
}
#accept-cookies {
    color: #1e8532;
}
@media screen and (max-width: 768px) {
    .cookie-container {
        overflow: scroll;
    }
}
</style>
<div class="cookie-container">
    <div class="cookie-higher-part">
        <img src="assets/img/cookie-yummy.jpg" alt="Illustration pour 'Cookie délicieux :p'" class="cookie-image">
        <p class="cookie-text-main">En poursuivant votre navigation sur ce site, vous acceptez que nous recueillions quelques cookies pour nous permettre de vous fournir une expérience optimale.</p>
    </div>
    <p class="cookie-text">En <strong>aucun cas</strong> vos données ne sont utilisées à des fins commerciales.</p>
    <div class="cookie-buttons">
        <a href="#" class="button bold cookie-link" id="privacy-policy">Voir la politique de confidentialité</a>
        <a href="<?= 'accept_cookies.php?redirection=' . $pageName ?>" class="button thin cookie-link" id="accept-cookies">J'accepte - Poursuivre ma navigation</a>
    </div>
</div>