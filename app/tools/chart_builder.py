import pandas as pd

def build_charts_for_csv(csv_path: str) -> list[dict]:
    df = pd.read_csv(csv_path)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return []

    #non numeric becomes x-axis
    label_col = next((c for c in df.columns if c not in numeric_cols), None)
    x = df[label_col] if label_col else df.index
    x_title = label_col or "index"

    charts: list[dict] = []
    first_col = numeric_cols[0]

    