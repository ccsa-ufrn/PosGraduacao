<?php

abstract class ClientOpenSIG
{
    /* endereços constantes */
    
    // raízes comuns
    const OAUTH_ROOT_DIR         = "OAuth2/"; // wrapper local de client oauth
    const API_URL_ROOT           = "http://apitestes.info.ufrn.br/"; // API de testes
    
    // links externos importantes
    const AUTHORIZATION_ENDPOINT = ClientOpenSIG::API_URL_ROOT . "authz-server/oauth/authorize";
    const TOKEN_ENDPOINT         = ClientOpenSIG::API_URL_ROOT . "authz-server/oauth/token";
    
    // raízes de serviços da opensig disponíveis
    const URL_SERVICE_ROOT = [
        'ensino'        => ClientOpenSIG::API_URL_ROOT."ensino-services/services/",
        'usuario'       => ClientOpenSIG::API_URL_ROOT."usuario-services/services/", // deprecated
        'stricto-sensu' => ClientOpenSIG::API_URL_ROOT."stricto-sensu-services/services/",
    ];
    
    
    /**
     * Client OAuth
     *
     * @var object
     */
    protected $client = null;
}