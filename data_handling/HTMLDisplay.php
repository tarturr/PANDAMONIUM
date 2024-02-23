<?php

require_once 'common/common_functions.php';

abstract class HTMLDisplay {
    private $key;

    public function __construct($key) {
        $this->key = $key;
    }

    public function display() {
        isLogged() ? $this->displayIfLogged() : $this->displayIfNotLogged();
    }

    protected abstract function displayIfLogged();
    protected abstract function displayIfNotLogged();

    public function getKey() {
        return $this->key;
    }
}


class CookieDisplay extends HTMLDisplay {
    private $pageName;

    function __construct($pageName) {
        parent::__construct('accept_cookies');
        $this->pageName = $pageName;
    }

    protected function displayIfLogged() {
        $this->displayIfNotLogged();
    }

    protected function displayIfNotLogged() {
        $pageName = $this->pageName;
        require_once 'cookie.php';
        ?>

        <style>
            .to-blur {
                filter: blur(5px);
            }
        </style>

        <?php
    }
}