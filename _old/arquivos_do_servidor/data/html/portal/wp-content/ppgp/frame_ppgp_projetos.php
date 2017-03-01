<?php
require_once(__DIR__."/ClientAPIsistemas.php");
require_once(__DIR__."/OAuth2/Client.php");
require_once(__DIR__."/ClientStrictoSensu.php");
$strictoSensu = new ClientStrictoSensu(ClientStrictoSensu::COD_UNIDADE['ppgp']);
$projetos = $strictoSensu->projetos();
?>
<script type="text/javascript">function alternar(idDetalhes){ var objDetalhes = document.getElementById(idDetalhes);var isVisivel = objDetalhes.getAttribute("style") == ""; objDetalhes.setAttribute("style", (isVisivel ? "display: none" : ""));return false; }</script>
<ul id="lista-projetos" style="margin-left: 20%">
    <?php
    $anoAnterior = 0;
    foreach ($projetos as $projeto):
    ?>
    <?php if ($anoAnterior != $projeto['ano']): ?>
    <li style="list-style-type: none; color: #8e8e8e; background-color: #ecf0f1; padding-left: 20px;"><?php echo $anoAnterior = $projeto['ano']; ?></li>
    <?php endif; ?>
    <li id="projeto-<?php echo $projeto['idProjeto']; ?>" class="lista-projetos-item"><a class="lista-projetos-item-titulo" id="<?php echo $projeto['idProjeto']; ?>" onclick="return alternar('detalhes-<?php echo $projeto['idProjeto']; ?>')" href="#"><?php echo $projeto['titulo']; ?></a>
        <ul id="detalhes-<?php echo $projeto['idProjeto']; ?>" style="display: none">
            <li><strong>Código:</strong> <?php echo $projeto['codPrefixo'].$projeto['codNumero']."-".$projeto['codAno']; ?></li>
            <li><strong>Situação:</strong> <?php echo $projeto['situacaoProjeto']; ?></li>
            <li><strong>Início:</strong> <?php echo $projeto['dataInicio']; ?></li>
            <li><strong>Fim:</strong> <?php echo $projeto['dataFim']; ?></li>
            <li><strong>Palavras-chave:</strong> <?php echo $projeto['palavraChave']; ?></li>
            <li><strong>Área de Conhecimento:</strong> <?php echo $projeto['areaConhecimento']; ?></li>
            <li><strong>Grupo de Pesquisa:</strong> <?php echo $projeto['grupaPesquisa']; ?></li>
            <li><strong>Linha de Pesquisa:</strong> <?php echo $projeto['linhaPesquisa']; ?></li>
            <li><strong>Descrição:</strong> <?php echo $projeto['descricao']; ?></li>
            <li><strong>E-mail:</strong> <?php echo $projeto['email']; ?></li>
            <li><strong>Membros:</strong><ul><?php foreach ($projeto['membrosProjeto'] as $membro): ?> <li><?php echo $membro['nome']." (".$membro['caterogia'].", ".$membro['funcao'].")"; ?>)</li><?php endforeach; ?></ul>
            </li>
        </ul>
    </li>
    <br/>
    <?php endforeach; ?>
</ul>