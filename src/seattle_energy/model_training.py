from pathlib import Path

import numpy as np
import pandas as pd
import bentoml
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "feature_engineered_cleaned_for_bento.csv"
TARGET_COLUMN = "SiteEnergyUse(kBtu)"
RANDOM_STATE = 42


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in {path}")
    return df


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col not in ["OSEBuildingID", TARGET_COLUMN]]


def evaluate(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> None:
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f"{name}: R2={r2:.4f}, MAE={mae:.2f}, RMSE={rmse:.2f}")


def build_search_model() -> RandomizedSearchCV:
    param_distributions = {
        "n_estimators": randint(100, 300),
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": randint(2, 10),
        "min_samples_leaf": randint(1, 6),
        "max_features": ["sqrt", "log2", 0.5, 0.75],
    }

    estimator = RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)
    return RandomizedSearchCV(
        estimator,
        param_distributions=param_distributions,
        n_iter=20,
        cv=3,
        scoring="neg_mean_squared_error",
        verbose=2,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def save_bento_model(model, features: list[str]) -> None:
    bentoml.sklearn.save_model(
        "random_forest_energy",
        model,
        custom_objects={"features": list(features)},
    )


def main() -> None:
    print(f"Loading processed dataset from {DATA_PATH}")
    df = load_dataset()
    features = get_feature_columns(df)
    X = df[features]
    y = df[TARGET_COLUMN]

    print("Splitting data into training and test sets")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE
    )

    search = build_search_model()
    print("Starting hyperparameter search for Random Forest")
    search.fit(X_train, y_train)
    best_model = search.best_estimator_

    print("Best hyperparameters:")
    print(search.best_params_)
    print("Evaluating training set")
    evaluate("Training", y_train, best_model.predict(X_train))
    print("Evaluating test set")
    evaluate("Test", y_test, best_model.predict(X_test))

    print("Saving model to BentoML store")
    save_bento_model(best_model, features)
    print("Saved BentoML model as 'random_forest_energy:latest'")


if __name__ == "__main__":
    main()
