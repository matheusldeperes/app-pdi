# ⚡ INSTRUÇÕES RÁPIDAS - Sistema de Avaliação e PDI

## Como Rodar o App

### Opção 1: Direto (recomendado)
```bash
cd "/Users/peres/Desktop/APP PDI"
streamlit run app.py
```

### Opção 2: Usando o script
```bash
cd "/Users/peres/Desktop/APP PDI"
chmod +x run.sh
./run.sh
```

---

## 🎯 Primeira Execução

Quando você rodar o app pela primeira vez:

1. ✅ O Streamlit abrirá automaticamente em `http://localhost:8501`
2. ✅ Um arquivo `avaliacoes_pdi.json` será criado com dados de exemplo
3. ✅ Você pode visualizar 3 colaboradores de exemplo (João, Maria, Carlos)

---

## 📝 Fluxo de Uso

### 1️⃣ **Adicionar Nova Avaliação**
- Menu lateral → "📝 Nova Avaliação"
- Preencha nome, avaliador e data
- Avalie 7 critérios de 1 a 5
- Preencha PDI (pontos fortes, gargalos, ações)
- Clique "Salvar"

### 2️⃣ **Editar/Excluir Colaborador**
- Menu lateral → "👥 Visualizar Colaboradores"
- Selecione o colaborador
- Visualize gráficos e detalhes
- Clique em "🗑️ Deletar" para remover

### 3️⃣ **Visualizar Relatórios**
- Menu lateral → "📊 Relatório"
- Veja gráficos de distribuição
- Analise curva de vitalidade
- Consulte média por critério

---

## 💾 Dados

Todos salvos em: `avaliacoes_pdi.json`

### Backup
Para fazer backup, copie o arquivo:
```bash
cp avaliacoes_pdi.json avaliacoes_pdi_backup.json
```

---

## ❓ Dúvidas?

### Não vejo dados salvos
- Verifique se `avaliacoes_pdi.json` existe na pasta
- Revise a aba "👥 Visualizar Colaboradores"

### Remover dados de exemplo
- Delete o arquivo `avaliacoes_pdi.json`
- Reabra o app - um novo arquivo vazio será criado

### App não inicia
- Verifique se as dependências estão instaladas:
  ```bash
  pip install -r requirements.txt
  ```

---

## 📊 Escala de Classificação

| Pontos | Status | Cor |
|--------|--------|-----|
| 31-35 | 🟢 ALTO DESEMPENHO | Verde |
| 16-30 | 🟡 MANUTENÇÃO | Amarelo |
| < 16 | 🔴 RISCO | Vermelho |

---

## 🔐 Segurança

- ✅ Dados armazenados **apenas localmente**
- ✅ Nenhum envio para servidores
- ✅ Acesso apenas neste computador
- ⚠️ Faça backups regularmente

---

**Desenvolvido para: SATTE ALAM MOTORS**
