# Build-Knowledge.ps1
# 一键构建题库索引 + 知识图谱
# 用法: .\Build-Knowledge.ps1

$Root = $PSScriptRoot
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=== 构建题库索引 ==="
python "$Root\src\build_index.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "索引构建失败" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== 构建知识图谱 ==="
python "$Root\src\build_graph.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "知识图谱构建失败" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== 一致性校验 ==="
python "$Root\src\validate_consistency.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "一致性校验发现警告，请查看上方输出" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "全部完成" -ForegroundColor Green
