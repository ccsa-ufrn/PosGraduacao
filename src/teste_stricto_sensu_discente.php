<?php

/*
Lista todos os discentes do PPGP
TODO: ordenar por turma
*/

require("access_token.php");


$discentes = $client->fetch(URL_SERVICE_ROOT['stricto-sensu']."consulta/discente/1672")['result'];


echo "<table>";
foreach ($discentes as $keyDiscente => $discente){    
    echo "<tr>";
    foreach ($discente as $dado => $valor){
        //var_dump($discente);
        if ($dado != 'orientacoesAcademica'){
            echo "<td>$valor</td>";
        }
    }
    echo "<tr>";
}
echo "</table>";

?>