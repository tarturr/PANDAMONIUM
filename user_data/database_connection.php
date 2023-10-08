<?php

class DatabaseConnection {
    private $connection;

    public function __construct($host = '0504-srv-sig', $user = 'nsi_eleve1', $password = 'eleve1', $databaseName = 'nsi_eleve1') {
        $this->connection = new PDO('mysql:host=' . $host . ';dbname=' . $databaseName, $user, $password);
        $this->connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    public function get(): PDO {
        return $this->connection;
    }
}