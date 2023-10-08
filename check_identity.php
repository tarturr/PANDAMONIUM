<?php

$user = 'nsi_eleve1';
$password = 'eleve1';
$connection = new PDO('mysql:host=0504-srv-sig;dbname=nsi_eleve1', $user, $password);
$connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$pseudo = $_POST['pseudo'];
$mdp = $_POST['mdp'];

$request = 'SELECT mot_de_passe FROM profil WHERE pseudo = "' . $pseudo . '"';
$verification = $connection->query('SELECT mot_de_passe FROM utilisateur WHERE pseudo = "' . $pseudo . '" OR email = "' . $pseudo . '"');
$pwd_bdd = null;

foreach ($verification as $row){
    $pwd_bdd = $row['mot_de_passe'];
}
echo $mdp;

if ($pwd_bdd == $mdp) {
    setcookie("connexion", $pseudo, time() + 60 * 60);
    header('Location: welcome.php');
    exit();
}
else {
    header('Location: connexion.html');
    exit();
}