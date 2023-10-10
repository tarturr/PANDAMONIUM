<?php

require 'UserDataManager.php';

class Profile implements UserDataManager {
    public $nom;
    public $prenom;
    public $description;
    public $qualites;
    public $defauts;
    public $emailPro;
    public $tel;
    public $disponibilites;

    private $pseudo;
    private $connection;

    public function __construct($connection, $nom, $prenom, $description, $qualites, $defauts, $emailPro, $tel, $disponibilites, $pseudo) {
        $this->connection = $connection;
        $this->nom = $nom;
        $this->prenom = $prenom;
        $this->description = $description;
        $this->qualites = $qualites;
        $this->defauts = $defauts;
        $this->emailPro = $emailPro;
        $this->tel = $tel;
        $this->disponibilites = $disponibilites;
        $this->pseudo = $pseudo;
    }


    public static function fetchFromPseudo($pseudo, $connection): ?Profile {
        $query = $connection->get()->prepare('SELECT * FROM profil WHERE pseudo = :pseudo');

        $query->bindParam(':pseudo', $pseudo);
        $query->execute();
        $result = $query->fetch();

        foreach ($result as $row) {
            return new Profile(
                $connection,
                $row['nom'],
                $row['prenom'],
                $row['description'],
                $row['qualites'],
                $row['defauts'],
                $row['email_pro'],
                $row['tel'],
                $row['disponibilites'],
                $pseudo
            );
        }

        return null;
    }

    public function createInDatabase(): bool {
        $sqlRequest = 'INSERT INTO profil VALUES(:nom, :prenom, :description, :qualites, :defauts, :email_pro, :tel, :disponibilites, :pseudo)';
        $request = $this->connection->get()->prepare($sqlRequest);

        return $request->execute([
            'nom'            => $this->nom,
            'prenom'         => $this->prenom,
            'description'    => $this->description,
            'qualites'       => $this->qualites,
            'defauts'        => $this->defauts,
            'email_pro'      => $this->emailPro,
            'tel'            => $this->tel,
            'disponibilites' => $this->disponibilites,
            'pseudo'         => $this->pseudo
        ]);
    }
}