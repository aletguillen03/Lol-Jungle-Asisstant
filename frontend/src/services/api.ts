import axios, { AxiosResponse } from 'axios';
import { User, UserCreate, GameSession, JungleTimer, RiotSummoner, RiotRankInfo } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// User API
export const userApi = {
  getUsers: (): Promise<AxiosResponse<User[]>> => api.get('/users'),
  getUser: (id: number): Promise<AxiosResponse<User>> => api.get(`/users/${id}`),
  getUserByRiotId: (riotId: string): Promise<AxiosResponse<User>> => api.get(`/users/riot/${riotId}`),
  createUser: (user: UserCreate): Promise<AxiosResponse<User>> => api.post('/users', user),
  updateUser: (id: number, user: Partial<User>): Promise<AxiosResponse<User>> => api.put(`/users/${id}`, user),
  deleteUser: (id: number): Promise<AxiosResponse<void>> => api.delete(`/users/${id}`),
};

// Game Sessions API
export const gameSessionApi = {
  getGameSessions: (): Promise<AxiosResponse<GameSession[]>> => api.get('/game-sessions'),
  getGameSession: (id: number): Promise<AxiosResponse<GameSession>> => api.get(`/game-sessions/${id}`),
  createGameSession: (session: Partial<GameSession>): Promise<AxiosResponse<GameSession>> => api.post('/game-sessions', session),
  updateGameSession: (id: number, session: Partial<GameSession>): Promise<AxiosResponse<GameSession>> => api.put(`/game-sessions/${id}`, session),
  deleteGameSession: (id: number): Promise<AxiosResponse<void>> => api.delete(`/game-sessions/${id}`),
};

// Jungle Timers API
export const jungleTimerApi = {
  getJungleTimers: (): Promise<AxiosResponse<JungleTimer[]>> => api.get('/jungle-timers'),
  getJungleTimer: (id: number): Promise<AxiosResponse<JungleTimer>> => api.get(`/jungle-timers/${id}`),
  createJungleTimer: (timer: Partial<JungleTimer>): Promise<AxiosResponse<JungleTimer>> => api.post('/jungle-timers', timer),
  updateJungleTimer: (id: number, timer: Partial<JungleTimer>): Promise<AxiosResponse<JungleTimer>> => api.put(`/jungle-timers/${id}`, timer),
  deleteJungleTimer: (id: number): Promise<AxiosResponse<void>> => api.delete(`/jungle-timers/${id}`),
};

// Riot API
export const riotApi = {
  getSummoner: (riotId: string, tagLine: string, region?: string): Promise<AxiosResponse<RiotSummoner>> => 
    api.get(`/riot/summoner/${riotId}/${tagLine}`, { params: { region } }),
  getSummonerByPuuid: (puuid: string, region?: string): Promise<AxiosResponse<any>> => 
    api.get(`/riot/summoner/puuid/${puuid}`, { params: { region } }),
  getRankInfo: (summonerId: string, region?: string): Promise<AxiosResponse<RiotRankInfo[]>> => 
    api.get(`/riot/rank/${summonerId}`, { params: { region } }),
  getRecentMatches: (puuid: string, count?: number, region?: string): Promise<AxiosResponse<string[]>> => 
    api.get(`/riot/matches/${puuid}`, { params: { count, region } }),
  getMatchDetails: (matchId: string, region?: string): Promise<AxiosResponse<any>> => 
    api.get(`/riot/match/${matchId}`, { params: { region } }),
};

// AI Assistant API
export const aiApi = {
  analyzeGame: (gameData: any): Promise<AxiosResponse<any>> => api.post('/ai/analyze-game', gameData),
  getJungleSuggestions: (gameContext: any): Promise<AxiosResponse<any>> => api.post('/ai/jungle-suggestions', gameContext),
  getChampionRecommendations: (userPreferences: any): Promise<AxiosResponse<any>> => api.post('/ai/champion-recommendations', userPreferences),
};

export default api; 