# 🚀 GUIA DE CONFIGURAÇÃO - Google Sheets Integration

## 📋 Pré-requisitos

- Conta Google
- Acesso ao Google Cloud Console
- 10 minutos para configuração

---

## 🔧 PASSO 1: Criar Projeto no Google Cloud

### 1.1 Acessar o Console
1. Acesse: https://console.cloud.google.com
2. Faça login com sua conta Google
3. Clique em **"Criar Projeto"** ou selecione um projeto existente

### 1.2 Criar Novo Projeto
1. Nome do projeto: `app-pdi-satte-alam` (ou outro nome)
2. Clique em **"Criar"**
3. Aguarde a criação (leva alguns segundos)

---

## 🔑 PASSO 2: Ativar APIs Necessárias

### 2.1 Google Sheets API
1. No menu lateral, vá em: **APIs e serviços** → **Biblioteca**
2. Busque por: `Google Sheets API`
3. Clique em **"Ativar"**
4. Aguarde a ativação

### 2.2 Google Drive API
1. Ainda na Biblioteca de APIs
2. Busque por: `Google Drive API`
3. Clique em **"Ativar"**
4. Aguarde a ativação

---

## 🎫 PASSO 3: Criar Service Account (Conta de Serviço)

### 3.1 Criar Conta
1. Vá em: **APIs e serviços** → **Credenciais**
2. Clique em: **+ CRIAR CREDENCIAIS** → **Conta de serviço**
3. Preencha:
   - **Nome**: `app-pdi-service`
   - **ID**: (será gerado automaticamente)
   - **Descrição**: `Conta de serviço para App PDI`
4. Clique em **"Criar e continuar"**
5. Em "Papel", selecione: **Editor**
6. Clique em **"Continuar"**
7. Clique em **"Concluir"**

### 3.2 Gerar Chave JSON
1. Na lista de contas de serviço, clique na que você acabou de criar
2. Vá na aba **"Chaves"**
3. Clique em **"Adicionar chave"** → **"Criar nova chave"**
4. Selecione tipo: **JSON**
5. Clique em **"Criar"**
6. ⚠️ Um arquivo JSON será baixado automaticamente - **GUARDE BEM ESSE ARQUIVO!**

O arquivo JSON terá este formato:
```json
{
  "type": "service_account",
  "project_id": "seu-projeto-12345",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "app-pdi-service@seu-projeto-12345.iam.gserviceaccount.com",
  ...
}
```

---

## 📊 PASSO 4: Criar e Compartilhar Google Sheets

### 4.1 Criar Planilha
1. Acesse: https://sheets.google.com
2. Clique em **"+ Blank"** (nova planilha em branco)
3. Renomeie para: **Avaliações PDI - SATTE ALAM**

### 4.2 Compartilhar com Service Account
1. Clique no botão **"Compartilhar"** (canto superior direito)
2. No campo de e-mail, cole o `client_email` do arquivo JSON
   - Exemplo: `app-pdi-service@seu-projeto-12345.iam.gserviceaccount.com`
3. Permissão: **Editor**
4. ⚠️ **DESMARQUE** a opção "Notificar pessoas"
5. Clique em **"Compartilhar"**

---

## 💻 PASSO 5: Configurar Localmente (Desenvolvimento)

### Opção A: Usar arquivo JSON diretamente
1. Renomeie o arquivo JSON baixado para: `service_account.json`
2. Mova para a pasta do projeto:
   ```bash
   mv ~/Downloads/seu-projeto-*.json "/Users/peres/Desktop/APP PDI/service_account.json"
   ```
3. O app detectará automaticamente

