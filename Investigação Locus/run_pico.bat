@echo off
set SCENARIO=C_pico
set USERS=200
set RUNTIME=5m
set REPS=5
set HOST=http://localhost:8080

if not exist "results\%SCENARIO%\" md "results\%SCENARIO%\"

echo Iniciando CenArio %SCENARIO%: %USERS% usuarios por %RUNTIME% (x%REPS%)

for /L %%i in (1, 1, %REPS%) do (
    echo Executando %SCENARIO% - Repeticao %%i/%REPS%...
    
    python -m locust -f locustfile.py --host=%HOST% --headless ^
           --users %USERS% --spawn-rate %USERS% ^
           --run-time %RUNTIME% ^
           --csv=results\%SCENARIO%\run_%%i
           
    echo Repeticao %%i finalizada.
    timeout /t 10 /nobreak
)

echo CenArio %SCENARIO% completo.