param([string]$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path)
$ErrorActionPreference='Stop'
$base=Join-Path $ProjectRoot 'data/h_orac_stage25b'
$priorityPath=Join-Path $base 'Stage25B1_FullText_Adjudication_Priority.csv'
$pubPath=Join-Path $base 'Stage25B_HORAC_Publication_Screening.csv'
$priority=Import-Csv $priorityPath
$pub=Import-Csv $pubPath

$decisions=@(
  @{batch='Batch 1';priority='Priority 1';doi='10.1089/jmf.2009.0024';candidates='Sinapic acid; Luteolin; Ferulic acid; p-Coumaric acid';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='Publisher PDF returned 403 and browser reached a Cloudflare security challenge; abstract confirms ORAC-FL but exact values and full methods are unavailable.';rank='Potentially rank-changing across four cutoff candidates; unresolved.'},
  @{batch='Batch 1';priority='Priority 1';doi='10.1021/jf0208132';candidates='Sinapic acid; p-Coumaric acid; Ferulic acid; Chlorogenic acid';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='Abstract/citation recovered but probe, exact ORAC values, units and compound-level source locations could not be verified from primary full text.';rank='Potentially rank-changing for rank 15–24 candidates; unresolved.'},
  @{batch='Batch 1';priority='Priority 1';doi='10.1016/j.jfca.2013.09.007';candidates='Myricetin';outcome='ASSAY_INCOMPATIBLE';tier='C';reason='Title and source identify a pyrogallol-red ORAC assay in acidic medium, not the frozen fluorescein H-ORAC construct.';rank='No primary-rank effect.'},
  @{batch='Batch 1';priority='Priority 1';doi='10.3164/jcbn.11-21';candidates='Myricetin; Epigallocatechin';outcome='ASSAY_INCOMPATIBLE';tier='C';reason='ORAC-EPR endpoint and cyclodextrin-solubilized system are not ORAC-FL.';rank='No primary-rank effect.'},
  @{batch='Batch 1';priority='Priority 1';doi='10.1016/j.foodchem.2009.05.061';candidates='Myricetin';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='OpenAlex identified an institutional open-access URL, but the handle no longer resolved; exact free-flavonol and HPβCD values could not be verified.';rank='Could change rank 22 median/heterogeneity; unresolved.'},
  @{batch='Batch 1';priority='Priority 1';doi='10.1016/j.foodres.2010.06.006';candidates='Epigallocatechin';outcome='QUANTITATIVE_VALUE_NOT_EXTRACTABLE';tier='X';reason='Primary article methods and assay identity were visible, but the numerical ORAC-FL table remained inaccessible; cyclodextrin conditions are rank-relevant.';rank='Could change rank 23; unresolved.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.3390/foods10081807';candidates='Eugenol';outcome='ELIGIBLE_PRIMARY';tier='B1';reason='Pure ≥99% compound; AAPH-fluorescein-Trolox, PBS pH 7, 37 °C, multi-concentration kinetic AUC; 2.12 ± 0.08 mol TE/mol, N=3.';rank='New rankable Low-confidence candidate below Top20 cutoff; no membership change.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.3390/foods10081807';candidates='Capsaicin';outcome='ELIGIBLE_PRIMARY';tier='B1';reason='Pure ≥95% compound; AAPH-fluorescein-Trolox, PBS pH 7, 37 °C, multi-concentration kinetic AUC; 1.60 ± 0.25 mol TE/mol, N=3.';rank='New rankable Low-confidence candidate below Top20 cutoff; no membership change.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.3390/foods10081807';candidates='Vanillin';outcome='ELIGIBLE_PRIMARY';tier='B1';reason='Pure ≥97% compound; AAPH-fluorescein-Trolox, PBS pH 7, 37 °C, multi-concentration kinetic AUC; 1.81 ± 0.19 mol TE/mol, N=3.';rank='New rankable Low-confidence candidate below Top20 cutoff; no membership change.'},
  @{batch='Batch 2';priority='Priority 2';doi='10.3390/pharmaceutics14102141';candidates='Baicalein';outcome='B2_MAINTAINED_AFTER_SECOND_REVIEW';tier='B2';reason='Core ORAC-FL method and 5.41 ± 0.33 mol TE/mol confirmed, but chromophore-specific optical blank/correction and decisive solvent/aggregation QC remain absent.';rank='Baicalein alone would replace Ferulic acid at the primary Top20 cutoff if B2 were admitted; B2 remains excluded.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.1021/jf403265b';candidates='Tyrosol';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='Abstract reports 0.83 ± 0.03 without HPβCD and 1.20 ± 0.11 with 0.8 mM HPβCD, but complete primary methods and independence/solvent details were not recovered.';rank='Values are below current cutoff; may change rankable N and confidence, not current Top20 membership.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.1016/j.bbagen.2010.11.004';candidates='Vanillin';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='Primary abstract confirms strong AAPH-derived ORAC activity but provides no exact value or complete ORAC-FL method.';rank='Could alter Vanillin median but current exact value is unavailable.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.1080/09168451.2016.1240606';candidates='Pterostilbene';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='Abstract confirms aglycone comparison but exact pterostilbene value, probe and conversion details were not recovered.';rank='Potential rankable candidate; unresolved.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.1016/j.foodchem.2010.11.092';candidates='Sesamol';outcome='SOURCE_NOT_RECOVERED';tier='X';reason='A public PDF endpoint had an invalid certificate and could not be safely opened; existing source confirms an assay but Sesamol exact table value was not recovered.';rank='Potential rankable candidate; unresolved.'},
  @{batch='Batch 2';priority='Priority 4';doi='10.3762/bjoc.11.151';candidates='Curcumin';outcome='QUANTITATIVE_VALUE_NOT_EXTRACTABLE';tier='X';reason='Open full text uses ORAC-FL for related compounds, but its experimental table does not report an original curcumin quantitative value.';rank='No Curcumin value added; no rank effect.'}
)

