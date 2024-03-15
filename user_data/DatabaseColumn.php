<?php

abstract class DatabaseColumn {

    private $connection;
    private $table;

    protected function __construct($connection, $table) {
        $this->connection = $connection;
        $this->table = $table;
    }

    public final function create(): bool {
        try {
            $this->connection->beginTransaction();
            $success = $this->createImpl();
            $this->connection->commit();

            return $success;
        } catch (PDOException $e) {
            $this->connection->rollBack();
            return false;
        }
    }

    public final function update($data) {
        if (count($data) == 0) return true;

        try {
            $this->connection->beginTransaction();
            $success = $this->prepare($this->buildUpdateRequest($data))->execute($data);
            $this->connection->commit();

            return $success;
        } catch (PDOException $e) {
            $this->connection->rollBack();
            return false;
        }
    }

    private function buildUpdateRequest($data) {
        $sqlRequest = 'UPDATE ' . $this->table . ' SET ';
        $left = count($data);

        foreach ($data as $column => $value) {
            $sqlRequest .= $column . ' = :' . $column;
            $left--;

            if ($left > 0) {
                $sqlRequest .= ', ';
            }
        }

        return $sqlRequest;
    }

    protected final function prepare($sqlRequest) {
        return $this->connection->prepare($sqlRequest);
    }

    public static abstract function fetchFrom($connection, $column);
    protected abstract function createImpl();
}