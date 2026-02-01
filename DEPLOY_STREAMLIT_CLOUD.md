# 🚀 DEPLOY NO STREAMLIT CLOUD - Guia Completo

## 📋 Pré-requisitos

✅ Conta GitHub  
✅ Repositório GitHub com o código  
✅ Credenciais do Google configuradas (veja SETUP_GOOGLE_SHEETS.md)  
✅ Google Sheets criado e compartilhado

---

## 🔥 DEPLOY RÁPIDO (5 minutos)

### 1️⃣ Preparar Repositório GitHub

```bash
# Commit das mudanças (se ainda não fez)
cd "/Users/peres/Desktop/APP PDI"
git add .
git commit -m "feat: Adiciona integração com Google Sheets para deploy na nuvem"

# Fazer push para GitHub
git push origin feature/google-sheets-integration
```

---

### 2️⃣ Criar Conta no Streamlit Cloud

1. Acesse: **https://share.streamlit.io**
2. Clique em **"Sign up"**
3. Escolha **"Continue with GitHub"**
4. Autorize o Streamlit Cloud a acessar seus repositórios

---

### 3️⃣ Deploy do App

#### 3.1 Iniciar Deploy
1. No painel do Streamlit Cloud, clique em **"New app"**
2. Configure:
   ```
   Repository: seu-usuario/app-pdi (ou nome do seu repo)
   Branch: feature/google-sheets-integration
   Main file path: app.py
   App URL (opcional): app-pdi-satte-alam (ou deixe sugestão)
   ```

#### 3.2 Configurar Secrets (IMPORTANTE!)
1. Clique em **"Advanced settings"**
2. Na seção **"Secrets"**, cole:

```toml
# Cole TODO o conteúdo do seu arquivo service_account.json aqui
# Mantenha o formato TOML conforme abaixo:

[gcp_service_account]
type = "service_account"
project_id = "SEU_PROJECT_ID"
private_key_id = "SUA_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nCOLE_SUA_CHAVE_PRIVADA_COMPLETA_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "SEU_SERVICE_ACCOUNT@SEU_PROJECT.iam.gserviceaccount.com"
client_id = "SEU_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

# Nome da sua planilha (certifique-se que está compartilhada!)
sheet_name = "Avaliações PDI - SATTE ALAM"
```

⚠️ **ATENÇÃO**: 
- Copie a chave privada COMPLETA (incluindo BEGIN e END)
- Use `\n` para quebras de linha na private_key
- Não adicione espaços extras

#### 3.3 Deploy!
1. Clique em **"Deploy!"**
2. Aguarde 2-3 minutos enquanto instala dependências
3. Seu app estará live! 🎉

---

## 🔗 URLs do App

Após o deploy, você terá:
- **URL pública**: `https://seu-usuario-app-pdi-xyz.streamlit.app`
- **Painel de gerenciamento**: `https://share.streamlit.io`

---

## ⚙️ Gerenciamento do App

### Atualizar o App
```bash
# Faça mudanças no código
# Commit e push
git add .
git commit -m "feat: Nova funcionalidade"
git push origin feature/google-sheets-integration

# O Streamlit Cloud detecta automaticamente e redeploya!
```

### Ver Logs
1. Acesse o painel: https://share.streamlit.io
2. Clique no seu app
3. Vá em **"Manage app"** → **"Logs"**

### Editar Secrets
1. No painel do app
2. **Settings** → **Secrets**
3. Edite e salve
4. App reiniciará automaticamente

### Reboot Manual
1. **Manage app** → **Reboot app**
2. Aguarde ~30 segundos

---

## 🎯 Verificações Pós-Deploy

### ✅ Checklist
- [ ] App abre sem erros
- [ ] Mensagem "✅ Conectado à planilha" aparece
- [ ] Pode criar nova avaliação
- [ ] Dados aparecem no Google Sheets
- [ ] Pode visualizar colaboradores
- [ ] Relatórios funcionam
- [ ] Pode deletar colaboradores

### 🐛 Se algo der errado
1. Verifique os logs no painel
2. Confirme que as credenciais estão corretas nos Secrets
3. Verifique se a planilha está compartilhada com o service account
4. Tente fazer reboot do app

---

## 🔒 Segurança e Privacidade

### Níveis de Privacidade do App

#### 🌐 Público (Padrão)
- Qualquer pessoa com o link pode acessar
- **Recomendado para**: Uso interno com link compartilhado

#### 🔐 Privado (Premium)
- Requer autenticação
- **Requer**: Plano pago do Streamlit Cloud
- Controle de acesso por usuário

### Proteger URL
Se não quer que seja facilmente encontrado:
1. Use URL personalizada difícil de adivinhar
2. Não compartilhe publicamente
3. Considere adicionar senha no app (custom auth)