$log=for($i=0;$i -lt $decisions.Count;$i++){
  $d=$decisions[$i]
  [pscustomobject]@{adjudication_id=('S25B1-ADJ-{0:D3}' -f ($i+1));batch=$d.batch;priority_tier=$d.priority;candidate=$d.candidates;DOI=$d.doi;PMID='';selection_reason='Rank-relevant cutoff, B2/X, fragile-evidence or Conditional-candidate priority';full_text_retrieval_status=if($d.outcome -match 'SOURCE_NOT_RECOVERED'){'not recovered'}elseif($d.outcome -match 'QUANTITATIVE_VALUE_NOT_EXTRACTABLE'){'full/partial primary source assessed'}else{'primary source assessed'};assay_identity=$d.outcome;quantitative_value=if($d.doi -eq '10.3390/foods10081807'){switch($d.candidates){'Eugenol'{'2.12 ± 0.08'}'Capsaicin'{'1.60 ± 0.25'}'Vanillin'{'1.81 ± 0.19'}}}elseif($d.candidates -eq 'Baicalein'){'5.41 ± 0.33'}else{''};unit=if($d.doi -in @('10.3390/foods10081807','10.3390/pharmaceutics14102141')){'mol TE/mol'}else{''};adjudicated_tier=$d.tier;eligibility_status=$d.outcome;decision_reason=$d.reason;second_review_status=if($d.candidates -eq 'Baicalein'){'focused second review completed; B2 retained'}elseif($d.tier -eq 'B1'){'rule reapplication completed; independent human second reviewer still pending'}else{'not applicable or source unresolved'};rank_effect=$d.rank;adjudication_date='2026-09-22'}
}
$log|Export-Csv (Join-Path $base 'Stage25B1_Rank_Relevant_Adjudication_Log.csv') -NoTypeInformation -Encoding utf8

foreach($row in $priority){
  $match=@($log|Where-Object{$_.DOI -eq $row.DOI -and ($_.candidate -split '; ' -contains $row.candidate)})
  if($match.Count){$row.adjudication_status=$match[0].eligibility_status}
}
$priority|Export-Csv $priorityPath -NoTypeInformation -Encoding utf8

foreach($row in $pub){
  $match=@($log|Where-Object{$_.DOI -eq $row.DOI -and ($_.candidate -split '; ' -contains $row.canonical_name)})
  if(!$match.Count){continue}
  $m=$match[0]
  switch($m.eligibility_status){
    'ASSAY_INCOMPATIBLE' {$row.method_screen_status='FULL_TEXT_ASSAY_INCOMPATIBLE_C';$row.H_ORAC_tier='C';$row.exclusion_reason='ASSAY_INCOMPATIBLE';$row.full_text_checked='yes'}
    'ELIGIBLE_PRIMARY' {$row.method_screen_status='FULL_TEXT_METHOD_COMPATIBLE_B1';$row.H_ORAC_tier='B1';$row.exclusion_reason='';$row.full_text_checked='yes'}
    'B2_MAINTAINED_AFTER_SECOND_REVIEW' {$row.method_screen_status='FULL_TEXT_METHOD_COMPATIBLE_B2_SECOND_REVIEW';$row.H_ORAC_tier='B2';$row.exclusion_reason='B2_OPTICAL_AND_SOLUBILITY_QC_INCOMPLETE';$row.full_text_checked='yes'}
    'QUANTITATIVE_VALUE_NOT_EXTRACTABLE' {$row.method_screen_status='FULL_TEXT_QUANTITATIVE_VALUE_NOT_EXTRACTABLE';$row.H_ORAC_tier='X';$row.exclusion_reason='QUANTITATIVE_VALUE_NOT_EXTRACTABLE';$row.full_text_checked='yes'}
    default {$row.method_screen_status='SOURCE_NOT_RECOVERED';$row.H_ORAC_tier='X';$row.exclusion_reason='SOURCE_NOT_RECOVERED';$row.full_text_checked='attempted_not_recovered'}
  }
  $row.reviewer='Stage25B.1 rank-relevant adjudication';$row.notes=$m.decision_reason
}
$pub|Export-Csv $pubPath -NoTypeInformation -Encoding utf8

