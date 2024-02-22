<?php
setcookie('cookies_accepted', 'True', 0, '/');
header('Location: ' . $_GET['redirection']);
exit();