<?php

// endereços constantes
// raízes comuns
const OAUTH_ROOT_DIR         = "OAuth2/";
const API_URL_ROOT           = "http://apitestes.info.ufrn.br/"; // API de testes
// links externos importantes
const AUTHORIZATION_ENDPOINT = API_URL_ROOT.'authz-server/oauth/authorize';
const TOKEN_ENDPOINT         = API_URL_ROOT.'authz-server/oauth/token';
// raízes de serviços da opensig disponíveis
const URL_SERVICE_ROOT = [
    "ensino" => API_URL_ROOT."ensino-services/services/",
    "usuario" => API_URL_ROOT."usuario-services/services/"
];

// imports
require(OAUTH_ROOT_DIR.'Client.php');
require(OAUTH_ROOT_DIR.'GrantType/IGrantType.php');
require(OAUTH_ROOT_DIR.'GrantType/ClientCredentials.php');
require(OAUTH_ROOT_DIR.'GrantType/AuthorizationCode.php');

// construtor do client
$client = new OAuth2\Client();

// setting token
$token = $client->getAccessToken(TOKEN_ENDPOINT, OAuth2\Client::GRANT_TYPE_CLIENT_CREDENTIALS);
$client->setAccessToken($token['result']['access_token']);
$client->setAccessTokenType(OAuth2\Client::ACCESS_TOKEN_BEARER); // tipo requerido pela opensig

?>