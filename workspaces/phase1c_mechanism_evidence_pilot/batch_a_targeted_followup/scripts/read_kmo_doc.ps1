$ErrorActionPreference='Stop'
$taskDir=Split-Path $PSScriptRoot -Parent
$sourceFile=Join-Path $taskDir 'local_sources/Kmo_EPMC_supplement.zip'
$docFile=Join-Path $taskDir 'local_sources/Kmo_DataS1_recovered.doc'
$archive=[System.IO.Compression.ZipFile]::OpenRead($sourceFile)
try {
 $entry=$archive.GetEntry('JCMM-27-2290-s006.doc')
 [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry,$docFile,$true)
} finally {$archive.Dispose()}
$word=$null
$document=$null
$isolated=$false
try {
 $word=New-Object -ComObject Word.Application
 if($word.Documents.Count -ne 0){throw 'Refusing to operate on a Word instance containing existing user documents'}
 $isolated=$true
 $word.Visible=$false
 $word.DisplayAlerts=0
 $word.AutomationSecurity=3
 $document=$word.Documents.Open($docFile,$false,$true,$false)
 $text=$document.Content.Text
 [System.IO.File]::WriteAllText((Join-Path $taskDir 'local_sources/Kmo_DataS1_readonly_text.txt'),$text,[System.Text.UTF8Encoding]::new($false))
 Write-Output $text
} finally {
 if($null -ne $document){$document.Close(0)}
 if($null -ne $word -and $isolated){$word.Quit(0)}
}
