# 🔧 TROUBLESHOOTING - Resolvendo Problemas

## ❌ App não inicia

### Problema: "command not found: streamlit"

**Solução:**
```bash
# Verifique se o Python venv está ativado
source .venv/bin/activate

# Ou use o caminho completo
/Users/peres/Desktop/APP\ PDI/.venv/bin/python -m streamlit run app.py
```

### Problema: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
# Instale as dependências
pip install -r requirements.txt

# Ou especificamente
pip install streamlit pandas plotly
```

### Problema: Porta 8501 já em uso

**Solução:**
```bash
# Use uma porta diferente
streamlit run app.py --server.port 8502

# Ou finalize o processo anterior
lsof -ti:8501 | xargs kill -9
```

---

## 📊 Gráficos não aparecem

### Problema: "Plotly not installed"

**Solução:**
```bash
pip install plotly>=5.17.0
```

### Problema: Gráfico em branco

**Solução:**
- Verifique se tem dados salvos
- Vá para "📝 Nova Avaliação" e salve um colaborador
- O gráfico só aparece em "📊 Relatório" se houver dados

---

## 💾 Dados não salvam

### Problema: "Permission denied: 'avaliacoes_pdi.json'"

**Solução:**
```bash
# Verifique permissões
ls -la avaliacoes_pdi.json

# Corrija as permissões
chmod 644 avaliacoes_pdi.json

# Se não tiver arquivo, delete e crie novo
rm avaliacoes_pdi.json
# Reabra o app e salve um novo colaborador
```

### Problema: Dados desapareceram

**Solução:**
1. Verifique se `avaliacoes_pdi.json` existe
2. Verifique o conteúdo:
   ```bash
   cat avaliacoes_pdi.json
   ```
3. Se estiver vazio ou corrompido:
   ```bash
   python verificar_sistema.py
   ```
4. Se for JSON inválido, delete e crie novo:
   ```bash
   rm avaliacoes_pdi.json
   ```

---

## 🖥️ Interface não carrega

### Problema: Browser mostra erro

**Solução:**
1. Feche o browser
2. Espere 5 segundos
3. Acesse novamente: `http://localhost:8501`
4. Se não funcionar, reinicie o app

### Problema: Interface congelada

**Solução:**
```bash
# Finalize o Streamlit
ctrl + C

# Aguarde 3 segundos
sleep 3

# Reinicie
streamlit run app.py
```

---

## ⚠️ Mensagens de Erro Comuns

### "ValueError: Expecting value"

**Causa:** Arquivo JSON corrompido

**Solução:**
```bash
# Backup do arquivo antigo
cp avaliacoes_pdi.json avaliacoes_pdi.json.bak

# Delete o corrompido
rm avaliacoes_pdi.json

# Reabra o app - um novo será criado
streamlit run app.py
```

### "FileNotFoundError: [Errno 2] No such file"

**Causa:** Arquivo `app.py` não encontrado

**Solução:**
```bash
# Verifique se está no diretório correto
pwd

# Deve mostrar: /Users/peres/Desktop/APP PDI

# Se não, navigate
cd "/Users/peres/Desktop/APP PDI"

# Verifique se app.py existe
ls -la app.py
```

### "TypeError: object is not subscriptable"

**Causa:** Dados em formato incorreto

**Solução:**
```bash
# Execute o verificador
python verificar_sistema.py

# Se mostrar erro no JSON, delete e recrie
rm avaliacoes_pdi.json
```

---

## 🔄 Dados Corrompidos

### Problema: JSON inválido

**Verificação:**
```bash
python -m json.tool avaliacoes_pdi.json
```

**Se der erro:** Arquivo está corrompido

**Solução:**
```bash
# Backup
cp avaliacoes_pdi.json avaliacoes_pdi_corrupted.json

# Delete
rm avaliacoes_pdi.json

# Recrie vazio
echo '{}' > avaliacoes_pdi.json

# Verifique
python verificar_sistema.py
```

---

## 🐌 App Lento

### Problema: Aplicativo carrega lentamente

**Causas possíveis:**
- Arquivo JSON muito grande (muitos colaboradores)
- Computador sobrecarregado
- Problema de conexão

**Soluções:**
```bash
# 1. Reinicie o app
ctrl + C
streamlit run app.py

# 2. Feche outros programas

# 3. Verifique tamanho do arquivo
ls -lh avaliacoes_pdi.json

# 4. Se muito grande, considere arquivar dados antigos
```

