<?php

require '../user_data/User.php';
require '../common/common_functions.php';

$connection = establishDatabaseConnection();

$dateFormatter = 'Y-m-d H:i:s';
$dateNow = new DateTime('now');
$strDateNow = $dateNow->format($dateFormatter);

$maxDate = $dateNow;
$maxDateInterval = new DateInterval('P15Y');
$maxDate->sub($maxDateInterval);

if (DateTime::createFromFormat($dateFormatter, $_POST['date_naiss']) > $maxDate) {
    sendToPageWithError('../register.php', 'Vous êtes trop jeune pour accéder au site !<br/>Vous devez avoir 15 ans minimum.');
}

$utilisateur = new User($connection, $_POST['pseudo'], $_POST['email'], $_POST['mot_de_passe'], $_POST['date_naiss'], $strDateNow, $strDateNow);

try {
    $utilisateur->create();
    setcookie('pseudo', $utilisateur->pseudo, time() + 60 * 60, '/');
    header('Location: ../welcome.php');
    exit();
} catch (PDOException $error) {
    $errorCode = $error->getCode();

    switch ($errorCode) {
        case 23000:
            sendToPageWithError('../register.php', 'Un utilisateur du nom de "' . $utilisateur->pseudo . '" existe déjà dans la base de données. Veuillez en choisir un autre.');
            break;
        default:
            sendToPageWithError('../register.php', $error->getMessage());
            break;
    }

}