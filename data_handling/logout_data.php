<?php

// Supprimer le cookie pour toutes les pages (mettre une durée de time() signifie que la durée du cookie est à 0 seconde).
setcookie('pseudo', '', time(), '/');
header('Location: ../' . $_GET['redirectTo']);
exit();