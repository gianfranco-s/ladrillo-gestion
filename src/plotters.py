from pandas import DataFrame
import plotly.express as px

def plot_materials_spending(spending_data: DataFrame) -> px.line:

    fig = px.line(
        spending_data,
        x="week",
        y="Spending",
        color="Spending Type",
        markers=True,
        labels={
            "week": "Week Start",
            "Spending": "Materials Spending (USD)",
            "Spending Type": ""
        },
    )
    fig.update_xaxes(dtick="W1", tickformat="%Y-%m-%d")
    fig.update_layout(legend_title_text="")
    return fig
