<?php

require_once("ClientOpenSIG.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."Client.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."GrantType/IGrantType.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."GrantType/ClientCredentials.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."GrantType/AuthorizationCode.php");

/*
Classe de acesso fácil aos dados do PPGP recuperados do SIGAA.

README: swagger dos json na wiki da OpenSIG.
*/
class ClientPPGP
{
    /* Identificação única da unidade do programa, dado coletado manualmente via busca do SIGAA. */
    const COD_PPGP = '1672';
    
    /**
     * Construct
     * Configura um client oauth para acessar o stricto-sensu service da OpenSIG.
     *
     * @return void
     */
    function __construct()
    {
        $client = new OAuth2\Client(); // wrapper terceiro
        
        $token = $client->getAccessToken(ClientOpenSIG::TOKEN_ENDPOINT, OAuth2\Client::GRANT_TYPE_CLIENT_CREDENTIALS);
        $client->setAccessToken($token['result']['access_token']);
        $client->setAccessTokenType(OAuth2\Client::ACCESS_TOKEN_BEARER); // requerido pela opensig
        
        $this->client = $client; // atributo
    }
    
    
    /**
     * Construct
     * Configura um client oauth para acessar o stricto-sensu service da OpenSIG.
     *
     * @return array com todos os discentes conforme previsto no swagger
     */
    function discentes(){
        $url = ClientOpenSIG::URL_SERVICE_ROOT['stricto-sensu']."consulta/discente/".ClientPPGP::COD_PPGP;
        return $this->client->fetch($url)['result'];
    }
}