import React from 'react';
import {
  Box,
  Typography,
  Slider,
  LinearProgress,
  Tooltip,
} from '@mui/material';

const ConfidenceIndicator = ({ 
  value, 
  label = "Confidence", 
  variant = "slider",
  showPercentage = true,
  color = "primary"
}) => {
  const confidenceMarks = [
    { value: 0, label: 'Low' },
    { value: 50, label: 'Medium' },
    { value: 100, label: 'High' },
  ];

  const getConfidenceColor = (val) => {
    if (val < 0.5) return 'error';
    if (val < 0.8) return 'warning';
    return 'success';
  };

  const confidencePercentage = Math.round(value * 100);
  const dynamicColor = getConfidenceColor(value);

  if (variant === "progress") {
    return (
      <Box sx={{ width: '100%', mt: 1 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body2" color="text.secondary">
            {label}
          </Typography>
          {showPercentage && (
            <Typography variant="body2" color={`${dynamicColor}.main`}>
              {confidencePercentage}%
            </Typography>
          )}
        </Box>
        <LinearProgress
          variant="determinate"
          value={confidencePercentage}
          color={dynamicColor}
          sx={{ height: 6, borderRadius: 3, mt: 0.5 }}
        />
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', mt: 1 }}>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {label}
      </Typography>
      <Tooltip title={`AI confidence: ${confidencePercentage}% - Based on data quality and model certainty`}>
        <Slider
          value={confidencePercentage}
          aria-label={label}
          valueLabelDisplay="auto"
          disabled
          marks={confidenceMarks}
          sx={{
            '& .MuiSlider-thumb': {
              color: `${dynamicColor}.main`,
            },
            '& .MuiSlider-track': {
              color: `${dynamicColor}.main`,
            },
            '& .MuiSlider-rail': {
              opacity: 0.3,
            },
          }}
        />
      </Tooltip>
    </Box>
  );
};

export default ConfidenceIndicator;
