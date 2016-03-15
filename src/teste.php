<?php

require("access_token.php");

// Set token
$client->setAccessToken($accessToken['result']['access_token']);
$client->setAccessTokenType(OAuth2\Client::ACCESS_TOKEN_BEARER);

// formando URL
$matricula = "2016035305";
const ENSINO_ROOT = "http://apitestes.info.ufrn.br/ensino-services/services/consulta/";
const ENSINO_SERVICE = "discente/matricula/";

$retorno = $client->fetch(ENSINO_ROOT.ENSINO_SERVICE.$matricula);

var_dump($retorno);

?>