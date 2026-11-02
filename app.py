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

# ---------------------------------------------------------------------------------------------
# Dashboard 2 – Painel de KPIs (métricas, gráficos e filtros definidos pelo aluno)
# ---------------------------------------------------------------------------------------------

# [IA] Claude Code – colunas usadas no Dashboard 2 (nomes originais do INMET)
COL_UMIDADE = "UMIDADE_RELATIVA_DO_AR__HORARIA_(%)"
COL_TEMPERATURA = "TEMPERATURA_DO_AR_-_BULBO_SECO__HORARIA_(°C)"
COL_CHUVA = "PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)"

# [IA] Claude Code – nomes dos meses em português: MESES[0] = "jan" ... MESES[11] = "dez"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

# [IA] Claude Code – expressão do Vega que escreve as datas do eixo X como "jan/2019"
# (month() do Vega vai de 0 a 11, por isso serve direto como posição na lista de meses)
ROTULO_EIXO_MES = (
    "['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']"
    "[month(datum.value)] + '/' + year(datum.value)"
)


# [IA] Claude Code – escreve um ano-mês como texto: (2019, 1) -> "jan/2019"
def rotulo_mes(ano, mes):
    return f"{MESES[mes - 1]}/{ano}"


# [IA] Claude Code – formata um número decimal no padrão brasileiro (78.4 -> "78,4")
def formatar_decimal(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


# [IA] Claude Code – soma a chuva de cada dia (coluna Data) e marca os dias com total >= 1 mm
def chuva_por_dia(dados):
    por_dia = dados.groupby("Data")[COL_CHUVA].sum().reset_index()
    por_dia["choveu"] = por_dia[COL_CHUVA] >= 1
    return por_dia


# [IA] Claude Code – tabela pequena com UMA linha por ano-mês: umidade média, temperatura média
# e quantidade de dias com chuva. É ela (e não as linhas brutas) que vai para o Altair
def resumo_mensal(dados):
    medias = dados.groupby(["date_year", "date_month"])[[COL_UMIDADE, COL_TEMPERATURA]].mean()

    dias = chuva_por_dia(dados)
    dias["date_year"] = dias["Data"].dt.year
    dias["date_month"] = dias["Data"].dt.month
    dias_com_chuva = dias.groupby(["date_year", "date_month"])["choveu"].sum()

    resumo = medias.join(dias_com_chuva).reset_index()
    resumo = resumo.rename(
        columns={COL_UMIDADE: "umidade", COL_TEMPERATURA: "temperatura", "choveu": "dias_chuva"}
    )
    # primeiro dia de cada mês, como data: é o que posiciona o ponto na linha do tempo
    resumo["mes"] = pd.to_datetime(
        resumo["date_year"].astype(str) + "-" + resumo["date_month"].astype(str) + "-01"
    )
    # texto "jan/2019", usado no tooltip
    resumo["rotulo"] = [rotulo_mes(a, m) for a, m in zip(resumo["date_year"], resumo["date_month"])]
    return resumo


# [IA] Claude Code – umidade média de um ano-mês no dataset COMPLETO (None se o mês não existe nos dados)
def umidade_do_mes(ano, mes):
    linhas = df[(df["date_year"] == ano) & (df["date_month"] == mes)]
    if linhas.empty:
        return None
    return linhas[COL_UMIDADE].mean()


# [IA] Claude Code – conteúdo da aba 2, seguindo o rascunho 2
with aba_kpis:
    st.subheader("Painel de KPIs")

    # [IA] Claude Code – filtros da aba 2 numa linha: Ano, Mês e Período
    data_minima = df["Data"].min().date()
    data_maxima = df["Data"].max().date()
    anos = sorted(df["date_year"].unique().tolist())

    col_ano, col_mes, col_periodo = st.columns(3)
    with col_ano:
        ano = st.selectbox("Ano", ["Todos"] + anos, key="kpi_ano")
    with col_mes:
        mes = st.selectbox("Mês", ["Todos"] + MESES, key="kpi_mes")
    with col_periodo:
        periodo = st.date_input(
            "Período",
            value=(data_minima, data_maxima),
            min_value=data_minima,
            max_value=data_maxima,
            format="DD/MM/YYYY",
            key="kpi_periodo",
        )

    # [IA] Claude Code – o date_input de intervalo devolve 2 datas, mas só 1 enquanto o usuário
    # escolheu apenas a data inicial (e 0 se ele apagou o campo)
    if len(periodo) == 2:
        inicio, fim = periodo
    elif len(periodo) == 1:
        inicio, fim = periodo[0], data_maxima
        st.caption("Só a data inicial foi escolhida: o período vai até a última data do dataset.")
    else:
        inicio, fim = data_minima, data_maxima

    # [IA] Claude Code – Ano e Período filtram métricas E gráficos
    filtro = df["Data"].between(pd.Timestamp(inicio), pd.Timestamp(fim))
    if ano != "Todos":
        filtro = filtro & (df["date_year"] == ano)
    df_periodo = df[filtro]

    # [IA] Claude Code – Mês filtra SOMENTE as métricas (os gráficos usam df_periodo, com todos os meses)
    if mes == "Todos":
        df_metricas = df_periodo
    else:
        numero_mes = MESES.index(mes) + 1  # "jan" -> 1, "fev" -> 2, ...
        df_metricas = df_periodo[df_periodo["date_month"] == numero_mes]

    if df_periodo.empty:
        # [IA] Claude Code – caso de borda: Ano + Período sem nenhuma linha
        st.warning("Nenhuma linha para o Ano e o Período escolhidos. Ajuste os filtros.")
    else:
        # [IA] Claude Code – as 4 métricas (st.metric) em 4 colunas
        if df_metricas.empty:
            st.warning("Nenhuma linha para o Mês escolhido dentro do Ano e do Período.")
        else:
            # Métrica 4: escolhe o mês de referência e o mês anterior
            if mes == "Todos":
                # último ano-mês disponível no período
                ultima_data = df_periodo["Data"].max()
                ano_ref, mes_ref = ultima_data.year, ultima_data.month
            else:
                # o mês escolhido, no ano mais recente disponível dentro de Ano/Período
                ano_ref, mes_ref = int(df_metricas["date_year"].max()), numero_mes
            if mes_ref == 1:
                ano_ant, mes_ant = ano_ref - 1, 12  # janeiro compara com dezembro do ano anterior
            else:
                ano_ant, mes_ant = ano_ref, mes_ref - 1

            umidade_ref = umidade_do_mes(ano_ref, mes_ref)
            umidade_ant = umidade_do_mes(ano_ant, mes_ant)
            texto_ref = rotulo_mes(ano_ref, mes_ref)
            texto_ant = rotulo_mes(ano_ant, mes_ant)
            if umidade_ant is None:
                # o mês anterior não existe nos dados: mostra "—" sem comparação
                variacao = "—"
                rotulo_variacao = "Variação da umidade"
                ajuda_variacao = f"Sem dados de {texto_ant} para comparar com {texto_ref}."
            else:
                diferenca = umidade_ref - umidade_ant
                # o "+" em :+.1f escreve sempre o sinal (+3.2 ou -3.2); depois troca o ponto por vírgula
                variacao = f"{diferenca:+.1f}".replace(".", ",") + " p.p."
                rotulo_variacao = f"Variação da umidade ({texto_ref} vs {texto_ant})"
                ajuda_variacao = (
                    f"Umidade média de {texto_ref} menos a de {texto_ant}, "
                    "em pontos percentuais (meses completos)."
                )

            dias_com_chuva = int(chuva_por_dia(df_metricas)["choveu"].sum())

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Umidade média", f"{formatar_decimal(df_metricas[COL_UMIDADE].mean())}%", border=True)
            m2.metric(
                "Temperatura média",
                f"{formatar_decimal(df_metricas[COL_TEMPERATURA].mean())} °C",
                border=True,
            )
            m3.metric(
                "Dias com chuva",
                formatar_inteiro(dias_com_chuva),
                help="Dias em que a soma da precipitação foi de 1 mm ou mais.",
                border=True,
            )
            m4.metric(rotulo_variacao, variacao, help=ajuda_variacao, border=True)

        # [IA] Claude Code – gráficos: dados agregados por ano-mês (uma linha por mês)
        resumo = resumo_mensal(df_periodo)
        eixo_x = alt.X(
            "yearmonth(mes):T", title=None, axis=alt.Axis(labelExpr=ROTULO_EIXO_MES, labelAngle=-45)
        )

        # [IA] Claude Code – monta um gráfico de linha; pontos invisíveis por cima recebem o tooltip
        def grafico_linha(coluna, titulo, titulo_y):
            base = alt.Chart(resumo).encode(
                x=eixo_x, y=alt.Y(f"{coluna}:Q", title=titulo_y, scale=alt.Scale(zero=False))
            )
            linha = base.mark_line(color=COR_DESTAQUE, strokeWidth=2)
            pontos = base.mark_circle(size=80, opacity=0).encode(
                tooltip=[
                    alt.Tooltip("rotulo:N", title="Mês"),
                    alt.Tooltip(f"{coluna}:Q", title=titulo_y, format=".1f"),
                ]
            )
            return (linha + pontos).properties(title=titulo, height=280)

        # [IA] Claude Code – linha 1 do rascunho: os dois gráficos de linha lado a lado
        g1, g2 = st.columns(2)
        with g1:
            st.altair_chart(
                grafico_linha("umidade", "Umidade relativa média por mês", "Umidade (%)"),
                width="stretch",
                alt="Gráfico de linha da umidade relativa média por mês",
            )
        with g2:
            st.altair_chart(
                grafico_linha("temperatura", "Temperatura média por mês", "Temperatura (°C)"),
                width="stretch",
                alt="Gráfico de linha da temperatura média por mês",
            )

        # [IA] Claude Code – linha 2 do rascunho: barras de dias com chuva na largura toda
        barras = (
            alt.Chart(resumo)
            .mark_bar(color=COR_DESTAQUE)
            .encode(
                x=eixo_x,
                y=alt.Y("dias_chuva:Q", title="Dias com chuva"),
                tooltip=[
                    alt.Tooltip("rotulo:N", title="Mês"),
                    alt.Tooltip("dias_chuva:Q", title="Dias com chuva"),
                ],
            )
            .properties(title="Dias com chuva (≥ 1 mm) por mês", height=260)
        )
        st.altair_chart(barras, width="stretch", alt="Gráfico de barras dos dias com chuva por mês")
