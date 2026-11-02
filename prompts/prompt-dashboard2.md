# Contexto
Mesmo projeto. Agora implemente a aba "Painel de KPIs" (Dashboard 2) no app.py,
EXATAMENTE com as escolhas abaixo, que foram definidas por mim. Não acrescente,
troque nem sugira métricas, gráficos ou filtros.

# Entrada
- Rascunho do layout: entregas/rascunho-dashboard2.jpg (siga o layout).
- Público-alvo (definido por mim): pessoas que querem acompanhar e entender o clima
  de Curitiba, para identificar meses mais secos, chuvosos ou quentes.

# Filtros (dentro da aba 2, não na sidebar)
- Ano: st.selectbox com "Todos" + os anos de date_year.
- Mês: st.selectbox com "Todos" + jan a dez.
- Período: st.date_input de intervalo (padrão: data mínima e máxima do dataset).
  Trate o caso de o usuário ter escolhido só a data inicial.
- Ano e Período filtram métricas E gráficos (os dois juntos).
  Mês filtra SOMENTE as métricas; os gráficos continuam com todos os meses.
- Se a combinação deixar 0 linhas, mostre um aviso em vez de erro.

# Métricas (st.metric, 4 colunas)
1. Umidade média: média de "UMIDADE_RELATIVA_DO_AR__HORARIA_(%)" nas linhas filtradas.
2. Temperatura média: média de "TEMPERATURA_DO_AR_-_BULBO_SECO__HORARIA_(°C)".
3. Dias com chuva: somar "PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)" por dia (coluna Data)
   e contar os dias com total >= 1 mm.
4. Variação da umidade: diferença, em pontos percentuais, entre a umidade média
   (coluna horária) do mês de referência e a do mês anterior.
   - Mês de referência: se o filtro Mês tiver um mês escolhido, é esse mês no ano
     mais recente disponível dentro de Ano/Período; se Mês = "Todos", é o último
     ano-mês disponível no período.
   - Para janeiro: comparar com dezembro do ano anterior. Se dezembro do ano
     anterior não existir nos dados, mostrar "—" sem comparação.
   - Mostre o valor da diferença (ex.: "+3,2 p.p.") e indique no rótulo ou no help
     quais meses foram comparados (ex.: "jan/2020 vs dez/2019").

# Gráficos (Altair; eixo X = linha do tempo ano-mês, ex.: jan/2019, fev/2019)
1. Linha: umidade média (coluna horária) por ano-mês.
2. Linha: temperatura média (coluna horária) por ano-mês.
3. Barras: quantidade de dias com chuva (mesma regra da métrica 3) por ano-mês.
- Agregue em pandas antes de enviar ao Altair (nunca as linhas brutas).
- Use a mesma cor de destaque do app, títulos descritivos neutros e tooltip com o valor.

# Restrições (regras de IA da disciplina — obrigatórias)
- Não interprete os dados nem escreva conclusões ou textos explicativos sobre o clima.
- Marque todo trecho criado ou alterado com: # [IA] Claude Code – <finalidade>
- Não altere a aba 1, os notebooks nem o README. Não faça commit nem push.
- Teste com AppTest: Ano "Todos" e um ano; Mês "Todos" e um mês; janeiro
  (com e sem dezembro anterior nos dados); período que zera os dados. Confira
  também a renderização dos gráficos (como você fez antes com vl-convert).
- Salve este prompt, exatamente como recebido, em prompts/prompt-dashboard2.md.
- Código simples e comentado em português.

# Formato de saída
Liste os arquivos alterados e explique em português simples, bloco por bloco,
o que a aba 2 faz.
