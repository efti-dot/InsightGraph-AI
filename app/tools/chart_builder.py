import pandas as pd
import plotly.express as px

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

    # Trend line for the first numeric column
    line_fig = px.line(df, x=x, y=first_col, markers=True, title=f"{first_col} over {x_title}")
    charts.append({"title": line_fig.layout.title.text, "figure_json": line_fig.to_json()})

    # Bar comparison
    if len(df) <= 50:
        bar_fig = px.bar(df, x=x, y=first_col, title=f"{first_col} by {x_title}")
        charts.append({"title": bar_fig.layout.title.text, "figure_json": bar_fig.to_json()})

    # Correlation heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        heat_fig = px.imshow(corr, text_auto=True, title="Correlation heatmap")
        charts.append({"title": "Correlation heatmap", "figure_json": heat_fig.to_json()})

    return charts