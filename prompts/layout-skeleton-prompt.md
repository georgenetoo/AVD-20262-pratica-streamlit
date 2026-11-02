# Contexto
Sou aluno da disciplina Análise e Visualização de Dados (CESAR School). Projeto: app
Streamlit com dois dashboards a partir da minha EDA do clima de Curitiba (dados horários
do INMET, ~213 mil linhas). O dado tratado está em data/clean/dataset.csv (gerado por
notebooks/eda-com-downloads.ipynb). Leia ROTEIRO.md, entregas/README.md e
ALTAIR-CROSSFILTER.md para entender a atividade. O app.py atual é o exemplo da
professora (Heart Disease) e deve ser substituído pelo meu.

# Entrada
- Rascunho do layout: entregas/rascunho-dashboard1.jpg (abra a imagem e siga o layout).
- Colunas: leia o cabeçalho de data/clean/dataset.csv.

# Tarefas
1. src/data_loader.py: adicione @st.cache_data e converta a coluna Data para datetime.
2. app.py com st.set_page_config(layout="wide") e duas abas (st.tabs):
   "Laboratório: correlação e distribuição" e "Painel de KPIs".
3. Sidebar do Dashboard 1:
   - st.multiselect com as colunas numéricas (seletor de variáveis). Padrão: as
     medições meteorológicas; deixe Diaano, date_year, date_month e date_day
     disponíveis, mas fora da seleção padrão.
   - Para cada variável selecionada, um st.slider de intervalo (mín–máx) que exclui
     as linhas fora da faixa.
   - Um texto mostrando quantas linhas restam depois dos filtros.
4. Aba 1 (Dashboard 1), com Altair:
   - Mapa de calor da matriz de correlação (st.radio para escolher Pearson ou
     Spearman), valores escritos nas células, escala divergente de -1 a 1,
     só o triângulo inferior.
   - Um histograma por variável selecionada, em grade de 2 colunas.
   - São ~213 mil linhas: calcule a correlação e os bins dos histogramas em
     pandas/numpy e envie ao Altair só os dados agregados, nunca as linhas brutas.
   - Trate os casos de borda: 0 variáveis (mensagem), 1 variável (sem mapa de calor,
     avisando que precisa de 2 ou mais) e filtros que deixam 0 linhas.
5. Aba 2 (Dashboard 2): apenas a ESTRUTURA vazia — uma linha de st.columns para
   3 a 5 st.metric e espaço para 3 gráficos, com comentários
   "# TODO (aluno): definido pelo aluno". NÃO crie, sugira nem calcule métricas,
   KPIs ou gráficos reais nesta aba.
6. .streamlit/config.toml: identidade visual coerente com o tema clima (temas light e
   dark), no formato que já existe no arquivo. Use a mesma cor de destaque nos gráficos.
7. requirements.txt: confirme que tudo que app.py e src/ importam está listado
   (Altair não precisa, vem com o Streamlit).
8. Teste com streamlit.testing.v1.AppTest os cenários: 0, 1 e 2+ variáveis, e um
   slider bem estreito. Corrija o que quebrar.
9. Salve este prompt, exatamente como recebido, em prompts/layout-skeleton-prompt.md
   (substituindo o template vazio).

# Restrições (regras de IA da disciplina — obrigatórias)
- Nunca escolha, sugira ou justifique métricas, KPIs ou gráficos do Dashboard 2.
  Nunca interprete os dados nem escreva conclusões, justificativas ou textos do README.
- Marque todo trecho que você criar ou alterar com: # [IA] Claude Code – <finalidade>
- Use sempre caminhos relativos. Não versione nada de data/raw. Não altere notebooks/.
- Não faça commit nem push.
- Código simples e comentado em português: sou iniciante e preciso saber explicar
  cada linha para a professora.

# Formato de saída
Ao final, liste os arquivos alterados e me explique em português simples, bloco por
bloco, o que cada parte do app.py faz.
