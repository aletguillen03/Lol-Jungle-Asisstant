import React from 'react';
import { Button, Box } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import { Dashboard, Person, SportsEsports, Timer } from '@mui/icons-material';

const Navigation: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <Dashboard /> },
    { path: '/profile', label: 'Perfil', icon: <Person /> },
    { path: '/game', label: 'Partida', icon: <SportsEsports /> },
    { path: '/timers', label: 'Timers', icon: <Timer /> },
  ];

  return (
    <Box sx={{ display: 'flex', gap: 2 }}>
      {navItems.map((item) => (
        <Button
          key={item.path}
          component={Link}
          to={item.path}
          startIcon={item.icon}
          sx={{
            color: location.pathname === item.path ? '#c89b3c' : '#f0e6d2',
            '&:hover': {
              backgroundColor: 'rgba(200, 155, 60, 0.1)',
            },
          }}
        >
          {item.label}
        </Button>
      ))}
    </Box>
  );
};

export default Navigation; 