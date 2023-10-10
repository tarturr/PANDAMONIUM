<?php

function sendToPageWithError($page, $errorMessage) {
    header('Location: ' . $page . '?errorMessage=' . $errorMessage);
    exit();
}