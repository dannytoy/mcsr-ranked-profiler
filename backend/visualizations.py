import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

if not os.path.exists('visuals'):
    os.makedirs('visuals')

from model_pipeline import load_data, clean_data, train_clustering_model, train_regression_model

def plot_elbow_method(df_scaled):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
        kmeans.fit(df_scaled)
        wcss.append(kmeans.inertia_)
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 11), wcss, marker='o', color='#2ecc71')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('WCSS')
    plt.savefig('visuals/elbow_method.png')
    plt.close()

def plot_correlation_heatmap(df):
    plt.figure(figsize=(12, 8))
    features = ['elo', 'avg_min', 'best_min', 'win_rate', 'consistency_ratio', 'total_games']
    sns.heatmap(df[features].corr(), annot=True, cmap='RdYlGn', fmt=".2f")
    plt.title('Correlation Heatmap: Performance Metrics')
    plt.xlabel('Feature')
    plt.ylabel('Feature')
    plt.savefig('visuals/correlation_heatmap.png')
    plt.close()

def plot_elo_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['elo'], bins=50, kde=True, color='skyblue')
    plt.title('Elo Distribution of Players')
    plt.xlabel('Elo')
    plt.ylabel('Number of Players')
    plt.savefig('visuals/elo_distribution.png')
    plt.close()

def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix: Predicted vs Actual Rank')
    plt.xlabel('Predicted Rank Tier')
    plt.ylabel('Actual Rank Tier')
    plt.savefig('visuals/confusion_matrix.png')
    plt.close()

def plot_archetype_scatter(df):
    plt.figure(figsize=(12, 8))

    archetype_map = {
        0: "The Consistent Player",
        1: "The Climber",
        2: "The Tilt Queuer"
    }
    df['Archetype'] = df['archetype_id'].map(archetype_map)

    palette = {
        "The Consistent Player": "#2ecc71", # Green
        "The Climber": "#3498db",           # Blue
        "The Tilt Queuer": "#e74c3c"        # Red
    }

    sns.scatterplot(
        data=df,
        x='win_rate',
        y='consistency_ratio',
        hue='Archetype',
        palette=palette,
        size='total_games',
        sizes=(20, 800), # Min and max bubble sizes
        alpha=0.7,
        edgecolor='black'
    )

    plt.title('Player Archetypes: Win Rate vs. Consistency (Bubble Size = Total Games)', fontsize=14, pad=15)
    plt.xlabel('Win Rate', fontsize=12)
    plt.ylabel('Consistency Ratio (Avg / Best)', fontsize=12)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, title="Archetypes & Games")

    plt.tight_layout()
    plt.savefig('visuals/archetype_scatter_2d.png', dpi=300)
    plt.close()

def plot_feature_importance(pipeline, feature_names):
    importances = pipeline.named_steps['regressor'].feature_importances_
    feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', hue='feature', data=feature_importance_df, palette='magma', legend=False)
    plt.title('Feature Importance for Rank Tier Prediction')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.savefig('visuals/feature_importance.png')
    plt.close()


if __name__ == '__main__':
    raw_data = load_data('playerdata.csv')
    df_cleaned = clean_data(raw_data)

    features_cluster = ['total_games', 'consistency_ratio', 'win_rate']
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_cleaned[features_cluster])

    plot_elbow_method(df_scaled)
    plot_correlation_heatmap(df_cleaned)
    plot_elo_distribution(df_cleaned)

    df_final, kmeans_model, cluster_scaler = train_clustering_model(df_cleaned)

    regression_features = ['avg_min', 'best_min', 'win_rate', 'consistency_ratio', 'total_games']
    X = df_final[regression_features]
    y_elo = df_final['elo']

    X_train, X_test, y_train, y_test_elo = train_test_split(X, y_elo, test_size=0.2, random_state=42)

    regression_pipeline = train_regression_model(X_train, y_train)
    y_pred_elo = regression_pipeline.predict(X_test)

    labels = ['Coal', 'Iron', 'Gold', 'Emerald', 'Diamond', 'Netherite']
    bins = [-1, 599, 899, 1199, 1499, 1999, 10000]

    y_pred_tier = pd.cut(y_pred_elo, bins=bins, labels=labels)
    y_test_tier = pd.cut(y_test_elo, bins=bins, labels=labels)

    plot_confusion_matrix(y_test_tier, y_pred_tier, labels)
    plot_archetype_scatter(df_final)

    plot_feature_importance(regression_pipeline, regression_features)

    print("Visualizations generated and saved in the 'visuals' folder.")