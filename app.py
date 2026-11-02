# [IA] Claude Code – bibliotecas usadas pelo app
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import load_data

# [IA] Claude Code – configuração da página: título da aba do navegador e layout largo
st.set_page_config(
    page_title="Clima de Curitiba",
    page_icon=":material/partly_cloudy_day:",
    layout="wide",
)

# [IA] Claude Code – cor de destaque dos gráficos: a MESMA do primaryColor em .streamlit/config.toml
COR_DESTAQUE = "#0277bd"

# [IA] Claude Code – nomes curtos só para exibir na tela (os nomes originais das colunas
# do INMET são longos e têm pontos, que o Altair confunde com campos aninhados)
NOMES_CURTOS = {
    "PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)": "Precipitação (mm)",
    "PRESSAO_ATMOSFERICA_AO_NIVEL_DA_ESTACAO__HORARIA_(mB)": "Pressão (mB)",
    "PRESSÃO_ATMOSFERICA_MAX.NA_HORA_ANT._(AUT)_(mB)": "Pressão máx. (mB)",
    "PRESSÃO_ATMOSFERICA_MIN._NA_HORA_ANT._(AUT)_(mB)": "Pressão mín. (mB)",
    "TEMPERATURA_DO_AR_-_BULBO_SECO__HORARIA_(°C)": "Temperatura (°C)",
    "TEMPERATURA_DO_PONTO_DE_ORVALHO_(°C)": "Ponto de orvalho (°C)",
    "TEMPERATURA_MÁXIMA_NA_HORA_ANT._(AUT)_(°C)": "Temperatura máx. (°C)",
    "TEMPERATURA_MÍNIMA_NA_HORA_ANT._(AUT)_(°C)": "Temperatura mín. (°C)",
    "TEMPERATURA_ORVALHO_MAX._NA_HORA_ANT._(AUT)_(°C)": "Orvalho máx. (°C)",
    "TEMPERATURA_ORVALHO_MIN._NA_HORA_ANT._(AUT)_(°C)": "Orvalho mín. (°C)",
    "UMIDADE_REL._MAX._NA_HORA_ANT._(AUT)_(%)": "Umidade máx. (%)",
    "UMIDADE_REL._MIN._NA_HORA_ANT._(AUT)_(%)": "Umidade mín. (%)",
    "UMIDADE_RELATIVA_DO_AR__HORARIA_(%)": "Umidade (%)",
    "VENTO__DIREÇÃO_HORARIA_(gr)_(°_(gr))": "Vento: direção (°)",
    "VENTO__RAJADA_MAXIMA_(m/s)": "Vento: rajada (m/s)",
    "VENTO__VELOCIDADE_HORARIA_(m/s)": "Vento: velocidade (m/s)",
    "RADIACAO_GLOBAL_(KJ/m²)": "Radiação global (KJ/m²)",
    "TEMPERATURA_MEDIA": "Temperatura média",
    "UMIDADE_MEDIA": "Umidade média",
    "Diaano": "Dia do ano",
    "date_year": "Ano",
    "date_month": "Mês",
    "date_day": "Dia do mês",
}

# [IA] Claude Code – colunas numéricas que ficam disponíveis no seletor, mas fora da seleção padrão
FORA_DO_PADRAO = ["Diaano", "date_year", "date_month", "date_day"]


# [IA] Claude Code – devolve o nome curto de uma coluna (ou o próprio nome, se não estiver no dicionário)
def nome_curto(coluna):
    return NOMES_CURTOS.get(coluna, coluna)


# [IA] Claude Code – formata números inteiros no padrão brasileiro (213.360 em vez de 213,360)
def formatar_inteiro(numero):
    return f"{numero:,}".replace(",", ".")


# [IA] Claude Code – calcula a correlação no pandas e devolve SÓ o triângulo inferior
# (abaixo da diagonal) numa tabela pequena: uma linha por célula do mapa de calor
def tabela_correlacao(dados, variaveis, metodo):
    matriz = dados[variaveis].corr(method=metodo)
    celulas = []
    for i, var_linha in enumerate(variaveis):
        for j, var_coluna in enumerate(variaveis):
            if j < i:  # j < i = abaixo da diagonal; a parte de cima é repetição (a matriz é simétrica)
                valor = matriz.iloc[i, j]
                celulas.append(
                    {
                        "linha": nome_curto(var_linha),
                        "coluna": nome_curto(var_coluna),
                        "correlacao": valor,
                        # texto escrito na célula; "–" quando não dá para calcular (variável sem variação)
                        "rotulo": "–" if pd.isna(valor) else f"{valor:.2f}".replace(".", ","),
                    }
                )
    return pd.DataFrame(celulas)


