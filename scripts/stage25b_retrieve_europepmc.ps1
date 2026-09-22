param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string]$SearchDate = (Get-Date -Format 'yyyy-MM-dd')
)

$ErrorActionPreference = 'Stop'
$candidatePath = Join-Path $ProjectRoot 'data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv'
$outputDir = Join-Path $ProjectRoot 'data/h_orac_stage25b/_working'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

function Escape-EpmcPhrase([string]$value) {
    return $value.Replace('"', '\"')
}

$candidates = Import-Csv -LiteralPath $candidatePath
$results = [System.Collections.Generic.List[object]]::new()
$logs = [System.Collections.Generic.List[object]]::new()

foreach ($candidate in $candidates) {
    $names = @($candidate.canonical_name)
    if ($candidate.synonyms_used) {
        $names += $candidate.synonyms_used -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    }
    $names = $names | Select-Object -Unique
    $nameClause = ($names | ForEach-Object { 'TITLE_ABS:"' + (Escape-EpmcPhrase $_) + '"' }) -join ' OR '
    $query = "($nameClause) AND (TITLE_ABS:ORAC OR TITLE_ABS:`"oxygen radical absorbance capacity`" OR (TITLE_ABS:AAPH AND TITLE_ABS:fluorescein))"
    $encoded = [uri]::EscapeDataString($query)
    $url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=$encoded&format=json&pageSize=1000&resultType=core"
    $response = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 90
    $records = @($response.resultList.result)
    $logs.Add([pscustomobject]@{
        candidate_id = $candidate.candidate_id
        candidate = $candidate.canonical_name
        database = 'Europe PMC'
        exact_search_query = $query
        search_date = $SearchDate
        number_retrieved = [int]$response.hitCount
        number_screened = $records.Count
        number_full_text_assessed = 0
        number_method_compatible = 0
        number_quantitative_extractable = 0
        search_status = 'DISCOVERY_COMPLETE_PENDING_FULL_TEXT_ADJUDICATION'
    })
    foreach ($record in $records) {
        $results.Add([pscustomobject]@{
            candidate_id = $candidate.candidate_id
            canonical_name = $candidate.canonical_name
            PubChem_CID = $candidate.PubChem_CID
            InChIKey = $candidate.InChIKey
            database_source = 'Europe PMC'
            discovery_query = $query
            retrieval_date = $SearchDate
            source_id = $record.id
            source = $record.source
            PMID = $record.pmid
            PMCID = $record.pmcid
            DOI = $record.doi
            title = $record.title
            abstract = $record.abstractText
            authors = $record.authorString
            journal = $record.journalTitle
            year = $record.pubYear
            publication_type = (@($record.pubTypeList.pubType) -join '; ')
            is_open_access = $record.isOpenAccess
            has_pdf = $record.hasPDF
            has_full_text = $record.inEPMC
            cited_by_count = $record.citedByCount
        })
    }
    Start-Sleep -Milliseconds 150
}

$results | Export-Csv -LiteralPath (Join-Path $outputDir 'EuropePMC_Discovery_Raw.csv') -NoTypeInformation -Encoding utf8
$logs | Export-Csv -LiteralPath (Join-Path $outputDir 'EuropePMC_Search_Log_Raw.csv') -NoTypeInformation -Encoding utf8
Write-Output "CANDIDATES=$($candidates.Count)"
Write-Output "DISCOVERY_ROWS=$($results.Count)"
Write-Output "UNIQUE_DOI=$(@($results.DOI | Where-Object { $_ } | ForEach-Object { $_.ToLowerInvariant() } | Select-Object -Unique).Count)"
Write-Output "OUTPUT_DIR=$outputDir"
