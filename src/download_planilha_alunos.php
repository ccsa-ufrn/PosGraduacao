<?php

$nomeFiltro = isset($_GET['ano']) ? $_GET['ano'] : 'Todos';

define('EOL', "<br/>");
define('URL_ROOT_DOWNLOAD', "localhost/OAuth2Client-OpenSIG-PHP/src/");
define('TITULO', "Alunos PPGP - $nomeFiltro");
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

$sheet = $objPHPExcel->setActiveSheetIndex(0);

// estilo das células - padrão
$styleCentralizado = array(
    'alignment' => array(
        'horizontal' => PHPExcel_Style_Alignment::HORIZONTAL_CENTER,
    )
);

$sheet->getDefaultStyle()->applyFromArray($styleCentralizado);

// estilo - largura das colunas
$sheet->getColumnDimension('A')->setWidth(15);
$sheet->getColumnDimension('B')->setWidth(60);
$sheet->getColumnDimension('C')->setWidth(40);
$sheet->getColumnDimension('D')->setWidth(30);
$sheet->getColumnDimension('E')->setWidth(30);

// estilo - cabeçalho
$sheet->getStyle('A1')->getFont()->setBold(true);
$sheet->getStyle('B1')->getFont()->setBold(true);
$sheet->getStyle('C1')->getFont()->setBold(true);
$sheet->getStyle('D1')->getFont()->setBold(true);
$sheet->getStyle('E1')->getFont()->setBold(true);

// povoamento - cabeçalho
$sheet->setCellValue("A1", 'Matrícula');
$sheet->setCellValue("B1", 'Nome');
$sheet->setCellValue("C1", 'E-mail');
$sheet->setCellValue("D1", 'Telefone');
$sheet->setCellValue("E1", 'Celular');

// povoamento - dados
$discentes = isset($_GET['ano']) ? $client->discentesPorAno($_GET['ano']) : $client->discentes();

foreach ($discentes as $key => $discente){
    $posY = $key + 2;

    $sheet->setCellValue("A$posY", $discente['matricula']);
    $sheet->setCellValue("B$posY", $discente['nome']);
    $sheet->setCellValue("C$posY", $discente['email']);
    $sheet->setCellValue("D$posY", 'TODO');
    $sheet->setCellValue("E$posY", 'TODO');
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
