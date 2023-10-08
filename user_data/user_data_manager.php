<?php

interface UserDataManager {
    public static function fetchFromPseudo($pseudo, $connection);
    public function createInDatabase(): bool;
}