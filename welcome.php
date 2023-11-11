<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiscordIn - Bienvenue !</title>
    <link rel="stylesheet" href="assets/css/header-style.css">
    <link rel="stylesheet" href="assets/css/welcome-style.css">
    <script src="https://kit.fontawesome.com/3198643e95.js" crossorigin="anonymous"></script>
</head>
<body>
    <?php require 'header.php'; ?>

    <p>Salut à toi, <span style="color: blue">
            <?php
            $pseudo = $_COOKIE['pseudo'];
            echo $pseudo;

//            if (!isset($pseudo)) {
//                sendToPageWithError('login.php', 'Votre session a expiré. Veuillez vous reconnecter.');
//            } else {
//                echo $pseudo;
//            }
            ?>
        </span> !</p>
    <script src="assets/js/header-dynamic.js"></script>
</body>
</html>