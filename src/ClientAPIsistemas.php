<?php

abstract class ClientAPIsistemas
{
    /* endereços constantes */
    
    // raízes comuns
    const OAUTH_ROOT_DIR         = "OAuth2/"; // wrapper local de client oauth
    const API_URL_ROOT           = "http://apitestes.info.ufrn.br/"; // API de testes
    
    // links externos importantes
    const AUTHORIZATION_ENDPOINT = ClientAPIsistemas::API_URL_ROOT . "authz-server/oauth/authorize";
    const TOKEN_ENDPOINT         = ClientAPIsistemas::API_URL_ROOT . "authz-server/oauth/token";
    
    // raízes de serviços da APIsistemas disponíveis
    const URL_SERVICE_ROOT = [
        'ensino'        => ClientAPIsistemas::API_URL_ROOT."ensino-services/services/",
        'usuario'       => ClientAPIsistemas::API_URL_ROOT."usuario-services/services/", // deprecated
        'stricto-sensu' => ClientAPIsistemas::API_URL_ROOT."stricto-sensu-services/services/",
        'docente'       => ClientAPIsistemas::API_URL_ROOT."docente-services/services/",
    ];
    
    
    /**
     * Client OAuth
     *
     * @var object
     */
    protected $client = null;
}
