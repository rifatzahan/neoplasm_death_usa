# xgboost_shap_pipeline.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Load your dataset
df = pd.read_csv(r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research\Cancer Data\US_Mortality_2019_2023_neoplasm_with_subtypes_recoded.csv", low_memory=False)

# Set Age Group as an ordered categorical variable
age_order = [
    "<= 14 years", "15 - 24 years", "25 - 34 years", "35 - 44 years",
    "45 - 54 years", "55 - 64 years", "65 - 74 years", "75 - 84 years",
    "85 years and older", "Age not stated"
]
df['Age Group'] = pd.Categorical(df['Age Group'], categories=age_order, ordered=True)

# Generate faceted stacked bar plots by Sex for each covariate vs. Cause of Death (normalized)
def generate_facet_bar(df, facet_row, title_prefix):
    figures = []
    for sex in df['Sex'].unique():
        subset = df[df['Sex'] == sex]
        count_df = subset.groupby([facet_row, 'malignant_type']).size().reset_index(name='count')
        total_per_group = count_df.groupby(facet_row)['count'].transform('sum')
        count_df['percent'] = count_df['count'] / total_per_group * 100

        fig = px.bar(
            count_df, x=facet_row, y='percent', color='malignant_type',
            barmode='stack', text=count_df['percent'].round(1).astype(str) + '%',
            title=f"{title_prefix} ({sex}) - Normalized",
            opacity=0.85,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_layout(
            yaxis_title='Percentage',
            xaxis_title=facet_row,
            legend_title='Cause of Death',
            width=700,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40),
            yaxis=dict(ticksuffix='%'),
            font=dict(size=12),
        )
        figures.append(fig)
    return figures

# Generate faceted unnormalized stacked bar plots by Sex for each covariate vs. Cause of Death
def generate_facet_bar_unnormalized(df, facet_row, title_prefix):
    figures = []
    for sex in df['Sex'].unique():
        subset = df[df['Sex'] == sex]
        count_df = subset.groupby([facet_row, 'malignant_type']).size().reset_index(name='count')

        fig = px.bar(
            count_df, x=facet_row, y='count', color='malignant_type',
            barmode='stack', text=count_df['count'],
            title=f"{title_prefix} ({sex}) - Raw Counts",
            opacity=0.85,
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            yaxis_title='Number of Deaths',
            xaxis_title=facet_row,
            legend_title='Cause of Death',
            width=700,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=12),
        )
        figures.append(fig)
    return figures

# Generate heatmap by covariate and sex
def generate_facet_heatmap(df, facet_row, title_prefix):
    figures = []
    for sex in df['Sex'].unique():
        subset = df[df['Sex'] == sex]
        heatmap_data = subset.groupby([facet_row, 'malignant_type']).size().unstack(fill_value=0)
        heatmap_percent = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_percent.values,
            x=heatmap_percent.columns.astype(str),
            y=heatmap_percent.index.astype(str),
            colorscale='YlGnBu',
            text=heatmap_percent.round(1).astype(str) + '%',
            hoverinfo='text',
            showscale=True
        ))

        fig.update_layout(
            title=f"{title_prefix} ({sex}) - Heatmap (%)",
            xaxis_title='Cause of Death',
            yaxis_title=facet_row,
            autosize=False,
            width=800,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=12),
        )
        figures.append(fig)
    return figures

# Generate time series plot with consistent colors and different line styles by sex
def generate_monthly_trend_by_sex(df, year_col='Data Year', month_col='Month_Of_Death', cause_col='malignant_type'):
    month_map = {
        'January': '01', 'February': '02', 'March': '03',
        'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09',
        'October': '10', 'November': '11', 'December': '12'
    }
    df[month_col] = df[month_col].astype(str).str.strip().map(month_map)
    df[year_col] = df[year_col].astype(str).str.strip()
    df['Year_Month'] = pd.to_datetime(df[year_col] + '-' + df[month_col], format='%Y-%m', errors='coerce')
    df = df[df['Year_Month'].notna()]

    trend_data = df.groupby(['Year_Month', cause_col, 'Sex']).size().reset_index(name='Deaths')

    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    cause_list = trend_data[cause_col].unique()
    cause_color_map = {cause: colors[i % len(colors)] for i, cause in enumerate(cause_list)}

    for cause in cause_list:
        for sex in ['Male', 'Female']:
            subset = trend_data[(trend_data[cause_col] == cause) & (trend_data['Sex'] == sex)]
            fig.add_trace(go.Scatter(
                x=subset['Year_Month'],
                y=subset['Deaths'],
                mode='lines+markers',
                name=f"{cause} ({sex})",
                line=dict(color=cause_color_map[cause], dash='solid' if sex == 'Male' else 'dash')
            ))

    fig.update_layout(
        title="Monthly Trend of Deaths by Cause of Death and Sex",
        xaxis_title='Year-Month',
        yaxis_title='Number of Deaths',
        width=1000,
        height=600,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(size=12),
        legend_title='Cause of Death (Sex)'
    )

    return [fig]

# Generate all plots by covariate and sex
covariates = ['Age Group', 'Education', 'Occupation', 'Marital Status', 'Race', 'Resident_Status']
all_figures = []

for cov in covariates:
    all_figures.extend(generate_facet_bar(df, cov, f"Deaths by {cov} and Cause"))
    all_figures.extend(generate_facet_bar_unnormalized(df, cov, f"Deaths by {cov} and Cause"))
    all_figures.extend(generate_facet_heatmap(df, cov, f"Deaths by {cov} and Cause"))

# Add monthly trend stratified by sex
all_figures.extend(generate_monthly_trend_by_sex(df))

# Save all plots to a single HTML
html_output_path = r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research\Cancer Data\visualization_deathsNeoplasm.html"

with open(html_output_path, 'w') as f:
    for fig in all_figures:
        f.write(pio.to_html(fig, include_plotlyjs='cdn', full_html=False))

print(f"✅ All visualizations saved to: {html_output_path}")

print(df.isnull().sum().sort_values(ascending=False))

