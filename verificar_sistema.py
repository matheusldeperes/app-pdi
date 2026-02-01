#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de verificação do Sistema de Avaliação e PDI
Verifica se tudo está configurado corretamente
"""

import sys
import os
import json
from pathlib import Path

def verificar_ambiente():
    """Verifica o ambiente Python"""
    print("🔍 VERIFICAÇÃO DO SISTEMA")
    print("=" * 60)
    
    # Python version
    print(f"✓ Python: {sys.version.split()[0]}")
    
    # Diretório
    print(f"✓ Diretório: {os.getcwd()}")
    
    print()

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("📦 VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("=" * 60)
    
    dependencias = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'plotly': 'Plotly'
    }
    
    todas_ok = True
    for modulo, nome in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {nome}: Instalado")
        except ImportError:
            print(f"❌ {nome}: NÃO ENCONTRADO")
            todas_ok = False
    
    print()
    
    if not todas_ok:
        print("⚠️  Instale as dependências com:")
        print("   pip install -r requirements.txt")
        print()
    
    return todas_ok

def verificar_arquivos():
    """Verifica se os arquivos principais existem"""
    print("📁 VERIFICAÇÃO DE ARQUIVOS")
    print("=" * 60)
    
    arquivos_obrigatorios = [
        'app.py',
        'requirements.txt'
    ]
    
    arquivos_opcionais = [
        'avaliacoes_pdi.json',
        'README.md',
        'INSTRUCOES_RAPIDAS.md'
    ]
    
    todas_ok = True
    
    print("Obrigatórios:")
    for arquivo in arquivos_obrigatorios:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"❌ {arquivo}: NÃO ENCONTRADO")
            todas_ok = False
    
    print("\nOpcionais:")
    for arquivo in arquivos_opcionais:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"⚠️  {arquivo}: não encontrado (será criado)")
    
    print()
    return todas_ok

def verificar_dados():
    """Verifica o arquivo de dados"""
    print("💾 VERIFICAÇÃO DE DADOS")
    print("=" * 60)
    
    if os.path.exists('avaliacoes_pdi.json'):
        try:
            with open('avaliacoes_pdi.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            print(f"✅ Arquivo JSON válido")
            print(f"   Colaboradores registrados: {len(dados)}")
            
            for id_col, dados_col in dados.items():
                nome = dados_col.get('nome', 'Desconhecido')
                pontos = dados_col.get('total_pontos', '?')
                classificacao = dados_col.get('classificacao', '?')
                print(f"   • {nome}: {pontos}/35 - {classificacao}")
            
        except json.JSONDecodeError:
            print("❌ Arquivo JSON corrompido")
            print("   Delete e reabra o app para criar um novo")
            return False
    else:
        print("⚠️  Arquivo de dados não existe")
        print("   Será criado ao rodar o app com a primeira avaliação")
    
    print()
    return True

def main():
    """Função principal"""
    print("\n")
    
    verificar_ambiente()
    deps_ok = verificar_dependencias()
    arquivos_ok = verificar_arquivos()
    dados_ok = verificar_dados()
    
    print("=" * 60)
    print("RESULTADO DA VERIFICAÇÃO")
    print("=" * 60)
    
    if deps_ok and arquivos_ok and dados_ok:
        print("✅ TUDO OK! Sistema pronto para usar.")
        print("\nPara iniciar o app, execute:")
        print("   streamlit run app.py")
        return 0
    else:
        print("⚠️  Há problemas a resolver")
        print("\nResolva os problemas e tente novamente.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
