import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Chip,
  Tooltip,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
} from '@mui/material';
import {
  Psychology as PsychologyIcon,
  TrendingUp as TrendingUpIcon,
  Factory as FactoryIcon,
  ExpandMore as ExpandMoreIcon,
  Info as InfoIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
} from '@mui/icons-material';

import { useMaterialistData } from '../contexts/MaterialistDataContext';
import ConfidenceIndicator from './ConfidenceIndicator';

const ConsciousnessAnalysis = () => {
  const { currentAnalysis, confidence } = useMaterialistData();
  const [feedback, setFeedback] = useState({});

  const handleFeedback = (indicator, type) => {
    setFeedback(prev => ({ ...prev, [indicator]: type }));
    // In real implementation, send feedback to backend
    console.log(`Feedback for ${indicator}: ${type}`);
  };

  const analysisData = currentAnalysis || {
    consciousness_breakdown: {
      class_awareness: 0.3,
      solidarity_capacity: 0.6,
      critical_thinking: 0.4,
      revolutionary_theory: 0.2,
    },
    material_conditions: {
      economic_inequality: 0.8,
      working_conditions: 0.7,
      social_mobility: 0.3,
      political_representation: 0.4,
    },
    primary_contradictions: [
      'productive_forces_vs_production_relations',
      'labor_vs_capital',
      'individual_vs_collective',
    ],
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <Typography variant="h5">
          <PsychologyIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Consciousness Analysis
        </Typography>
        <Chip label="AI-Generated Insights" variant="outlined" size="small" />
      </Box>

      <Grid container spacing={3}>
        {/* Consciousness Breakdown */}
        <Grid item xs={12} md={6}>
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                Class Consciousness Components
              </Typography>
              <Tooltip title="AI analysis of subjective consciousness factors">
                <IconButton size="small" sx={{ ml: 1 }}>
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </AccordionSummary>
            <AccordionDetails>
              <List>
                {Object.entries(analysisData.consciousness_breakdown).map(([key, value]) => (
                  <React.Fragment key={key}>
                    <ListItem>
                      <ListItemIcon>
                        <PsychologyIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        secondary={
                          <Box>
                            <LinearProgress
                              variant="determinate"
                              value={value * 100}
                              sx={{ mt: 1, height: 8, borderRadius: 4 }}
                              color={value > 0.6 ? 'success' : value > 0.3 ? 'warning' : 'error'}
                            />
                            <Typography variant="caption" color="text.secondary">
                              {(value * 100).toFixed(1)}% development
                            </Typography>
                          </Box>
                        }
                      />
                      <Box>
                        <IconButton
                          size="small"
                          onClick={() => handleFeedback(key, 'positive')}
                          color={feedback[key] === 'positive' ? 'success' : 'default'}
                        >
                          <ThumbUpIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleFeedback(key, 'negative')}
                          color={feedback[key] === 'negative' ? 'error' : 'default'}
                        >
                          <ThumbDownIcon fontSize="small" />
                        </IconButton>
                      </Box>
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        </Grid>

        {/* Material Conditions */}
        <Grid item xs={12} md={6}>
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                Material Conditions
              </Typography>
              <Tooltip title="Objective economic and social conditions">
                <IconButton size="small" sx={{ ml: 1 }}>
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </AccordionSummary>
            <AccordionDetails>
              <List>
                {Object.entries(analysisData.material_conditions).map(([key, value]) => (
                  <React.Fragment key={key}>
                    <ListItem>
                      <ListItemIcon>
                        <FactoryIcon color="secondary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        secondary={
                          <Box>
                            <LinearProgress
                              variant="determinate"
                              value={value * 100}
                              sx={{ mt: 1, height: 8, borderRadius: 4 }}
                              color={value > 0.6 ? 'error' : value > 0.3 ? 'warning' : 'success'}
                            />
                            <Typography variant="caption" color="text.secondary">
                              {(value * 100).toFixed(1)}% severity
                            </Typography>
                          </Box>
                        }
                      />
                      <Box>
                        <IconButton
                          size="small"
                          onClick={() => handleFeedback(`material_${key}`, 'positive')}
                          color={feedback[`material_${key}`] === 'positive' ? 'success' : 'default'}
                        >
                          <ThumbUpIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleFeedback(`material_${key}`, 'negative')}
                          color={feedback[`material_${key}`] === 'negative' ? 'error' : 'default'}
                        >
                          <ThumbDownIcon fontSize="small" />
                        </IconButton>
                      </Box>
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        </Grid>

        {/* Primary Contradictions */}
        <Grid item xs={12}>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                Primary Contradictions Detected
              </Typography>
              <Tooltip title="Key systemic contradictions driving instability">
                <IconButton size="small" sx={{ ml: 1 }}>
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </AccordionSummary>
            <AccordionDetails>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {analysisData.primary_contradictions.map((contradiction, index) => (
                  <Chip
                    key={index}
                    label={contradiction.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    color="warning"
                    variant="outlined"
                    icon={<TrendingUpIcon />}
                  />
                ))}
              </Box>
              <ConfidenceIndicator 
                value={confidence * 0.85} 
                label="Contradiction Detection Confidence"
                variant="progress"
              />
            </AccordionDetails>
          </Accordion>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default ConsciousnessAnalysis;
