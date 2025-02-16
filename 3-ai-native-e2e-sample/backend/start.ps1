# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
}

# Set debug logging
$env:LOG_LEVEL = "DEBUG"

# Ensure we're in the backend directory
Set-Location $PSScriptRoot
uvicorn main:app --reload --host 0.0.0.0 --port 8002 