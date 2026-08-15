"""Modeling helpers for LSTM/GRU stock price prediction experiments."""

from __future__ import annotations

import os
import random

import numpy as np
import tensorflow as tf
from keras.callbacks import EarlyStopping
from keras.layers import GRU, LSTM, Dense, Dropout
from keras.models import Sequential

from .sequence_data import SequenceDataset

DEFAULT_SEED = 50


def set_reproducible_seed(seed: int = DEFAULT_SEED) -> None:
    """Set random seeds used by Python, NumPy, and TensorFlow."""

    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


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
        validation_split=0.2,
        shuffle=False,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)],
        verbose=1,
    )
    return model
