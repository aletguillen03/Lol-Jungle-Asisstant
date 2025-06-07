import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

const GameSession: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ color: '#c89b3c', mb: 4 }}>
        Sesión de Partida
      </Typography>
      
      <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
        <Typography sx={{ color: '#a09b8c' }}>
          Seguimiento en tiempo real de la partida actual
        </Typography>
      </Paper>
    </Box>
  );
};

export default GameSession; 