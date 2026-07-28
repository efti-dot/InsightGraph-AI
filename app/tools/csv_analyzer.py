import pandas as pd

def analyze_csv(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)

    summary: dict = {
        "file": csv_path,
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": {k: int(v) for k, v in df.isna().sum().to_dict().items() if v > 0},
    }

    numeric_cols = df.select_dtypes(include="number").columns

    stats = {}
    for col in numeric_cols:
        stats[col] = {
            "mean": round(float(df[col].mean()), 2),
            "min": round(float(df[col].min()), 2),
            "max": round(float(df[col].max()), 2),
            "sum": round(float(df[col].sum()), 2),
        }
    summary["numeric_stats"] = stats

    
    if len(df) >= 2 and len(numeric_cols) > 0:
        growth = {}
        for col in numeric_cols:
            first, last = df[col].iloc[0], df[col].iloc[-1]
            if pd.notna(first) and pd.notna(last) and first != 0:
                pct = round(((last - first) / first) * 100, 1)
                growth[col] = f"{pct}%"
        summary["growth_first_to_last"] = growth

    return summary