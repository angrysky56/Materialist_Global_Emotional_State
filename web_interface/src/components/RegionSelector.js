import React from 'react';
import {
  Paper,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
} from '@mui/material';
import PublicIcon from '@mui/icons-material/Public';

import { useMaterialistData } from '../contexts/MaterialistDataContext';

const RegionSelector = () => {
  const { selectedRegion, setSelectedRegion } = useMaterialistData();

  const regions = [
    { code: 'USA', name: 'United States', flag: '🇺🇸' },
    { code: 'CHN', name: 'China', flag: '🇨🇳' },
    { code: 'DEU', name: 'Germany', flag: '🇩🇪' },
    { code: 'FRA', name: 'France', flag: '🇫🇷' },
    { code: 'GBR', name: 'United Kingdom', flag: '🇬🇧' },
    { code: 'JPN', name: 'Japan', flag: '🇯🇵' },
    { code: 'IND', name: 'India', flag: '🇮🇳' },
    { code: 'BRA', name: 'Brazil', flag: '🇧🇷' },
    { code: 'ZAF', name: 'South Africa', flag: '🇿🇦' },
    { code: 'RUS', name: 'Russia', flag: '🇷🇺' },
  ];

  const handleRegionChange = (event) => {
    setSelectedRegion(event.target.value);
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <PublicIcon sx={{ mr: 1 }} />
        <Typography variant="h6">
          Regional Analysis
        </Typography>
      </Box>

      <FormControl fullWidth>
        <InputLabel id="region-select-label">Select Region</InputLabel>
        <Select
          labelId="region-select-label"
          value={selectedRegion}
          label="Select Region"
          onChange={handleRegionChange}
        >
          {regions.map((region) => (
            <MenuItem key={region.code} value={region.code}>
              <Box display="flex" alignItems="center">
                <span style={{ marginRight: 8, fontSize: '1.2em' }}>
                  {region.flag}
                </span>
                {region.name}
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Box mt={2}>
        <Chip 
          label="Real-time Data" 
          color="success" 
          size="small"
          sx={{ mr: 1 }}
        />
        <Chip 
          label="AI Analysis" 
          variant="outlined" 
          size="small"
        />
      </Box>
    </Paper>
  );
};

export default RegionSelector;
