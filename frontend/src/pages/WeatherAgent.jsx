import React, { useState } from 'react';
import { Cloud, MapPin, Thermometer, Droplets, Wind, Loader, AlertTriangle } from 'lucide-react';
import { weatherAPI } from '../api/client';

const WeatherAgent = () => {
  const [location, setLocation] = useState('Mumbai');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await weatherAPI.analyze(location);
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Failed to fetch weather data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Cloud size={28} className="text-cyan-400" />
          <span>Weather Agent</span>
        </h1>
        <p className="text-sm text-gray-400">Real-time weather analysis and flood risk assessment</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">🌤️ Weather Input</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <MapPin size={14} className="inline mr-1" />
                Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2 text-gray-200"
                placeholder="Enter city name"
              />
            </div>
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium"
            >
              {loading ? <Loader size={18} className="animate-spin mx-auto" /> : 'Get Weather'}
            </button>
            {error && <div className="text-red-400 text-sm">❌ {error}</div>}
          </div>
        </div>

        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📊 Weather Data</h3>
          {results?.data ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Temperature</p>
                  <p className="text-lg font-bold text-white">
                    {results.data.current?.temperature || 'N/A'}°C
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Humidity</p>
                  <p className="text-lg font-bold text-white">
                    {results.data.current?.humidity || 'N/A'}%
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Rainfall</p>
                  <p className="text-lg font-bold text-white">
                    {results.data.current?.rainfall || 0} mm
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Risk Level</p>
                  <p className={`text-lg font-bold ${
                    results.data.risk_level === 'CRITICAL' ? 'text-red-500' :
                    results.data.risk_level === 'HIGH' ? 'text-orange-500' :
                    results.data.risk_level === 'MEDIUM' ? 'text-yellow-500' :
                    'text-green-500'
                  }`}>
                    {results.data.risk_level || 'Unknown'}
                  </p>
                </div>
              </div>
              {results.data.forecast && (
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-2">Forecast (Next 6 hours)</p>
                  <div className="space-y-1">
                    {results.data.forecast.slice(0, 3).map((item, idx) => (
                      <div key={idx} className="flex justify-between text-sm">
                        <span className="text-gray-400">{item.time}</span>
                        <span className="text-gray-300">{item.rain_mm}mm - {item.condition}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-48 text-gray-500">
              <Cloud size={48} className="mb-3 opacity-20" />
              <p className="text-sm">Enter a location to get weather data</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WeatherAgent;