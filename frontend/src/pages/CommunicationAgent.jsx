import React, { useState } from 'react';
import { MessageSquare, FileText, Send, AlertTriangle, Loader } from 'lucide-react';
import { communicationAPI } from '../api/client';

const CommunicationAgent = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);

    try {
      const mockData = {
        weather_data: { data: { risk_level: 'HIGH' } },
        detection_data: { data: { analysis: { people_detected: 35 } } },
        prediction_data: { data: { predictions: { urgency_level: 'CRITICAL' } } },
        resource_data: { data: {} },
        incident_location: 'Mumbai Flood Zone'
      };
      const response = await communicationAPI.generate(mockData);
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <MessageSquare size={28} className="text-cyan-400" />
          <span>Communication Agent</span>
        </h1>
        <p className="text-sm text-gray-400">Emergency alerts, reports, and communications</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📢 Generate Report</h3>
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium flex items-center justify-center space-x-2"
          >
            {loading ? (
              <Loader size={18} className="animate-spin" />
            ) : (
              <>
                <FileText size={18} />
                <span>Generate Incident Report</span>
              </>
            )}
          </button>
          {error && <div className="mt-3 text-red-400 text-sm">❌ {error}</div>}
        </div>

        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📋 Report Preview</h3>
          {results?.data ? (
            <div className="space-y-3">
              <div className="bg-dark-bg/50 rounded-lg p-3">
                <p className="text-xs text-gray-400">Incident ID</p>
                <p className="text-sm text-white font-medium">{results.data.incident_id}</p>
              </div>
              <div className="bg-dark-bg/50 rounded-lg p-3 max-h-48 overflow-y-auto">
                <p className="text-xs text-gray-400">Executive Summary</p>
                <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono mt-1">
                  {results.data.executive_summary}
                </pre>
              </div>
              {results.data.alerts?.sms && (
                <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
                  <p className="text-xs text-gray-400">📱 SMS Alert</p>
                  <p className="text-sm text-gray-300">{results.data.alerts.sms}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-48 text-gray-500">
              <MessageSquare size={48} className="mb-3 opacity-20" />
              <p className="text-sm">Generate a report to preview</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CommunicationAgent;