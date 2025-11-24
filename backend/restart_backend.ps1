# Script to restart backend server on port 8000
# Kills existing process and starts new one in background

Write-Host "=== Backend Server Restart Script ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Kill any process using port 8000
Write-Host "Step 1: Checking for processes on port 8000..." -ForegroundColor Yellow

try {
    $processInfo = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if ($processInfo) {
        $processId = $processInfo.OwningProcess
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        
        if ($process) {
            Write-Host "Found process: $($process.ProcessName) (PID: $processId)" -ForegroundColor Yellow
            Write-Host "Terminating process..." -ForegroundColor Yellow
            Stop-Process -Id $processId -Force
            Start-Sleep -Seconds 2
            Write-Host "Process terminated successfully!" -ForegroundColor Green
        }
    } else {
        Write-Host "No process found on port 8000" -ForegroundColor Green
    }
} catch {
    Write-Host "No process found on port 8000 or already terminated" -ForegroundColor Green
}

Write-Host ""

# Step 2: Navigate to backend directory
Write-Host "Step 2: Navigating to backend directory..." -ForegroundColor Yellow
Set-Location "C:\JK\dev\repo\radicads\backend"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Step 3: Start new backend process in background
Write-Host "Step 3: Starting backend server in background..." -ForegroundColor Yellow

# Start the process using Start-Process with -WindowStyle Hidden
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\JK\dev\repo\radicads\backend'; & .\.venv\Scripts\Activate.ps1; `$env:GEMINI_API_KEY = 'AIzaSyAAD5TdEPiKCDe8H3g_6EJa48SWbIj6rYY'; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Hidden

Write-Host "Backend server starting in background..." -ForegroundColor Green
Write-Host ""

# Step 4: Wait and verify the server is running
Write-Host "Step 4: Waiting for server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Verifying server is running..." -ForegroundColor Yellow
try {
    $connection = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if ($connection) {
        $serverPid = $connection.OwningProcess
        $serverProcess = Get-Process -Id $serverPid -ErrorAction SilentlyContinue
        
        Write-Host "Server is running!" -ForegroundColor Green
        Write-Host "  Process: $($serverProcess.ProcessName)" -ForegroundColor Green
        Write-Host "  PID: $serverPid" -ForegroundColor Green
        Write-Host "  Port: 8000" -ForegroundColor Green
        Write-Host ""
        Write-Host "Server is ready at: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API docs available at: http://localhost:8000/docs" -ForegroundColor Cyan
    } else {
        Write-Host "Warning: Could not verify server on port 8000" -ForegroundColor Red
        Write-Host "The server may still be starting up. Check manually in a few seconds." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Warning: Could not verify server status" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Restart Complete ===" -ForegroundColor Cyan
