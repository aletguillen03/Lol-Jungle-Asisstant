import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

const UserProfile: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ color: '#c89b3c', mb: 4 }}>
        Perfil de Usuario
      </Typography>
      
      <Paper sx={{ p: 3, backgroundColor: '#1e2328', border: '1px solid #463714' }}>
        <Typography sx={{ color: '#a09b8c' }}>
          Configuración del perfil y estadísticas del jugador
        </Typography>
      </Paper>
    </Box>
  );
};

export default UserProfile; 