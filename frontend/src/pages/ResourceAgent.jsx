import React, { useState } from 'react';
import { Package, Home, Heart, Droplets, Users, Loader, MapPin } from 'lucide-react';
import { resourceAPI } from '../api/client';

const ResourceAgent = () => {
  const [location, setLocation] = useState('Mumbai');
  const [people, setPeople] = useState(50);
  const [severity, setSeverity] = useState('HIGH');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await resourceAPI.analyze({
        location,
        people_affected: people,
        severity,
      });
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Failed to analyze resources');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Package size={28} className="text-cyan-400" />
          <span>Resource Agent</span>
        </h1>
        <p className="text-sm text-gray-400">Shelter, medical, and rescue resource management</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📦 Resource Input</h3>
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
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                <Users size={14} className="inline mr-1" />
                People Affected
              </label>
              <input
                type="number"
                value={people}
                onChange={(e) => setPeople(Number(e.target.value))}
                className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2 text-gray-200"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Severity</label>
              <select
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
                className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2 text-gray-200"
              >
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
                <option value="CRITICAL">Critical</option>
              </select>
            </div>
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium"
            >
              {loading ? <Loader size={18} className="animate-spin mx-auto" /> : 'Analyze Resources'}
            </button>
          </div>
        </div>

        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📊 Resource Status</h3>
          {results ? (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Shelters</p>
                  <p className="text-lg font-bold text-white">
                    {results.data?.nearest_shelters?.length || 0} found
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Hospitals</p>
                  <p className="text-lg font-bold text-white">
                    {results.data?.nearest_hospitals?.length || 0} found
                  </p>
                </div>
              </div>
              {results.data?.resource_allocation && (
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Sufficiency</p>
                  <p className={`text-sm font-bold ${
                    results.data.resource_allocation.resource_sufficiency === 'ADEQUATE' ? 'text-green-500' :
                    results.data.resource_allocation.resource_sufficiency === 'PARTIAL' ? 'text-yellow-500' :
                    'text-red-500'
                  }`}>
                    {results.data.resource_allocation.resource_sufficiency}
                  </p>
                </div>
              )}
              {results.data?.resource_gaps?.length > 0 && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">⚠️ Resource Gaps</p>
                  <ul className="space-y-1">
                    {results.data.resource_gaps.map((gap, idx) => (
                      <li key={idx} className="text-sm text-red-400">• {gap}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-48 text-gray-500">
              <Package size={48} className="mb-3 opacity-20" />
              <p className="text-sm">Enter parameters to check resources</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResourceAgent;