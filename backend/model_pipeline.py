import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    df = df.dropna(subset=['elo']).copy()

    df['avg_min'] = df['averagetime'] / 60000
    df['best_min'] = df['besttime'] / 60000
    df['consistency_ratio'] = df['avg_min'] / df['best_min']
    df['total_games'] = df['wins'] + df['losses']
    df['win_rate'] = df['wins'] / df['total_games']

    df = df[df['total_games'] >= 10]
    df = df[df['consistency_ratio'] <= 5]

    bins = [-1, 599, 899, 1199, 1499, 1999, 10000]
    labels = ['Coal', 'Iron', 'Gold', 'Emerald', 'Diamond', 'Netherite']
    df['rank_tier'] = pd.cut(df['elo'], bins=bins, labels=labels)

    return df

def train_clustering_model(df):
    features = ['total_games', 'consistency_ratio', 'win_rate']
    new_df = df[features]

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(new_df)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['archetype_id'] = kmeans.fit_predict(df_scaled)

    joblib.dump(kmeans, 'kmeans_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

    return df, kmeans, scaler

def train_regression_model(X_train, y_train):
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, 'elo_regressor_pipeline.pkl')
    return pipeline

def predict_pipeline(player_stats):
    kmeans = joblib.load('kmeans_model.pkl')
    scaler_cluster = joblib.load('scaler.pkl')
    regression_pipeline = joblib.load('elo_regressor_pipeline.pkl')

    df_input = pd.DataFrame([player_stats])

    df_input['avg_min'] = df_input['averagetime'] / 60000
    df_input['best_min'] = df_input['besttime'] / 60000
    df_input['consistency_ratio'] = df_input['avg_min'] / df_input['best_min']
    df_input['total_games'] = df_input['wins'] + df_input['losses']
    df_input['win_rate'] = df_input['wins'] / df_input['total_games']

    cluster_features = ['total_games', 'consistency_ratio', 'win_rate']
    X_cluster_scaled = scaler_cluster.transform(df_input[cluster_features])
    archetype = kmeans.predict(X_cluster_scaled)[0]

    archetype_map = {
        0: "The Consistent Player",
        1: "The Climber",
        2: "The Tilt Queuer"
    }

    regression_features = ['avg_min', 'best_min', 'win_rate', 'consistency_ratio', 'total_games']
    predicted_elo = regression_pipeline.predict(df_input[regression_features])[0]

    bins = [-1, 599, 899, 1199, 1499, 1999, 10000]
    labels = ['Coal', 'Iron', 'Gold', 'Emerald', 'Diamond', 'Netherite']
    predicted_tier = pd.cut([predicted_elo], bins=bins, labels=labels)[0]

    return {
        "predicted_elo": round(predicted_elo),
        "predicted_rank_tier": str(predicted_tier),
        "predicted_archetype": archetype_map.get(archetype, "Unknown")
    }

if __name__ == '__main__':
    raw_data = load_data('playerdata.csv')
    df_cleaned = clean_data(raw_data)

    df_final, kmeans_model, cluster_scaler = train_clustering_model(df_cleaned)

    regression_features = ['avg_min', 'best_min', 'win_rate', 'consistency_ratio', 'total_games']
    X = df_final[regression_features]
    y = df_final['elo'] # Training purely on the EXACT Elo number

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = train_regression_model(X_train, y_train)

    y_pred_elo = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred_elo)

    bins = [-1, 599, 899, 1199, 1499, 1999, 10000]
    labels = ['Coal', 'Iron', 'Gold', 'Emerald', 'Diamond', 'Netherite']
    y_pred_tier = pd.cut(y_pred_elo, bins=bins, labels=labels)
    y_test_tier = pd.cut(y_test, bins=bins, labels=labels)
    accuracy = (y_pred_tier == y_test_tier).mean()

    print(f"Mean Absolute Error: Model is off by an average of {mae:.0f} Elo points.")
    print(f"Tier Binning Accuracy: {accuracy:.2%}")
    print("Pipeline complete with updated MCSR Rank Tiers.")