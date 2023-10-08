<?php

require 'user_data_manager.php';

class Utilisateur implements UserDataManager {
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

    public static function fetchFromPseudo($pseudo, $connection): ?Utilisateur {
        $query = $connection->get()->prepare('SELECT * FROM utilisateur WHERE pseudo = :pseudo');

        $query->bindParam(':pseudo', $pseudo);
        $query->execute();
        $result = $query->fetch();

        foreach ($result as $row) {
            return new Utilisateur(
                $connection,
                $row['pseudo'],
                $row['email'],
                $row['mot_de_passe'],
                $row['date_naiss'],
                $row['date_enregistre'],
                $row['date_connecte'],
                (count($row['liste_amis']) > 0 ? explode(',', $row['liste_amis']) : array()),
                Profile::fetchFromPseudo($pseudo, $connection)
            );
        }

        return null;
    }

    public function createInDatabase(): bool {
        $sqlRequest = 'INSERT INTO utilisateur VALUES(:pseudo, :email, :mot_de_passe, :date_naiss, :date_enregistre, :date_connecte, NULL)';
        $request = $this->connection->get()->prepare($sqlRequest);

        return $request->execute([
            'pseudo'          => $this->pseudo,
            'email'           => $this->email,
            'mot_de_passe'    => $this->motDePasse,
            'date_naiss'      => $this->dateNaiss,
            'date_enregistre' => $this->dateEnregistre,
            'date_connecte'   => $this->dateConnecte
        ]);
//        $request->bindParam(':pseudo',          $data['pseudo']);
//        $request->bindParam(':email',           $data['email']);
//        $request->bindParam(':mot_de_passe',    $data['mot_de_passe']);
//        $request->bindParam(':date_naiss',      $data['date_naiss']);
//        $request->bindParam(':date_enregistre', $data['date_enregistre']);
//        $request->bindParam(':date_connecte',   $data['date_connecte']);
    }
}