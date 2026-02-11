@echo off
title Lansare PTCC
echo [1/2] Se verifica mediul Python...

python -m streamlit run src/app/app.py

if %errorlevel% neq 0 (
    echo [EROARE] Streamlit nu este instalat!
    echo Se incearca instalarea automata...
    python -m pip install streamlit
    echo Incearca sa pornesti din nou fisierul dupa instalare.
)
timeout 2 >nul
exit