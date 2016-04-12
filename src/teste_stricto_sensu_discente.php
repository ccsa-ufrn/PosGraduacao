<?php

/*
Lista todos os discentes do PPGP
*/
require_once("ClientAPIsistemas.php");
require_once("ClientPPGP.php");

$clientPPGP = new ClientPPGP();
$discentes = isset($_GET['ano']) ? $clientPPGP->discentesPorAno($_GET['ano']) : $clientPPGP->discentes();

?>

<h3>PPGP: Discentes</h3>
<hr/>
    
<form method="get" action="prototipo_discentes.php">    
    <label for="inAno">Buscar alunos por</label>
    <input type="number" name="ano" id="inAno" step="1" min="1960" max="<?php echo date('Y'); ?>" placeholder="ano de ingresso" value="<?php echo $_GET['ano']; ?>" required="required"/>
    
    <input type="submit" value="Filtrar"/>
    <a href="prototipo_discentes.php"><input type="button" value="Todos"/></a>
</form>

<br/>

<?php if (count($discentes)): ?>

<table style="text-align: center">
    
    <tr>
        <th>Matrícula</th>
        <th>Nome</th>
        <th>Nível</th>
        <th>Orientação</th>
        <th>Coorientação</th>
    </tr>
    
    <?php foreach ($discentes as $discente): ?>
    
    <tr id="<?php echo $discente['idDiscente']; ?>">
        <td><?php echo $discente['matricula']; ?></td>
        <td><?php echo $discente['nome']; ?></td>
        <td><?php echo $discente['descricaoNivel']; ?></td>
        <td><?php
            if (isset($discente['orientacoesAcademica'][0])): 
                echo $discente['orientacoesAcademica'][0]['nome'];
            else:
                echo "(Nenhuma)";
            endif; ?></td>
        <td><?php
            if (isset($discente['orientacoesAcademica'][1])): 
                echo $discente['orientacoesAcademica'][1]['nome'];
            else:
                echo "(Nenhuma)";
            endif; ?></td>
    </tr>
    
    <?php endforeach; ?>
    
</table>

<?php else: ?>

<div>
    <p>Nada encontrado.</p>
</div>

<?php endif; ?>
