#!/bin/bash

# Script para iniciar o app Streamlit

echo "🚀 Iniciando Sistema de Avaliação e PDI..."
echo ""

# Ativar ambiente virtual (opcional)
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Rodar o Streamlit
streamlit run app.py
