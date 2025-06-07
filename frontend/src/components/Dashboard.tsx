import React from 'react';
import { Grid, Paper, Typography, Box, Card, CardContent } from '@mui/material';
import { TrendingUp, EmojiEvents, Timer, Analytics } from '@mui/icons-material';

const Dashboard: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ color: '#c89b3c', mb: 4 }}>
        Dashboard del Jungler
      </Typography>
      
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
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Timer sx={{ color: '#c89b3c', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#f0e6d2' }}>
                  Objetivos
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ color: '#c89b3c' }}>
                8.2
              </Typography>
              <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                Promedio por partida
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Analytics sx={{ color: '#c89b3c', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#f0e6d2' }}>
                  KDA
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ color: '#c89b3c' }}>
                2.4
              </Typography>
              <Typography variant="body2" sx={{ color: '#a09b8c' }}>
                Promedio
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Games */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#c89b3c' }}>
              Partidas Recientes
            </Typography>
            <Typography sx={{ color: '#a09b8c' }}>
              Aquí se mostrarán las partidas recientes con análisis de IA
            </Typography>
          </Paper>
        </Grid>

        {/* AI Suggestions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#c89b3c' }}>
              Sugerencias de IA
            </Typography>
            <Typography sx={{ color: '#a09b8c' }}>
              Consejos personalizados basados en tu estilo de juego
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 