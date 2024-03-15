<?php

require 'Profile.php';

class User extends DatabaseColumn {
    public $pseudo;
    public $email;
    public $motDePasse;
    public $dateNaiss;
    public $dateEnregistre;
    public $dateConnecte;
    public $listeAmis;
    public $profil;

    public function __construct($connection, $pseudo, $email, $motDePasse, $dateNaiss, $dateEnregistre, $dateConnecte, $listeAmis = array(), $profil = null) {
        parent::__construct($connection, "utilisateur");

        $this->pseudo = $pseudo;
        $this->email = $email;
        $this->motDePasse = $motDePasse;
        $this->dateNaiss = $dateNaiss;
        $this->dateEnregistre = $dateEnregistre;
        $this->dateConnecte = $dateConnecte;
        $this->listeAmis = $listeAmis;
        $this->profil = $profil;
    }

    public static final function fetchFrom($connection, $column) {
        $sqlRequest = 'SELECT * FROM utilisateur WHERE pseudo = :pseudo';
        $query = $connection->prepare($sqlRequest);

        $query->bindParam(':pseudo', $column);
        $query->execute();
        $result = $query->fetch();

        if ($result) {
            return new User(
                $connection,
                $result['pseudo'],
                $result['email'],
                $result['mot_de_passe'],
                $result['date_naiss'],
                $result['date_enregistre'],
                $result['date_connecte'],
                (strlen($result['liste_amis']) > 0 ? explode(',', $result['liste_amis']) : array()),
                Profile::fetchFrom($connection, $column)
            );
        }

        return null;
    }

    protected final function createImpl() {
        $sqlRequest = 'INSERT INTO utilisateur VALUES(:pseudo, :email, :mot_de_passe, :date_naiss, :date_enregistre, :date_connecte, :liste_amis)';
        $request = $this->prepare($sqlRequest);

        return $request->execute([
            'pseudo'          => $this->pseudo,
            'email'           => $this->email,
            'mot_de_passe'    => $this->motDePasse,
            'date_naiss'      => $this->dateNaiss,
            'date_enregistre' => $this->dateEnregistre,
            'date_connecte'   => $this->dateConnecte,
            'liste_amis'      => (count($this->listeAmis) > 0 ? explode(',', $this->listeAmis) : '')
        ]);
    }

    public function tryToConnect($password) {
        if ($password == $this->motDePasse) {
            $this->update(['date_connecte' => (new DateTime('now'))->format('Y-m-d H:i:s')]);
            return true;
        }

        return false;
    }
}