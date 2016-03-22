<?php

/*
Lista todos os projetos do PPGP
*/
require_once("ClientOpenSIG.php");
require_once("ClientPPGP.php");

$ppgp = new ClientPPGP();
$projetos = $ppgp->projetos();
var_dump($projetos[0]);
?>

<h3>PPGP: Projetos de Pesquisa</h3>

<ul>
    
    <?php foreach ($projetos as $projeto): ?>
    
    <li id="<?php echo $projeto['idProjeto']; ?>">
        
        [<?php echo $projeto['ano']; ?>] <?php echo $projeto['titulo']; ?>
        <ul>
            <li>Ok</li>
        </ul>
        
    </li>
    
    <?php endforeach; ?>
    
</ul>