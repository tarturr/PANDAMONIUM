<?php
require_once 'common/common_functions.php';
require_once 'data_handling/HTMLPlaceholder.php';

class NavbarDisplay extends HTMLDisplay {
    protected function displayIfLogged() { ?>
        <a href="profil.php" class="button thin"><i class="fa-solid fa-user"></i> <?= $_COOKIE['pseudo'] ?></a>
        <a href="data_handling/logout_data.php?redirectTo=welcome.php" class="button bold">Se déconnecter <i class="fa-solid fa-arrow-right-from-bracket"></i></a>
    <?php }

    protected function displayIfNotLogged() { ?>
        <a href="login.php" class="button bold"><i class="fa-solid fa-arrow-right-to-bracket"></i> Se connecter</a>
        <a href="register.php" class="button thin"><i class="fa-solid fa-user-plus"></i> S'enregistrer</a>
    <?php }
}

$placeHolder = new HTMLPlaceholder('header', new NavbarDisplay('navbar'));
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

    <button class="user-menu button bold"><i class="fa-solid fa-user"></i></button>

    <div class="account">
        <?php $placeHolder->display('navbar'); ?>
    </div>
</header>

<script src="assets/js/header-dynamic.js"></script>