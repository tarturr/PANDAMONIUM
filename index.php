<?php
require_once 'data_handling/HTMLPlaceholder.php';
require_once 'common/common_functions.php';

$display = new HTMLPlaceholder('index');
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PANDEMONIUM - Accueil</title>
    <link rel="stylesheet" href="assets/css/header-style.css">
    <link rel="stylesheet" href="assets/css/index-style.css">
    <script src="https://kit.fontawesome.com/3198643e95.js" crossorigin="anonymous"></script>
</head>
<body>
    <?php require_once 'header.php'; ?>

    <section id="landing-page">
        <article class="presentation">
            <div class="text">
                <h1>Le réseau social des jeunes et étudiants.</h1>
                <p>
                    Créé en 2023, PANDEMONIUM est un réseau social utilisable par tous les lycéens souhaitant communiquer
                    entre eux et avoir un profil professionnel !
                </p>
            </div>

            <a href="#more" class="button thin">En savoir plus</a>
        </article>

        <img src="assets/img/jeunes.jpg" alt="Photo de jeunes sur leur écran.">
    </section>

    <img src="assets/img/wave.png" alt="" class="wave">
</body>
</html>