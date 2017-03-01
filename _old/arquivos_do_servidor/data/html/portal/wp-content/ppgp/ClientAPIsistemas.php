<?php

abstract class ClientAPIsistemas
{
    /* endereços constantes */
    
    // raízes comuns
    const LOCAL_ROOT             = "https://ccsa.ufrn.br/portal/wp-content/ppgp/"; // diretório deste app
    const OAUTH_ROOT_DIR         = ClientAPIsistemas::LOCAL_ROOT . "OAuth2/"; // wrapper local de client oauth
    
    // links externos importantes pro oauth
    const API_URL_ROOT           = "http://apitestes.info.ufrn.br/"; // API externa de testes
    const AUTHORIZATION_ENDPOINT = ClientAPIsistemas::API_URL_ROOT . "authz-server/oauth/authorize"; // auth
    const TOKEN_ENDPOINT         = ClientAPIsistemas::API_URL_ROOT . "authz-server/oauth/token"; // token
    
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
