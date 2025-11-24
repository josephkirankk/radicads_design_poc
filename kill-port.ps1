param(
    [Parameter(Mandatory=$true)]
    [int]$Port
)

Write-Host "Searching for processes using port $Port..." -ForegroundColor Cyan

# Get the process ID using the specified port
$connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue

if ($connections) {
    $processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    
    Write-Host "Found $($processIds.Count) process(es) using port $Port" -ForegroundColor Yellow
    
    foreach ($processId in $processIds) {
        # Skip system processes (PID 0 and 4)
        if ($processId -eq 0 -or $processId -eq 4) {
            Write-Host "Skipping system process (PID: $processId)" -ForegroundColor Gray
            continue
        }

        try {
            $process = Get-Process -Id $processId -ErrorAction Stop
            Write-Host "Killing process: $($process.ProcessName) (PID: $processId)" -ForegroundColor Red
            Stop-Process -Id $processId -Force
            Write-Host "Successfully killed process $processId" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to kill process $processId : $_" -ForegroundColor Red
        }
    }
}
else {
    Write-Host "No processes found using port $Port" -ForegroundColor Yellow
}

