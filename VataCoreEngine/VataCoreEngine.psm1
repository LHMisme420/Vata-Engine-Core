class VataStateObject {
    [string]$TaskId
    [string]$Payload
    [string]$VataType
    
    VataStateObject([string]$id, [string]$data) {
        if ([string]::IsNullOrEmpty($data)) {
            throw "VATA_CRITICAL_FAULT: Empty token strings are barred from the active data stream."
        }
        $this.TaskId = $id
        $this.Payload = $data
        $this.VataType = "VataStateObject"
    }
}

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

    hidden [PSCustomObject] SendRpcRequest([string]$Method, [string]$RawParamsJson) {
        # Fix: Enforce a clean, non-scientific integer format string for the RPC transaction ID
        $IdString = (Get-Random -Minimum 10000 -Maximum 99999).ToString()
        $Body = '{"jsonrpc":"2.0","method":"' + $Method + '","params":' + $RawParamsJson + ',"id":' + $IdString + '}'

        $Headers = @{ 
            "Content-Type" = "application/json"
            "User-Agent"   = "Mozilla/5.0"
        }
        
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
        $Response = $this.SendRpcRequest("eth_blockNumber", "[]")
        return [Convert]::ToInt64($Response.result, 16)
    }
}

class VataEngine {
    hidden [string]$SandboxRoot
    hidden [hashtable]$MaskedEnvironment

    VataEngine([string]$sandboxPath) {
        $ResolvedPath = [System.IO.Path]::GetFullPath($sandboxPath)
        $this.SandboxRoot = $ResolvedPath.ToLower().TrimEnd("\")
        if (-not (Test-Path $this.SandboxRoot)) {
            New-Item -ItemType Directory -Path $this.SandboxRoot -Force | Out-Null
        }

        $this.MaskedEnvironment = @{}
        $Targets = @("PATH", "COMPUTERNAME", "USERNAME", "USERPROFILE")
        $RealEnv = [System.Environment]::GetEnvironmentVariables("Process")
        foreach ($Key in $RealEnv.Keys) {
            if ($Targets -contains $Key.ToUpper()) {
                $this.MaskedEnvironment[$Key] = "[VATA_MASKED_BOUNDARY]"
            } else {
                $this.MaskedEnvironment[$Key] = $RealEnv[$Key]
            }
        }
    }
}
