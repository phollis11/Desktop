import pandas as pd
import os
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers

# -------------------------------
# Paths
# -------------------------------
raw_file = r"C:\Users\pholl\Downloads\all_teams.csv"
filtered_file = r"C:\Users\pholl\Downloads\all_teams_filtered.pkl"
preprocessor_path = r"C:\Users\pholl\Downloads\hockey_preprocessor.pkl"
saved_model_path = r"C:\Users\pholl\Downloads\hockey_win_model.keras"

# -------------------------------
# Load or preprocess data
# -------------------------------
if os.path.exists(filtered_file):
    df_filtered = pd.read_pickle(filtered_file)
    print("Loaded filtered DataFrame from file.")
else:
    df = pd.read_csv(raw_file)
    df = df[df["situation"] == "all"]

    # Convert numeric columns
    numeric_cols = [
        "shotsOnGoalFor", "shotsOnGoalAgainst",
        "lowDangerShotsFor", "mediumDangerShotsFor", "highDangerShotsFor",
        "lowDangerShotsAgainst", "mediumDangerShotsAgainst", "highDangerShotsAgainst",
        "goalsFor", "goalsAgainst"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Create binary win label
    df["win"] = (df["goalsFor"] > df["goalsAgainst"]).astype(int)

    # Select final columns
    columns = [
        "home_or_away",
        "shotsOnGoalFor", "shotsOnGoalAgainst",
        "lowDangerShotsFor", "mediumDangerShotsFor", "highDangerShotsFor",
        "lowDangerShotsAgainst", "mediumDangerShotsAgainst", "highDangerShotsAgainst",
        "win"
    ]
    df_filtered = df[columns]

    df_filtered.to_pickle(filtered_file)
    print("Filtered DataFrame created and saved.")

# -------------------------------
# Feature selection
# -------------------------------
feature_cols = [
    "home_or_away",
    "shotsOnGoalFor", "shotsOnGoalAgainst",
    "lowDangerShotsFor", "mediumDangerShotsFor", "highDangerShotsFor",
    "lowDangerShotsAgainst", "mediumDangerShotsAgainst", "highDangerShotsAgainst"
]

X = df_filtered[feature_cols]
y = df_filtered["win"]

categorical_cols = ["home_or_away"]
numeric_cols = [c for c in feature_cols if c not in categorical_cols]

# -------------------------------
# Train/test split BEFORE fitting preprocessor (prevents leakage)
# -------------------------------
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Load or create preprocessor
# -------------------------------
if os.path.exists(preprocessor_path):
    with open(preprocessor_path, "rb") as f:
        preprocessor = pickle.load(f)
    print("Loaded saved preprocessor.")

    X_train = preprocessor.transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

else:
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ])

    preprocessor.fit(X_train_raw)

    X_train = preprocessor.transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

    with open(preprocessor_path, "wb") as f:
        pickle.dump(preprocessor, f)

    print("Preprocessor fit and saved.")

# -------------------------------
# Early stopping
# -------------------------------
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=5, restore_best_weights=True
)

# -------------------------------
# Load or train model
# -------------------------------
if os.path.exists(saved_model_path):
    model = tf.keras.models.load_model(saved_model_path)
    print("Loaded saved model.")
else:
    model = models.Sequential([
        layers.Input(shape=(X_train.shape[1],)),
        layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.1),
        layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.1),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=50,
        batch_size=32,
        callbacks=[early_stop],
        verbose=1
    )

    model.save(saved_model_path)
    print("Model trained and saved.")

# -------------------------------
# Evaluate model
# -------------------------------
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.3f}")

# -------------------------------
# Prediction Function
# -------------------------------
def predict_game_winner(game_dict):
    """Predict probability of home team winning."""
    game_df = pd.DataFrame([game_dict])
    with open(preprocessor_path, "rb") as f:
        preproc = pickle.load(f)
    processed = preproc.transform(game_df)

    prob = model.predict(processed)[0][0]
    pred_class = int(prob > 0.5)
    return pred_class, prob

# -------------------------------
# Example Prediction
# ------------------------
