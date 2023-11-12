<?php require_once 'common/common_functions.php' ?>

<header id="top-page">
    <div class="tool-bar">
        <a class="logo" href="/"><img src="assets/img/logo.png" alt="Logo de DiscordIn"></a>

        <nav id="tools">
            <a href="#">Qui sommes-nous ?</a>
            <a href="#">Nouveautés</a>
            <a href="#">Personnes</a>
            <a href="#">Serveurs populaires</a>
        </nav>
    </div>

    <hr>

    <div class="account">
        <?php if (isLogged()) { ?>
            <a href="profil.php" class="link"><i class="fa-solid fa-user"></i> <?= $_COOKIE['pseudo'] ?></a>
            <a href="data_handling/logout_data.php?redirectTo=welcome.php" class="btn">Se déconnecter <i class="fa-solid fa-arrow-right-from-bracket"></i></a>
        <?php } else { ?>
            <a href="login.php" class="btn"><i class="fa-solid fa-arrow-right-to-bracket"></i> Se connecter</a>
            <a href="register.php" class="link"><i class="fa-solid fa-user-plus"></i> S'enregistrer</a>
        <?php } ?>
    </div>
</header>