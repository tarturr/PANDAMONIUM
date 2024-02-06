<?php
require_once 'common/common_functions.php';
require_once 'data_handling/HTMLPlaceholder.php';

class NavbarDisplay extends HTMLDisplay {
    protected function displayIfLogged(): void { ?>
        <a href="profil.php" class="link"><i class="fa-solid fa-user"></i> <?= $_COOKIE['pseudo'] ?></a>
        <a href="data_handling/logout_data.php?redirectTo=welcome.php" class="btn">Se déconnecter <i class="fa-solid fa-arrow-right-from-bracket"></i></a>
    <?php }

    protected function displayIfNotLogged(): void { ?>
        <a href="login.php" class="btn"><i class="fa-solid fa-arrow-right-to-bracket"></i> Se connecter</a>
        <a href="register.php" class="link"><i class="fa-solid fa-user-plus"></i> S'enregistrer</a>
    <?php }
}

$placeHolder = new HTMLPlaceholder('header', array(new NavbarDisplay('navbar')));
?>

<header id="top-page">
    <div class="tool-bar">
        <a class="logo" href="/">
            <img src="assets/img/logo-no-icon.png" class="logo-text" alt="Logo de PANDEMONIUM sans l'icône">
            <img src="assets/img/icon.png" class="logo-icon" alt="Icône du logo PANDEMONIUM">
        </a>

        <nav id="tools">
            <a href="#">Qui sommes-nous ?</a>
            <a href="#">Nouveautés</a>
            <a href="#">Personnes</a>
            <a href="#">Serveurs populaires</a>
        </nav>
    </div>

    <hr>

    <div class="account">
        <?php $placeHolder->display('navbar'); ?>
    </div>
</header>

<script src="assets/js/header-dynamic.js"></script>