"""Modeling helpers for LSTM/GRU stock price prediction experiments."""

from __future__ import annotations

import os
import random
from dataclasses import dataclass

import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import GRU, LSTM, Dense, Dropout
from keras.models import Sequential
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf


DEFAULT_SEED = 50


@dataclass(frozen=True)
class SequenceDataset:
    """Train/test arrays prepared for recurrent neural networks."""

    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    feature_scaler: MinMaxScaler
    label_scaler: MinMaxScaler


def set_reproducible_seed(seed: int = DEFAULT_SEED) -> None:
    """Set random seeds used by Python, NumPy, and TensorFlow."""

    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


def choose_pca_components(frame: pd.DataFrame, min_components: int = 3) -> int:
    """Choose PCA dimensions using cumulative variance and eigenvalue criteria."""

    pca = PCA(n_components=max(len(frame.columns) - 1, 1))
    pca.fit(frame)

    cumulative = pca.explained_variance_ratio_.cumsum()
    variance_index = next(
        (index + 1 for index, value in enumerate(cumulative) if value >= 0.7),
        len(cumulative),
    )

    eigenvalues = list(pca.explained_variance_)
    eigen_index = next(
        (index + 1 for index, value in enumerate(eigenvalues) if value >= 1),
        min_components,
    )
    return max(variance_index, eigen_index, min_components)


def scale_and_reduce_features(
    frame: pd.DataFrame,
    target_column: str = "Close",
) -> tuple[pd.DataFrame, MinMaxScaler, MinMaxScaler]:
    """Scale features, reduce non-target columns with PCA, and reattach target."""

    feature_frame = frame.drop(columns=[target_column])
    target_values = frame[target_column].values.reshape(-1, 1)

    feature_scaler = MinMaxScaler()
    scaled_features = pd.DataFrame(
        feature_scaler.fit_transform(feature_frame),
        columns=feature_frame.columns,
        index=feature_frame.index,
    )

    components = choose_pca_components(scaled_features)
    principal = pd.DataFrame(
        PCA(n_components=components).fit_transform(scaled_features),
        index=frame.index,
    )

    label_scaler = MinMaxScaler()
    principal[target_column] = label_scaler.fit_transform(target_values)
    return principal, feature_scaler, label_scaler


def make_sequence_dataset(
    frame: pd.DataFrame,
    window_size: int = 20,
    predict_day: int = 1,
    target_column: str = "Close",
    test_size: float = 0.2,
    random_state: int = DEFAULT_SEED,
) -> SequenceDataset:
    """Create train/test sequence arrays for next-day price prediction."""

    reduced, feature_scaler, label_scaler = scale_and_reduce_features(frame, target_column)
    features = reduced.drop(columns=[target_column])
    labels = reduced[target_column]

    feature_list: list[pd.DataFrame] = []
    label_list: list[pd.Series] = []
    for start in range(len(features) - window_size - predict_day + 1):
        end = start + window_size
        feature_list.append(features.iloc[start:end])
        label_list.append(labels.iloc[end : end + predict_day])

    x = np.array(feature_list)
    y = np.array(label_list)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        shuffle=False,
    )
    return SequenceDataset(x_train, x_test, y_train, y_test, feature_scaler, label_scaler)


def build_recurrent_model(
    input_shape: tuple[int, int],
    model_type: str = "gru",
    units: int = 16,
    dropout: float = 0.2,
    output_size: int = 1,
) -> Sequential:
    """Build a compact LSTM or GRU regression model."""

    model = Sequential()
    recurrent_layer = GRU if model_type.lower() == "gru" else LSTM
    model.add(recurrent_layer(units=units, input_shape=input_shape))
    if dropout > 0:
        model.add(Dropout(dropout))
    model.add(Dense(output_size))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


def train_model(
    dataset: SequenceDataset,
    model_type: str = "gru",
    units: int = 16,
    dropout: float = 0.2,
    epochs: int = 100,
    batch_size: int = 16,
) -> Sequential:
    """Train a recurrent model with early stopping."""

    set_reproducible_seed()
    model = build_recurrent_model(
        input_shape=(dataset.x_train.shape[1], dataset.x_train.shape[2]),
        model_type=model_type,
        units=units,
        dropout=dropout,
        output_size=dataset.y_train.shape[1],
    )
    model.fit(
        dataset.x_train,
        dataset.y_train,
        validation_data=(dataset.x_test, dataset.y_test),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)],
        verbose=1,
    )
    return model
