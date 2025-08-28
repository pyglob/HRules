$Here = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Venv = Join-Path $Here ".venv"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found"
    exit 1
}

if (-not (Test-Path $Venv)) {
    python -m venv $Venv
}

& "$Venv\Scripts\Activate.ps1"

pip install --upgrade pip > $null
pip install -e $Here > $null

python -m hrules.cli $args
