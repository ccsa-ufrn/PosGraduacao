<?php

require_once("ClientOpenSIG.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."Client.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."GrantType/IGrantType.php");
require_once(ClientOpenSIG::OAUTH_ROOT_DIR."GrantType/ClientCredentials.php");

/*
Classe de acesso fácil aos dados do PPGP recuperados do SIGAA.

README: swagger dos json na wiki da OpenSIG.
*/
class ClientPPGP extends ClientOpenSIG
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
     * Solicita ao servidor a lista da equipe do ppgp.
     *
     * @return array com todos a equipe conforme previsto no swagger
     */
    function equipe(){
        $url = ClientOpenSIG::URL_SERVICE_ROOT['stricto-sensu']."consulta/equipeprograma/".ClientPPGP::COD_PPGP;
        return $this->client->fetch($url)['result'];
    }
    
    /**
     * Solicita ao servidor a lista de discentes do ppgp.
     *
     * @return array com todos os discentes conforme previsto no swagger
     */
    function discentes(){
        $url = ClientOpenSIG::URL_SERVICE_ROOT['stricto-sensu']."consulta/discente/".ClientPPGP::COD_PPGP;
        return $this->client->fetch($url)['result'];
    }
    
    /**
     * Solicita ao servidor a lista de projetos do ppgp.
     *
     * @return array com todos os projetos conforme previsto no swagger
     */
    function projetos(){
        $url = ClientOpenSIG::URL_SERVICE_ROOT['stricto-sensu']."consulta/projeto/".ClientPPGP::COD_PPGP;
        return $this->client->fetch($url)['result'];
    }
    
    /**
     * Solicita ao servidor a lista de discentes e retorna somente os de um ano de ingresso específico.
     *
     * @param string ano em formato AAAA
     * @return array com todos os discentes (filtrados por ano) conforme previsto no swagger
     */
    function discentesPorAno($ano){
        $discentes = $this->discentes();
        $discentesFiltrados = array();
        
        foreach($discentes as $discente){
            $posicao = strpos($discente['matricula'], $ano); // a matricula indica o ano
            if (!($posicao === false) && $posicao == 0){ // encontrou e tá no início
                $discentesFiltrados[] = $discente;
            }
        }
        
        return $discentesFiltrados;
    }
    
    /**
     * Solicita ao servidor os dados de um docente encontrado por nome.
     *
     * @param string nome do docente em caracteres comuns
     * @return array com informações do docente conforme previsto no swagger
     */
    function docentePorNome($nome){
        $url = ClientOpenSIG::URL_SERVICE_ROOT['docente']."consulta/perfilnome/".urlencode($nome);
        $res = $this->client->fetch($url);
        //return $url;
        return var_dump($res);
    }
}