<?php

const OAUTH_ROOT = "OAuth2/";

require(OAUTH_ROOT.'Client.php');
require(OAUTH_ROOT.'GrantType/IGrantType.php');
require(OAUTH_ROOT.'GrantType/ClientCredentials.php');
require(OAUTH_ROOT.'GrantType/AuthorizationCode.php');

const REDIRECT_URI           = 'http://localhost/oauth-client/src/OAuth2/teste.php';
const AUTHORIZATION_ENDPOINT = 'http://apitestes.info.ufrn.br/authz-server/oauth/authorize';
const TOKEN_ENDPOINT         = 'http://apitestes.info.ufrn.br/authz-server/oauth/token';

$client = new OAuth2\Client();
$accessToken = $client->getAccessToken(TOKEN_ENDPOINT, OAuth2\Client::GRANT_TYPE_CLIENT_CREDENTIALS);

var_dump($accessToken);

?>