---

## 📱 Interface distorcida no Mobile

### Problema: Layout desorganizado em celular

**Solução:**
- Use em portrait (vertical)
- Zoom out no browser
- Use um computador para melhor experiência

---

## 🔐 Dados Não Aparecem Após Salvar

### Problema: Salva mas não mostra em "Visualizar"

**Causas:**
- Cache do browser
- Página não foi recarregada

**Solução:**
```bash
# Ao salvar, clique em "Visualizar Colaboradores"
# ou
# Recarregue a página: F5

# Se ainda não aparecer:
# 1. Verifique o JSON
cat avaliacoes_pdi.json

# 2. Se estiver vazio, o JSON não foi salvo corretamente
# 3. Verificar permissões de escrita
touch avaliacoes_pdi.json
```

---

## 💻 Problemas Específicos macOS

### Problema: "Permission denied" ao executar run.sh

**Solução:**
```bash
chmod +x run.sh
./run.sh
```

### Problema: "command not found" com python

**Solução:**
```bash
# Use python3 explicitamente
python3 -m streamlit run app.py

# Ou use o venv
source .venv/bin/activate
streamlit run app.py
```

### Problema: Watchdog warning

**Solução:** (Opcional - não afeta funcionamento)
```bash
pip install watchdog
```

---

## 🔍 Debug: Verificar Tudo

### Script completo de verificação

```bash
#!/bin/bash

echo "🔍 VERIFICAÇÃO COMPLETA DO SISTEMA"
echo ""

# 1. Verificar Python
echo "1️⃣ Python:"
python3 --version

# 2. Verificar dependências
echo ""
echo "2️⃣ Dependências:"
python3 -c "import streamlit; print('✅ Streamlit OK')" 2>&1
python3 -c "import pandas; print('✅ Pandas OK')" 2>&1
python3 -c "import plotly; print('✅ Plotly OK')" 2>&1

# 3. Verificar arquivos
echo ""
echo "3️⃣ Arquivos:"
ls -la app.py requirements.txt avaliacoes_pdi.json 2>&1 | grep -E "^-"

# 4. Verificar JSON
echo ""
echo "4️⃣ JSON:"
python3 -m json.tool avaliacoes_pdi.json > /dev/null && echo "✅ JSON válido" || echo "❌ JSON corrompido"

# 5. Iniciar app
echo ""
echo "5️⃣ Iniciando app..."
streamlit run app.py
```

### Ou use o script pronto:
```bash
python verificar_sistema.py
```

---

## 📞 Se Nada Funcionar

1. **Delete tudo do projeto exceto documentação**
   ```bash
   rm -f avaliacoes_pdi.json .streamlit/config.toml
   ```

2. **Reinstale dependências**
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

3. **Reinicie o terminal e computador**

4. **Tente novamente**
   ```bash
   streamlit run app.py
   ```

---

## ✅ Como Verificar se Tudo Está OK

```bash
# 1. Executar verificação
python verificar_sistema.py

# Resultado esperado:
# ✅ TUDO OK! Sistema pronto para usar.
```

Se aparecer ✅ em tudo, o sistema está funcionando corretamente!

---

## 📊 Diagnóstico Rápido

| Sintoma | Causa Possível | Solução |
|---------|---|---|
| Nenhum colaborador visível | Arquivo JSON vazio | Salve um novo |
| Gráfico em branco | Sem dados | Crie dados de exemplo |
| Erro ao salvar | JSON corrompido | Delete e recrie |
| App lento | Muitos dados | Arquive dados antigos |
| Interface confusa | Cache browser | Limpe cache (Ctrl+Shift+Del) |
| Não consegue deletar | Permissões | `chmod 644 arquivo.json` |

---

## 🆘 Último Recurso

Se nada funcionar:

1. **Faça backup dos dados:**
   ```bash
   cp avaliacoes_pdi.json avaliacoes_pdi_backup.json
   ```

2. **Delete tudo exceto documentação:**
   ```bash
   rm -rf .venv .streamlit __pycache__ *.pyc
   ```

3. **Reinstale do zero:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Restaure dados se necessário:**
   ```bash
   cp avaliacoes_pdi_backup.json avaliacoes_pdi.json
   ```

5. **Teste novamente:**
   ```bash
   streamlit run app.py
   ```

---

**Versão**: 1.0  
**Atualizado**: 1º de fevereiro de 2026  
**Suporte**: Consulte a documentação ou tente as soluções acima
