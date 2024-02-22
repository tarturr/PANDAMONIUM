<?php

function sendToPageWithError($page, $errorMessage) {
    header('Location: ' . $page . '?errorMessage=' . $errorMessage);
    exit();
}

function establishDatabaseConnection($host = '0504-srv-sig', $user = 'nsi_eleve1', $password = 'eleve1', $databaseName = 'nsi_eleve1'): PDO {
    $connection = new PDO('mysql:host=' . $host . ';dbname=' . $databaseName, $user, $password);
    $connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    return $connection;
}

function hasAcceptedCookies() {
    return isset($_COOKIE['cookies_accepted']);
}

function isLogged(): bool {
    return isset($_COOKIE['pseudo']);
}