# [IA] Claude Code – calcula os bins do histograma com numpy e devolve só 20 linhas
# (início, fim e contagem de cada barra), em vez das ~213 mil linhas brutas
def tabela_histograma(serie, numero_de_bins=20):
    contagens, bordas = np.histogram(serie, bins=numero_de_bins)
    return pd.DataFrame({"inicio": bordas[:-1], "fim": bordas[1:], "contagem": contagens})


# [IA] Claude Code – carrega os dados (com cache) e separa as colunas numéricas
df = load_data()
colunas_numericas = df.select_dtypes(include="number").columns.tolist()
padrao = [coluna for coluna in colunas_numericas if coluna not in FORA_DO_PADRAO]

st.title("Clima de Curitiba: dados horários do INMET")

# [IA] Claude Code – sidebar do Dashboard 1: seletor de variáveis + um slider de intervalo por variável
with st.sidebar:
    st.header("Filtros")
    st.caption("Valem para a aba Laboratório.")

    variaveis = st.multiselect(
        "Variáveis",
        options=colunas_numericas,
        default=padrao,
        format_func=nome_curto,  # mostra o nome curto, mas guarda o nome original da coluna
        key="variaveis",
        help="Variáveis usadas no mapa de calor e nos histogramas.",
    )

    intervalos = {}
    for var in variaveis:
        # coluna de números inteiros: slider de 1 em 1; coluna decimal: slider de 0,1 em 0,1
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        if minimo == maximo:
            continue  # o st.slider exige mínimo < máximo; uma coluna constante não tem o que filtrar
        intervalos[var] = st.slider(
            nome_curto(var),
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

# [IA] Claude Code – aplica os sliders: mantém só as linhas dentro de TODOS os intervalos.
# A "máscara" é uma coluna de True/False: começa toda True e cada slider desliga as linhas fora da faixa
mascara = pd.Series(True, index=df.index)
for var, (inicio, fim) in intervalos.items():
    mascara = mascara & df[var].between(inicio, fim)
df_filtrado = df[mascara]

# [IA] Claude Code – texto com quantas linhas restam depois dos filtros
with st.sidebar:
    st.markdown(
        f"**{formatar_inteiro(len(df_filtrado))}** de {formatar_inteiro(len(df))} linhas "
        "dentro dos intervalos escolhidos."
    )

# [IA] Claude Code – as duas abas do app (Dashboard 1 e Dashboard 2)
aba_laboratorio, aba_kpis = st.tabs(["Laboratório: correlação e distribuição", "Painel de KPIs"])

# [IA] Claude Code – Dashboard 1: mapa de calor à esquerda e grade de histogramas à direita (rascunho 1)
with aba_laboratorio:
    col_correlacao, col_distribuicao = st.columns([1.1, 1], gap="large")

    with col_correlacao:
        st.subheader("Correlação")
        metodo = st.radio("Método", ["Pearson", "Spearman"], horizontal=True, key="metodo_correlacao")

        # casos de borda: menos de 2 variáveis ou menos de 2 linhas não formam uma correlação
        if len(variaveis) < 2:
            st.info("O mapa de calor precisa de 2 ou mais variáveis selecionadas na barra lateral.")
        elif len(df_filtrado) < 2:
            st.warning("Os filtros deixaram menos de 2 linhas: não dá para calcular a correlação.")
        else:
            corr = tabela_correlacao(df_filtrado, variaveis, metodo.lower())
            ordem = [nome_curto(var) for var in variaveis]
            n = len(variaveis)
            tamanho_texto = 14 if n <= 6 else 11 if n <= 12 else 8  # letra menor quando há muitas células

            # base comum: coluna no eixo x e linha no eixo y, na ordem escolhida no seletor
            # [IA] Claude Code – eixos que mostram TODOS os nomes: labelOverlap=False não esconde
            # rótulos sobrepostos, labelAngle=-45 inclina o texto e labelLimit corta nomes muito longos (px)
            base = alt.Chart(corr).encode(
                x=alt.X(
                    "coluna:N",
                    sort=ordem[:-1],
                    title=None,
                    axis=alt.Axis(labelAngle=-45, labelOverlap=False, labelLimit=160),
                ),
                y=alt.Y(
                    "linha:N",
                    sort=ordem[1:],
                    title=None,
                    axis=alt.Axis(labelOverlap=False, labelLimit=160),
                ),
            )
            # retângulos coloridos: escala divergente fixa de -1 a 1, com o neutro no 0
            celulas = base.mark_rect().encode(
                color=alt.Color(
                    "correlacao:Q",
                    title=metodo,
                    scale=alt.Scale(scheme="blueorange", domain=[-1, 1], domainMid=0),
                ),
                tooltip=[
                    alt.Tooltip("linha:N", title="Variável 1"),
                    alt.Tooltip("coluna:N", title="Variável 2"),
                    alt.Tooltip("rotulo:N", title=metodo),
                ],
            )
            # valor escrito em cada célula: branco nas cores fortes, preto nas claras
            valores = base.mark_text(fontSize=tamanho_texto).encode(
                text="rotulo:N",
                color=alt.condition(
                    "abs(datum.correlacao) > 0.6", alt.value("white"), alt.value("black")
                ),
            )
            st.altair_chart(
                (celulas + valores).properties(height=max(250, 32 * (n - 1))),
                width="stretch",
                alt=f"Mapa de calor da correlação de {metodo} entre as variáveis selecionadas (triângulo inferior)",
            )
            if corr["correlacao"].isna().any():
                st.caption("Células com “–”: alguma variável ficou sem variação dentro do filtro.")

    with col_distribuicao:
        st.subheader("Distribuição")

        # casos de borda: nenhuma variável ou nenhuma linha depois dos filtros
        if not variaveis:
            st.info("Selecione pelo menos 1 variável na barra lateral para ver os histogramas.")
        elif df_filtrado.empty:
            st.warning("Nenhuma linha dentro dos intervalos escolhidos. Amplie algum slider.")
        else:
            # um histograma por variável, em grade de 2 colunas (de 2 em 2 variáveis por linha)
            for inicio in range(0, len(variaveis), 2):
                colunas = st.columns(2)
                for coluna, var in zip(colunas, variaveis[inicio : inicio + 2]):
                    bins = tabela_histograma(df_filtrado[var])
                    # [IA] Claude Code – barras sem cantos arredondados: com x + x2 (bins prontos),
                    # o cornerRadius fazia o Vega-Lite não desenhar nenhuma barra
                    histograma = (
                        alt.Chart(bins)
                        .mark_bar(color=COR_DESTAQUE)
                        .encode(
                            # bin="binned" avisa ao Altair que os bins já vieram calculados do numpy
                            x=alt.X("inicio:Q", bin="binned", title=nome_curto(var)),
                            x2="fim:Q",
                            y=alt.Y("contagem:Q", title="Linhas"),
                            tooltip=[
                                alt.Tooltip("inicio:Q", title="De", format=".1f"),
                                alt.Tooltip("fim:Q", title="Até", format=".1f"),
                                alt.Tooltip("contagem:Q", title="Linhas", format=","),
                            ],
                        )
                        .properties(height=220)
                    )
                    with coluna:
                        st.altair_chart(
                            histograma, width="stretch", alt=f"Histograma de {nome_curto(var)}"
                        )

# [IA] Claude Code – Dashboard 2: só a ESTRUTURA vazia; o conteúdo é definido pelo aluno
with aba_kpis:
    st.subheader("Painel de KPIs")

    # TODO (aluno): definido pelo aluno – widgets que controlam este painel
    # TODO (aluno): definido pelo aluno – quais dados este painel usa

    # [IA] Claude Code – linha de métricas (ajuste a quantidade entre 3 e 5)
    NUMERO_DE_METRICAS = 4  # TODO (aluno): definido pelo aluno
    colunas_metricas = st.columns(NUMERO_DE_METRICAS)
    for numero, coluna in enumerate(colunas_metricas, start=1):
        with coluna:
            # TODO (aluno): definido pelo aluno – trocar este espaço por um st.metric(...)
            st.container(border=True).caption(f"Espaço para a métrica {numero}")

    # [IA] Claude Code – espaço para 3 gráficos (a disposição pode mudar conforme o rascunho 2)
    colunas_graficos = st.columns(3)
    for numero, coluna in enumerate(colunas_graficos, start=1):
        with coluna:
            # TODO (aluno): definido pelo aluno – trocar este espaço por um st.altair_chart(...)
            st.container(border=True, height=300).caption(f"Espaço para o gráfico {numero}")