$summary=Import-Csv (Join-Path $base 'Stage25B_HORAC_Candidate_Summary.csv')
$experiment=Import-Csv (Join-Path $base 'Stage25B_HORAC_Experiment_Evidence.csv')
foreach($s in $summary){
  $cp=@($pub|Where-Object candidate_id -eq $s.candidate_id)
  $pendingN=@($cp|Where-Object method_screen_status -eq 'PENDING_FULL_TEXT_ADJUDICATION').Count
  $s.publication_screened_N=$cp.Count
  $s.full_text_assessed_N=@($cp|Where-Object{$_.full_text_checked -eq 'yes'}).Count
  $s.method_compatible_publication_N=@($cp|Where-Object{$_.H_ORAC_tier -in @('A','B1','B2')}).Count
  if($pendingN){$s.major_method_caveat="$pendingN publication(s) remain pending prioritized full-text adjudication"}
  elseif(!$s.major_method_caveat){$s.major_method_caveat='No pending rank-relevant publication identified in current queue'}
  $s.human_review_required=if($pendingN -or @($experiment|Where-Object{$_.candidate_id -eq $s.candidate_id -and $_.second_reviewer_status -match 'HUMAN|PENDING'}).Count){'yes'}else{'no'}
}
$summary|Export-Csv (Join-Path $base 'Stage25B_HORAC_Candidate_Summary.csv') -NoTypeInformation -Encoding utf8
$checkpointSummary=Import-Csv (Join-Path $base 'checkpoints/stage25b_initial_2026-09-21/Stage25B_HORAC_Candidate_Summary.csv')
$rows=[System.Collections.Generic.List[object]]::new()
foreach($batchSpec in @(@{name='Frozen Stage25B checkpoint';data=$checkpointSummary},@{name='After Batch 1';data=$checkpointSummary},@{name='After Batch 2';data=$summary})){
  foreach($mode in @('A-only','A+B1 primary','A+B1+B2 sensitivity')){
    $primary=@($batchSpec.data|Where-Object quantitative_rank_eligible -eq 'yes'|Sort-Object @{Expression={[double]$_.A_B1_median};Descending=$true},canonical_name)
    $b2=@($batchSpec.data|Where-Object{$_.A_B1_B2_median -ne ''}|Sort-Object @{Expression={[double]$_.A_B1_B2_median};Descending=$true},canonical_name)
    $set=if($mode -eq 'A+B1 primary'){$primary}elseif($mode -eq 'A+B1+B2 sensitivity'){$b2}else{@()}
    if(!$set.Count){$rows.Add([pscustomobject]@{batch=$batchSpec.name;analysis=$mode;rank='';candidate='NO_TIER_A_EVIDENCE';median='';Top20_member='no';eligible_experiment_N=0;confidence='Not rankable';heterogeneity='';interpretation='HUMAN REVIEW REQUIRED — TIER A FEASIBILITY; rubric unchanged'})}
    for($i=0;$i -lt $set.Count;$i++){
      $x=$set[$i];$rows.Add([pscustomobject]@{batch=$batchSpec.name;analysis=$mode;rank=$i+1;candidate=$x.canonical_name;median=if($mode -eq 'A+B1+B2 sensitivity'){$x.A_B1_B2_median}else{$x.A_B1_median};Top20_member=if($i -lt 20){'yes'}else{'no'};eligible_experiment_N=$x.independent_eligible_experiment_N;confidence=$x.evidence_confidence;heterogeneity=$x.heterogeneity_flag;interpretation=if($mode -eq 'A-only'){'No Tier A evidence'}elseif($mode -eq 'A+B1+B2 sensitivity'){'B2 inclusion changes Top20 membership'}elseif($batchSpec.name -eq 'After Batch 2'){'Primary Top20 membership unchanged; rankable N increased'}else{'Primary checkpoint ranking'}})
    }
  }
}
$rows|Export-Csv (Join-Path $base 'Stage25B1_Top20_Cutoff_Sensitivity.csv') -NoTypeInformation -Encoding utf8

$log|Group-Object batch,priority_tier|Select-Object Name,Count|Format-Table -AutoSize
Write-Output "ADJUDICATION_LOG_ROWS=$($log.Count)"
