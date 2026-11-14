"""Comparação descritiva dos sistemas sobre os datasets selecionados (trabalho do grupo).

Entrada: a avaliação final (`results/test.csv`, gerada uma única vez por
`final_test` após o congelamento do protocolo). A unidade de comparação é o
DATASET: cada sistema recebe uma medida por dataset, a média dos 3 folds
externos oficiais (`src.pipeline.results.per_dataset`, que também aplica a regra
de completude). Os folds de um mesmo dataset não são tratados como observações
independentes.

A comparação é puramente descritiva: contagens de vitórias, empates e derrotas,
postos médios e diferenças médias. Não há testes de hipótese nem intervalos de
confiança; as conclusões do relatório devem ser formuladas como descrição do
comportamento observado nos datasets escolhidos, não como generalização. A
análise não retroalimenta o modelo, o espaço de busca nem a seleção de datasets.

Todas as funções recebem `higher_is_better`: verdadeiro para AUC, acurácia e
G-Mean; falso para entropia cruzada e tempos (ver
`src.pipeline.evaluate.HIGHER_IS_BETTER`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.pipeline.results import ok_results, per_dataset

DEFAULT_SYSTEM = "group_default"
TUNED_SYSTEM = "group_tuned"


def wins_ties_losses(
    table: pd.DataFrame,
    reference: str,
    higher_is_better: bool = True,
    tolerance: float = 0.0,
) -> pd.DataFrame:
    """Vitórias, empates e derrotas do sistema de referência contra cada outro, dataset a dataset.

    Args:
        table: tabela `dataset x sistema` com UMA medida por dataset (média dos
            folds externos), por exemplo a saída de `per_dataset`.
        reference: coluna do sistema de referência (em geral `group_tuned`).
        higher_is_better: orientação da métrica.
        tolerance: diferenças com |d| <= tolerance contam como empate.

    Para cada dataset, a diferença orientada é d = referência - outro quando
    maior é melhor e d = outro - referência quando menor é melhor, de modo que
    d > 0 sempre favorece a referência.

    Regra de empate: um dataset conta como empate quando |d| <= tolerance; com o
    valor padrão (tolerance = 0.0), só há empate quando as duas médias são
    exatamente iguais. Vitória exige d > tolerance e derrota, d < -tolerance.
    Uma tolerância diferente de zero deve ser declarada a priori no relatório.

    Returns:
        DataFrame com uma linha por sistema diferente da referência, na ordem das
        colunas de `table`, e as colunas:
            reference (str), other (str),
            wins (int): datasets com d > tolerance,
            ties (int): datasets com |d| <= tolerance,
            losses (int): datasets com d < -tolerance,
            mean_diff (float): média de d sobre os datasets,
            std_diff (float): desvio padrão amostral de d (ddof = 1).
        wins + ties + losses é igual ao número de datasets (linhas de `table`).
    """
    raise NotImplementedError("TODO(grupo): compare a coluna de referência com cada outra coluna, dataset a dataset")


def mean_rank_per_dataset(table: pd.DataFrame, higher_is_better: bool = True) -> pd.DataFrame:
    """Resumo, por sistema, dos postos obtidos em cada dataset.

    Args:
        table: tabela `dataset x sistema` com UMA medida por dataset (média dos
            folds externos), por exemplo a saída de `per_dataset`.
        higher_is_better: orientação da métrica.

    Em cada dataset (linha), os sistemas recebem postos 1, 2, ..., k (1 = melhor);
    empates recebem o posto médio.

    Returns:
        DataFrame com uma linha por sistema, ordenado por mean_rank crescente, e
        as colunas:
            model (str),
            mean_rank (float): posto médio sobre os datasets,
            std_rank (float): desvio padrão amostral dos postos (ddof = 1),
            n_first (int): número de datasets em que o sistema tem posto 1
                (empates no primeiro lugar contam para todos os empatados).
    """
    raise NotImplementedError("TODO(grupo): ranqueie os sistemas em cada dataset (empates com posto médio) e resuma por sistema")


def ablation_table(
    raw: pd.DataFrame, metric: str = "auc_ovo", higher_is_better: bool = True
) -> pd.DataFrame:
    """Configuração padrão vs. com busca de hiperparâmetros do modelo do grupo, por dataset.

    Args:
        raw: resultados da avaliação final no formato de `results/test.csv`
            (uma linha por dataset, fold externo e sistema).
        metric: métrica comparada.
        higher_is_better: orientação da métrica.

    Usa apenas linhas com status "ok" e apenas datasets em que `group_default` e
    `group_tuned` concluíram todos os folds externos (regra de `per_dataset`).
    A medida de cada sistema em um dataset é a média dos folds externos.

    Returns:
        DataFrame indexado por task_id (ordem crescente), uma linha por dataset,
        com as colunas:
            group_default (float), group_tuned (float): média da métrica nos folds;
            diff (float): diferença orientada, com diff > 0 favorecendo a versão
                com busca (group_tuned - group_default quando maior é melhor e
                group_default - group_tuned quando menor é melhor);
            outcome (str): "win" (diff > 0), "tie" (diff == 0) ou "loss" (diff < 0),
                do ponto de vista de group_tuned;
            tune_time_s (float): tempo médio de busca de group_tuned nos folds.
    """
    raise NotImplementedError("TODO(grupo): monte a tabela por dataset com per_dataset, a diferença orientada e o tempo de busca")


def ablation_summary(ablation: pd.DataFrame) -> dict[str, float | int]:
    """Resumo da ablação sobre os datasets.

    Args:
        ablation: saída de `ablation_table`.

    Returns:
        Dicionário com:
            n_datasets (int): número de datasets comparados;
            mean_default (float), mean_tuned (float): média, sobre os datasets,
                das colunas group_default e group_tuned;
            mean_diff (float): média de diff (> 0 favorece a versão com busca);
            wins (int), ties (int), losses (int): contagens de outcome;
            mean_tune_time_s (float): média de tune_time_s sobre os datasets.
    """
    raise NotImplementedError("TODO(grupo): agregue as colunas da ablação sobre os datasets")
