<?php

/*
Lista todos os discentes do PPGP
TODO: ordenar por turma
*/
require_once("ClientOpenSIG.php");
require_once("ClientPPGP.php");

$clientPPGP = new ClientPPGP();
$discentes = $clientPPGP->discentes();

?>
<table style='text-align: center'>
    
    <tr>
        <th>#</th>
        <th>Matrícula</th>
        <th>Nome</th>
        <th>E-mail</th>
        <th>Nível</th>
        <th>Orientação</th>
        <th>Coorientação</th>
    </tr>
    
    <?php foreach ($discentes as $keyDiscente => $discente): ?>
    
    <tr>
        <td><?php echo $discente['idDiscente']; ?></td>
        <td><?php echo $discente['matricula']; ?></td>
        <td><?php echo $discente['nome']; ?></td>
        <td><?php echo $discente['email']; ?></td>
        <td><?php echo $discente['descricaoNivel']; ?></td>
        <td><?php echo $discente['orientacoesAcademica'][0]['nome']; ?></td>
        <td><?php
            if (isset($discente['orientacoesAcademica'][1])): 
                echo discente['orientacoesAcademica'][1]['nome'];
            else:
                echo "(Nenhuma)";
            endif; ?></td>
    </tr>
    
    <?php endforeach; ?>
    
</table>