# Entregáveis: materiais de apoio

Esta pasta reúne os materiais de partida para os entregáveis exigidos pelo enunciado da disciplina IF699 Aprendizagem de Máquina (graduação, oferta 2026.2, release 2026.2.1). As datas de entrega e de apresentação serão definidas pelo professor e divulgadas à turma. Os grupos não são obrigados a usar LaTeX, mas a estrutura e o nível de detalhe sugeridos devem ser respeitados.

| Arquivo | O que é | Como usar |
|---|---|---|
| `projeto-final-IF699-2026.2.pdf` | Enunciado completo do Projeto Final: objetivos, modelos tema, seleção dos 12 datasets, protocolo de treino, validação e teste, estudo de overfitting, comparação descritiva, entregáveis, avaliação e glossário. | Leia antes de começar; é a referência normativa do projeto. |
| `relatorio-template-IF699.pdf` | Estrutura do relatório: resumo, introdução, Etapa 1 (fundamentação teórica do modelo tema), Etapa 2 (seleção dos 12 datasets, protocolo experimental de treino, validação e teste com as fases, os arquivos, os commits do lock e dos resultados e a saída de `check_protocol`, sistemas, sensibilidade e estudo específico do modelo quando exigidos, estudo de overfitting e viés-variância com tabelas e figuras (inclusive matrizes de confusão nas predições de validação), implementação, avaliação final com a comparação entre validação interna e teste, resultados, comparação descritiva (média e desvio por dataset, vitórias, empates e derrotas, posto médio e padrão vs. com busca), análise por regime, custo vs. desempenho, respostas aos roteiros dos notebooks 04 e 05, inclusive a pergunta conceitual sobre os limites das conclusões com 12 datasets sem teste de hipótese), discussão com ameaças à validade, reprodutibilidade, referências e apêndices (tabela dos datasets, espaço de busca, resultados por dataset e registro do protocolo). | Use como esqueleto; substitua os campos entre colchetes e mantenha as seções na ordem proposta. |
| `slides-template-IF699.pdf` | Estrutura sugerida da apresentação (cerca de 12 frames) para 10 minutos em dois blocos contíguos de 5 minutos (Etapa 1 e Etapa 2), com frames de protocolo (diagrama do fluxo) e de overfitting. | Use como esqueleto. Os comentários do arquivo-fonte (`fontes/slides-template/slides.tex`) sugerem uma distribuição dos frames entre os integrantes; essa indicação não aparece no PDF. |
| `rubrica-IF699.pdf` | Rubrica de avaliação que decompõe o esquema 40 + 50 + 10 do enunciado (explicação do modelo, experimentos e apresentação) em critérios com pesos e quatro níveis de desempenho sem lacunas (item ausente vale 0), inclusive o critério de implementação da comparação descritiva, o de protocolo experimental e estudo de overfitting, a verificação por `check_protocol` e pelo histórico git e a penalidade por uso do teste anterior ao commit do lock ou por reexecução da avaliação final. | Consulte durante o trabalho como guia do que será avaliado. |

Os arquivos-fonte (`.tex`) do relatório e dos slides estão em `fontes/`:

- `fontes/common/preamble.tex`: preâmbulo usado pelo relatório;
- `fontes/relatorio-template/relatorio.tex`: compilar dentro de `fontes/relatorio-template/` com `pdflatex relatorio.tex` (duas passadas);
- `fontes/slides-template/slides.tex`: compilar dentro de `fontes/slides-template/` com `pdflatex slides.tex` (duas passadas; usa o pacote `tikz` para o diagrama do protocolo).

A rubrica é distribuída apenas em PDF, pois serve de referência para a avaliação e não compõe os entregáveis do grupo.

Figuras e tabelas geradas por `notebooks/04_analise_descritiva.ipynb` e `notebooks/05_overfitting.ipynb` ficam em `results/figures/` e podem ser incluídas diretamente nos fontes (ajuste os caminhos relativos em `\includegraphics`).
