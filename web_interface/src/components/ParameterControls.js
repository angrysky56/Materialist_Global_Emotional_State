import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Slider,
  FormLabel,
  Tooltip,
  IconButton,
  Chip,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Psychology as PsychologyIcon,
  Engineering as EngineeringIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';

import { useMaterialistData } from '../contexts/MaterialistDataContext';

const ParameterControls = () => {
  const { analysisParams, updateAnalysisParams } = useMaterialistData();

  const handleParamChange = (param) => (event, newValue) => {
    updateAnalysisParams({ [param]: newValue });
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <SettingsIcon sx={{ mr: 1 }} />
        <Typography variant="h6">
          Analysis Parameters
        </Typography>
        <Chip 
          label="User Controllable" 
          size="small" 
          variant="outlined"
          sx={{ ml: 2 }}
        />
      </Box>

      <Typography variant="body2" color="text.secondary" paragraph>
        Adjust these parameters to explore different theoretical weightings.
        Changes are applied in real-time to the analysis.
      </Typography>

      <Box sx={{ mb: 3 }}>
        <Box display="flex" alignItems="center" mb={1}>
          <PsychologyIcon sx={{ mr: 1, fontSize: 20 }} />
          <FormLabel>Consciousness Weight</FormLabel>
          <Tooltip title="How much emphasis to place on subjective class consciousness vs material conditions">
            <IconButton size="small">
              <SettingsIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
        <Slider
          value={analysisParams.consciousnessWeight}
          onChange={handleParamChange('consciousnessWeight')}
          min={0}
          max={1}
          step={0.1}
          marks={[
            { value: 0, label: 'Material Focus' },
            { value: 0.5, label: 'Balanced' },
            { value: 1, label: 'Consciousness Focus' },
          ]}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Box display="flex" alignItems="center" mb={1}>
          <EngineeringIcon sx={{ mr: 1, fontSize: 20 }} />
          <FormLabel>Material Conditions Weight</FormLabel>
        </Box>
        <Slider
          value={analysisParams.materialConditionsWeight}
          onChange={handleParamChange('materialConditionsWeight')}
          min={0}
          max={1}
          step={0.1}
          marks={[
            { value: 0, label: 'Minimal' },
            { value: 0.5, label: 'Standard' },
            { value: 1, label: 'Deterministic' },
          ]}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Box display="flex" alignItems="center" mb={1}>
          <TrendingUpIcon sx={{ mr: 1, fontSize: 20 }} />
          <FormLabel>Historical Momentum Weight</FormLabel>
        </Box>
        <Slider
          value={analysisParams.historicalMomentumWeight}
          onChange={handleParamChange('historicalMomentumWeight')}
          min={0}
          max={1}
          step={0.1}
          marks={[
            { value: 0, label: 'Present Only' },
            { value: 0.3, label: 'Moderate' },
            { value: 1, label: 'Historical Focus' },
          ]}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
        />
      </Box>

      <Box sx={{ mb: 2 }}>
        <FormLabel>Confidence Threshold</FormLabel>
        <Slider
          value={analysisParams.confidenceThreshold}
          onChange={handleParamChange('confidenceThreshold')}
          min={0.1}
          max={1}
          step={0.05}
          marks={[
            { value: 0.1, label: 'Low' },
            { value: 0.7, label: 'Standard' },
            { value: 0.95, label: 'High' },
          ]}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
        />
      </Box>
    </Paper>
  );
};

export default ParameterControls;
