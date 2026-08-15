from __future__ import annotations

import numpy as np
import pandas as pd

from src.sequence_data import make_sequence_dataset


def _future_peak_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Open": np.arange(12, dtype=float),
            "Volume": np.arange(100, 112, dtype=float),
            "Close": np.arange(10, 22, dtype=float),
        }
    )


def test_sequence_dataset_fits_scalers_on_training_period_when_future_values_peak() -> None:
    given_frame = _future_peak_frame()

    when_dataset = make_sequence_dataset(
        given_frame,
        window_size=2,
        predict_day=1,
        test_size=0.25,
    )

    assert when_dataset.feature_scaler.data_max_.tolist() == [8.0, 108.0]
    assert when_dataset.label_scaler.data_max_[0] == 18.0


def test_sequence_dataset_keeps_targets_in_time_order_when_test_period_is_held_out() -> None:
    given_frame = _future_peak_frame()

    when_dataset = make_sequence_dataset(
        given_frame,
        window_size=2,
        predict_day=1,
        test_size=0.25,
    )

    assert when_dataset.y_train.max() < when_dataset.y_test.min()
