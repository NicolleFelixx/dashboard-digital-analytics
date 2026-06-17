# 📊 Digital Analytics Dashboard — E-commerce

Dashboard web interativo que analisa métricas de **aquisição, comportamento e conversão** de um e-commerce, construído com **Python + Streamlit**.

> ⚠️ **Dados sintéticos** gerados para fins de demonstração (ver `generate_data.py`). A estrutura segue o modelo de dados do **Google Analytics 4**, então pode ser facilmente trocada por um export real do GA4 via BigQuery.

🔗 **Acesse o dashboard ao vivo:** _(adicione aqui o link do Streamlit Cloud depois do deploy)_

---

## 🎯 Pergunta de negócio

> Quais canais e dispositivos trazem mais sessões, onde está o gargalo do funil e qual canal gera mais receita?

Este projeto responde a essas perguntas de forma visual e interativa, permitindo filtrar por período, canal e dispositivo.

## ✨ O que o dashboard mostra

- **KPIs principais:** sessões, usuários, taxa de conversão, receita e ticket médio
- **Série temporal** de sessões ao longo do tempo
- **Receita por canal** de aquisição
- **Funil de conversão:** sessões → visualizações de produto → carrinho → compra
- **Receita por dispositivo** (mobile, desktop, tablet)
- **Tabela de desempenho** por canal com taxa de conversão

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-F72585?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-F72585?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-9D4EDD?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-9D4EDD?style=for-the-badge&logo=streamlit&logoColor=white)

## 🚀 Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/NicolleFelixx/dashboard-digital-analytics.git
cd dashboard-digital-analytics

# 2. Instale as dependências
pip install -r requirements.txt

# 3. (Opcional) Gere os dados de exemplo novamente
python generate_data.py

# 4. Rode o app
streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

## 📁 Estrutura do projeto

```
dashboard-digital-analytics/
├── app.py                # aplicação Streamlit (dashboard)
├── generate_data.py      # gera os dados sintéticos
├── requirements.txt      # dependências
├── data/
│   └── ga4_ecommerce_sample.csv
└── .streamlit/
    └── config.toml       # tema visual
```

## 💡 Principais insights (exemplo)

_Preencha esta seção com o que você observar ao explorar os dados, por exemplo:_

- O canal **Email** tem a maior taxa de conversão, apesar de menor volume de sessões.
- O **mobile** concentra a maioria das sessões, mas converte menos que o desktop.
- O maior gargalo do funil está entre **visualização de produto e adição ao carrinho**.

## 🔄 Próximos passos

- [ ] Conectar com dados reais do GA4 via BigQuery
- [ ] Adicionar comparação entre períodos (mês atual vs. anterior)
- [ ] Incluir análise de coorte / retenção

---

Feito com 💜 por **Nicolle Felix** — [LinkedIn](https://www.linkedin.com/in/nicolle-felix-4ab62b2aa) · [GitHub](https://github.com/NicolleFelixx)
