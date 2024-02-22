<?php

require 'HTMLDisplay.php';

class HTMLPlaceholder {
    private $pageName;
    private $displays;

    public function __construct($pageName, $displays) {
        $this->pageName = $pageName . '.php';
        $this->displays = $displays;
    }

    public function display($key): void {
        foreach ($this->displays as $display) {
            if (strcasecmp($key, $display->getKey()) == 0) {
                $display->display();
                return;
            }
        }

        throw new InvalidArgumentException('The "' . $key . '" does not exist in the ' . $this->pageName . ' html placeholder.');
    }
}