<?php

require '../user_data/User.php';
require '../common/common_functions.php';

$connection = establishDatabaseConnection();

$pseudo = $_POST['pseudo'];
$mdp = $_POST['mdp'];

$user = User::fetchFrom($connection, $pseudo);

if ($user == null) {
    sendToPageWithError('../login.php', 'Aucun utilisateur sous le nom de "' . $pseudo .
        '" n\'existe dans la base de données.');
}

if (!$user->tryToConnect($mdp)) {
    sendToPageWithError('../login.php', 'Le mot de passe entré est incorrect. Réessayez à nouveau.');
}

setcookie('pseudo', $pseudo, time() + 60 * 60, '/');
header('Location: ../welcome.php');
exit();