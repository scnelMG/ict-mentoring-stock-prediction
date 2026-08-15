from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


@dataclass(frozen=True, slots=True)
class SequenceDataset:
    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    feature_scaler: MinMaxScaler
    label_scaler: MinMaxScaler


def make_sequence_dataset(
    frame: pd.DataFrame,
    window_size: int = 20,
    predict_day: int = 1,
    target_column: str = "Close",
    test_size: float = 0.2,
) -> SequenceDataset:
    _validate_dataset_arguments(frame, window_size, predict_day, target_column, test_size)
    split_index = int(len(frame) * (1 - test_size))
    train_frame = frame.iloc[:split_index]
    feature_frame = frame.drop(columns=[target_column])

    feature_scaler = MinMaxScaler()
    feature_scaler.fit(train_frame.drop(columns=[target_column]))
    scaled_features = feature_scaler.transform(feature_frame)

    component_count = _pca_component_count(
        scaled_features[:split_index],
        minimum=3,
    )
    reducer = PCA(n_components=component_count)
    reducer.fit(scaled_features[:split_index])
    reduced_features = reducer.transform(scaled_features)

    label_scaler = MinMaxScaler()
    label_scaler.fit(train_frame[[target_column]])
    scaled_labels = label_scaler.transform(frame[[target_column]]).ravel()

    return _split_sequence_windows(
        reduced_features,
        scaled_labels,
        split_index,
        window_size,
        predict_day,
        feature_scaler,
        label_scaler,
    )


def _validate_dataset_arguments(
    frame: pd.DataFrame,
    window_size: int,
    predict_day: int,
    target_column: str,
    test_size: float,
) -> None:
    if target_column not in frame.columns:
        raise KeyError(f"Missing target column: {target_column}")
    if window_size < 1 or predict_day < 1:
        raise ValueError("window_size and predict_day must be positive")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between zero and one")

    split_index = int(len(frame) * (1 - test_size))
    if split_index <= window_size or len(frame) - split_index < predict_day:
        raise ValueError("frame is too short for the requested chronological split")


def _pca_component_count(training_features: np.ndarray, minimum: int) -> int:
    component_limit = min(training_features.shape)
    if component_limit < 1:
        raise ValueError("at least one training feature is required")

    fitted = PCA(n_components=component_limit).fit(training_features)
    cumulative_variance = fitted.explained_variance_ratio_.cumsum()
    variance_count = next(
        (index + 1 for index, value in enumerate(cumulative_variance) if value >= 0.7),
        component_limit,
    )
    eigenvalue_count = next(
        (index + 1 for index, value in enumerate(fitted.explained_variance_) if value >= 1),
        1,
    )
    return min(max(variance_count, eigenvalue_count, minimum), component_limit)


def _split_sequence_windows(
    features: np.ndarray,
    labels: np.ndarray,
    split_index: int,
    window_size: int,
    predict_day: int,
    feature_scaler: MinMaxScaler,
    label_scaler: MinMaxScaler,
) -> SequenceDataset:
    train_features: list[np.ndarray] = []
    train_labels: list[np.ndarray] = []
    test_features: list[np.ndarray] = []
    test_labels: list[np.ndarray] = []

    for end_index in range(window_size, len(features) - predict_day + 1):
        window_features = features[end_index - window_size : end_index]
        window_labels = labels[end_index : end_index + predict_day]
        if end_index + predict_day <= split_index:
            train_features.append(window_features)
            train_labels.append(window_labels)
        else:
            test_features.append(window_features)
            test_labels.append(window_labels)

    if not train_features or not test_features:
        raise ValueError("the requested split does not produce both train and test windows")

    return SequenceDataset(
        x_train=np.asarray(train_features),
        x_test=np.asarray(test_features),
        y_train=np.asarray(train_labels),
        y_test=np.asarray(test_labels),
        feature_scaler=feature_scaler,
        label_scaler=label_scaler,
    )
