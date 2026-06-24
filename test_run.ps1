using module ".\VataCoreEngine\VataCoreEngine.psm1"

try {
    # Force TLS 1.2 negotiation explicitly
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

    # Switch to an endpoint explicitly built for raw programmatic routing
    $RpcEndpoint = "https://rpc.flashbots.net"
    $Client = [VataNetworkClient]::new($RpcEndpoint, "0x0000000000000000000000000000000000000000")
    
    Write-Host "`n[+] Routing via Programmatic Open Gateway ($RpcEndpoint)..." -ForegroundColor Green
    $CurrentBlock = $Client.GetLatestBlockNumber()

    Write-Host "[+] VATA Network Interface Online." -ForegroundColor Green
    Write-Host "[+] Node Synced. Current Target Chain Block Height: $CurrentBlock" -ForegroundColor Yellow
} catch {
    Write-Host "[!] Core Transmission Failure: $_" -ForegroundColor Red
}
