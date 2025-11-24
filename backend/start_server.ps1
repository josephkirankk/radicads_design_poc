Set-Location "c:\JK\dev\repo\radicads\backend"
& .\.venv\Scripts\Activate.ps1
$env:GEMINI_API_KEY = "AIzaSyAAD5TdEPiKCDe8H3g_6EJa48SWbIj6rYY"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
