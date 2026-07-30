import pandas as pd
from langchain_core.tools import tool


def _load(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)


@tool
def list_columns(csv_path: str) -> str:
    df = _load(csv_path)
    lines = [f"{col}: {dtype}" for col, dtype in df.dtypes.items()]
    return f"Columns in {csv_path} ({len(df)} rows):\n" + "\n".join(lines)


@tool
def top_n(csv_path: str, sort_column: str, n: int = 5, ascending: bool = False) -> str:
    df = _load(csv_path)
    if sort_column not in df.columns:
        return f"Column '{sort_column}' not found. Available columns: {list(df.columns)}"
    result = df.sort_values(sort_column, ascending=ascending).head(n)
    return result.to_string(index=False)


@tool
def group_and_aggregate(csv_path: str, group_by_column: str, agg_column: str, agg_func: str = "sum") -> str:
    df = _load(csv_path)
    for col in (group_by_column, agg_column):
        if col not in df.columns:
            return f"Column '{col}' not found. Available columns: {list(df.columns)}"
    if agg_func not in {"sum", "mean", "max", "min", "count"}:
        return f"agg_func must be one of sum, mean, max, min, count (got '{agg_func}')"
    result = df.groupby(group_by_column)[agg_column].agg(agg_func).sort_values(ascending=False)
    return result.to_string()


CSV_TOOLS = [list_columns, top_n, group_and_aggregate]