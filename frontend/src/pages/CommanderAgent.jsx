import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Play, Loader, CheckCircle, AlertTriangle, 
  Cloud, Camera, TrendingUp, Compass, Package, Heart, MessageSquare,
  MapPin, Users, Upload
} from 'lucide-react';
import { commanderAPI } from '../api/client';

const agentSteps = [
  { id: 'weather', name: 'Weather Agent', icon: Cloud, status: 'pending' },
  { id: 'detection', name: 'Detection Agent', icon: Camera, status: 'pending' },
  { id: 'prediction', name: 'Prediction Agent', icon: TrendingUp, status: 'pending' },
  { id: 'rescue', name: 'Rescue Agent', icon: Compass, status: 'pending' },
  { id: 'resource', name: 'Resource Agent', icon: Package, status: 'pending' },
  { id: 'medical', name: 'Medical Agent', icon: Heart, status: 'pending' },
  { id: 'communication', name: 'Communication Agent', icon: MessageSquare, status: 'pending' },
];

const CommanderAgent = () => {
  const [location, setLocation] = useState('Mumbai');
  const [peopleAffected, setPeopleAffected] = useState('');
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [agents, setAgents] = useState(agentSteps);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(-1);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setResults(null);
    setCurrentStep(-1);

    setAgents(agentSteps.map(a => ({ ...a, status: 'pending' })));

    try {
      const formData = new FormData();
      formData.append('location', location);
      if (image) formData.append('image', image);
      if (peopleAffected) formData.append('people_affected_estimate', peopleAffected);

      const simulateAgentExecution = async () => {
        for (let i = 0; i < agentSteps.length; i++) {
          setCurrentStep(i);
          setAgents(prev => prev.map((a, idx) => 
            idx === i ? { ...a, status: 'running' } : a
          ));
          await new Promise(resolve => setTimeout(resolve, 1200));
          setAgents(prev => prev.map((a, idx) => 
            idx === i ? { ...a, status: 'completed' } : a
          ));
        }
      };

      const [apiResponse] = await Promise.all([
        commanderAPI.analyze(formData),
        simulateAgentExecution()
      ]);

      setResults(apiResponse.data);
      setCurrentStep(-1);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Failed to analyze incident. Please try again.');
      setCurrentStep(-1);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'text-gray-500 border-gray-500';
      case 'running': return 'text-yellow-500 border-yellow-500 animate-pulse';
      case 'completed': return 'text-green-500 border-green-500';
      default: return 'text-gray-500 border-gray-500';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return <span className="w-4 h-4 rounded-full border-2 border-gray-500" />;
      case 'running': return <Loader size={16} className="animate-spin text-yellow-500" />;
      case 'completed': return <CheckCircle size={16} className="text-green-500" />;
      default: return <span className="w-4 h-4 rounded-full border-2 border-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <AlertTriangle size={28} className="text-cyan-400" />
          <span>Commander Agent</span>
        </h1>
        <p className="text-sm text-gray-400">Orchestrate all agents for complete disaster response</p>
      </div>

      <div className="glass rounded-xl border border-dark-border p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <MapPin size={16} className="inline mr-1" />
              Location
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2.5 text-gray-200 focus:outline-none focus:border-blue-500"
              placeholder="Enter city"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Users size={16} className="inline mr-1" />
              People Affected (Estimate)
            </label>
            <input
              type="number"
              value={peopleAffected}
              onChange={(e) => setPeopleAffected(e.target.value)}
              className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2.5 text-gray-200 focus:outline-none focus:border-blue-500"
              placeholder="Estimated people"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Upload size={16} className="inline mr-1" />
              Drone Image
            </label>
            <div className="flex items-center space-x-3">
              <label className="flex-1 cursor-pointer">
                <div className="bg-dark-bg border-2 border-dashed border-dark-border rounded-lg p-3 text-center hover:border-blue-500 transition-colors">
                  <span className="text-xs text-gray-400">Upload Image</span>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                </div>
              </label>
              {imagePreview && (
                <div className="w-14 h-14 rounded-lg overflow-hidden border border-dark-border flex-shrink-0">
                  <img src={imagePreview} alt="Preview" className="w-full h-full object-cover" />
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="mt-4 flex justify-end">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-8 py-3 rounded-lg font-medium flex items-center space-x-2 transition-all"
          >
            {loading ? (
              <>
                <Loader size={18} className="animate-spin" />
                <span>Executing Agents...</span>
              </>
            ) : (
              <>
                <Play size={18} />
                <span>Execute Commander</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="glass rounded-xl border border-dark-border p-6">
        <h3 className="text-sm font-semibold text-gray-300 mb-4">⚡ Agent Execution Flow</h3>
        <div className="space-y-3">
          {agents.map((agent, idx) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className={`flex items-center space-x-4 p-3 rounded-lg border transition-all ${
                currentStep === idx ? 'border-yellow-500/50 bg-yellow-500/5' : 'border-dark-border'
              } ${agent.status === 'completed' ? 'bg-green-500/5 border-green-500/30' : ''}`}
            >
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-dark-bg">
                <agent.icon size={18} className={agent.status === 'completed' ? 'text-green-500' : 'text-gray-400'} />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-300">{agent.name}</p>
                {currentStep === idx && (
                  <p className="text-xs text-yellow-500 animate-pulse">Executing...</p>
                )}
                {agent.status === 'completed' && (
                  <p className="text-xs text-green-500">✓ Complete</p>
                )}
              </div>
              <div className={`flex items-center justify-center w-8 h-8 rounded-full border-2 ${getStatusColor(agent.status)}`}>
                {getStatusIcon(agent.status)}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      <AnimatePresence>
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass rounded-xl border border-dark-border p-6"
          >
            <h3 className="text-sm font-semibold text-gray-300 mb-4">📋 Disaster Response Plan</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <div className="bg-dark-bg/50 rounded-lg p-3">
                <p className="text-xs text-gray-400">Status</p>
                <p className="text-sm font-semibold text-green-500">{results.status}</p>
              </div>
              <div className="bg-dark-bg/50 rounded-lg p-3">
                <p className="text-xs text-gray-400">Urgency</p>
                <p className={`text-sm font-semibold ${
                  results.urgency === 'CRITICAL' ? 'text-red-500' :
                  results.urgency === 'HIGH' ? 'text-orange-500' :
                  results.urgency === 'MEDIUM' ? 'text-yellow-500' : 'text-green-500'
                }`}>{results.urgency}</p>
              </div>
              <div className="bg-dark-bg/50 rounded-lg p-3">
                <p className="text-xs text-gray-400">Risk Score</p>
                <p className="text-sm font-semibold text-white">{results.risk_score}%</p>
              </div>
              <div className="bg-dark-bg/50 rounded-lg p-3">
                <p className="text-xs text-gray-400">Agents Executed</p>
                <p className="text-sm font-semibold text-white">{results.execution_order?.length || 0}/7</p>
              </div>
            </div>

            {results.report && (
              <div className="space-y-4">
                <div className="bg-dark-bg/50 rounded-lg p-4">
                  <p className="text-sm font-medium text-gray-400">Executive Summary</p>
                  <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono mt-2">
                    {results.report.executive_summary}
                  </pre>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-400 mb-2">Recommended Actions</p>
                  <ul className="list-disc list-inside space-y-1">
                    {results.report.recommended_actions?.map((action, idx) => (
                      <li key={idx} className="text-sm text-gray-300">{action}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400">
          ❌ {error}
        </div>
      )}
    </div>
  );
};

export default CommanderAgent;