param([string]$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path)
$ErrorActionPreference='Stop'
$base=Join-Path $ProjectRoot 'data/h_orac_stage25b'
$pub=Import-Csv (Join-Path $base 'stage25b/Stage25B_HORAC_Publication_Screening.csv')
$summary=Import-Csv (Join-Path $base 'stage25b/Stage25B_HORAC_Candidate_Summary.csv')
$rank=Import-Csv (Join-Path $base 'stage25b/Stage25B_HORAC_Quantitative_Ranking.csv')
$raw=Import-Csv (Join-Path $base '_working/EuropePMC_Discovery_Raw.csv')

$rankMap=@{};foreach($r in $rank){$rankMap[$r.candidate_id]=[int]$r.rank}
$summaryMap=@{};foreach($s in $summary){$summaryMap[$s.candidate_id]=$s}
$abstractMap=@{};foreach($r in $raw){$key="$($r.candidate_id)|$($r.DOI.ToLowerInvariant())|$($r.PMID)|$($r.source_id)";if(!$abstractMap.ContainsKey($key)){$abstractMap[$key]=$r.abstract}}

$out=[System.Collections.Generic.List[object]]::new()
foreach($p in ($pub|Where-Object method_screen_status -eq 'PENDING_FULL_TEXT_ADJUDICATION')){
  $s=$summaryMap[$p.candidate_id];$cr=if($rankMap.ContainsKey($p.candidate_id)){$rankMap[$p.candidate_id]}else{$null}
  $key="$($p.candidate_id)|$($p.DOI.ToLowerInvariant())|$($p.PMID)|$($p.publication_id)"
  $abs=if($abstractMap.ContainsKey($key)){$abstractMap[$key]}else{''};$txt=("$($p.title) $abs")
  $quant=if($txt -match '(?i)(\d+(?:\.\d+)?\s*(?:±|\+/-)\s*\d|µmol\s*TE|umol\s*TE|Trolox equivalent|mol\s*TE)'){'likely'}elseif($txt -match '(?i)ORAC value|ORAC activit|oxygen radical absorbance capacity'){'possible'}else{'unclear'}
  $method=if($txt -match '(?i)AAPH' -and $txt -match '(?i)fluorescein' -and $txt -match '(?i)Trolox'){'strong H-ORAC-FL signal'}elseif($txt -match '(?i)ORAC-FL|ORAC fluorescence|ORAC-fluorescence'){'probable ORAC-FL'}elseif($txt -match '(?i)ORAC|oxygen radical absorbance capacity'){'ORAC variant unresolved'}else{'weak'}
  $potentialTier=if($method -eq 'strong H-ORAC-FL signal' -and $quant -ne 'unclear'){'A/B1/B2 pending full text'}elseif($method -in @('strong H-ORAC-FL signal','probable ORAC-FL')){'B1/B2/X pending full text'}else{'C/X or eligible pending method identity'}
  $isCutoff=($cr -and $cr -ge 15 -and $cr -le 25)
  $isFragile=([int]$s.independent_eligible_experiment_N -le 1 -or $s.evidence_confidence -eq 'Low' -or $s.heterogeneity_flag -eq 'HIGH_HETEROGENEITY')
  $isConditional=($s.Stage25B_status -eq 'Conditional')
  $uncertainty=($txt -match '(?i)figure|unit|isomer|glycoside|aglycone|solvent|cyclodextrin|fluorescen|absorb|quench|aggregation|duplicate')
  if($isCutoff){$tier='Priority 1'}elseif($uncertainty -and ($cr -and $cr -le 25)){$tier='Priority 2'}elseif($isFragile){$tier='Priority 3'}elseif($isConditional){$tier='Priority 4'}else{$tier='Priority 5'}
  $effects=[System.Collections.Generic.List[string]]::new();if($isCutoff){$effects.Add('direct rank 15–25 membership/cutoff effect')};if($isFragile){$effects.Add('median/confidence/heterogeneity sensitive')};if($isConditional){$effects.Add('Conditional method-QC effect')};if($quant -ne 'unclear'){$effects.Add('quantitative value may be extractable')}
  $reason=if($effects.Count){$effects -join '; '}else{'outside current cutoff and no metadata signal of immediate rank impact'}
  $out.Add([pscustomobject]@{
    candidate=$p.canonical_name;candidate_id=$p.candidate_id;current_provisional_H_ORAC_rank=$cr;current_candidate_median=$s.median_H_ORAC_mol_TE_per_mol;current_eligible_experiment_N=$s.independent_eligible_experiment_N;current_confidence=$s.evidence_confidence;current_Stage25B_status=$s.Stage25B_status
    publication_id=$p.publication_id;DOI=$p.DOI;PMID=$p.PMID;title=$p.title;full_text_available=$p.full_text_available
    potential_H_ORAC_relevance=$method;potential_quantitative_value=$quant;potential_eligibility_tier=$potentialTier;potential_effect_on_candidate_median=if($isFragile -or $quant -ne 'unclear'){'possible'}else{'low/unknown'};potential_effect_on_evidence_confidence=if([int]$s.independent_eligible_experiment_N -le 2){'possible upgrade if independent eligible'}else{'limited unless method/independence changes'};potential_effect_on_Top20_membership=if($isCutoff){'direct'}elseif($cr -and $cr -le 30){'possible'}elseif($quant -eq 'likely'){'possible if large value'}else{'low/unknown'};priority_tier=$tier;reason=$reason;adjudication_status='PENDING_PRIORITY_REVIEW'
  })
}
$path=Join-Path $base 'stage25b1/Stage25B1_FullText_Adjudication_Priority.csv'
$out|Sort-Object @{Expression={switch($_.priority_tier){'Priority 1'{1}'Priority 2'{2}'Priority 3'{3}'Priority 4'{4}default{5}}}},current_provisional_H_ORAC_rank,candidate,title|Export-Csv $path -NoTypeInformation -Encoding utf8
$out|Group-Object priority_tier|Sort-Object Name|Select-Object Name,Count|Format-Table -AutoSize
Write-Output "TOTAL=$($out.Count)"
