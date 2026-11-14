"""Aceitação de src/pipeline/descriptive.py: comparação descritiva por dataset."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.pipeline.descriptive import (
    ablation_summary,
    ablation_table,
    mean_rank_per_dataset,
    wins_ties_losses,
)
from tests.dados_sinteticos import raw_results


def _with_default(raw: pd.DataFrame, delta: float = 0.02) -> pd.DataFrame:
    """Acrescenta group_default (pior que group_tuned em `delta`) e tempo de busca de 30 s."""
    tuned = raw[raw["model"] == "group_tuned"]
    default = tuned.assign(
        model="group_default",
        auc_ovo=tuned["auc_ovo"] - delta,
        cross_entropy=tuned["cross_entropy"] + delta,
    )
    out = pd.concat([raw, default], ignore_index=True)
    out.loc[out["model"] == "group_tuned", "tune_time_s"] = 30.0
    return out


def test_wins_ties_losses_by_hand():
    table = pd.DataFrame(
        {"g": [0.80, 0.70, 0.90], "a": [0.75, 0.70, 0.95], "b": [0.70, 0.60, 0.80]},
        index=pd.Index([1, 2, 3], name="task_id"),
    )
    out = wins_ties_losses(table, "g").set_index("other")
    assert list(out.index) == ["a", "b"]
    assert (out.loc["a", "wins"], out.loc["a", "ties"], out.loc["a", "losses"]) == (1, 1, 1)
    assert (out.loc["b", "wins"], out.loc["b", "ties"], out.loc["b", "losses"]) == (3, 0, 0)
    assert out.loc["a", "mean_diff"] == pytest.approx(0.0)
    assert out.loc["a", "std_diff"] == pytest.approx(np.std([0.05, 0.0, -0.05], ddof=1))
    assert set(out["reference"]) == {"g"}
    lower = wins_ties_losses(table, "g", higher_is_better=False).set_index("other")
    assert (lower.loc["b", "wins"], lower.loc["b", "losses"]) == (0, 3)
    assert lower.loc["b", "mean_diff"] == pytest.approx(-0.1)
    tol = wins_ties_losses(table, "g", tolerance=0.06).set_index("other")
    assert tol.loc["a", "ties"] == 3


def test_wins_ties_losses_uses_one_measure_per_dataset():
    raw = raw_results(n_datasets=6)
    table = raw.pivot_table(index="task_id", columns="model", values="auc_ovo")
    out = wins_ties_losses(table, "group_tuned")
    assert len(out) == 3
    assert (out[["wins", "ties", "losses"]].sum(axis=1) == 6).all()  # datasets, não folds


def test_mean_rank_per_dataset_by_hand():
    table = pd.DataFrame({"g": [0.9, 0.8, 0.7], "a": [0.8, 0.8, 0.9], "b": [0.7, 0.6, 0.8]})
    out = mean_rank_per_dataset(table)
    assert list(out.columns[:3]) == ["model", "mean_rank", "std_rank"]
    out = out.set_index("model")
    assert out.loc["g", "mean_rank"] == pytest.approx((1 + 1.5 + 3) / 3)
    assert out.loc["a", "mean_rank"] == pytest.approx((2 + 1.5 + 1) / 3)
    assert out.loc["b", "mean_rank"] == pytest.approx((3 + 3 + 2) / 3)
    assert out.loc["g", "std_rank"] == pytest.approx(np.std([1, 1.5, 3], ddof=1))
    assert out.index[-1] == "b"
    assert (out.loc["g", "n_first"], out.loc["a", "n_first"], out.loc["b", "n_first"]) == (2, 2, 0)
    lower = mean_rank_per_dataset(table, higher_is_better=False).set_index("model")
    assert lower.loc["b", "mean_rank"] == pytest.approx((1 + 1 + 2) / 3)
    assert lower.index[0] == "b"


def test_ablation_table_per_dataset():
    raw = _with_default(raw_results(n_datasets=5))
    out = ablation_table(raw)
    assert len(out) == 5 and out.index.name == "task_id"
    assert {"group_default", "group_tuned", "diff", "outcome", "tune_time_s"} <= set(out.columns)
    expected = raw[raw["model"] == "group_tuned"].groupby("task_id")["auc_ovo"].mean()
    np.testing.assert_allclose(out["group_tuned"].to_numpy(), expected.to_numpy())
    np.testing.assert_allclose(out["diff"].to_numpy(), 0.02)
    assert (out["outcome"] == "win").all()
    assert out["tune_time_s"].to_numpy() == pytest.approx(30.0)
    lower = ablation_table(raw, metric="cross_entropy", higher_is_better=False)
    assert (lower["diff"] > 0).all()  # versão com busca tem entropia cruzada menor


def test_ablation_table_drops_incomplete_datasets():
    raw = _with_default(raw_results(n_datasets=4))
    failed = (raw["task_id"] == 1001) & (raw["model"] == "group_default") & (raw["fold"] == 2)
    raw.loc[failed, "status"] = "error"
    out = ablation_table(raw)
    assert 1001 not in out.index and len(out) == 3


def test_ablation_summary():
    raw = _with_default(raw_results(n_datasets=5))
    summary = ablation_summary(ablation_table(raw))
    assert summary["n_datasets"] == 5
    assert summary["wins"] + summary["ties"] + summary["losses"] == 5
    assert summary["mean_tuned"] - summary["mean_default"] == pytest.approx(0.02)
    assert summary["mean_diff"] == pytest.approx(0.02)
    assert summary["mean_tune_time_s"] == pytest.approx(30.0)
