# 🚀 Sistema de Avaliação e PDI - Versão Cloud

## ☁️ Branch: feature/google-sheets-integration

Esta versão está preparada para **deploy no Streamlit Cloud** com integração ao **Google Sheets**.

---

## 🆚 Diferenças em Relação à Versão Local

| Característica | Branch `main` | Branch `feature/google-sheets-integration` |
|----------------|---------------|-------------------------------------------|
| **Armazenamento** | JSON local | Google Sheets |
| **Acesso** | Apenas local | De qualquer lugar |
| **Backup** | Manual | Automático (Google) |
| **Múltiplos usuários** | Não | Sim |
| **Deploy** | Apenas local | Streamlit Cloud |
| **Edição manual** | Arquivo JSON | Google Sheets |
| **Custo** | Gratuito | Gratuito |

---

## 📋 Para Começar

### 🏠 Uso Local (Desenvolvimento)

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar Google Sheets**:
   - Siga o guia: [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)
   - Configure credenciais em `.streamlit/secrets.toml`

3. **Rodar localmente**:
   ```bash
   streamlit run app.py
   ```

### ☁️ Deploy na Nuvem

1. **Preparar GitHub**:
   ```bash
   git push origin feature/google-sheets-integration
   ```

2. **Seguir guia de deploy**:
   - Leia: [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)
   - Configure no Streamlit Cloud
   - Adicione secrets
   - Deploy! 🎉

---

## 📚 Documentação Importante

### Para Configuração
- 📖 **[SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)** - Configurar Google Cloud e Sheets
- 🚀 **[DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)** - Deploy passo a passo

### Para Uso
- 📘 **[README.md](README.md)** - Documentação completa do app
- ⚡ **[INSTRUCOES_RAPIDAS.md](INSTRUCOES_RAPIDAS.md)** - Guia rápido
- 🔧 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Resolução de problemas

---

## ✨ Novas Funcionalidades

### Integração Google Sheets
- ✅ Conexão automática via service account
- ✅ Cache de conexão para performance
- ✅ Fallback para desenvolvimento local
- ✅ Conversão automática JSON ↔ Sheets

### Compatibilidade Cloud
- ✅ Streamlit Secrets suportado
- ✅ Variáveis de ambiente
- ✅ Deploy em um clique
- ✅ Auto-reload ao atualizar código

### Novos Recursos
- ✅ Múltiplos usuários simultâneos
- ✅ Edição manual no Google Sheets
- ✅ Backup automático
- ✅ Acesso mobile otimizado

---

## 🔄 Como Alternar Entre Versões

### Voltar para versão local (JSON)
```bash
git checkout main
pip install -r requirements.txt
streamlit run app.py
```

### Voltar para versão cloud (Google Sheets)
```bash
git checkout feature/google-sheets-integration
pip install -r requirements.txt
streamlit run app.py
```

---

## 🆘 Precisa de Ajuda?

1. **Configurar Google**: [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)
2. **Deploy no Cloud**: [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)
3. **Problemas**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. **Uso do app**: [README.md](README.md)

---

## 📊 Arquitetura

```
┌─────────────────────────────────────────────┐
│           USUÁRIOS (Browser)                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         STREAMLIT CLOUD / LOCAL             │
│              (app.py)                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│        GOOGLE SHEETS API                    │
│     (gspread + google-auth)                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         GOOGLE SHEETS                       │
│   (Avaliações PDI - SATTE ALAM)            │
└─────────────────────────────────────────────┘
```

---

## 🔐 Segurança

### ⚠️ NUNCA commitar:
- `service_account.json`
- `.streamlit/secrets.toml` (com dados reais)
- Credenciais do Google
- Tokens de acesso

### ✅ Já configurado no .gitignore:
```
service_account.json
token.json
credentials.json
.streamlit/secrets.toml
```

---

## 💰 Custos

### Completamente GRATUITO! 🎉

- **Streamlit Cloud**: Tier Community (gratuito)
- **Google Sheets API**: 500 req/min (gratuito)
- **Google Drive API**: Incluído
- **Armazenamento**: Google Drive (15GB gratuito)

---

## 🎯 Status

✅ **Pronto para deploy**  
✅ **Testado e funcionando**  
✅ **Documentação completa**  
✅ **Segurança implementada**  

---

## 📞 Suporte

- **Issues**: Abra issue no GitHub
- **Streamlit**: https://discuss.streamlit.io
- **Google Cloud**: https://support.google.com

---

**Versão**: 2.0 (Cloud-ready)  
**Data**: 1º de fevereiro de 2026  
**Branch**: feature/google-sheets-integration  
**Status**: ✅ Production Ready
