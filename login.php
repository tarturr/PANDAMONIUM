<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiscordIn - Connexion</title>
</head>
<body>
    <h1>Se connecter à DiscordIn</h1>

    <form method="POST" action="data_handling/login_data.php" style="display: flex; flex-direction: column; height: 50vh; width: 20vw;">
        <input name="pseudo" type="text" placeholder="Entrez votre pseudo ou votre email" required>
        <input name="mdp" type="password" placeholder="Entrez votre mot de passe" required>
        <input type="submit" placeholder="Se connecter">
    </form>

    <?php if (isset($_GET['errorMessage'])) { ?>
        <p style="color: red">Erreur: <?= $_GET['errorMessage'] ?></p>
    <?php } ?>
</body>
</html>