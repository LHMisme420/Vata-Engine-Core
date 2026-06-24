@{
    ModuleVersion     = '1.2.0'
    GUID              = 'a4b2c1d3-e4f5-4a6b-7c8d-9e0f1a2b3c4d'
    Author            = 'Leroy H. Mason'
    CompanyName       = 'Sovereign Forensic Systems'
    Copyright         = '(c) 2026 Leroy H. Mason. All rights reserved.'
    Description       = 'Verifiable Autonomous Trust Architecture (VATA) Core Engine.'
    PowerShellVersion = '5.1'  # Dynamically lowered to accommodate standard host environment
    NestedModules     = @('VataCoreEngine.psm1', 'VataNetworkClient.psm1')
    ClassesToExport   = @('VataStateObject', 'VataEngine', 'VataNetworkClient')
}
