<?php

/*
Lista todos os docentes do PPGP
TODO: 
- link do docente para sua página oficial, exemplo: https://sigaa.ufrn.br/sigaa/public/docente/portal.jsf?siape=1064645
- ou lattes
*/
require_once("ClientAPIsistemas.php");
require_once("ClientPPGP.php");

$ppgp = new ClientPPGP();
$equipe = $ppgp->equipe();

?>

<style type="text/css">
    #tabela-equipe{
        text-align: center;
    }
    
    #tabela-equipe tr{
        /*border-bottom: 1px solid black;*/
    }
    
    #tabela-equipe th{
        background-color: #ecf0f1;
    }
    
    #tabela-equipe td{
        padding-left: 13px;
        padding-right: 13px;
        padding-bottom: 7px;
    }
    
    #tabela-equipe .nome-professor{
        text-align: left;
    }
    
    
</style>

<h3>PPGP: Equipe</h3>
<hr/>

<table id="tabela-equipe">
    
    <tr>
        <th>Nome</th>
        <th>Vínculo</th>
        <th>Nível</th>
        <th>E-mail</th>
    </tr>
    
    <?php foreach ($equipe as $membro): ?>
    
    <tr id="<?php echo $membro['idEquipePrograma']; ?>">
        <td class="nome-professor">
            <?php echo $membro['nome']; ?>
            <?php if ($lattes=$ppgp->lattesDoDocentePorNome($membro['nome'])): ?>
            <a href="<?php echo $lattes; ?>" target="_blank"><img src="http://www.ufpa.br/ppba/images/lattes.gif" alt="CV Lattes"/></a><?php endif; ?>
        </td>
        <td><?php echo $membro['vinculo']; ?></td>
        <td><?php echo $membro['nivel']; ?></td>
        <td><?php echo $membro['email']; ?></td>
    </tr>
    
    <?php endforeach; ?>
    
</table>
