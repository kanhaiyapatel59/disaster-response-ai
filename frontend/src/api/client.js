import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Weather Agent
export const weatherAPI = {
  analyze: (location, useCache = true) => 
    api.post('/api/weather/analyze', { location, use_cache: useCache }),
  status: () => api.get('/api/weather/status'),
};

// Detection Agent
export const detectionAPI = {
  analyze: (formData) => 
    api.post('/api/detection/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  status: () => api.get('/api/detection/status'),
};

// Prediction Agent
export const predictionAPI = {
  analyze: (weatherData, detectionData) => 
    api.post('/api/prediction/analyze', { weather_data: weatherData, detection_data: detectionData }),
  status: () => api.get('/api/prediction/status'),
};

// Resource Agent
export const resourceAPI = {
  analyze: (data) => 
    api.post('/api/resources/analyze', data),
  status: () => api.get('/api/resources/status'),
  summary: () => api.get('/api/resources/summary'),
};

// Communication Agent
export const communicationAPI = {
  generate: (data) => 
    api.post('/api/communication/generate', data),
  status: () => api.get('/api/communication/status'),
};

// Commander Agent
export const commanderAPI = {
  analyze: (formData) => 
    api.post('/api/incident/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  status: () => api.get('/api/incident/status'),
};

// Health
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;