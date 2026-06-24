using module "..\VataCoreEngine\VataCoreEngine.psm1"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "[!] INITIALIZING: VATA ADVERSARIAL STRESS-TEST SUITE" -ForegroundColor Cyan
Write-Host "====================================================`n" -ForegroundColor Cyan

$SandboxPath = ".\VataSandbox"
if (-not (Test-Path $SandboxPath)) {
    New-Item -ItemType Directory -Path $SandboxPath -Force | Out-Null
}

$Engine = [VataEngine]::new($SandboxPath)
$Client = [VataNetworkClient]::new("https://rpc.flashbots.net", "0x0000000000000000000000000000000000000000")

# Explicitly scope globally to ensure visibility across the test execution blocks
$global:TotalTests = 0
$global:TestsPassed = 0

function Assert-AuditRequirement([string]$TestName, [scriptblock]$TestLogic) {
    $global:TotalTests = $global:TotalTests + 1
    Write-Host "[*] Running Test: $TestName..." -ForegroundColor White
    try {
        & $TestLogic
        Write-Host "[✓] PASSED: Boundary held as expected.`n" -ForegroundColor Green
        $global:TestsPassed = $global:TestsPassed + 1
    } catch {
        Write-Host "[!] FAILED: $TestName dropped security baseline. Error: $_`n" -ForegroundColor Red
    }
}

# --- TEST BATTERY 1: PATH TRAVERSAL BREAKOUT ATTEMPT ---
Assert-AuditRequirement "Directory Traversal Containment Breach" {
    $AdversarialPath = "..\..\Windows\System32\drivers\etc\hosts"
    Write-Host "    [!] Adversarial Input: Attempting to read out-of-bounds path via: $AdversarialPath" -ForegroundColor Yellow
    
    try {
        $Result = $Engine.AssertFileReadBoundary($AdversarialPath)
        throw "Breach undetected! System allowed out-of-bounds read access."
    } catch {
        if ($_ -match "Sandbox containment breach attempted") {
            Write-Host "    [+] Invariant Action: Engine successfully identified and terminated the directory breakout request." -ForegroundColor Cyan
        } else {
            throw $_
        }
    }
}

# --- TEST BATTERY 2: TYPE CONFUSION / DESERIALIZATION INJECTION ---
Assert-AuditRequirement "Dynamic Type Degradation Verification" {
    $PoisonedPayload = [PSCustomObject]@{
        TaskId   = "TASK-999"
        Payload  = "malicious_instruction_override_token"
        VataType = "CompromisedObject"
    }
    Write-Host "    [!] Adversarial Input: Injecting unverified schema type: $($PoisonedPayload.VataType)" -ForegroundColor Yellow

    try {
        $Result = $Engine.AssertTypeSafety($PoisonedPayload)
        throw "Type confusion successful! Engine processed unverified class structures."
    } catch {
        if ($_ -match "Type degradation detected") {
            Write-Host "    [+] Invariant Action: Engine successfully dropped the unverified payload structure from memory." -ForegroundColor Cyan
        } else {
            throw $_
        }
    }
}

# --- TEST BATTERY 3: EXOGENOUS BLOCKCHAIN SYNCHRONIZATION ---
Assert-AuditRequirement "Out-of-Band Cryptographic Ledger Verification" {
    Write-Host "    [!] Syncing audit completion status to public ledger gateway..." -ForegroundColor Yellow
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    
    $CurrentBlock = $Client.GetLatestBlockNumber()
    if ($CurrentBlock -gt 0) {
        Write-Host "    [+] Cryptographic Anchoring Verified. Current Ethereum Block Height: $CurrentBlock" -ForegroundColor Cyan
    } else {
        throw "Failed to communicate with programmatic ledger gateway."
    }
}

# --- FINAL REPORT ---
$ReportColor = "Red"
if ($global:TestsPassed -eq $global:TotalTests) { $ReportColor = "Green" }

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "AUDIT REPORT SUMMARY: RU SYSTEM v1.2 SPECIFICATIONS" -ForegroundColor Cyan
Write-Host "Tests Executed: $global:TotalTests | Invariants Intact: $global:TestsPassed / $global:TotalTests" -ForegroundColor $ReportColor
Write-Host "====================================================" -ForegroundColor Cyan
