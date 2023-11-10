<?php

require 'DatabaseColumn.php';

class Profile extends DatabaseColumn {
    public string $nom;
    public string $prenom;
    public string $description;
    public string $qualites;
    public string $defauts;
    public string $emailPro;
    public string $tel;
    public string $disponibilites;

    private string $pseudo;

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


    public static final function fetchFrom($connection, $column): ?Profile {
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

    protected final function createImpl(): bool {
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