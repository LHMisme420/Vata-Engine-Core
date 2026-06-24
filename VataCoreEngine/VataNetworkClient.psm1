class VataNetworkClient {
    hidden [string]$RpcUrl
    hidden [string]$AnchorContract

    VataNetworkClient([string]$endpointUrl, [string]$contractAddress) {
        if ([string]::IsNullOrEmpty($endpointUrl)) {
            throw "VATA_NETWORK_FAULT: Target RPC provider URL cannot be null."
        }
        $this.RpcUrl = $endpointUrl
        $this.AnchorContract = if ([string]::IsNullOrEmpty($contractAddress)) { "0x0000000000000000000000000000000000000000" } else { $contractAddress }
    }

    hidden [PSCustomObject] SendRpcRequest([string]$Method, [array]$Params) {
        $Body = @{
            jsonrpc = "2.0"
            method  = $Method
            params  = $Params
            id      = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        } | ConvertTo-Json -Depth 10 -Compress

        $Headers = @{ "Content-Type" = "application/json" }
        
        try {
            $Response = Invoke-RestMethod -Uri $this.RpcUrl -Method Post -Headers $Headers -Body $Body
            if ($null -ne $Response.error) {
                throw "RPC_NODE_ERROR: $($Response.error.message)"
            }
            return $Response
        } catch {
            throw "VATA_NETWORK_TRANSMISSION_FAILURE: Connection to node timed out or refused. Details: $_"
        }
    }

    [string] GetLatestBlockNumber() {
        $Response = $this.SendRpcRequest("eth_blockNumber", @())
        return [Convert]::ToInt64($Response.result, 16)
    }
}
