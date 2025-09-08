import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Types for our Materialist analysis data
const initialState = {
  currentAnalysis: null,
  historicalData: [],
  loading: false,
  error: null,
  confidence: 0,
  lastUpdated: null,
  selectedRegion: 'USA',
  timeRange: '1Y',
  
  // Analysis parameters that users can control
  analysisParams: {
    consciousnessWeight: 0.5,
    materialConditionsWeight: 0.5,
    historicalMomentumWeight: 0.3,
    confidenceThreshold: 0.7,
  },

  // Methods (will be added in next chunk)
  updateAnalysisParams: () => {},
  fetchAnalysis: () => {},
  fetchHistoricalData: () => {},
  setSelectedRegion: () => {},
  setTimeRange: () => {},
};

const MaterialistDataContext = createContext(initialState);

export const useMaterialistData = () => {
  const context = useContext(MaterialistDataContext);
  if (!context) {
    throw new Error('useMaterialistData must be used within MaterialistDataProvider');
  }
  return context;
};

export const MaterialistDataProvider = ({ children }) => {
  const [state, setState] = useState(initialState);

  // Fetch current analysis from backend
  const fetchAnalysis = async (region = state.selectedRegion) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      // API call to backend running on port 5001
      const response = await axios.get(`http://localhost:5001/api/analysis/${region}`, {
        params: state.analysisParams
      });
      
      setState(prev => ({
        ...prev,
        currentAnalysis: response.data,
        confidence: response.data.confidence || 0.8,
        lastUpdated: new Date(),
        loading: false,
      }));
    } catch (error) {
      console.error('Error fetching analysis:', error);
      setState(prev => ({
        ...prev,
        error: error.message,
        loading: false,
      }));
    }
  };

  // Fetch historical data for trend analysis
  const fetchHistoricalData = async (region = state.selectedRegion, timeRange = state.timeRange) => {
    try {
      const response = await axios.get(`http://localhost:5001/api/historical/${region}`, {
        params: { timeRange, ...state.analysisParams }
      });
      
      setState(prev => ({
        ...prev,
        historicalData: response.data,
      }));
    } catch (error) {
      console.error('Error fetching historical data:', error);
    }
  };

  // Update analysis parameters (implements user control principle)
  const updateAnalysisParams = (newParams) => {
    setState(prev => ({
      ...prev,
      analysisParams: { ...prev.analysisParams, ...newParams }
    }));
    
    // Automatically refetch analysis with new parameters
    fetchAnalysis(state.selectedRegion);
  };

  const setSelectedRegion = (region) => {
    setState(prev => ({ ...prev, selectedRegion: region }));
    fetchAnalysis(region);
    fetchHistoricalData(region);
  };

  const setTimeRange = (timeRange) => {
    setState(prev => ({ ...prev, timeRange }));
    fetchHistoricalData(state.selectedRegion, timeRange);
  };

  // Initialize data on mount
  useEffect(() => {
    fetchAnalysis();
    fetchHistoricalData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const contextValue = {
    ...state,
    updateAnalysisParams,
    fetchAnalysis,
    fetchHistoricalData,
    setSelectedRegion,
    setTimeRange,
  };

  return (
    <MaterialistDataContext.Provider value={contextValue}>
      {children}
    </MaterialistDataContext.Provider>
  );
};
