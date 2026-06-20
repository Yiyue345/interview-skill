# Build-Knowledge.ps1
# Build the question index and knowledge graph.
# Usage: .\Build-Knowledge.ps1

$Root = $PSScriptRoot
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=== Build question index ==="
python "$Root\src\build_index.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Index build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Build knowledge graph ==="
python "$Root\src\build_graph.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Knowledge graph build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Validate consistency ==="
python "$Root\src\validate_consistency.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Consistency validation failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Build completed" -ForegroundColor Green
