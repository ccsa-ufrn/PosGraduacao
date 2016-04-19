<?php

/*
Lista todos os projetos do PPGP
*/
require_once("ClientAPIsistemas.php");
require_once("ClientPPGP.php");

$ppgp = new ClientPPGP();
$projetos = $ppgp->projetos();
?>

<script type="text/javascript">
    /* Altera a visibilidade dos detalhes do obj clicado 
    PS: Gambiarra temporária */
    function alternar(obj){
        var idDetalhes = "detalhes-" + obj.getAttribute("id");
        var objDetalhes = document.getElementById(idDetalhes);
        
        var isVisivel = objDetalhes.getAttribute("style") == "";
        
        objDetalhes.setAttribute("style", (isVisivel ? "display: none" : ""));
        return false;
    }
</script>


<h3>PPGP: Projetos de Pesquisa</h3>
<hr/>

<ul id="lista-projetos">
    
    <?php
    $anoAnterior = 0;
    foreach ($projetos as $projeto):
    ?>
    
    <?php if ($anoAnterior != $projeto['ano']): ?>
    <li style="list-style-type: none; color: #fff; background-color: #2574A9; padding-left: 20px;"><?php echo $anoAnterior = $projeto['ano']; ?></li>
    <?php endif; ?>
    
    <li id="projeto-<?php echo $projeto['idProjeto']; ?>" class="lista-projetos-item">
        
        <a class="lista-projetos-item-titulo" id="<?php echo $projeto['idProjeto']; ?>" onclick="return alternar(this)" href="#"><?php echo $projeto['titulo']; ?></a>
        
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
            <li>
                <strong>Membros:</strong>
                <ul>
                    <?php foreach ($projeto['membrosProjeto'] as $membro): ?>
                    <li><?php echo $membro['nome']." (".$membro['caterogia'].", ".$membro['funcao'].")"; ?>)</li>
                    <?php endforeach; ?>
                </ul>
            </li>
        </ul>
        
    </li>
    <br/>
    <?php endforeach; ?>
    
</ul>