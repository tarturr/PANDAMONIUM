<?php

require 'DatabaseColumn.php';

class Profile extends DatabaseColumn {
    public $nom;
    public $prenom;
    public $description;
    public $qualites;
    public $defauts;
    public $emailPro;
    public $tel;
    public $disponibilites;

    private $pseudo;

    public function __construct($connection, $nom, $prenom, $description, $qualites, $defauts, $emailPro, $tel, $disponibilites, $pseudo) {
        parent::__construct($connection, "profil");
        
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


    public static final function fetchFrom($connection, $column) {
        $sqlRequest = 'SELECT * FROM profil WHERE pseudo = :pseudo';
        $query = $connection->prepare($sqlRequest);

        $query->bindParam(':pseudo', $column);
        $query->execute();
        $result = $query->fetch();

        if ($result) {
            return new Profile(
                $connection,
                $result['nom'],
                $result['prenom'],
                $result['description'],
                $result['qualites'],
                $result['defauts'],
                $result['email_pro'],
                $result['tel'],
                $result['disponibilites'],
                $column
            );
        }

        return null;
    }

    protected final function createImpl() {
        $sqlRequest = 'INSERT INTO profil VALUES(:nom, :prenom, :description, :qualites, :defauts, :email_pro, :tel, :disponibilites, :pseudo)';
        $request = $this->prepare($sqlRequest);

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