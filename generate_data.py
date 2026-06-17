"""
Gera um dataset sintético (porém realista) de Digital Analytics / E-commerce.
Cada linha = um dia, por canal e por dispositivo, com métricas de funil.

Rode com:  python generate_data.py
Isso cria o arquivo  data/ga4_ecommerce_sample.csv

OBS: quando você tiver dados reais do GA4 (via export do BigQuery),
basta gerar um CSV com as mesmas colunas e trocar o arquivo.
"""

import numpy as np
import pandas as pd

np.random.seed(42)  # garante que os dados sejam sempre os mesmos

# ---- Configuração ----
DIAS = 90
CANAIS = {
    "Organic Search": {"base": 800, "cr": 0.030},
    "Paid Search":    {"base": 500, "cr": 0.040},
    "Direct":         {"base": 600, "cr": 0.035},
    "Social":         {"base": 450, "cr": 0.018},
    "Email":          {"base": 250, "cr": 0.055},
    "Referral":       {"base": 200, "cr": 0.025},
}
DISPOSITIVOS = {"Mobile": 0.58, "Desktop": 0.36, "Tablet": 0.06}
CATEGORIAS = ["Moda", "Eletrônicos", "Casa", "Beleza", "Esportes", "Livros"]

datas = pd.date_range(end=pd.Timestamp.today().normalize(), periods=DIAS)

linhas = []
for data in datas:
    # padrão semanal (fim de semana cai um pouco) + leve tendência de crescimento
    fator_semana = 0.85 if data.weekday() >= 5 else 1.0
    tendencia = 1 + (data - datas[0]).days / DIAS * 0.25
    ruido_dia = np.random.normal(1.0, 0.08)

    for canal, cfg in CANAIS.items():
        for disp, peso in DISPOSITIVOS.items():
            sessoes = int(cfg["base"] * peso * fator_semana * tendencia * ruido_dia)
            if sessoes <= 0:
                continue
            usuarios = int(sessoes * np.random.uniform(0.80, 0.92))
            product_views = int(sessoes * np.random.uniform(0.55, 0.72))
            add_to_cart = int(product_views * np.random.uniform(0.18, 0.28))

            # mobile converte um pouco menos
            ajuste_cr = 0.85 if disp == "Mobile" else 1.0
            cr = cfg["cr"] * ajuste_cr * np.random.uniform(0.85, 1.15)
            compras = int(sessoes * cr)
            compras = min(compras, add_to_cart)  # não pode comprar sem add no carrinho

            ticket_medio = np.random.uniform(150, 400)
            receita = round(compras * ticket_medio, 2)

            linhas.append({
                "data": data.date(),
                "canal": canal,
                "dispositivo": disp,
                "categoria_top": np.random.choice(CATEGORIAS),
                "sessoes": sessoes,
                "usuarios": usuarios,
                "product_views": product_views,
                "add_to_cart": add_to_cart,
                "compras": compras,
                "receita": receita,
            })

df = pd.DataFrame(linhas)
df.to_csv("data/ga4_ecommerce_sample.csv", index=False)
print(f"OK! {len(df)} linhas geradas em data/ga4_ecommerce_sample.csv")
print(df.head())
