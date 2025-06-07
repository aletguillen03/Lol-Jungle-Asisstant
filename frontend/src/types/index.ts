// User types
export interface User {
  id: number;
  riot_id: string;
  summoner_name: string;
  tag_line: string;
  region: string;
  rank_tier?: string;
  rank_division?: string;
  league_points: number;
  preferred_jungle_champions?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UserCreate {
  riot_id: string;
  summoner_name: string;
  tag_line: string;
  region?: string;
  rank_tier?: string;
  rank_division?: string;
  league_points?: number;
  preferred_jungle_champions?: string;
}

// Game Session types
export interface GameSession {
  id: number;
  user_id: number;
  match_id: string;
  champion_name: string;
  game_mode: string;
  game_duration?: number;
  won?: boolean;
  kills: number;
  deaths: number;
  assists: number;
  cs_score: number;
  jungle_cs: number;
  vision_score: number;
  objectives_secured?: string;
  ai_suggestions?: string;
  notes?: string;
  started_at: string;
  ended_at?: string;
  created_at: string;
}

// Jungle Timer types
export interface JungleTimer {
  id: number;
  game_session_id: number;
  objective_type: string;
  objective_name: string;
  spawn_time: string;
  respawn_time?: string;
  is_secured: boolean;
  secured_by_team?: string;
  game_time_minutes: number;
  is_active: boolean;
  notes?: string;
  created_at: string;
}

// Riot API types
export interface RiotSummoner {
  puuid: string;
  gameName: string;
  tagLine: string;
}

export interface RiotSummonerDetails {
  id: string;
  accountId: string;
  puuid: string;
  name: string;
  profileIconId: number;
  revisionDate: number;
  summonerLevel: number;
}

export interface RiotRankInfo {
  leagueId: string;
  queueType: string;
  tier: string;
  rank: string;
  summonerId: string;
  summonerName: string;
  leaguePoints: number;
  wins: number;
  losses: number;
  veteran: boolean;
  inactive: boolean;
  freshBlood: boolean;
  hotStreak: boolean;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  message: string;
  status: number;
  detail?: string;
} 