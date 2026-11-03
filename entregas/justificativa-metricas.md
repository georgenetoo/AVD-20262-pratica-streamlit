# Justificativa das métricas — Dashboard 2

**Público-alvo:** Pessoas que querem acompanhar e entender o clima de Curitiba.

**Decisão apoiada pelo painel:** Identificar os meses mais secos, chuvosos ou quentes para ajudar no planejamento de atividades ao ar livre.

**Observação sobre as variáveis:** Usar as colunas medidas a cada hora: Temperatura (°C) e Umidade (%), pois assim sabemos de onde vêm os valores e como calcular as médias.

**Observação sobre os dados:** Remover as 5.832 linhas duplicadas identificadas para evitar distorções nas métricas e nos gráficos.

## Métrica 1: Umidade média

- **Variável:** `UMIDADE_RELATIVA_DO_AR__HORARIA_(%)`
- **O que mede:** A média da umidade do ar no período selecionado.
- **Por que foi escolhida:** Porque ajuda a identificar os períodos em que o ar fica mais seco ou mais úmido.
- **Público-alvo:** Pessoas que querem acompanhar e entender o clima de Curitiba.
- **Qual decisão pode ser apoiada por essa métrica?** Escolher períodos com condições de umidade mais agradáveis para realizar atividades ao ar livre.
- **O que comunica ao público-alvo:** Mostra o nível médio de umidade do ar, em porcentagem, durante o período escolhido.

## Métrica 2: Temperatura média

- **Variável:** `TEMPERATURA_DO_AR_-_BULBO_SECO__HORARIA_(°C)`
- **O que mede:** A média das temperaturas registradas no período escolhido.
- **Por que foi escolhida:** Porque permite identificar os períodos mais quentes e mais frios de Curitiba.
- **Público-alvo:** Pessoas que querem acompanhar e entender o clima de Curitiba.
- **Qual decisão pode ser apoiada por essa métrica?** Escolher os meses com temperaturas mais agradáveis para passeios e atividades ao ar livre.
- **O que comunica ao público-alvo:** Mostra a temperatura média, em graus Celsius, no período selecionado.

## Métrica 3: Dias com chuva

- **Variável:** `PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)` e `Data`
- **O que mede:** A quantidade de dias que tiveram pelo menos 1 mm de chuva acumulada.
- **Por que foi escolhida:** Porque ajuda a identificar os períodos em que chove com mais frequência.
- **Público-alvo:** Pessoas que querem acompanhar e entender o clima de Curitiba.
- **Qual decisão pode ser apoiada por essa métrica?** Planejar atividades ao ar livre em meses que historicamente apresentam menos dias de chuva.
- **O que comunica ao público-alvo:** Mostra quantos dias tiveram chuva no período selecionado, considerando o limite de 1 mm por dia.

## Métrica 4: Variação da umidade

- **Variável:** `UMIDADE_RELATIVA_DO_AR__HORARIA_(%)`, `date_year` e `date_month`
- **O que mede:** A diferença entre a umidade média de um mês e a do mês anterior, em pontos percentuais. Quando um mês é selecionado, ele é comparado com o anterior. Se estiver em "Todos", é utilizado o último mês disponível no período. Se houver vários anos, considera-se o mais recente. Em janeiro, a comparação é feita com dezembro do ano anterior. São utilizados os meses completos, mesmo que estejam fora do período filtrado. Se não houver dados suficientes, a variação não é calculada.
- **Por que foi escolhida:** Porque permite perceber se a umidade está aumentando ou diminuindo de um mês para o outro.
- **Público-alvo:** Pessoas que querem acompanhar e entender o clima de Curitiba.
- **Qual decisão pode ser apoiada por essa métrica?** Observar as mudanças na umidade para escolher períodos com condições mais adequadas para atividades ao ar livre.
- **O que comunica ao público-alvo:** Mostra se a umidade média aumentou ou diminuiu em relação ao mês anterior e qual foi essa diferença em pontos percentuais.