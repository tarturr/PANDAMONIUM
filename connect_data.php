<?php

$connection = new DatabaseConnection('localhost', 'root', '');

$pseudo = $_POST['pseudo'];
$mdp = $_POST['mdp'];

$user = Utilisateur::fetchFromPseudo($pseudo, $connection);

if (!$user->tryToConnect($mdp)) {
    sendToPageWithError('connect.php', 'Le mot de passe entré est incorrect. Réessayez à nouveau.');
}

setcookie("connexion", $pseudo, time() + 60 * 60);
header('Location: welcome.php');
exit();