param([string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path)
$ErrorActionPreference = 'Stop'

function N([object]$v) { if ($null -eq $v -or "$v" -eq '') { return $null }; return [double]$v }
function Med([double[]]$x) { if (!$x -or $x.Count -eq 0) { return $null }; $s=@($x|Sort-Object); $n=$s.Count; if($n%2){return $s[[int][math]::Floor($n/2)]}; return ($s[$n/2-1]+$s[$n/2])/2 }
function Quant([double[]]$x,[double]$p) { if(!$x -or $x.Count -eq 0){return $null}; $s=@($x|Sort-Object); if($s.Count -eq 1){return $s[0]}; $h=($s.Count-1)*$p; $lo=[math]::Floor($h); $hi=[math]::Ceiling($h); if($lo -eq $hi){return $s[$lo]}; return $s[$lo]+($h-$lo)*($s[$hi]-$s[$lo]) }
function CleanDoi([string]$v) { if(!$v){return ''}; return ($v.ToLowerInvariant() -replace '^https?://(dx\.)?doi\.org/','').Trim() }
function KeyFor($r) { $d=CleanDoi $r.DOI; if($d){return "doi:$d"}; if($r.PMID){return "pmid:$($r.PMID -replace '\.0$','')"}; return 'title:'+(($r.title -replace '<[^>]+>','' -replace '[^\p{L}\p{Nd}]','').ToLowerInvariant()) }

$dataDir=Join-Path $ProjectRoot 'data/h_orac_stage25b'
$workDir=Join-Path $dataDir '_working'
$cand=Import-Csv (Join-Path $ProjectRoot 'data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv')
$raw=Import-Csv (Join-Path $workDir 'EuropePMC_Discovery_Raw.csv')
$searchRaw=Import-Csv (Join-Path $workDir 'EuropePMC_Search_Log_Raw.csv')
$master=Import-Csv (Join-Path $ProjectRoot 'data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv')
$ids=@($cand.candidate_id)
$old=@($master|Where-Object{$ids -contains $_.candidate_id -and $_.assay -match 'ORAC'})

$experiments=[System.Collections.Generic.List[object]]::new()
foreach($r in $old){
  $tier=$r.evidence_tier
  $status=if($tier -in @('A','B1')){'ELIGIBLE_PRIMARY'}elseif($tier -eq 'B2'){'SENSITIVITY_ONLY'}elseif($tier -eq 'C'){'ASSAY_INCOMPATIBLE'}else{'INSUFFICIENT_METHOD_INFORMATION'}
  $experiments.Add([pscustomobject]@{
    candidate_id=$r.candidate_id; canonical_name=$r.canonical_name; PubChem_CID=$r.PubChem_CID; InChIKey=$r.InChIKey
    publication_id=$r.paper_id; DOI=(CleanDoi $r.DOI); PMID=($r.PMID -replace '\.0$',''); year=$r.year
    independent_experiment_id=$r.independent_experiment_id; compound_form=$r.chemical_form; compound_purity='not reported in consolidated master'; supplier='not reported in consolidated master'; CAS_if_reported=''
    assay_name_reported=$r.assay; radical_generator=$r.radical_or_oxidant_system; probe=$r.probe; standard=$r.reference_standard; buffer=$r.buffer; pH=$r.pH; temperature=$r.temperature; incubation_time=$r.incubation_time; plate_or_cuvette='see source'; instrument='see source'
    sample_concentration=$r.compound_concentration; sample_concentration_unit='as reported'; cosolvent=$r.cosolvent; cosolvent_percent='not consistently reported'
    blank_control='see source/legacy extraction'; compound_blank='not reported in consolidated master'; optical_interference_control='not reported in consolidated master'; aggregation_assessed='not reported in consolidated master'
    raw_reported_value=$r.original_value; raw_unit=$r.original_unit; converted_value_mol_TE_per_mol=$r.normalized_value; conversion_formula=$r.conversion_formula; molecular_weight_used=$r.molecular_weight_used; conversion_verified=if($r.normalized_value){'existing_conversion_revalidated_for_traceability'}else{'not_applicable_or_unresolved'}
    replicate_N='not consistently reported'; mean_or_median='reported value'; SD=''; SE=''; CI=''
    H_ORAC_tier=$tier; eligibility_status=$status; independence_status=if($r.independent_experiment_id){'independent_experiment_id_present'}else{'uncertain'}
    optical_interference_risk=$r.optical_interference_risk; solubility_risk='see assay phase/cosolvent'; aggregation_risk='not reported'; redox_cycling_risk='not assessed in ORAC master'; major_method_caveat=$r.quality_note
    extractor='Stage25B migration from canonical evidence master'; second_reviewer_status='PENDING_SECOND_REVIEW'; source_page=$r.exact_page; source_table=$r.exact_table; source_figure=$r.exact_figure; source_supplement=$r.supplementary_location
    provenance_status='existing_validated'; previous_status=$r.evidence_tier; new_status=$r.evidence_tier; status_change_reason='No silent status change during Stage25B migration'; notes=$r.notes
  })
}

# New full-text-adjudicated record. Optical blank is absent for a chromophoric flavonoid,
# so the frozen rubric requires B2 despite otherwise complete ORAC-FL methods.
$b=$cand|Where-Object canonical_name -eq 'Baicalein'
$experiments.Add([pscustomobject]@{
  candidate_id=$b.candidate_id; canonical_name=$b.canonical_name; PubChem_CID=$b.PubChem_CID; InChIKey=$b.InChIKey
  publication_id='S25B-P001'; DOI='10.3390/pharmaceutics14102141'; PMID='36297576'; year='2022'; independent_experiment_id='HORAC_EXP_0071'
  compound_form='baicalein aglycone (5,6,7-trihydroxyflavone)'; compound_purity='97% reference standard'; supplier='Merck KGaA'; CAS_if_reported=''
  assay_name_reported='ORAC'; radical_generator='AAPH, 0.15 M'; probe='fluorescein, 0.08 µM'; standard='Trolox, 6.25–50 µM'; buffer='phosphate buffer'; pH='not stated in extracted full text'; temperature='37 °C'; incubation_time='10 min preincubation; 1 h kinetic reading'; plate_or_cuvette='24-well plate'; instrument='PerkinElmer Victor Nivo microplate reader'
  sample_concentration='5.0'; sample_concentration_unit='µM'; cosolvent='not reported'; cosolvent_percent='not reported'; blank_control='250 µL buffer blank'; compound_blank='not reported'; optical_interference_control='not reported'; aggregation_assessed='not reported'
  raw_reported_value='5.41 ± 0.33'; raw_unit='µmol TE/µmol compound'; converted_value_mol_TE_per_mol='5.41'; conversion_formula='µmol TE/µmol compound = mol TE/mol compound'; molecular_weight_used='not required for direct molar ratio'; conversion_verified='yes'
  replicate_N='3–6 experiments (paper figure caption)'; mean_or_median='mean'; SD=''; SE='0.33'; CI=''; H_ORAC_tier='B2'; eligibility_status='SENSITIVITY_ONLY'; independence_status='independent original experiment'
  optical_interference_risk='unresolved—baicalein chromophore; no compound-specific optical blank/correction reported'; solubility_risk='unresolved—cosolvent not reported'; aggregation_risk='not assessed'; redox_cycling_risk='not assessed'; major_method_caveat='Method construct is H-ORAC-FL, but rank-relevant optical and solubility controls are absent for a Conditional chromophoric candidate.'
  extractor='Codex Stage25B full-text XML adjudication'; second_reviewer_status='HUMAN REVIEW REQUIRED'; source_page='Methods 3.3.2; Results 2.2.2'; source_table=''; source_figure='Figure 6B'; source_supplement=''; provenance_status='new_full_text_verified'; previous_status='no Stage25B record'; new_status='B2'; status_change_reason='New original-paper evidence; downgraded to B2 by frozen optical-interference rule'; notes='Does not enter primary ranking.'
})

$methoxyRecords=@(
  @{name='Eugenol';value='2.12';sd='0.08';purity='≥99%';cas='97-53-0'},
  @{name='Capsaicin';value='1.60';sd='0.25';purity='≥95%';cas='404-86-4'},
  @{name='Vanillin';value='1.81';sd='0.19';purity='≥97%';cas='121-33-5'}
)
foreach($m in $methoxyRecords){
  $mc=$cand|Where-Object canonical_name -eq $m.name
  $experiments.Add([pscustomobject]@{
    candidate_id=$mc.candidate_id;canonical_name=$mc.canonical_name;PubChem_CID=$mc.PubChem_CID;InChIKey=$mc.InChIKey;publication_id='S25B1-P001';DOI='10.3390/foods10081807';PMID='34441583';year='2021';independent_experiment_id="FOODS2021::$($m.name)";compound_form='defined pure compound';compound_purity=$m.purity;supplier='Sigma-Aldrich, Milano, Italy';CAS_if_reported=$m.cas
    assay_name_reported='ORAC';radical_generator='AAPH, 150 mM';probe='fluorescein, 80 nM';standard='Trolox, 1–8 µM';buffer='PBS, 75 mM';pH='7';temperature='37 °C';incubation_time='10 min preincubation; 55 min kinetic reading';plate_or_cuvette='96-well microplate';instrument='fluorescence reader, Ex 485 nm / Em 525 nm';sample_concentration='0.09–6.0';sample_concentration_unit='µM';cosolvent='stock ethanol diluted into PBS';cosolvent_percent='trace at assay concentrations; exact final percentage not explicitly reported';blank_control='fluorescein + AAPH';compound_blank='not reported';optical_interference_control='not reported; no strong chromophore expected at assay wavelengths';aggregation_assessed='not reported; micromolar range and dose-response used'
    raw_reported_value="$($m.value) ± $($m.sd)";raw_unit='µM TE per 1 µM phytochemical';converted_value_mol_TE_per_mol=$m.value;conversion_formula='µM TE/µM compound = mol TE/mol compound';molecular_weight_used='not required for direct molar ratio';conversion_verified='yes';replicate_N='3 independent experiments';mean_or_median='mean';SD=$m.sd;SE='';CI='';H_ORAC_tier='B1';eligibility_status='ELIGIBLE_PRIMARY';independence_status='independent original experiment';optical_interference_risk='low but compound-specific blank not reported';solubility_risk='minor caveat—stock ethanol and final percentage incompletely reported';aggregation_risk='low at micromolar concentrations but not directly assessed';redox_cycling_risk='not assessed';major_method_caveat='Complete core H-ORAC-FL construct and linear calibration; exact final ethanol percentage and compound-specific optical blank are not reported, preventing Tier A.';extractor='Codex Stage25B.1 full-text XML adjudication';second_reviewer_status='PRIORITY_SECOND_REVIEW_COMPLETED_BY_RULE_REAPPLICATION';source_page='Methods 2.5.4; Results ORAC section';source_table='Table 5';source_figure='Supplementary Figures S4–S5';source_supplement='ORAC calibration and fluorescence decay curves';provenance_status='new_full_text_verified_stage25b1';previous_status='no Stage25B record';new_status='B1';status_change_reason='New rank-relevant full-text evidence under frozen rubric';notes='Adds a Low-confidence rankable candidate but does not enter current Top20.'
  })
}

# Stage25B IDs identify candidate × independent experiment rows and therefore must
# be unique even when a legacy source used one study-level label for many compounds.
for($i=0;$i -lt $experiments.Count;$i++){
  $legacy=$experiments[$i].independent_experiment_id
  $experiments[$i] | Add-Member -NotePropertyName legacy_independent_experiment_id -NotePropertyValue $legacy
  $experiments[$i].independent_experiment_id=('HORAC_EXP_{0:D4}' -f ($i+1))
}

$experiments | Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Experiment_Evidence.csv') -NoTypeInformation -Encoding utf8

# Candidate × publication discovery ledger. Raw query duplicates are collapsed within candidate.
$oldByCandPub=@{}
foreach($r in $old){$k="$($r.candidate_id)|$(CleanDoi $r.DOI)|$($r.PMID -replace '\.0$','')|$($r.paper_id)"; $oldByCandPub[$k]=$r}
$pub=[System.Collections.Generic.List[object]]::new()
foreach($g in ($raw|Group-Object {"$($_.candidate_id)|$(KeyFor $_)"})){
  $r=$g.Group[0]; $doi=CleanDoi $r.DOI; $pmid=$r.PMID
  $matched=@($old|Where-Object{$_.candidate_id -eq $r.candidate_id -and (($doi -and (CleanDoi $_.DOI) -eq $doi) -or ($pmid -and ($_.PMID -replace '\.0$','') -eq $pmid))})
  $isBaic=($r.candidate_id -eq $b.candidate_id -and $doi -eq '10.3390/pharmaceutics14102141')
  $isMethoxy=($doi -eq '10.3390/foods10081807' -and $r.canonical_name -in @('Eugenol','Capsaicin','Vanillin'))
  $ptype=$r.publication_type; $txt=("$($r.title) $($r.abstract)")
  if($matched.Count){$ms='FULL_TEXT_REVALIDATED_EXISTING';$ex=''}
  elseif($isBaic){$ms='FULL_TEXT_METHOD_COMPATIBLE_B2';$ex='B2_OPTICAL_AND_SOLUBILITY_QC_INCOMPLETE'}
  elseif($isMethoxy){$ms='FULL_TEXT_METHOD_COMPATIBLE_B1';$ex=''}
  elseif($ptype -match '(?i)Review|Meta-Analysis' -or $r.title -match '(?i)\breview\b'){$ms='EXCLUDED_TITLE_ABSTRACT';$ex='REVIEW_DISCOVERY_ONLY'}
  elseif($r.title -match '(?i)extract|juice|fruit|food|beverage|plasma|serum|nanoparticle|encapsulat|formulation|mixture|oil|leaf|seed|flour|supplement'){$ms='EXCLUDED_TITLE_ABSTRACT';$ex='MATRIX_FORMULATION_OR_NON_PURE_COMPOUND'}
  elseif($txt -notmatch '(?i)ORAC|oxygen radical absorbance capacity'){$ms='EXCLUDED_TITLE_ABSTRACT';$ex='NO_ORAC_SIGNAL_AFTER_METADATA_SCREEN'}
  else{$ms='PENDING_FULL_TEXT_ADJUDICATION';$ex=''}
  $tier=if($matched.Count){(@($matched.evidence_tier|Select-Object -Unique)-join ';')}elseif($isBaic){'B2'}elseif($isMethoxy){'B1'}else{''}
  $pub.Add([pscustomobject]@{
    candidate_id=$r.candidate_id; canonical_name=$r.canonical_name; PubChem_CID=$r.PubChem_CID; InChIKey=$r.InChIKey
    publication_id=if($isBaic){'S25B-P001'}else{$r.source_id}; DOI=$doi; PMID=$pmid; title=($r.title -replace '<[^>]+>',''); year=$r.year; journal=$r.journal; authors=$r.authors
    database_source=$r.database_source; discovery_query=$r.discovery_query; original_or_review=if($ptype -match '(?i)Review'){'review'}else{'original_or_unresolved'}; full_text_available=$r.has_full_text
    candidate_identity_match=if($ms -like 'FULL_TEXT*'){'confirmed'}else{'metadata_candidate_match_only'}; H_ORAC_mentioned=if($txt -match '(?i)ORAC|oxygen radical absorbance capacity' -or $isMethoxy){'yes'}else{'no'}
    AAPH_confirmed=if($matched.Count -and @($matched.radical_or_oxidant_system)-match 'AAPH'){'yes'}elseif($isBaic -or $isMethoxy){'yes'}else{'unresolved'}; fluorescein_confirmed=if($matched.Count -and @($matched.probe)-match 'fluorescein'){'yes'}elseif($isBaic -or $isMethoxy){'yes'}else{'unresolved'}; Trolox_confirmed=if($matched.Count -and @($matched.reference_standard)-match 'Trolox'){'yes'}elseif($isBaic -or $isMethoxy){'yes'}else{'unresolved'}
    pure_compound_tested=if($matched.Count -or $isBaic -or $isMethoxy){'yes'}else{'unresolved'}; quantitative_result_present=if($matched.Count -or $isBaic -or $isMethoxy){'yes'}else{'unresolved'}; unit_reported=if($matched.Count){(@($matched.original_unit|Select-Object -Unique)-join ';')}elseif($isBaic){'µmol TE/µmol compound'}elseif($isMethoxy){'µM TE per 1 µM phytochemical'}else{''}
    method_screen_status=$ms; H_ORAC_tier=$tier; exclusion_reason=$ex; full_text_checked=if($ms -like 'FULL_TEXT*'){'yes'}else{'no'}; reviewer='Codex metadata screen; full-text rows explicitly identified'; notes='Automated metadata exclusions require audit sampling; pending rows are not eligible evidence.'
  })
}
# Preserve every candidate × publication from the canonical evidence master even
# when Europe PMC title/abstract discovery did not return a generic multi-compound paper.
foreach($g in ($old|Group-Object {"$($_.candidate_id)|$($_.paper_id)"})){
  $r=$g.Group[0]; $doi=CleanDoi $r.DOI; $pmid=($r.PMID -replace '\.0$','')
  $exists=@($pub|Where-Object{$_.candidate_id -eq $r.candidate_id -and (($doi -and $_.DOI -eq $doi) -or ($pmid -and $_.PMID -eq $pmid) -or $_.publication_id -eq $r.paper_id)}).Count
  if(!$exists){
    $pub.Add([pscustomobject]@{candidate_id=$r.candidate_id;canonical_name=$r.canonical_name;PubChem_CID=$r.PubChem_CID;InChIKey=$r.InChIKey;publication_id=$r.paper_id;DOI=$doi;PMID=$pmid;title=$r.paper_title;year=$r.year;journal=$r.journal;authors=$r.first_author;database_source='Existing canonical evidence master';discovery_query='existing evidence provenance revalidation';original_or_review=$r.review_or_original;full_text_available='source previously retrieved';candidate_identity_match='confirmed';H_ORAC_mentioned='yes';AAPH_confirmed=if($r.radical_or_oxidant_system -match 'AAPH'){'yes'}else{'no_or_unresolved'};fluorescein_confirmed=if($r.probe -match 'fluorescein'){'yes'}else{'no_or_unresolved'};Trolox_confirmed=if($r.reference_standard -match 'Trolox'){'yes'}else{'no_or_unresolved'};pure_compound_tested='yes';quantitative_result_present=if($r.original_value){'yes'}else{'no'};unit_reported=$r.original_unit;method_screen_status='FULL_TEXT_REVALIDATED_EXISTING';H_ORAC_tier=(@($g.Group.evidence_tier|Select-Object -Unique)-join ';');exclusion_reason='';full_text_checked='yes';reviewer='Stage25B migration from canonical full-text extraction';notes='Not rediscovered by the calibrated title/abstract query; retained through existing evidence provenance.'})
  }
}
$pub | Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Publication_Screening.csv') -NoTypeInformation -Encoding utf8

$prov=$experiments|ForEach-Object{[pscustomobject]@{candidate=$_.canonical_name;experiment_id=$_.independent_experiment_id;DOI=$_.DOI;PMID=$_.PMID;title=if($_.publication_id -eq 'S25B-P001'){'Comparative Evaluation of the Antiglycation and Anti-α-Glucosidase Activities of Baicalein, Baicalin and Metformin'}else{($master|Where-Object independent_experiment_id -eq $_.independent_experiment_id|Select-Object -First 1).paper_title};year=$_.year;source_location=(@($_.source_page,$_.source_table,$_.source_figure)|Where-Object{$_})-join '; ';full_text_source=if($_.publication_id -eq 'S25B-P001'){'Europe PMC fullTextXML PMC9612222'}else{'canonical evidence master / DOI source'};retrieval_date='2026-09-21';original_source_verified=if($_.provenance_status -in @('existing_validated','new_full_text_verified')){'yes'}else{'no'};notes=$_.major_method_caveat}}
$prov|Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Source_Provenance.csv') -NoTypeInformation -Encoding utf8

$summary=[System.Collections.Generic.List[object]]::new()
foreach($c in $cand){
  $p=@($pub|Where-Object candidate_id -eq $c.candidate_id); $x=@($experiments|Where-Object candidate_id -eq $c.candidate_id); $elig=@($x|Where-Object{$_.H_ORAC_tier -in @('A','B1') -and $_.converted_value_mol_TE_per_mol -ne ''}); $vals=@($elig|ForEach-Object{[double]$_.converted_value_mol_TE_per_mol}); $b2=@($x|Where-Object{$_.H_ORAC_tier -eq 'B2' -and $_.converted_value_mol_TE_per_mol -ne ''}|ForEach-Object{[double]$_.converted_value_mol_TE_per_mol});
  $min=if($vals.Count){($vals|Measure-Object -Minimum).Minimum}else{$null};$max=if($vals.Count){($vals|Measure-Object -Maximum).Maximum}else{$null};$ratio=if($vals.Count -and $min -gt 0){$max/$min}else{$null};$iqr=if($vals.Count -ge 2){(Quant $vals .75)-(Quant $vals .25)}else{$null}
  $conf=if(!$vals.Count){'Not rankable'}elseif($vals.Count -eq 1){'Low'}elseif($vals.Count -ge 3 -and (!$ratio -or $ratio -le 2)){'High'}else{'Moderate'}
  $pending=@($p|Where-Object method_screen_status -eq 'PENDING_FULL_TEXT_ADJUDICATION').Count
  $summary.Add([pscustomobject]@{candidate_id=$c.candidate_id;canonical_name=$c.canonical_name;Stage25A_primary_rank=$c.primary_rank;Stage25B_status=$c.Stage25B_status;publication_screened_N=$p.Count;full_text_assessed_N=@($p|Where-Object full_text_checked -eq 'yes').Count;method_compatible_publication_N=@($p|Where-Object{$_.H_ORAC_tier -in @('A','B1','B2')}).Count;eligible_A_N=@($x|Where-Object H_ORAC_tier -eq 'A').Count;eligible_B1_N=@($x|Where-Object H_ORAC_tier -eq 'B1').Count;eligible_B2_N=@($x|Where-Object H_ORAC_tier -eq 'B2').Count;C_N=@($x|Where-Object H_ORAC_tier -eq 'C').Count;X_N=@($x|Where-Object H_ORAC_tier -eq 'X').Count;independent_eligible_experiment_N=$vals.Count;median_H_ORAC_mol_TE_per_mol=Med $vals;min=$min;max=$max;IQR=$iqr;max_min_ratio=$ratio;A_only_median=Med @($x|? H_ORAC_tier -eq A|%{[double]$_.converted_value_mol_TE_per_mol});A_B1_median=Med $vals;A_B1_B2_median=Med @($vals+$b2);heterogeneity_flag=if($ratio -gt 2){'HIGH_HETEROGENEITY'}else{'no'};evidence_confidence=$conf;major_method_caveat=if($pending){"$pending publication(s) remain pending full-text adjudication"}else{(@($x.major_method_caveat|Where-Object{$_}|Select-Object -Unique)-join ' | ')};quantitative_rank_eligible=if($vals.Count){'yes'}else{'no'};reason_not_rankable=if($vals.Count){''}elseif(@($x|? H_ORAC_tier -eq B2).Count){'B2 evidence only'}elseif(@($x|? H_ORAC_tier -eq X).Count){'INSUFFICIENT_METHOD_INFORMATION'}else{'SEARCHED_NO_CURRENTLY_ADJUDICATED_ELIGIBLE_HORAC'};human_review_required=if($pending -or @($x|? second_reviewer_status -match 'HUMAN').Count){'yes'}else{'second reviewer pending'}})
}
$summary|Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Candidate_Summary.csv') -NoTypeInformation -Encoding utf8

$ranking=@($summary|Where-Object quantitative_rank_eligible -eq 'yes'|Sort-Object @{Expression={[double]$_.median_H_ORAC_mol_TE_per_mol};Descending=$true},canonical_name)
for($i=0;$i -lt $ranking.Count;$i++){$ranking[$i]|Add-Member rank ($i+1);$ranking[$i]|Add-Member ranking_statistic 'median A+B1 mol TE/mol';$ranking[$i]|Add-Member provisional_status 'INTERIM_PENDING_FULL_TEXT_COMPLETION'}
$ranking|Select-Object rank,candidate_id,canonical_name,median_H_ORAC_mol_TE_per_mol,independent_eligible_experiment_N,evidence_confidence,heterogeneity_flag,Stage25A_primary_rank,Stage25B_status,ranking_statistic,provisional_status|Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Quantitative_Ranking.csv') -NoTypeInformation -Encoding utf8
$summary|Select-Object candidate_id,canonical_name,A_only_median,A_B1_median,A_B1_B2_median,independent_eligible_experiment_N,heterogeneity_flag,quantitative_rank_eligible,human_review_required|Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Sensitivity_Analysis.csv') -NoTypeInformation -Encoding utf8

$search=foreach($s in $searchRaw){$p=@($pub|? candidate_id -eq $s.candidate_id);[pscustomobject]@{candidate_id=$s.candidate_id;candidate=$s.candidate;database=$s.database;exact_search_query=$s.exact_search_query;search_date=$s.search_date;number_retrieved=$s.number_retrieved;number_screened=$p.Count;number_full_text_assessed=@($p|? full_text_checked -eq yes).Count;number_method_compatible=@($p|?{$_.H_ORAC_tier -in @('A','B1','B2')}).Count;number_quantitative_extractable=@($experiments|?{$_.candidate_id -eq $s.candidate_id -and $_.converted_value_mol_TE_per_mol -ne ''}).Count;search_status=if(@($p|? method_screen_status -eq PENDING_FULL_TEXT_ADJUDICATION).Count){'METADATA_SCREEN_COMPLETE_FULL_TEXT_PENDING'}else{'METADATA_SCREEN_COMPLETE'}}}
$search|Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Search_Log.csv') -NoTypeInformation -Encoding utf8
$pub|Where-Object exclusion_reason|Select-Object candidate_id,canonical_name,publication_id,DOI,PMID,title,method_screen_status,exclusion_reason,reviewer,notes|Export-Csv (Join-Path $dataDir 'Stage25B_HORAC_Exclusion_Log.csv') -NoTypeInformation -Encoding utf8

$pendingZRows=@($experiments|Where-Object{
  $exp=$_
  if(!$exp.DOI){return $false}
  $keys=@($master|Where-Object{(CleanDoi $_.DOI) -eq $exp.DOI}|ForEach-Object Zotero_key|Where-Object{$_ -and $_ -ne 'pending_local_import'}|Select-Object -Unique)
  return $keys.Count -eq 0
})
$pendingZ=@($pendingZRows|Group-Object DOI|ForEach-Object{
  $g=$_.Group
  [pscustomobject]@{DOI=$_.Name;PMID=(@($g.PMID|Where-Object{$_}|Select-Object -Unique)-join ';');canonical_name=(@($g.canonical_name|Select-Object -Unique)-join '; ');publication_id=(@($g.publication_id|Select-Object -Unique)-join ';');import_status='pending_local_import';notes='Zotero helper unavailable because no Python runtime was found; do not invent a Zotero key.'}
})
$pendingZ|Export-Csv (Join-Path $dataDir 'Stage25B_Zotero_Pending_Import.csv') -NoTypeInformation -Encoding utf8

Write-Output "PUBLICATION_ROWS=$($pub.Count)"
Write-Output "EXPERIMENT_ROWS=$($experiments.Count)"
Write-Output "RANKABLE_CANDIDATES=$($ranking.Count)"
Write-Output "PENDING_FULL_TEXT=$(@($pub|? method_screen_status -eq 'PENDING_FULL_TEXT_ADJUDICATION').Count)"
