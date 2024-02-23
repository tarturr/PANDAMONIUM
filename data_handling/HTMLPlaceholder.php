<?php

require 'HTMLDisplay.php';
require_once 'common/common_functions.php';

class HTMLPlaceholder {
    private $pageName;
    private $displays;

    public function __construct($pageName, ...$displays) {
        $this->pageName = $pageName . '.php';
        $this->displays = $displays;

        if (!hasAcceptedCookies()) {
            (new CookieDisplay($this->pageName))->display();
        }
    }

    public function getPageName() {
        return $this->pageName;
    }

    public function display($key) {
        foreach ($this->displays as $display) {
            if (strcasecmp($key, $display->getKey()) == 0) {
                $display->display();
                return;
            }
        }

        throw new InvalidArgumentException('The "' . $key . '" does not exist in the ' . $this->pageName . ' html placeholder.');
    }
}