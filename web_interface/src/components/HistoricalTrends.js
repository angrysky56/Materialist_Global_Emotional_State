import React from 'react';
import {
  Paper,
  Typography,
  Box,
  ToggleButton,
  ToggleButtonGroup,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  Timeline as TimelineIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  History as HistoryIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';

import { useMaterialistData } from '../contexts/MaterialistDataContext';

const HistoricalTrends = () => {
  const { timeRange, setTimeRange } = useMaterialistData();

  const handleTimeRangeChange = (event, newTimeRange) => {
    if (newTimeRange !== null) {
      setTimeRange(newTimeRange);
    }
  };

  const mockHistoricalEvents = [
    {
      year: 2024,
      event: 'Rising Labor Unrest',
      type: 'warning',
      description: 'Increased strike activity detected across multiple sectors',
      confidence: 0.85,
    },
    {
      year: 2023,
      event: 'Inequality Peak',
      type: 'crisis',
      description: 'Wealth inequality reached historical high',
      confidence: 0.92,
    },
    {
      year: 2022,
      event: 'Consciousness Shift',
      type: 'positive',
      description: 'Measurable increase in class consciousness indicators',
      confidence: 0.78,
    },
  ];

  const getEventIcon = (type) => {
    switch (type) {
      case 'warning':
        return <WarningIcon color="warning" />;
      case 'crisis':
        return <TrendingUpIcon color="error" />;
      case 'positive':
        return <TrendingDownIcon color="success" />;
      default:
        return <HistoryIcon />;
    }
  };

  const getEventColor = (type) => {
    switch (type) {
      case 'warning':
        return 'warning';
      case 'crisis':
        return 'error';
      case 'positive':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <Typography variant="h6">
          <TimelineIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Historical Analysis
        </Typography>
        <Tooltip title="AI-detected patterns from historical data">
          <IconButton size="small">
            <InfoIcon />
          </IconButton>
        </Tooltip>
      </Box>

      <ToggleButtonGroup
        value={timeRange}
        exclusive
        onChange={handleTimeRangeChange}
        size="small"
        sx={{ mb: 3 }}
      >
        <ToggleButton value="6M">6 Months</ToggleButton>
        <ToggleButton value="1Y">1 Year</ToggleButton>
        <ToggleButton value="5Y">5 Years</ToggleButton>
        <ToggleButton value="10Y">10 Years</ToggleButton>
      </ToggleButtonGroup>

      <Typography variant="subtitle2" gutterBottom>
        Key Historical Events
      </Typography>

      <List dense>
        {mockHistoricalEvents.map((event, index) => (
          <ListItem key={index} sx={{ px: 0 }}>
            <ListItemIcon>
              {getEventIcon(event.type)}
            </ListItemIcon>
            <ListItemText
              primary={
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography variant="body2" fontWeight="bold">
                    {event.year}: {event.event}
                  </Typography>
                  <Chip
                    label={`${(event.confidence * 100).toFixed(0)}% confidence`}
                    size="small"
                    color={getEventColor(event.type)}
                    variant="outlined"
                  />
                </Box>
              }
              secondary={event.description}
            />
          </ListItem>
        ))}
      </List>

      <Box mt={2}>
        <Chip 
          label="AI Historical Analysis" 
          variant="outlined" 
          size="small"
          sx={{ mr: 1 }}
        />
        <Chip 
          label="Pattern Recognition" 
          color="primary" 
          size="small"
        />
      </Box>
    </Paper>
  );
};

export default HistoricalTrends;
