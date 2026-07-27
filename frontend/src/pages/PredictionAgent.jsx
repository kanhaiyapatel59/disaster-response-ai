import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Cloud, Camera, AlertTriangle, Loader, MapPin } from 'lucide-react';
import { predictionAPI } from '../api/client';

const PredictionAgent = () => {
  const [weatherRisk, setWeatherRisk] = useState(50);
  const [rainfall, setRainfall] = useState(5);
  const [humidity, setHumidity] = useState(75);
  const [people, setPeople] = useState(20);
  const [floodPercent, setFloodPercent] = useState(40);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const weatherData = {
        weather_risk: weatherRisk,
        rainfall: rainfall,
        humidity: humidity,
      };
      const detectionData = {
        people: people,
        flood_percentage: floodPercent,
      };

      const response = await predictionAPI.analyze(weatherData, detectionData);
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Failed to generate predictions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <TrendingUp size={28} className="text-cyan-400" />
          <span>Prediction Agent</span>
        </h1>
        <p className="text-sm text-gray-400">AI-powered flood prediction and risk assessment</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📊 Input Parameters</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <Cloud size={14} className="inline mr-1" />
                Weather Risk: {weatherRisk}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={weatherRisk}
                onChange={(e) => setWeatherRisk(Number(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <Cloud size={14} className="inline mr-1" />
                Rainfall (mm): {rainfall}
              </label>
              <input
                type="range"
                min="0"
                max="20"
                step="0.5"
                value={rainfall}
                onChange={(e) => setRainfall(Number(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <Cloud size={14} className="inline mr-1" />
                Humidity (%): {humidity}
              </label>
              <input
                type="range"
                min="30"
                max="100"
                value={humidity}
                onChange={(e) => setHumidity(Number(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <Camera size={14} className="inline mr-1" />
                People Detected: {people}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={people}
                onChange={(e) => setPeople(Number(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <Camera size={14} className="inline mr-1" />
                Flood Area (%): {floodPercent}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={floodPercent}
                onChange={(e) => setFloodPercent(Number(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center space-x-2">
                  <Loader size={18} className="animate-spin" />
                  <span>Predicting...</span>
                </span>
              ) : (
                'Generate Prediction'
              )}
            </button>

            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
                ❌ {error}
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">🔮 Prediction Results</h3>
          
          {results ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Urgency</p>
                  <p className={`text-lg font-bold ${
                    results.data?.predictions?.urgency_level === 'CRITICAL' ? 'text-red-500' :
                    results.data?.predictions?.urgency_level === 'HIGH' ? 'text-orange-500' :
                    results.data?.predictions?.urgency_level === 'MEDIUM' ? 'text-yellow-500' :
                    'text-green-500'
                  }`}>
                    {results.data?.predictions?.urgency_level || 'Unknown'}
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Risk Score</p>
                  <p className="text-lg font-bold text-white">
                    {results.data?.predictions?.overall_risk_score || 0}%
                  </p>
                </div>
              </div>

              {results.data?.predictions?.water_level_rise && (
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Water Level Rise</p>
                  <p className="text-sm font-medium text-white">
                    Current: {results.data.predictions.water_level_rise.current_rise_percent}% → 
                    Predicted: {results.data.predictions.water_level_rise.predicted_rise_percent}%
                  </p>
                  <p className="text-xs text-yellow-500 mt-1">
                    {results.data.predictions.water_level_rise.category}
                  </p>
                </div>
              )}

              {results.data?.predictions?.road_accessibility && (
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Road Accessibility</p>
                  <p className="text-sm font-medium text-white">
                    {results.data.predictions.road_accessibility.status}
                  </p>
                  <p className="text-xs text-gray-400">
                    Score: {results.data.predictions.road_accessibility.accessibility_score}%
                  </p>
                </div>
              )}

              {results.data?.recommended_actions && (
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-2">Recommended Actions</p>
                  <ul className="space-y-1">
                    {results.data.recommended_actions.slice(0, 3).map((action, idx) => (
                      <li key={idx} className="text-sm text-gray-300">• {action}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-gray-500">
              <TrendingUp size={48} className="mb-3 opacity-20" />
              <p className="text-sm">Adjust parameters to generate predictions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictionAgent;