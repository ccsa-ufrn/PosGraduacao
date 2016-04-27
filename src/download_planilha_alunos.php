<?php

define('EOL', "<br/>");
define('URL_ROOT_DOWNLOAD', "localhost/OAuth2Client-OpenSIG-PHP/src/");
define('TITULO', "Alunos PPGP");
define('DESCRICAO', "Lista de contatos de alunos do Programa de Pós-Graduação em Gestão Pública.");

/** Includes */
require_once dirname(__FILE__) . '/PHPExcel/PHPExcel.php';
require_once("ClientAPIsistemas.php");
require_once("ClientPPGP.php");

// objetos utilitários
$objPHPExcel = new PHPExcel();
$client = new ClientPPGP();

// propriedades
$objPHPExcel->getProperties()->setCreator("Mazuh")
    ->setLastModifiedBy("AssTec CCSA")
    ->setTitle(TITULO)
    ->setDescription(DESCRICAO);


// preenche células - cabeçalho
$objPHPExcel->setActiveSheetIndex(0)
            ->setCellValue("A1", 'Matrícula')
            ->setCellValue("B1", 'Nome')
            ->setCellValue("C1", 'E-mail')
            ->setCellValue("D1", 'Telefone')
            ->setCellValue("E1", 'Celular');

// preenche células - dados
$discentes = isset($_GET['ano']) ? $client->discentesPorAno($_GET['ano']) : $client->discentes();

foreach ($discentes as $key => $discente){
    $posY = $key + 2;

    $objPHPExcel->setActiveSheetIndex(0)
                ->setCellValue("A$posY", $discente['matricula'])
                ->setCellValue("B$posY", $discente['nome'])
                ->setCellValue("C$posY", $discente['email'])
                ->setCellValue("D$posY", 'TODO')
                ->setCellValue("E$posY", 'TODO');
}


// salva arquivo em formato excel (compatível com versão mínima de 2007)
/*
TODO: colocar em uma pasta temp/ ou outro diretório pra não virar bagunça.
(Meramente modificar o $arquivoLocal pra '/temp/arquivo.xlxs' não funciona,
será preciso checar ou modificar o código fonte da biblioteca.)
*/
$arquivoLocal = TITULO.'.xlsx';

echo date('H:i:s') , " Tentando escrever arquivo no formato Excel2007" , EOL;
echo "Arquivo $arquivoLocal" , EOL;

$objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel2007');
$objWriter->save($arquivoLocal);


// cabô!
echo date('H:i:s') , " Terminou de escrever arquivo" , EOL;
echo "Criado em " , getcwd() , EOL;

header("location: $arquivoLocal");

/*
TODO: script para apagar o arquivo depois de baixado, ele deve ser temporário
pra não acumular lixo no servidor.
*/
