<?php

require 'user_data/database_connection.php';
require 'user_data/utilisateur.php';

function sendToRegisterWithError($errorMessage) {
    header('Location: register.php?errorMessage=' . $errorMessage);
    exit();
}

$connection = new DatabaseConnection('localhost', 'root', '');

$dateFormatter = 'Y-m-d H:i:s';
$dateNow = new DateTime('now');
$strDateNow = $dateNow->format($dateFormatter);

$maxDate = $dateNow;
$maxDateInterval = new DateInterval('P15Y');
$maxDate->sub($maxDateInterval);

if (DateTime::createFromFormat($dateFormatter, $_POST['date_naiss']) > $maxDate) {
    sendToRegisterWithError('Vous êtes trop jeune pour accéder au site !<br/>Vous devez avoir 15 ans minimum.');
}

$utilisateur = new Utilisateur($connection, $_POST['pseudo'], $_POST['email'], $_POST['mot_de_passe'], $_POST['date_naiss'], $strDateNow, $strDateNow);

//$sqlRequest = 'INSERT INTO utilisateur
//    VALUES(:pseudo, :email, :mot_de_passe, :date_naiss, :date_enregistre, :date_connecte, NULL)';
//$request = $connection->get()->prepare($sqlRequest);
//
//$request->bindParam(':pseudo',          $_POST['pseudo']);
//$request->bindParam(':email',           $_POST['email']);
//$request->bindParam(':mot_de_passe',    $_POST['mot_de_passe']);
//$request->bindParam(':date_naiss',      $_POST['date_naiss']);
//$request->bindParam(':date_enregistre', $strDateNow);
//$request->bindParam(':date_connecte',   $strDateNow);

try {
    if (!$utilisateur->createInDatabase()) {
        sendToRegisterWithError("An error has occurred while sending data into the database.");
    } else {
        setcookie('pseudo', $utilisateur->pseudo, time() + 60 * 60);
        header('Location: welcome.php');
        exit();
    }
} catch (PDOException $error) {
    sendToRegisterWithError($error->getMessage());
}