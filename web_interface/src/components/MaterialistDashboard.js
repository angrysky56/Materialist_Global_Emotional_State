import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
} from '@mui/material';
import {
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  Psychology as PsychologyIcon,
  TrendingUp as TrendingUpIcon,
  Groups as GroupsIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';

import { useMaterialistData } from '../contexts/MaterialistDataContext';
import ConsciousnessAnalysis from './ConsciousnessAnalysis';
import ConfidenceIndicator from './ConfidenceIndicator';
import HistoricalTrends from './HistoricalTrends';
import RegionSelector from './RegionSelector';
import ParameterControls from './ParameterControls';

const MaterialistDashboard = () => {
  const { 
    currentAnalysis, 
    loading, 
    error, 
    confidence 
  } = useMaterialistData();
  
  const [explanationDialog, setExplanationDialog] = useState(false);
  const [selectedIndicator, setSelectedIndicator] = useState(null);

  const handleExplainIndicator = (indicator) => {
    setSelectedIndicator(indicator);
    setExplanationDialog(true);
  };

  if (loading) {
    return <Typography>Loading analysis...</Typography>;
  }

  if (error) {
    return (
      <Alert severity="error">
        Error loading analysis: {error}
      </Alert>
    );
  }

  return (
    <Box>
      {/* Control Panel */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <RegionSelector />
        </Grid>
        <Grid item xs={12} md={8}>
          <ParameterControls />
        </Grid>
      </Grid>

      {/* Main Analysis Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Consciousness Type Card */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 2, height: '200px' }}>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Typography variant="h6" gutterBottom>
                <PsychologyIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Consciousness Type
              </Typography>
              <Tooltip title="AI-detected based on material conditions analysis">
                <IconButton 
                  size="small"
                  onClick={() => handleExplainIndicator('consciousness')}
                >
                  <InfoIcon />
                </IconButton>
              </Tooltip>
            </Box>
            
            <Typography variant="h4" color="primary" sx={{ mb: 1 }}>
              {currentAnalysis?.consciousness_type || 'Reified'}
            </Typography>
            
            <ConfidenceIndicator 
              value={confidence * 0.8} 
              label="Detection Confidence"
            />
            
            <Chip 
              label="AI-Generated" 
              size="small" 
              variant="outlined"
              sx={{ mt: 1 }}
            />
          </Paper>
        </Grid>

        {/* Revolutionary Potential Card */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 2, height: '200px' }}>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Typography variant="h6" gutterBottom>
                <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Revolutionary Potential
              </Typography>
              <Tooltip title="Based on contradiction intensity and class consciousness">
                <IconButton 
                  size="small"
                  onClick={() => handleExplainIndicator('revolutionary_potential')}
                >
                  <InfoIcon />
                </IconButton>
              </Tooltip>
            </Box>
            
            <Typography variant="h4" color="secondary" sx={{ mb: 1 }}>
              {((currentAnalysis?.revolutionary_potential || 0) * 100).toFixed(1)}%
            </Typography>
            
            <ConfidenceIndicator 
              value={confidence * 0.9} 
              label="Prediction Confidence"
            />
            
            {(currentAnalysis?.revolutionary_potential || 0) > 0.7 && (
              <Chip 
                label="High Risk" 
                color="warning" 
                size="small"
                sx={{ mt: 1 }}
              />
            )}
          </Paper>
        </Grid>

        {/* Solidarity Level Card */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 2, height: '200px' }}>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Typography variant="h6" gutterBottom>
                <GroupsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Solidarity Level
              </Typography>
              <Tooltip title="Worker organization and collective action capacity">
                <IconButton 
                  size="small"
                  onClick={() => handleExplainIndicator('solidarity')}
                >
                  <InfoIcon />
                </IconButton>
              </Tooltip>
            </Box>
            
            <Typography variant="h4" color="success.main" sx={{ mb: 1 }}>
              {((currentAnalysis?.solidarity_level || 0) * 100).toFixed(1)}%
            </Typography>
            
            <ConfidenceIndicator 
              value={confidence * 0.85} 
              label="Assessment Confidence"
            />
          </Paper>
        </Grid>

        {/* Crisis Indicators Card */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 2, height: '200px' }}>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Typography variant="h6" gutterBottom>
                <WarningIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Crisis Indicators
              </Typography>
              <Tooltip title="Active contradictions signaling systemic instability">
                <IconButton 
                  size="small"
                  onClick={() => handleExplainIndicator('crisis')}
                >
                  <InfoIcon />
                </IconButton>
              </Tooltip>
            </Box>
            
            <Typography variant="h4" color="error.main" sx={{ mb: 1 }}>
              {currentAnalysis?.crisis_indicators?.length || 0}
            </Typography>
            
            <Typography variant="body2" color="text.secondary">
              Active Contradictions
            </Typography>
            
            <ConfidenceIndicator 
              value={confidence} 
              label="Detection Confidence"
            />
          </Paper>
        </Grid>
      </Grid>

      {/* Detailed Analysis Components */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <ConsciousnessAnalysis />
        </Grid>
        <Grid item xs={12} lg={4}>
          <HistoricalTrends />
        </Grid>
      </Grid>

      {/* Explanation Dialog - Implements XAI principles */}
      <Dialog 
        open={explanationDialog} 
        onClose={() => setExplanationDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          AI Analysis Explanation: {selectedIndicator}
        </DialogTitle>
        <DialogContent>
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">How This Was Calculated</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography paragraph>
                This indicator is derived from multiple data sources using machine learning 
                algorithms trained on historical materialist theory.
              </Typography>
              {selectedIndicator === 'consciousness' && (
                <Typography paragraph>
                  <strong>Consciousness Type</strong> is determined by analyzing:
                  • Union density and worker organization levels
                  • Strike frequency and collective bargaining coverage
                  • Media concentration and narrative dominance
                  • Educational access and critical thinking indicators
                </Typography>
              )}
              {selectedIndicator === 'revolutionary_potential' && (
                <Typography paragraph>
                  <strong>Revolutionary Potential</strong> combines:
                  • Material conditions severity (inequality, unemployment)
                  • Subjective consciousness development
                  • Historical momentum and crisis indicators
                  • International solidarity factors
                </Typography>
              )}
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Data Sources & Confidence</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography paragraph>
                Primary data sources: OECD, ILO, World Bank, national statistics
              </Typography>
              <Typography paragraph>
                Confidence level: {(confidence * 100).toFixed(1)}% based on data quality 
                and theoretical alignment.
              </Typography>
            </AccordionDetails>
          </Accordion>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExplanationDialog(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MaterialistDashboard;
