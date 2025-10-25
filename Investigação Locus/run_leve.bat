@echo off
set SCENARIO=A_leve
set USERS=50
set RUNTIME=10m
set REPS=5
set HOST=http://localhost:8080

REM Cria a pasta de resultados (se não existir)
if not exist "results\%SCENARIO%\" md "results\%SCENARIO%\"

echo Iniciando CenArio %SCENARIO%: %USERS% usuarios por %RUNTIME% (x%REPS%)

REM O 'for /L' A A sintaxe A: (variavel, inicio, incremento, fim)
for /L %%i in (1, 1, %REPS%) do (
    echo Executando %SCENARIO% - Repeticao %%i/%REPS%...
    
    python -m locust -f locustfile.py --host=%HOST% --headless ^
           --users %USERS% --spawn-rate %USERS% ^
           --run-time %RUNTIME% ^
           --csv=results\%SCENARIO%\run_%%i
           
    echo Repeticao %%i finalizada.
    REM 'timeout /t 10' A o equivalente ao 'sleep 10'
    timeout /t 10 /nobreak
)

echo CenArio %SCENARIO% completo.