<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PANDEMONIUM - Inscription</title>
</head>
<body>

    <h1>S'inscrire</h1>

    <form action="data_handling/register_data.php" method="POST" style="display: flex; flex-direction: column; height: 50vh; width: 20vw;">
        <input name="pseudo" type="text" placeholder="Pseudo" required>
        <input name="email" type="email" placeholder="Email" required>
        <input name="mot_de_passe" type="password" placeholder="Mot de passe" required>
        <input name="date_naiss" type="date" placeholder="Date de naissance" required>
        <input type="submit" placeholder="S'inscrire">
    </form>

    <?php if (isset($_GET['errorMessage'])) { ?>
        <p style="color: red">Une erreur est survenue lors de l'envoi des informations dans la base de données.<br/>Erreur: <?= $_GET['errorMessage'] ?></p>
    <?php } ?>
    
</body>
</html>