<?php

require("access_token.php");

// exemplo
$retorno = $client->fetch(URL_SERVICE_ROOT['usuario']."usuario/mazuh/info");

var_dump($retorno);

/*
Foi observado que o usuário acima, por exemplo, não funciona. Deve haver
limitações de acesso na api de testes a serem descobertas.
*/

?>