<?php
require_once(__DIR__."/ClientAPIsistemas.php");
require_once(__DIR__."/OAuth2/Client.php");
require_once(__DIR__."/ClientStrictoSensu.php");
$strictoSensu = new ClientStrictoSensu(ClientStrictoSensu::COD_UNIDADE['ppgp']);
$equipe = $strictoSensu->equipe();
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
            <?php if ($lattes=$strictoSensu->lattesDoDocentePorNome($membro['nome'])): ?>
            <a href="<?php echo $lattes; ?>" target="_blank"><img src="http://www.ufpa.br/ppba/images/lattes.gif" alt="CV Lattes"/></a><?php endif; ?>
        </td>
        <td><?php echo $membro['vinculo']; ?></td>
        <td><?php echo $membro['nivel']; ?></td>
        <td><?php echo $membro['email']; ?></td>
    </tr>
    <?php endforeach; ?>
</table>
