export interface PlayerProfile {
  username: string;
  official_elo: number;
  predicted_elo: number;
  average_time: number;
  best_time: number;
  total_wins: number;
  total_losses: number;
  win_rate: number;
  total_games: number;
  consistency_ratio: number;
  official_rank: string;
  predicted_rank: string;
  player_archetype: string;
}
