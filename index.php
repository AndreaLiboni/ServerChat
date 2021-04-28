<?php
$json_resp = json_decode(file_get_contents("http://ergast.com/api/f1/current/last/qualifying.json"))->MRData->RaceTable->Races[0]->QualifyingResults;
$json_grid = [];

for ($i=0; $i < 20; $i++) { 
    $line = array("P"=>$i+1, "num_pilota"=>$json_resp[$i]->number, "tempo"=>$json_resp[$i]->Q1);
    array_push($json_grid, $line);
}

echo json_encode($json_grid);
?>