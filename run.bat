@echo off
REM Verifica se o venv existe
IF NOT EXIST "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Verifica se o requirements.txt existe
IF EXIST "requirements.txt" (
    echo Instalando dependencias do requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo [Aviso] Nenhum requirements.txt encontrado. Pulando instalação de dependencias.
)

REM Define variáveis de ambiente
set FLASK_APP=app.py
set FLASK_DEBUG=1

REM Inicia o servidor Flask
echo Iniciando servidor Flask com debug ativado...
flask run
