/**
 * API Service for ConvoAI Backend Communication
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },

  // Session management
  async startSession() {
    const response = await api.post('/session/start');
    return response.data;
  },

  async submitResponse(sessionId, responseText) {
    const response = await api.post(`/session/${sessionId}/respond`, {
      response: responseText
    });
    return response.data;
  },

  async getSessionSummary(sessionId) {
    const response = await api.get(`/session/${sessionId}/summary`);
    return response.data;
  },

  async getFinalAnalysis(sessionId) {
    const response = await api.get(`/session/${sessionId}/analysis/final`);
    return response.data;
  },

  async getSessionStatus(sessionId) {
    const response = await api.get(`/session/${sessionId}/status`);
    return response.data;
  },

  async skipQuestion(sessionId) {
    const response = await api.post(`/session/${sessionId}/skip`);
    return response.data;
  },

  async endSession(sessionId) {
    const response = await api.post(`/session/${sessionId}/end`);
    return response.data;
  },

  async getQuestionCategories() {
    const response = await api.get('/questions/categories');
    return response.data;
  }
};

export default apiService;