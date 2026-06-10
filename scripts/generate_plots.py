import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

theme_columns = [
    'Love/Romance',
    'Heartbreak/Loss',
    'Party/Celebration',
    'Empowerment/Confidence',
    'Ambition/Success',
    'Mental Health/Inner Struggle',
    'Nostalgia/Reflection',
    'Social Commentary',
    'Sexual Desire',
    'Resilience/Survival'
]

theme_colors = {
    'Love/Romance': '#d45087',
    'Heartbreak/Loss': '#665191',
    'Party/Celebration': '#ffa600',
    'Empowerment/Confidence': '#2f9c95',
    'Ambition/Success': '#f95d6a',
    'Mental Health/Inner Struggle': '#003f5c',
    'Nostalgia/Reflection': '#8c6d31',
    'Social Commentary': '#7a5195',
    'Sexual Desire': '#ff7c43',
    'Resilience/Survival': '#3f88c5'
}

def plot_theme_score_change_2020s_vs_1960s(df):
    decade_scores = df.groupby('decade')[theme_columns].mean()
    change = decade_scores.loc[2020] - decade_scores.loc[1960]
    plot_df = change.rename('score_change').reset_index().rename(columns={'index': 'theme'}).sort_values('score_change', ascending=False)
    colors = ['#665191' if value < 0 else '#2f9c95' for value in plot_df['score_change']]
    fig, ax = plt.subplots(figsize=(15, 10))
    bars = ax.barh(plot_df['theme'], plot_df['score_change'], color=colors, height=0.8)

    for bar, value in zip(bars, plot_df['score_change']):
        label_x = value + 0.005 if value >= 0 else value - 0.005
        ha = 'left' if value >= 0 else 'right'
        ax.text(label_x, bar.get_y() + bar.get_height()/2, f'{value:+.2f}', va='center', ha=ha, fontsize=14)

    ax.axvline(0, color='0.2', linewidth=1.2)
    ax.invert_yaxis()
    ax.set_xlim(-0.31, 0.23)
    ax.set_title('Theme Score Change: 2020s vs 1960s', fontsize=24, fontweight='bold', pad=20)
    ax.set_xlabel('Change in average theme score', fontsize=14)
    ax.set_ylabel('')
    ax.grid(axis='x', color='0.88', linewidth=1)
    ax.grid(axis='y', visible=False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    fig.savefig('figs/theme_score_change_2020s_vs_1960s.png', dpi=300)
    plt.close(fig)

def plot_theme_score_trends_by_year(df):
    plot_df = df.copy()
    plot_df['year'] = pd.to_datetime(plot_df['date']).dt.year
    yearly_scores = plot_df.groupby('year')[theme_columns].mean().reset_index().melt(id_vars='year', value_vars=theme_columns, var_name='theme', value_name='score')
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(16,18), sharex=True, sharey=True)
    axes = axes.flatten()

    for ax, theme in zip(axes, theme_columns):
        theme_scores = yearly_scores[yearly_scores['theme'] == theme].sort_values('year')
        years = theme_scores['year'].to_numpy()
        scores = theme_scores['score'].to_numpy()
        color = theme_colors[theme]
        ax.plot(years, scores, color=color, linewidth=2.4)
        ax.fill_between(years, scores, 0, color=color, alpha=0.17)
        ax.set_title(theme, loc='left', fontsize=13, fontweight='bold', pad=7)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_ylim(0, 0.7)
        ax.grid(axis='y', color='0.88', linewidth=0.8)
        ax.grid(axis='x', visible=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    fig.suptitle('Theme Score Trends Over Time', fontsize=32, fontweight='bold', y=0.95)
    fig.supxlabel('Year', fontsize=20, y=0.05)
    fig.supylabel('Average Theme Score', fontsize=20)
    fig.tight_layout(rect=[0.06, 0.055, 0.995, 0.935], h_pad=1.2, w_pad=1.0)
    fig.savefig('figs/theme_score_trends_by_year.png', dpi=300)
    plt.close(fig)

def plot_theme_pca_trajectories(df):
    centroids = df.dropna(subset=['primary_theme', 'decade', 'pca_1', 'pca_2']).groupby(['primary_theme', 'decade'], as_index=False).agg(
        pca1_centroid=('pca_1', 'mean'), pca2_centroid=('pca_2', 'mean'), n_songs=('trackTitle', 'size')).sort_values(['primary_theme', 'decade'])
    fig, ax = plt.subplots(figsize=(16, 11))
    sns.lineplot(data=centroids, x='pca1_centroid', y='pca2_centroid', hue='primary_theme', hue_order=theme_columns, 
        palette=theme_colors, marker='o', markersize=8, linewidth=2.5, ax=ax)
    
    for _, row in centroids.iterrows():
        ax.annotate(str(int(row['decade'])), (row['pca1_centroid'], row['pca2_centroid']), 
            xytext=(5, 4), textcoords='offset points', fontsize=8, alpha=0.9)
    
    ax.axhline(0, color='0.7', linewidth=1, zorder=0)
    ax.axvline(0, color='0.7', linewidth=1, zorder=0)
    ax.set_title('Theme Trajectories Across PCA Space', fontsize=24, pad=20)
    ax.set_xlabel('PCA 1 Centroid', fontsize=16)
    ax.set_ylabel('PCA 2 Centroid', fontsize=16)
    ax.legend(title='Theme', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False)
    fig.tight_layout()
    fig.savefig('figs/theme_score_trajectories_by_decade.png', dpi=300)
    plt.close(fig)

def main():
    df = pd.read_parquet('data/processed/songs_with_themes_embeddings.parquet')

    sns.set_theme(style='whitegrid', context='talk')
    plot_theme_score_change_2020s_vs_1960s(df)
    plot_theme_score_trends_by_year(df)
    plot_theme_pca_trajectories(df)

if __name__ == '__main__':
    main()