from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from model_pipeline import predict_pipeline

app = FastAPI(
    title="MCSR Ranked Profiler API",
    version="1.6.2"
)
origins = [
    "https://mcsr-ranked-profiler.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileResponse(BaseModel):
    username: str
    official_elo: int
    predicted_elo: int
    average_time: float
    best_time: float
    total_wins: int
    total_losses: int
    win_rate: float
    total_games: int
    consistency_ratio: float
    official_rank: str
    predicted_rank: str
    player_archetype: str

def get_specific_rank(elo: int) -> str:
    if elo < 400: return "Coal 1"
    elif elo < 500: return "Coal 2"
    elif elo < 600: return "Coal 3"
    elif elo < 700: return "Iron 1"
    elif elo < 800: return "Iron 2"
    elif elo < 900: return "Iron 3"
    elif elo < 1000: return "Gold 1"
    elif elo < 1100: return "Gold 2"
    elif elo < 1200: return "Gold 3"
    elif elo < 1300: return "Emerald 1"
    elif elo < 1400: return "Emerald 2"
    elif elo < 1500: return "Emerald 3"
    elif elo < 1650: return "Diamond 1"
    elif elo < 1800: return "Diamond 2"
    elif elo < 2000: return "Diamond 3"
    else: return "Netherite"

@app.get("/profile/{username}", response_model=ProfileResponse)
def get_player_profile(username: str):
    url = f"https://mcsrranked.com/api/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Player not found in MCSR Ranked database.")

    data = response.json().get("data", {})

    official_elo = data.get("eloRate", 0)
    nickname = data.get("nickname", username)

    stats_season = data.get("statistics", {}).get("season", {})

    wins = stats_season.get("wins", {}).get("ranked", 0)
    losses = stats_season.get("loses", {}).get("ranked", 0)
    besttime = stats_season.get("bestTime", {}).get("ranked", 0)

    completions = stats_season.get("completions", {}).get("ranked", 0)
    completion_time_total = stats_season.get("completionTime", {}).get("ranked", 0)

    if besttime == 0 or (wins + losses) == 0 or completions == 0:
        raise HTTPException(status_code=400, detail="Not enough ranked data to profile this player.")

    averagetime = completion_time_total / completions
    total_games = wins + losses
    win_rate = wins / total_games

    avg_min = averagetime / 60000
    best_min = besttime / 60000
    consistency_ratio = avg_min / best_min if best_min > 0 else 0

    player_stats_dict = {
        "averagetime": averagetime,
        "besttime": besttime,
        "wins": wins,
        "losses": losses
    }

    prediction = predict_pipeline(player_stats_dict)

    return ProfileResponse(
        username=nickname,
        official_elo=official_elo,
        predicted_elo=prediction["predicted_elo"],
        average_time=averagetime,
        best_time=besttime,
        total_wins=wins,
        total_losses=losses,
        win_rate=win_rate,
        total_games=total_games,
        consistency_ratio=consistency_ratio,
        official_rank=get_specific_rank(official_elo),
        predicted_rank=get_specific_rank(prediction["predicted_elo"]),
        player_archetype=prediction["predicted_archetype"]
    )

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the MCSR Ranked Profiler API! We are currently Live!",
    }