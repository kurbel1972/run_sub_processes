@echo off
REM Change console code page to UTF-8
chcp 65001 > nul

REM Generate a unique execution ID using date and time
set exec_id=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set exec_id=%exec_id: =0%

REM Print log header
echo 🔍 4_RUN_SUB_PROCESSES - Running Python script RUN_SUB_PROCESSES on %date% %time% [ID:%exec_id%]

REM Defina o local e o nome do arquivo de log
set LOGFILE=C:\Pessoal\Trabalho\GIT\run_sub_processes\log.txt

REM Limpe o arquivo de log antes de iniciar o script (opcional)
REM echo. > %LOGFILE%

REM Adicione um comentário "Começou" ao arquivo de log
REM Adicione a data e hora ao comentário "Começou" no arquivo de log
echo %DATE% %TIME% Começou run_sub_processes [ID:%exec_id%] >> %LOGFILE%

REM Redirecione a saída padrão e de erro para o arquivo de log
cd C:\Pessoal\Trabalho\GIT\run_sub_processes
call .venv\Scripts\activate
python run_sub_processes.py >> %LOGFILE% 2>&1

echo %DATE% %TIME% Acabou run_sub_processes [ID:%exec_id%] >> %LOGFILE%