import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Chip,
  Alert,
  LinearProgress
} from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import AnalyticsIcon from '@mui/icons-material/Analytics';

import MaterialistDashboard from './components/MaterialistDashboard';
import { MaterialistDataProvider } from './contexts/MaterialistDataContext';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#d32f2f', // Revolutionary red
    },
    secondary: {
      main: '#ffd700', // Gold for solidarity
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 700,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

function App() {
  const [loading, setLoading] = useState(true);
  const [dataStatus, setDataStatus] = useState('connecting');

  useEffect(() => {
    // Simulate initial data loading
    const timer = setTimeout(() => {
      setLoading(false);
      setDataStatus('connected');
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <MaterialistDataProvider>
        <AppBar position="static" sx={{ mb: 3 }}>
          <Toolbar>
            <AnalyticsIcon sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Materialist Global Emotional State Monitor
            </Typography>
            <Chip 
              icon={<SmartToyIcon />} 
              label="AI-Powered Analysis" 
              variant="outlined" 
              size="small"
              sx={{ ml: 2 }}
            />
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl">
          <Alert 
            severity="info" 
            sx={{ mb: 3, '& .MuiAlert-message': { width: '100%' } }}
          >
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="body2">
                This analysis uses AI to interpret material conditions through a Marxist lens. 
                All predictions include confidence intervals and explanatory data.
              </Typography>
              {dataStatus === 'connected' && (
                <Chip label="Live Data Connected" color="success" size="small" />
              )}
            </Box>
          </Alert>

          {loading ? (
            <Box sx={{ width: '100%', mb: 2 }}>
              <Typography variant="body2" gutterBottom>
                Loading global materialist analysis...
              </Typography>
              <LinearProgress />
            </Box>
          ) : (
            <MaterialistDashboard />
          )}
        </Container>
      </MaterialistDataProvider>
    </ThemeProvider>
  );
}

export default App;
