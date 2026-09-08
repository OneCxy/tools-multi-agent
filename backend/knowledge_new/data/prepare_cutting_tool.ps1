$ErrorActionPreference = 'Stop'
$dataRoot = (Resolve-Path -LiteralPath 'backend/knowledge_new/data').Path
$sourceRoot = Join-Path $dataRoot 'cutting_tool'
$archiveRoot = Join-Path $dataRoot 'cutting_tool_original'
$adminRoot = Join-Path $dataRoot 'cutting_tool_admin'
foreach ($target in @($sourceRoot, $archiveRoot, $adminRoot)) {
    $resolved = [System.IO.Path]::GetFullPath($target)
    if (-not $resolved.StartsWith($dataRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path outside data directory: $resolved"
    }
}
if ((Test-Path -LiteralPath $archiveRoot) -or (Test-Path -LiteralPath $adminRoot)) {
    throw 'Archive or administration directory already exists; refusing to overwrite.'
}
$entries = @(Get-Content -LiteralPath (Join-Path $sourceRoot 'manifest.jsonl') -Encoding UTF8 | ForEach-Object { $_ | ConvertFrom-Json })
if ($entries.Count -ne 700) { throw 'Expected 700 source entries.' }
$formulaSpecs = @{
    453 = @('车削转速计算', 'n = 1000 × vc / (π × D)', '车削；D为当前加工处的工件直径。', 'n：转速，r/min；vc：切削速度，m/min；D：工件直径，mm。', 'vc = 190 m/min，D = 55 mm', 'n', (1000 * 190 / ([Math]::PI * 55)), 'r/min')
    459 = @('车削切削速度反算', 'vc = π × D × n / 1000', '车削；D为当前加工处的工件直径。', 'vc：切削速度，m/min；D：工件直径，mm；n：转速，r/min。', 'D = 45 mm，n = 1000 r/min', 'vc', ([Math]::PI * 45 * 1000 / 1000), 'm/min')
    465 = @('车削进给速度计算', 'vf = fn × n', '车削；每转进给量与转速对应同一加工工况。', 'vf：进给速度，mm/min；fn：每转进给量，mm/rev；n：转速，r/min。', 'fn = 0.12 mm/rev，n = 900 r/min', 'vf', (0.12 * 900), 'mm/min')
    471 = @('铣削工作台进给计算', 'vf = fz × z × n', '铣削；z为用于进给计算的有效齿数。', 'vf：工作台进给速度，mm/min；fz：每齿进给量，mm/tooth；z：有效齿数；n：转速，r/min。', 'fz = 0.09 mm/tooth，z = 5，n = 1100 r/min', 'vf', (0.09 * 5 * 1100), 'mm/min')
    477 = @('铣削每齿进给反算', 'fz = vf / (z × n)', '铣削；有效齿数与转速均须大于零。', 'fz：每齿进给量，mm/tooth；vf：工作台进给速度，mm/min；z：有效齿数；n：转速，r/min。', 'vf = 700 mm/min，z = 5，n = 1300 r/min', 'fz', (700 / (5 * 1300)), 'mm/tooth')
    483 = @('车削加工时间计算', 'tm = L / (fn × n)', '恒定转速和每转进给量下的单次车削行程；不含换刀等辅助时间。', 'tm：加工时间，min；L：本次计算的进给行程长度，mm；fn：每转进给量，mm/rev；n：转速，r/min。', 'L = 100 mm，fn = 0.17 mm/rev，n = 850 r/min', 'tm', (100 / (0.17 * 850)), 'min')
    489 = @('车削近似材料去除率计算', 'Q ≈ ap × fn × vc', '车削的近似材料去除率估算；按下列单位代入。', 'Q：材料去除率，cm³/min；ap：切深，mm；fn：每转进给量，mm/rev；vc：切削速度，m/min。', 'ap = 1.25 mm，fn = 0.17 mm/rev，vc = 160 m/min', 'Q', (1.25 * 0.17 * 160), 'cm³/min')
    495 = @('主轴扭矩计算', 'T = 9550 × P / n', '已知主轴机械输出功率及对应转速时；不将电机额定功率直接视为主轴实际输出功率。', 'T：扭矩，N·m；P：主轴机械输出功率，kW；n：转速，r/min。', 'P = 6 kW，n = 600 r/min', 'T', (9550 * 6 / 600), 'N·m')
}
$prepared = @()
$mapping = @()
$names = @{}
foreach ($entry in $entries) {
    $path = [System.IO.Path]::GetFullPath((Join-Path $sourceRoot $entry.path))
    if (-not $path.StartsWith($sourceRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid manifest path.' }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $entry.sha256) { throw "Source hash mismatch: $path" }
    $number = [int]($entry.knowledge_id -replace '^CTK-', '')
    $text = [System.IO.File]::ReadAllText($path)
    $titleMatch = [regex]::Match($text, '(?m)^# (.+)\r?$')
    if (-not $titleMatch.Success) { throw "Missing heading: $path" }
    $title = $titleMatch.Groups[1].Value.Trim()
    $representative = $number
    if ($number -ge 453 -and $number -le 500) {
        $representative = 453 + [int]([Math]::Floor(($number - 453) / 6) * 6)
        $spec = $formulaSpecs[$representative]
        $title = $spec[0]
        if ($number -eq $representative) {
            $sources = [regex]::Match($text, '(?s)## 来源\s*\r?\n(.+)$').Groups[1].Value.Trim()
            if (-not $sources) { throw "Missing sources: $path" }
            $result = ([double]$spec[6]).ToString('0.####', [Globalization.CultureInfo]::InvariantCulture)
            $text = "# $title`n`n## 结论`n$($spec[1])。`n`n## 适用条件`n$($spec[2])`n`n## 说明`n$($spec[3])`n`n已知：$($spec[4])。`n结果：$($spec[5]) ≈ $result $($spec[7])。`n`n示例数值用于说明计算方法，不是推荐切削参数；使用前核对机床能力与刀具工况。`n`n## 来源`n$sources`n"
        }
    }
    $filename = ('CTK{0:D4}-{1}.md' -f $representative, $title)
    $mapping += [PSCustomObject]@{ original_id=$entry.knowledge_id; original_path=$entry.path; output_path=$filename }
    if ($number -ne $representative) { continue }
    if ($filename -match '[\\/:*?"<>|]') { throw "Invalid filename: $filename" }
    if ($names.ContainsKey($filename)) { throw "Duplicate filename: $filename" }
    $names[$filename] = $true
    $prepared += [PSCustomObject]@{ name=$filename; text=$text; knowledge_id=$entry.knowledge_id; title=$title; category=$entry.category }
}
if ($prepared.Count -ne 660) { throw 'Expected 660 prepared cards.' }
Move-Item -LiteralPath $sourceRoot -Destination $archiveRoot
New-Item -ItemType Directory -Path $sourceRoot, $adminRoot | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)
$manifest = foreach ($card in $prepared) {
    $destination = Join-Path $sourceRoot $card.name
    [System.IO.File]::WriteAllText($destination, $card.text, $utf8)
    [PSCustomObject]@{ knowledge_id=$card.knowledge_id; title=$card.title; category=$card.category; path=('cutting_tool/' + $card.name); sha256=(Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant() } | ConvertTo-Json -Compress
}
[System.IO.File]::WriteAllLines((Join-Path $adminRoot 'manifest.jsonl'), [string[]]$manifest, $utf8)
$mapLines = @($mapping | ForEach-Object { $_ | ConvertTo-Json -Compress })
[System.IO.File]::WriteAllLines((Join-Path $adminRoot 'migration_map.jsonl'), [string[]]$mapLines, $utf8)
Write-Output "Prepared $($prepared.Count) cards; archived $($entries.Count) originals."
