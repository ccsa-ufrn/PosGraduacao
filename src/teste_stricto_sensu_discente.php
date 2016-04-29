<?php

/*
Lista todos os discentes do PPGP
*/
require_once("ClientAPIsistemas.php");
require_once("ClientPPGP.php");

$clientPPGP = new ClientPPGP();
$discentes = isset($_GET['ano']) ? $clientPPGP->discentesPorAno($_GET['ano']) : $clientPPGP->discentes();

?>

<script type="text/javascript" src="alternar-visibilidades.js"></script>

<h3>PPGP: Discentes</h3>
<hr/>

<form method="get" action="prototipo_discentes.php">    
    <label for="inAno">Especificar busca por</label>
    <input type="number" name="ano" id="inAno" step="1" min="1960" max="<?php echo date('Y'); ?>" placeholder="ano de ingresso" value="<?php echo $_GET['ano']; ?>" required="required"/>

    <div>
        <span>e</span>
        <input type="submit" value="Filtrar" class="btn btn-primary"/>
        <span>ou</span>
        <a href="prototipo_discentes.php"><input type="button" value="Exibir todos" class="btn btn-success"/></a>
    </div>

</form>

<br/>

<?php if (count($discentes)): ?>

<?php foreach ($discentes as $discente): ?>

<ul>
    <li>
        <a id="<?php echo $discente['idDiscente']; ?>" onclick="return alternar('detalhes-<?php echo $discente['idDiscente']; ?>')" href="#">
            <?php echo $discente['nome']; ?> <small>(<?php echo $discente['matricula']; ?>)</small>
        </a>

        <ul id="detalhes-<?php echo $discente['idDiscente']; ?>" style="display: none">
            <li><strong>Nível:</strong> <?php echo $discente['descricaoNivel']; ?></li>

            <?php if (isset($discente['orientacoesAcademica'][0])): ?>
            <li><strong>Orientação:</strong> <?php echo $discente['orientacoesAcademica'][0]['nome']; ?></li>
            <?php endif; ?>

            <?php if (isset($discente['orientacoesAcademica'][1])): ?>
            <li><strong>Coorientação:</strong> <?php echo $discente['orientacoesAcademica'][1]['nome']; ?></li>
            <?php endif; ?>
        </ul>
    </li>
</ul>

<?php endforeach; ?>

<br/>

<p>Se você tiver autorização, poderá <a href="download_planilha_alunos.php<?php
    if (isset($_GET['ano'])):
    echo '?ano='.$_GET['ano']; 
    endif; ?>" target="_blank">baixar esta lista</a>.</p>
<p>Durante a fase de testes, o download é livre, pois os dados privados estão ocultos.</p>

<?php else: ?>

<div>
    <p>Nada encontrado.</p>
</div>

<?php endif; ?>
