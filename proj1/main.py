import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def load_data() -> pd.DataFrame:
    """
    Load online Titanic dataset.
    This dataset has numeric, categorical, and missing values.
    """
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
    df = pd.read_csv(url)
    return df


def explore_dataframe(df: pd.DataFrame, target_col: str | None = None) -> None:
    """
    Basic DataFrame exploration before machine learning.
    """

    print("\n==============================")
    print("1. SHAPE")
    print("==============================")
    print(df.shape)

    print("\n==============================")
    print("2. FIRST 5 ROWS")
    print("==============================")
    print(df.head())

    print("\n==============================")
    print("3. DATA TYPES AND NON-NULL COUNTS")
    print("==============================")
    print(df.info())

    print("\n==============================")
    print("4. MISSING VALUES COUNT")
    print("==============================")
    print(df.isna().sum().sort_values(ascending=False))

    print("\n==============================")
    print("5. MISSING VALUES PERCENTAGE")
    print("==============================")
    missing_pct = df.isna().mean().sort_values(ascending=False) * 100
    print(missing_pct)

    print("\n==============================")
    print("6. NUMERIC STATISTICS")
    print("==============================")
    print(df.describe())

    print("\n==============================")
    print("7. CATEGORICAL STATISTICS")
    print("==============================")
    print(df.describe(include="object"))

    print("\n==============================")
    print("8. UNIQUE VALUES PER COLUMN")
    print("==============================")
    print(df.nunique().sort_values())

    print("\n==============================")
    print("9. DUPLICATE ROWS")
    print("==============================")
    print(df.duplicated().sum())

    if target_col and target_col in df.columns:
        print("\n==============================")
        print("10. TARGET DISTRIBUTION")
        print("==============================")
        print(df[target_col].value_counts(dropna=False))
        print("\nTarget percentage:")
        print(df[target_col].value_counts(normalize=True, dropna=False) * 100)

    print("\n==============================")
    print("11. CORRELATION")
    print("==============================")
    print(df.corr(numeric_only=True))


def prepare_ml_data(df: pd.DataFrame, target_col: str):
    """
    Create train/test split and preprocessing pipeline.
    """

    # Drop columns that are not useful or have too many missing values for this demo
    drop_cols = ["deck", "embark_town", "alive", "class", "who", "adult_male"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # Remove rows where target is missing
    df = df.dropna(subset=[target_col])

    X = df.drop(columns=[target_col])
    y = df[target_col]

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    print("\n==============================")
    print("FEATURE GROUPS")
    print("==============================")
    print("Numeric columns:", numeric_cols)
    print("Categorical columns:", categorical_cols)

    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ],
        remainder="drop",
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Fit only on training data
    X_train_processed = preprocess.fit_transform(X_train)

    # Transform test data using same fitted preprocessor
    X_test_processed = preprocess.transform(X_test)

    print("\n==============================")
    print("PROCESSED DATA SHAPES")
    print("==============================")
    print("X_train raw:", X_train.shape)
    print("X_test raw:", X_test.shape)
    print("X_train processed:", X_train_processed.shape)
    print("X_test processed:", X_test_processed.shape)

    return X_train_processed, X_test_processed, y_train, y_test, preprocess


def main():
    target_col = "survived"

    df = load_data()

    explore_dataframe(df, target_col=target_col)

    X_train_processed, X_test_processed, y_train, y_test, preprocess = prepare_ml_data(
        df,
        target_col=target_col,
    )

    print("\nReady for ML model training.")


if __name__ == "__main__":
    main()