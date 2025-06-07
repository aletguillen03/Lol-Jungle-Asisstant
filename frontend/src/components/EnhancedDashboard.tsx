// frontend/src/components/EnhancedDashboard.tsx

import React, { useState, useEffect } from 'react';
import {
  Grid, Paper, Typography, Box, Card, CardContent, Button,
  Alert, Chip, LinearProgress, Avatar, List, ListItem, 
  ListItemText, ListItemAvatar, Divider
} from '@mui/material';
import {
  TrendingUp, EmojiEvents, Timer, Analytics, PlayArrow,
  Person, Visibility, Assessment, TrendingDown
} from '@mui/icons-material';
import { useSummoner, useRecentMatches } from '../hooks/useApi';

interface DashboardProps {
  riotId?: string;
  tagLine?: string;
  region?: string;
}

const EnhancedDashboard: React.FC<DashboardProps> = ({
  riotId = "Not Alet",
  tagLine = "LAS", 
  region = "las"
}) => {
  const [liveGameStatus, setLiveGameStatus] = useState<'checking' | 'in_game' | 'not_in_game'>('checking');
  const [aiSuggestions, setAiSuggestions] = useState<string[]>([]);

  // Fetch summoner data
  const { data: summonerData, isLoading: summonerLoading, error: summonerError } = useSummoner(riotId, tagLine, region);
  
  // Fetch recent matches if we have summoner data
  const { data: recentMatches, isLoading: matchesLoading } = useRecentMatches(
    summonerData?.puuid, 
    10, 
    region
  );

  // Check for live game
  useEffect(() => {
    const checkLiveGame = async () => {
      try {
        const response = await fetch(`/api/v1/jungle/live-game/${riotId}/${tagLine}?region=${region}`);
        const data = await response.json();
        setLiveGameStatus(data.in_game ? 'in_game' : 'not_in_game');
      } catch (error) {
        console.error('Error checking live game:', error);
        setLiveGameStatus('not_in_game');
      }
    };

    checkLiveGame();
    const interval = setInterval(checkLiveGame, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, [riotId, tagLine, region]);

  // Mock AI suggestions (replace with real API call)
  useEffect(() => {
    setAiSuggestions([
      "Considera practicar tu claro inicial con Graves para mejorar tu tempo early game",
      "Tu winrate con Kindred es alto - úsala más en ranked",
      "Prioriza más la visión en river después del minuto 10"
    ]);
  }, []);

  if (summonerLoading) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress sx={{ backgroundColor: '#463714', '& .MuiLinearProgress-bar': { backgroundColor: '#c89b3c' } }} />
        <Typography sx={{ mt: 2, color: '#a09b8c', textAlign: 'center' }}>
          Cargando datos de {riotId}...
        </Typography>
      </Box>
    );
  }

  if (summonerError) {
    return (
      <Alert severity="error" sx={{ mt: 4, backgroundColor: '#1e2328', border: '1px solid #d32f2f' }}>
        Error cargando datos del summoner. Verifica que "{riotId}#{tagLine}" sea correcto en la región LAS.
      </Alert>
    );
  }

  return (
    <Box>
      {/* Header con información del summoner */}
      <Paper sx={{ p: 3, mb: 4, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar 
            sx={{ 
              width: 60, 
              height: 60, 
              mr: 2, 
              backgroundColor: '#c89b3c',
              fontSize: '1.5rem'
            }}
          >
            {riotId.charAt(0)}
          </Avatar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" sx={{ color: '#c89b3c' }}>
              {riotId}#{tagLine}
            </Typography>
            <Typography variant="subtitle1" sx={{ color: '#a09b8c' }}>
              Región: LAS • Jungler Principal
            </Typography>
          </Box>
          {liveGameStatus === 'in_game' && (
            <Chip 
              icon={<PlayArrow />}
              label="EN PARTIDA"
              color="success"
              variant="outlined"
              sx={{ 
                color: '#00ff00', 
                borderColor: '#00ff00',
                '& .MuiChip-icon': { color: '#00ff00' }
              }}
            />
          )}
        </Box>
        
        {liveGameStatus === 'in_game' && (
          <Alert severity="info" sx={{ backgroundColor: 'rgba(76, 175, 80, 0.1)', border: '1px solid #4caf50' }}>
            Partida activa detectada. Los timers y análisis en tiempo real están disponibles.
            <Button 
              variant="contained" 
              size="small" 
              sx={{ ml: 2, backgroundColor: '#c89b3c', '&:hover': { backgroundColor: '#a0782a' } }}
            >
              Ver Partida
            </Button>
          </Alert>
        )}
      </Paper>

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ color: '#c89b3c', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#f0e6d2' }}>
                  Winrate
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ color: '#c89b3c' }}>
                67%
              </Typography>
              <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                Últimas 20 partidas
              </Typography>
              <Box sx={{ mt: 1 }}>
                <Chip label="+3% esta semana" size="small" sx={{ backgroundColor: '#4caf50', color: 'white' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <EmojiEvents sx={{ color: '#c89b3c', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#f0e6d2' }}>
                  Rango
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ color: '#c89b3c' }}>
                Gold II
              </Typography>
              <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                45 LP
              </Typography>
              <Box sx={{ mt: 1 }}>
                <Chip label="Promo a Gold I" size="small" sx={{ backgroundColor: '#ff9800', color: 'white' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Timer sx={{ color: '#c89b3c', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#f0e6d2' }}>
                  Objetivos/Partida
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ color: '#c89b3c' }}>
                8.2
              </Typography>
              <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                Promedio últimas 10
              </Typography>
              <Box sx={{ mt: 1 }}>
                <Chip label="Top 15% junglers" size="small" sx={{ backgroundColor: '#9c27b0', color: 'white' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Analytics sx={{ color: '#c89b3c', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#f0e6d2' }}>
                  KDA Promedio
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ color: '#c89b3c' }}>
                2.4
              </Typography>
              <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                7.2 / 5.1 / 9.8
              </Typography>
              <Box sx={{ mt: 1 }}>
                <Chip label="Mejorando" size="small" sx={{ backgroundColor: '#4caf50', color: 'white' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Campeones Favoritos */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#c89b3c', mb: 2 }}>
              Campeones de Jungla Más Jugados
            </Typography>
            
            <List>
              {[
                { name: 'Graves', games: 23, winrate: 74, kda: 2.8 },
                { name: 'Kindred', games: 18, winrate: 67, kda: 2.5 },
                { name: "Kha'Zix", games: 15, winrate: 60, kda: 3.1 },
                { name: 'Nidalee', games: 12, winrate: 58, kda: 2.2 }
              ].map((champion, index) => (
                <React.Fragment key={champion.name}>
                  <ListItem>
                    <ListItemAvatar>
                      <Avatar sx={{ backgroundColor: '#c89b3c', width: 40, height: 40 }}>
                        {champion.name.charAt(0)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography sx={{ color: '#f0e6d2' }}>{champion.name}</Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Chip 
                              label={`${champion.winrate}% WR`} 
                              size="small" 
                              sx={{ 
                                backgroundColor: champion.winrate >= 65 ? '#4caf50' : champion.winrate >= 55 ? '#ff9800' : '#f44336',
                                color: 'white' 
                              }} 
                            />
                            <Chip 
                              label={`${champion.kda} KDA`} 
                              size="small" 
                              sx={{ backgroundColor: '#1976d2', color: 'white' }} 
                            />
                          </Box>
                        </Box>
                      }
                      secondary={
                        <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                          {champion.games} partidas jugadas
                        </Typography>
                      }
                    />
                  </ListItem>
                  {index < 3 && <Divider sx={{ backgroundColor: '#463714' }} />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Sugerencias de IA */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#c89b3c', mb: 2 }}>
              Sugerencias de IA Personalizadas
            </Typography>
            
            <List>
              {aiSuggestions.map((suggestion, index) => (
                <React.Fragment key={index}>
                  <ListItem sx={{ pl: 0 }}>
                    <ListItemAvatar>
                      <Avatar sx={{ backgroundColor: '#1976d2', width: 32, height: 32, fontSize: '0.8rem' }}>
                        AI
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography sx={{ color: '#f0e6d2', fontSize: '0.9rem' }}>
                          {suggestion}
                        </Typography>
                      }
                    />
                  </ListItem>
                  {index < aiSuggestions.length - 1 && <Divider sx={{ backgroundColor: '#463714', ml: 5 }} />}
                </React.Fragment>
              ))}
            </List>
            
            <Button 
              variant="outlined" 
              fullWidth 
              sx={{ 
                mt: 2, 
                borderColor: '#c89b3c', 
                color: '#c89b3c',
                '&:hover': { 
                  backgroundColor: 'rgba(200, 155, 60, 0.1)',
                  borderColor: '#c89b3c'
                }
              }}
            >
              Obtener Más Consejos
            </Button>
          </Paper>
        </Grid>

        {/* Acciones Rápidas */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#c89b3c', mb: 2 }}>
              Acciones Rápidas
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="contained"
                  fullWidth
                  startIcon={<PlayArrow />}
                  sx={{ 
                    backgroundColor: '#c89b3c',
                    '&:hover': { backgroundColor: '#a0782a' },
                    py: 1.5
                  }}
                  disabled={liveGameStatus !== 'not_in_game'}
                >
                  Iniciar Sesión
                </Button>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<Timer />}
                  sx={{ 
                    borderColor: '#c89b3c',
                    color: '#c89b3c',
                    '&:hover': { 
                      backgroundColor: 'rgba(200, 155, 60, 0.1)',
                      borderColor: '#c89b3c'
                    },
                    py: 1.5
                  }}
                >
                  Ver Timers
                </Button>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<Assessment />}
                  sx={{ 
                    borderColor: '#c89b3c',
                    color: '#c89b3c',
                    '&:hover': { 
                      backgroundColor: 'rgba(200, 155, 60, 0.1)',
                      borderColor: '#c89b3c'
                    },
                    py: 1.5
                  }}
                >
                  Analizar Última Partida
                </Button>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<Person />}
                  sx={{ 
                    borderColor: '#c89b3c',
                    color: '#c89b3c',
                    '&:hover': { 
                      backgroundColor: 'rgba(200, 155, 60, 0.1)',
                      borderColor: '#c89b3c'
                    },
                    py: 1.5
                  }}
                >
                  Configurar Perfil
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default EnhancedDashboard;