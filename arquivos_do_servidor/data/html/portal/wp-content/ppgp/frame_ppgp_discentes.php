<?php
require_once(__DIR__."/ClientAPIsistemas.php");
require_once(__DIR__."/OAuth2/Client.php");
require_once(__DIR__."/ClientStrictoSensu.php");
$strictoSensu = new ClientStrictoSensu(ClientStrictoSensu::COD_UNIDADE['ppgp']);
$discentes = isset($_GET['ano']) ? $strictoSensu->discentesPorAno($_GET['ano']) : $strictoSensu->discentes();
?>
<script type="text/javascript">function alternar(idDetalhes){ var objDetalhes = document.getElementById(idDetalhes);var isVisivel = objDetalhes.getAttribute("style") == ""; objDetalhes.setAttribute("style", (isVisivel ? "display: none" : ""));return false; }</script>
<form method="get" action="https://ccsa.ufrn.br/portal/">
    <input type="hidden" name="page_id" value="6314" required/>
    <label for="inAno">Especificar busca por</label><input type="number" name="ano" id="inAno" step="1" min="1960" max="<?php echo date('Y'); ?>" placeholder="ano de ingresso" value="<?php echo $_GET['ano']; ?>" required="required"/><div> <span>e</span> <input type="submit" value="Filtrar" class="btn btn-primary"/> <span>ou</span> <a href="https://ccsa.ufrn.br/portal/?page_id=6314"><input type="button" value="Exibir todos" class="btn btn-success"/></a></div>
</form>
<br/><br/>
<?php if (count($discentes)): ?>
<ul style="margin-left: 250px">
    <?php foreach ($discentes as $discente): ?>
    <li>
        <a id="<?php echo $discente['idDiscente']; ?>" onclick="return alternar('detalhes-<?php echo $discente['idDiscente']; ?>')" href="#"> <?php echo $discente['nome']; ?> <small>(<?php echo $discente['matricula']; ?>)</small></a>
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
    <br/>
    <?php endforeach; ?>
</ul>
<?php else: ?>
<div>
    <p>Nada encontrado.</p>
</div>
<?php endif; ?>
