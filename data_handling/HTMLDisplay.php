<?php

require_once 'common/common_functions.php';

abstract class HTMLDisplay {
    private string $key;

    public function __construct($key) {
        $this->key = $key;
    }

    public function display(): void {
        isLogged() ? $this->displayIfLogged() : $this->displayIfNotLogged();
    }

    protected abstract function displayIfLogged();
    protected abstract function displayIfNotLogged();

    public function getKey(): string {
        return $this->key;
    }
}