### Opção B: Usar .streamlit/secrets.toml (Recomendado)
1. Abra o arquivo JSON baixado
2. Copie todo o conteúdo
3. Edite `.streamlit/secrets.toml`
4. Cole no formato:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "seu-projeto-12345"
   private_key_id = "abc123..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "app-pdi-service@seu-projeto-12345.iam.gserviceaccount.com"
   client_id = "123456789"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
   ```

---

## ☁️ PASSO 6: Deploy no Streamlit Cloud

### 6.1 Criar Repositório GitHub
```bash
# Se ainda não fez:
git remote add origin https://github.com/SEU_USUARIO/app-pdi.git
git push -u origin feature/google-sheets-integration
```

### 6.2 Deploy no Streamlit Cloud
1. Acesse: https://share.streamlit.io
2. Faça login com GitHub
3. Clique em **"New app"**
4. Configure:
   - **Repository**: Seu repositório
   - **Branch**: `feature/google-sheets-integration`
   - **Main file path**: `app.py`
5. Clique em **"Advanced settings"**

### 6.3 Adicionar Secrets
1. Na seção "Secrets", cole TODO o conteúdo do arquivo JSON:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "seu-projeto-12345"
   private_key_id = "abc123..."
   private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_COMPLETA_AQUI\n-----END PRIVATE KEY-----\n"
   client_email = "app-pdi-service@seu-projeto-12345.iam.gserviceaccount.com"
   client_id = "123456789"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
   
   sheet_name = "Avaliações PDI - SATTE ALAM"
   ```

2. Clique em **"Save"**
3. Clique em **"Deploy!"**

### 6.4 Aguardar Deploy
- O Streamlit Cloud instalará as dependências
- Aguarde 2-3 minutos
- Seu app estará disponível em: `https://seu-usuario-app-pdi-xyz.streamlit.app`

---

## ✅ PASSO 7: Testar

1. Abra o app (localmente ou no Streamlit Cloud)
2. Deve aparecer: "✅ Conectado à planilha: Avaliações PDI - SATTE ALAM"
3. Crie uma avaliação de teste
4. Verifique no Google Sheets se os dados apareceram
5. Sucesso! 🎉

---

## 🔒 SEGURANÇA

### ⚠️ IMPORTANTE:
- **NUNCA** commite `service_account.json` no Git
- **NUNCA** compartilhe o arquivo JSON publicamente
- O `.gitignore` já está configurado para ignorar esses arquivos
- Use sempre Streamlit Secrets no Cloud

### Arquivos que NÃO devem ser commitados:
- `service_account.json`
- `.streamlit/secrets.toml` (com credenciais reais)
- `credentials.json`
- `token.json`

---

## 🆘 Problemas Comuns

### "Credenciais não encontradas"
**Solução**: Verifique se o arquivo JSON está no lugar certo ou se o secrets.toml está configurado

### "Permission denied"
**Solução**: Certifique-se de ter compartilhado a planilha com o `client_email` do service account

### "API not enabled"
**Solução**: Ative Google Sheets API e Google Drive API no Console

### "Invalid credentials"
**Solução**: Gere uma nova chave JSON e substitua

---

## 📊 Estrutura da Planilha

O app criará automaticamente estas colunas:

| Coluna | Descrição |
|--------|-----------|
| ID | Identificador único (Nome_Data) |
| Nome | Nome do colaborador |
| Avaliador | Nome do gestor |
| Data | Data da avaliação |
| Scores_JSON | Notas por critério (JSON) |
| Observacoes_JSON | Observações (JSON) |
| Total_Pontos | Soma total (0-35) |
| Classificacao | 🟢/🟡/🔴 Status |
| Pontos_Fortes_JSON | PDI - Pontos fortes (JSON) |
| Gargalos_JSON | PDI - Gargalos (JSON) |
| Acoes_Melhoria_JSON | PDI - Ações (JSON) |
| Timestamp | Data/hora do registro |

---

## 🎯 Benefícios do Google Sheets

✅ Dados persistem na nuvem  
✅ Backup automático do Google  
✅ Acesso de qualquer lugar  
✅ Múltiplos usuários podem acessar  
✅ Pode editar manualmente no Sheets  
✅ Gratuito até 50k requisições/dia  
✅ Histórico de versões do Google  

---

## 📞 Recursos Adicionais

- [Documentação Google Cloud](https://cloud.google.com/docs)
- [API Google Sheets](https://developers.google.com/sheets/api)
- [gspread Documentation](https://docs.gspread.org)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

**Pronto!** 🚀 Seu app agora funciona com Google Sheets e pode ser hospedado no Streamlit Cloud!
