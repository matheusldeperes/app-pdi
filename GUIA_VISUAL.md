# 📸 GUIA VISUAL - Sistema de Avaliação e PDI

## 🎬 Visão Geral do App

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Sistema de Avaliação e Plano de Desenvolvimento        │
│  Gestão de Performance e PDI - SATTE ALAM MOTORS           │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ⚙️ MENU LATERAL                                              │
├──────────────────────────────────────────────────────────────┤
│  ○ 📝 Nova Avaliação                                         │
│  ○ 👥 Visualizar Colaboradores                              │
│  ○ 📊 Relatório                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📝 Tela 1: Nova Avaliação

```
┌────────────────────────────────────────────────────────────────┐
│                    FORMULÁRIO DE AVALIAÇÃO                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ Nome do Colaborador: [________________]                        │
│ Avaliador:          [________________]                        │
│ Data:               [DD/MM/YYYY]                              │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 🎯 MATRIZ DE COMPETÊNCIAS                                     │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│ Organização (manutenção de box)                               │
│ [1]  [2]  [3]  [4]  [5] ← Nota      [Observações...]         │
│                                                                │
│ Trabalho em Equipe                                            │
│ [1]  [2]  [3]  [4]  [5] ← Nota      [Observações...]         │
│                                                                │
│ (... 5 critérios mais)                                        │
│                                                                │
│ ═══════════════════════════════════════════════════════════   │
│ Total de Pontos: 28/35 - 🟡 MANUTENÇÃO                       │
│ ═══════════════════════════════════════════════════════════   │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 📋 PLANO DE DESENVOLVIMENTO INDIVIDUAL (PDI)                 │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│ ✅ Pontos Fortes        │  ❌ Gargalos                        │
│ [_________________]     │  [_________________]                │
│ [_________________]     │  [_________________]                │
│                                                                │
│ 🚀 Ações de Melhoria                                          │
│ [_________________] → Como: [_________________]              │
│ [_________________] → Como: [_________________]              │
│                                                                │
│        ┌──────────────────────┐                               │
│        │  💾 SALVAR AVALIAÇÃO │                               │
│        └──────────────────────┘                               │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 👥 Tela 2: Visualizar Colaboradores

```
┌────────────────────────────────────────────────────────────────┐
│               COLABORADORES REGISTRADOS                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ Selecione um colaborador: [João Silva ▼]                      │
│                                                                │
│                            📋 Avaliação de João Silva          │
│                                              🗑️ [Deletar]     │
│                                                                │
│ Avaliador: Gerente Técnico    Data: 2026-02-01                │
│ Classificação: 🟢 ALTO DESEMPENHO                             │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 🎯 NOTAS POR CRITÉRIO                                         │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│ ┌──────────────────────┐  ┌──────────────────────┐            │
│ │ Critério    | Nota   │  │   Gráfico de Radar   │            │
│ ├──────────────────────┤  │     (Interativo)     │            │
│ │ Organização │  4     │  │                      │            │
│ │ Equipe      │  5     │  │                      │            │
│ │ Comunic.    │  4     │  │   [Visualização]     │            │
│ │ Eficiência  │  5     │  │                      │            │
│ │ Qualidade   │  4     │  │                      │            │
│ │ Processos   │  5     │  │                      │            │
│ │ Capacitação │  4     │  │                      │            │
│ └──────────────────────┘  └──────────────────────┘            │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 📋 PLANO DE DESENVOLVIMENTO INDIVIDUAL                         │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│ ✅ Pontos Fortes                 ❌ Gargalos                  │
│ • Liderança natural              • Quer fazer tudo sozinho     │
│ • Zero retrabalhos               • Pouco registro no sistema   │
│                                                                │
│ 🚀 Ações de Melhoria                                          │
│ ┌─ Ação 1 ────────────────────────────────────────────┐      │
│ │ Curso de liderança e gestão de equipes            │      │
│ │ Prazos: Próximos 3 meses - 1 curso por mês       │      │
│ └─────────────────────────────────────────────────────┘      │
│ ┌─ Ação 2 ────────────────────────────────────────────┐      │
│ │ Treinar para posição de Líder Técnico             │      │
│ │ Prazos: Acompanhamento mensal com gerente         │      │
│ └─────────────────────────────────────────────────────┘      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 Tela 3: Relatório

