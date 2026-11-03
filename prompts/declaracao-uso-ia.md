# Declaração de Uso de IA

**Nome:** George Almerio Alves Neto (turma 5A — gaan@cesar.school)
**Data:** 02/11/2026 (entrega em 03/11/2026)

> Documento oficial assinado via gov.br, com o registro completo bloco a bloco (9 usos): `prompts/DECLARACAO_IA.pdf`.

## Ferramenta

- **Claude (claude.ai, chat web)** — modelo Claude Opus 5.5, assinatura paga. Tutor de setup e ambiente, código de exportação do dataset, elaboração dos prompts a partir do meu rascunho e das minhas especificações, depuração, transcrição/revisão ortográfica da justificativa, orientação do deploy e montagem da declaração.
- **Claude Code (extensão oficial do VS Code)** — modelo Claude Opus 5.5 (esforço High). Inserção de células no notebook, esqueleto do `app.py`, Dashboard 1, identidade visual, correções e implementação do Dashboard 2 conforme minhas especificações.
- **Skill oficial do Streamlit** (`developing-with-streamlit`, instalada com `streamlit skills --yes`, Streamlit 1.66.1) — **usada**, lida automaticamente pelo Claude Code.

## Prompt usado

Os prompts principais estão salvos na íntegra, exatamente como enviados:

1. **Esqueleto + Dashboard 1** (Template de Prompt: Contexto, Entrada, Restrições, Formato de saída), a partir de `entregas/rascunho-dashboard1.jpg` → `prompts/layout-skeleton-prompt.md`
2. **Dashboard 2**, com o público-alvo, as métricas, os gráficos e os filtros definidos por mim, a partir de `entregas/rascunho-dashboard2.jpg` → `prompts/prompt-dashboard2.md`
3. **Correção dos gráficos do Dashboard 1** (Claude Code):

```text
Rodei o app e vi 2 problemas na tela (os testes do AppTest não pegam isso):

1. Os histogramas aparecem só com os eixos, SEM nenhuma barra, em todas as
   variáveis. Descubra a causa (confira o spec com chart.to_dict() e os dados
   enviados) e corrija para as barras aparecerem.
2. No mapa de calor, o eixo X esconde metade dos nomes das variáveis
   (sobreposição). Faça todos os nomes aparecerem (ex.: labelOverlap=False,
   ângulo inclinado e limite de tamanho do texto).

Mesmas regras de antes: marque o que alterar com # [IA] Claude Code – <finalidade>,
não faça commit e me explique em poucas linhas o que causava cada problema.
```

4. **Inserção das células de exportação no notebook** (Claude Code): pedido para remover a linha `!pip install kagglehub` e adicionar ao final de `notebooks/eda-com-downloads.ipynb` 4 células com conteúdo fixo (pastas, cópia do CSV bruto, conversão de tipos e exportação), sem executar o notebook nem alterar outros arquivos.

Os demais usos (dúvidas de ambiente, Git, deploy e revisão de texto) foram conversas de tutoria no claude.ai, registradas no PDF.

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** o código do Dashboard 1 (filtros, mapa de calor e histogramas), a identidade visual, a implementação do Dashboard 2 e as células de exportação/conversão de tipos do notebook. Aceitei porque funcionaram nos testes manuais no navegador e eu sei explicar cada bloco. Também aceitei dois ajustes de apresentação feitos pela ferramenta por conta própria (nomes curtos das variáveis e mapa de calor sem a diagonal).
- **Modificado:** removi a linha `!pip install` do notebook e acrescentei a remoção de 5.832 linhas duplicadas (`drop_duplicates()`), decisão minha após a ferramenta apontar o problema. Nas ambiguidades levantadas sobre o Dashboard 2, eu decidi cada ponto: colunas horárias, regra do mês de referência, janeiro comparado com dezembro do ano anterior, eixo ano-mês, filtro Mês só nas métricas e meses completos na métrica 4. As sugestões de clareza para a justificativa e para a reflexão foram aplicadas a meu critério.
- **Rejeitado:** a primeira versão dos gráficos do Dashboard 1, porque os histogramas apareciam sem barras e os rótulos do mapa de calor ficavam ocultos. Ela foi substituída pela correção do prompt 3. A IA não escolheu métricas, não escreveu a justificativa e não interpretou os dados.