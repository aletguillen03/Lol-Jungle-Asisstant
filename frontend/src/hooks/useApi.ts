import { useQuery, useMutation, useQueryClient } from 'react-query';
import { userApi, gameSessionApi, jungleTimerApi, riotApi } from '../services/api';
import { User, UserCreate, GameSession, JungleTimer } from '../types';

// User hooks
export const useUsers = () => {
  return useQuery('users', () => userApi.getUsers().then(res => res.data));
};

export const useUser = (id: number) => {
  return useQuery(['user', id], () => userApi.getUser(id).then(res => res.data), {
    enabled: !!id,
  });
};

export const useUserByRiotId = (riotId: string) => {
  return useQuery(['user', 'riot', riotId], () => userApi.getUserByRiotId(riotId).then(res => res.data), {
    enabled: !!riotId,
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation((user: UserCreate) => userApi.createUser(user).then(res => res.data), {
    onSuccess: () => {
      queryClient.invalidateQueries('users');
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, user }: { id: number; user: Partial<User> }) => userApi.updateUser(id, user).then(res => res.data),
    {
      onSuccess: (data) => {
        queryClient.invalidateQueries('users');
        queryClient.invalidateQueries(['user', data.id]);
      },
    }
  );
};

// Game Session hooks
export const useGameSessions = () => {
  return useQuery('gameSessions', () => gameSessionApi.getGameSessions().then(res => res.data));
};

export const useGameSession = (id: number) => {
  return useQuery(['gameSession', id], () => gameSessionApi.getGameSession(id).then(res => res.data), {
    enabled: !!id,
  });
};

export const useCreateGameSession = () => {
  const queryClient = useQueryClient();
  return useMutation((session: Partial<GameSession>) => gameSessionApi.createGameSession(session).then(res => res.data), {
    onSuccess: () => {
      queryClient.invalidateQueries('gameSessions');
    },
  });
};

// Jungle Timer hooks
export const useJungleTimers = () => {
  return useQuery('jungleTimers', () => jungleTimerApi.getJungleTimers().then(res => res.data));
};

export const useCreateJungleTimer = () => {
  const queryClient = useQueryClient();
  return useMutation((timer: Partial<JungleTimer>) => jungleTimerApi.createJungleTimer(timer).then(res => res.data), {
    onSuccess: () => {
      queryClient.invalidateQueries('jungleTimers');
    },
  });
};

// Riot API hooks
export const useSummoner = (riotId: string, tagLine: string, region?: string) => {
  return useQuery(
    ['summoner', riotId, tagLine, region],
    () => riotApi.getSummoner(riotId, tagLine, region).then(res => res.data),
    {
      enabled: !!(riotId && tagLine),
    }
  );
};

export const useRecentMatches = (puuid: string, count?: number, region?: string) => {
  return useQuery(
    ['matches', puuid, count, region],
    () => riotApi.getRecentMatches(puuid, count, region).then(res => res.data),
    {
      enabled: !!puuid,
    }
  );
};

export const useMatchDetails = (matchId: string, region?: string) => {
  return useQuery(
    ['match', matchId, region],
    () => riotApi.getMatchDetails(matchId, region).then(res => res.data),
    {
      enabled: !!matchId,
    }
  );
}; 