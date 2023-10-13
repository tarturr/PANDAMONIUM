<?php

require 'Profile.php';

class User implements UserDataManager {
    public $pseudo;
    public $email;
    public $motDePasse;
    public $dateNaiss;
    public $dateEnregistre;
    public $dateConnecte;
    public $listeAmis;
    public $profil;

    private $connection;

    public function __construct($connection, $pseudo, $email, $motDePasse, $dateNaiss, $dateEnregistre, $dateConnecte, $listeAmis = array(), $profil = null) {
        $this->pseudo = $pseudo;
        $this->email = $email;
        $this->motDePasse = $motDePasse;
        $this->dateNaiss = $dateNaiss;
        $this->dateEnregistre = $dateEnregistre;
        $this->dateConnecte = $dateConnecte;
        $this->listeAmis = $listeAmis;
        $this->profil = $profil;

        $this->connection = $connection;
    }

    public static function fetchFromPseudo($pseudo, $connection): ?User {
        $query = $connection->prepare('SELECT * FROM utilisateur WHERE pseudo = :pseudo');

        $query->bindParam(':pseudo', $pseudo);
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
                Profile::fetchFromPseudo($pseudo, $connection)
            );
        }

        return null;
    }

    public function createInDatabase(): bool {
        $sqlRequest = 'INSERT INTO utilisateur VALUES(:pseudo, :email, :mot_de_passe, :date_naiss, :date_enregistre, :date_connecte, :liste_amis)';
        $request = $this->connection->prepare($sqlRequest);

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

    public function update($data): bool {
        if (count($data) == 0) return true;

        $strRequest = 'UPDATE utilisateur SET ';
        $left = count($data);

        foreach ($data as $column => $value) {
            $strRequest = $strRequest . $column . ' = :' . $column;
            $left--;

            if ($left > 0) {
                $strRequest = $strRequest . ', ';
            }
        }

        $request = $this->connection->prepare($strRequest);
        return $request->execute($data);
    }

    public function tryToConnect($password): bool {
        if ($password == $this->motDePasse) {
            $this->update(['date_connecte' => (new DateTime('now'))->format('Y-m-d H:i:s')]);
            return true;
        }

        return false;
    }
}