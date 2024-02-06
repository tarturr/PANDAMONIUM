<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PANDEMONIUM - Bienvenue !</title>
    <link rel="stylesheet" href="assets/css/header-style.css">
    <link rel="stylesheet" href="assets/css/welcome-style.css">
    <script src="https://kit.fontawesome.com/3198643e95.js" crossorigin="anonymous"></script>
</head>
<body>
    <?php
    require 'header.php';
    require_once 'common/common_functions.php';
    ?>

    <?php if (isLogged()) { ?>
        <p>Salut à toi, <span style="color: blue"><?= $_COOKIE['pseudo'] ?></span> !</p>
    <?php } else { ?>
        <p>N'hésitez pas à vous connecter pour profiter de toutes les fonctionnalités du site web ! :)</p>
    <?php } ?>
</body>
</html>