```
┌────────────────────────────────────────────────────────────────┐
│           📊 RELATÓRIO GERAL DE PERFORMANCE                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ ┌─────────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│ │ Colaboradores: 3    │  │ Média: 19.3/35   │  │ Alto Des.: 1│ │
│ └─────────────────────┘  └──────────────────┘  └────────────┘ │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 📊 DISTRIBUIÇÃO DE PONTUAÇÕES                                 │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│ ┌──────────────────────────┐  ┌──────────────────────────┐    │
│ │ Gráfico de Barras        │  │ Curva de Vitalidade      │    │
│ │                          │  │ (Distribuição Normal)    │    │
│ │  João    31 ██████████   │  │                          │    │
│ │  Maria   19 ██████       │  │    ╱╲                    │    │
│ │  Carlos   8 ██           │  │   ╱  ╲                   │    │
│ │                          │  │  ╱    ╲                  │    │
│ │                          │  │ ╱      ╲                 │    │
│ │                          │  │ ← Risco │Manutenção│Alto │    │
│ └──────────────────────────┘  └──────────────────────────┘    │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 📋 RESUMO DE TODOS OS COLABORADORES                           │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│ │ Nome    │ Avaliador │ Data       │ Pontos │ Classificação   │
│ ├─────────┼───────────┼────────────┼────────┼─────────────────┤
│ │ João    │ Gerente   │ 2026-02-01 │  31   │ 🟢 ALTO DES.    │
│ │ Maria   │ Gerente   │ 2026-02-01 │  19   │ 🟡 MANUTENÇÃO   │
│ │ Carlos  │ Gerente   │ 2026-02-01 │  8    │ 🔴 RISCO        │
│                                                                │
│ ───────────────────────────────────────────────────────────   │
│ 🎯 ANÁLISE POR CRITÉRIO                                       │
│ ───────────────────────────────────────────────────────────   │
│                                                                │
│  Organização ████████░░ 3.2                                    │
│  Equipe      ███████░░░ 3.1                                    │
│  Comunicação ███████░░░ 3.0                                    │
│  Eficiência  ████████░░ 3.2                                    │
│  Qualidade   ██████░░░░ 2.7                                    │
│  Processos   ████████░░ 3.2                                    │
│  Capacitação ██████░░░░ 2.1                                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Códigos de Cores

### Classificação de Performance
```
🟢 ALTO DESEMPENHO (Verde #00A86B)
   ↓
   31 a 35 pontos
   "Candidato à promoção/bonificação"
   
🟡 MANUTENÇÃO (Amarelo #FFD700)
   ↓
   16 a 30 pontos
   "Colaborador estável, necessita ajustes"
   
🔴 RISCO (Vermelho #FF6B6B)
   ↓
   Abaixo de 16 pontos
   "Performance crítica"
```

### Indicadores Visuais
- ✅ Pontos Fortes (verde/positivo)
- ❌ Gargalos (vermelho/negativo)
- 🚀 Ações de Melhoria (azul/progresso)
- 📊 Dados de Estrutura (roxo)

---

## 🔄 Fluxo de Dados

```
┌──────────────────────────────────────────────────────────────┐
│                        USUÁRIO                               │
└──────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   STREAMLIT (Interface)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────┐       │
│  │ Formulário  │  │ Visualizar  │  │   Relatório    │       │
│  │ (Input)     │  │ (Edit/Del)  │  │  (Gráficos)    │       │
│  └─────────────┘  └─────────────┘  └────────────────┘       │
└──────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              PROCESSAMENTO (Python/Pandas)                   │
│   • Validação de dados                                       │
│   • Cálculos (totais, médias)                                │
│   • Classificações                                           │
└──────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│         ARMAZENAMENTO PERSISTENTE (JSON Local)               │
│                  avaliacoes_pdi.json                         │
│                                                              │
│  {                                                           │
│    "João Silva_2026-02-01": {                                │
│      "nome": "João Silva",                                   │
│      "scores": {...},                                       │
│      "total_pontos": 31,                                     │
│      ...                                                     │
│    }                                                         │
│  }                                                           │
└──────────────────────────────────────────────────────────────┘
                          │
                    Persiste
               Entre execuções
                do aplicativo
```

---

## 📱 Responsividade

O app adapta-se a diferentes tamanhos de tela:

```
Desktop (Recomendado)          Mobile/Tablet
┌──────────────────┐          ┌───────────┐
│ ◀ MENU │ CONTEÚDO│          │ ◀ ≡ │APP  │
│        │ (2cols) │          │ ─────────│
│        │ Lado-a- │     →    │ CONTEÚDO │
│        │ lado    │          │ (Stack)  │
└──────────────────┘          └───────────┘
```

---

## ⚡ Performance

- **Carregamento**: < 2 segundos (primeira vez)
- **Interações**: Resposta imediata
- **Gráficos**: Renderização em tempo real
- **Dados**: Salvos localmente (sem internet)

---

## 🔐 Fluxo de Segurança

```
Computador → App → JSON Local → Backup Manual
  Local       ✓      ✓            ✓
  Seguro     ✓      ✓            ✓
```

Nenhum dado sai do seu computador!

---

**Versão**: 1.0  
**Data**: 1º de fevereiro de 2026  
**Status**: ✅ Pronto para Produção