---

## 💰 Custos

### Streamlit Cloud
- **Community (Gratuito)**:
  - 1 app privado
  - Ilimitados apps públicos
  - 1GB RAM
  - 1 CPU
  - ✅ **Suficiente para este projeto!**

- **Teams ($250/mês)**:
  - Múltiplos apps privados
  - Mais recursos
  - SSO/SAML

### Google Cloud
- **Google Sheets API**: Gratuito até 500 requisições/minuto
- **Este app**: ~5-10 requisições por avaliação
- ✅ **Bem dentro do limite gratuito!**

---

## 📊 Limites e Performance

### Streamlit Cloud (Grátis)
- **Apps ativos**: Ilimitados (públicos)
- **RAM**: 1GB
- **CPU**: 1 core compartilhado
- **Armazenamento**: Não aplicável (usa Google Sheets)
- **Sleep**: App hiberna após 7 dias sem uso (acorda automaticamente)

### Google Sheets
- **Linhas**: Até 10 milhões por planilha
- **Colunas**: Até 18.278 colunas
- **Requisições**: 500/minuto (gratuito)
- ✅ **Para 100 colaboradores**: ~1% dos limites

---

## 🚀 Otimizações

### Para melhor performance:

1. **Cache de conexão**
   ```python
   @st.cache_resource  # ✅ Já implementado!
   def conectar_google_sheets():
   ```

2. **Batch updates**
   ```python
   # O app já faz isso: atualiza tudo de uma vez
   worksheet.update(f'A2:L{len(rows)+1}', rows)
   ```

3. **Reload seletivo**
   - Use `st.rerun()` apenas quando necessário
   - Evite recarregar dados a cada interação

---

## 🔄 Workflow de Atualização

```mermaid
graph LR
    A[Código Local] --> B[Git Commit]
    B --> C[Git Push]
    C --> D[GitHub]
    D --> E[Streamlit Cloud Detecta]
    E --> F[Auto Deploy]
    F --> G[App Atualizado]
```

---

## 📱 Acesso Mobile

O app funciona perfeitamente em:
- ✅ iPhone/iPad
- ✅ Android
- ✅ Tablets
- ✅ Desktop

**Dica**: Adicione à tela inicial do celular:
1. Safari/Chrome → Menu
2. "Adicionar à Tela Inicial"
3. Ícone do app criado! 📱

---

## 🌐 Domínio Customizado (Opcional)

### Com Streamlit Teams ($250/mês)
1. Pode usar seu próprio domínio
2. Exemplo: `avaliacoes.sattealammotors.com.br`

### Alternativa Gratuita
1. Use o subdomínio do Streamlit
2. É profissional e confiável
3. Exemplo: `satte-alam-pdi.streamlit.app`

---

## 👥 Compartilhar com Equipe

### Opção 1: Link Direto
```
https://seu-app.streamlit.app
```
Compartilhe com gestores via:
- WhatsApp
- Email
- Intranet

### Opção 2: QR Code
Gere um QR Code do link para facilitar acesso mobile

### Opção 3: Embed
Incorpore em site/intranet:
```html
<iframe src="https://seu-app.streamlit.app" 
        width="100%" 
        height="800px">
</iframe>
```

---

## 📈 Monitoramento

### Métricas Disponíveis
No painel do Streamlit Cloud:
- Número de visitantes
- Tempo de resposta
- Erros
- Uso de recursos

### Google Sheets
- Veja atividade em: Arquivo → Histórico de versões
- Restaure versões antigas se necessário

---

## 🆘 Troubleshooting

### Erro: "Unable to connect to Google Sheets"
**Solução**: 
1. Verifique Secrets
2. Confirme compartilhamento da planilha
3. Teste credenciais localmente primeiro

### Erro: "Module not found"
**Solução**: 
1. Verifique `requirements.txt`
2. Force reinstall no Streamlit Cloud (reboot)

### App muito lento
**Solução**:
1. Verifique quantidade de dados
2. Considere paginar resultados
3. Use cache adequadamente

### App hibernou
**Normal!** Após 7 dias sem uso, acorda automaticamente ao acessar.

---

## 🎉 Pronto!

Seu app agora está:
- ✅ Na nuvem
- ✅ Acessível de qualquer lugar
- ✅ Com backup automático
- ✅ Sem custo

**URL do seu app**: `https://[seu-app].streamlit.app`

Compartilhe com sua equipe e comece a avaliar! 🚀

---

## 📞 Suporte

- **Streamlit Community**: https://discuss.streamlit.io
- **Documentação**: https://docs.streamlit.io
- **GitHub Issues**: No seu repositório
- **Google Cloud**: https://support.google.com

---

**Última atualização**: 1º de fevereiro de 2026  
**Versão**: 2.0 (Cloud-ready)
