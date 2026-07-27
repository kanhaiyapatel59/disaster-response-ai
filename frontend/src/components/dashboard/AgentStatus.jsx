import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Loader, Clock, XCircle } from 'lucide-react';

const AgentStatus = ({ agents }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle size={14} className="text-green-500" />;
      case 'running':
        return <Loader size={14} className="text-yellow-500 animate-spin" />;
      case 'waiting':
        return <Clock size={14} className="text-gray-500" />;
      case 'completed':
        return <CheckCircle size={14} className="text-blue-500" />;
      default:
        return <XCircle size={14} className="text-red-500" />;
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'active': return 'status-dot active';
      case 'running': return 'status-dot running';
      case 'waiting': return 'status-dot waiting';
      case 'completed': return 'status-dot completed';
      default: return 'status-dot waiting';
    }
  };

  return (
    <div className="glass rounded-xl border border-dark-border p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">🤖 AI Agents Status</h3>
      <div className="space-y-3">
        {agents.map((agent, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.05 }}
            className="flex items-center justify-between p-2 rounded-lg bg-dark-bg/50"
          >
            <div className="flex items-center space-x-3">
              <span className={getStatusClass(agent.status)}></span>
              <span className="text-sm text-gray-300">{agent.name}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-gray-500">{agent.status}</span>
              {getStatusIcon(agent.status)}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default AgentStatus;