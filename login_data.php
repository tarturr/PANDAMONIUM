<?php

require 'user_data/User.php';
require 'common/common_functions.php';

$connection = establishDatabaseConnection('localhost', 'root', '');

$pseudo = $_POST['pseudo'];
$mdp = $_POST['mdp'];

$user = User::fetchFrom($connection, $pseudo);

if (!$user->tryToConnect($mdp)) {
    sendToPageWithError('login.php', 'Le mot de passe entré est incorrect. Réessayez à nouveau.');
}

setcookie("connexion", $pseudo, time() + 60 * 60);
header('Location: welcome.php');
exit();