import React from 'react';
import { motion } from 'framer-motion';

const RiskGauge = ({ score = 0, label = 'Risk Level' }) => {
  // Ensure score is between 0 and 100
  const normalizedScore = Math.min(Math.max(score, 0), 100);
  
  const getColor = (value) => {
    if (value > 70) return 'text-red-500';
    if (value > 40) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getBgColor = (value) => {
    if (value > 70) return 'bg-red-500';
    if (value > 40) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getLabel = (value) => {
    if (value > 70) return '⚠️ Critical';
    if (value > 40) return '⚡ Elevated';
    return '✅ Normal';
  };

  return (
    <div className="glass rounded-xl border border-dark-border p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-3">{label}</h3>
      <div className="relative">
        <div className="flex justify-between mb-1">
          <span className="text-xs text-gray-500">Low</span>
          <span className="text-xs text-gray-500">High</span>
        </div>
        <div className="w-full h-3 bg-dark-bg rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${normalizedScore}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
            className={`h-full rounded-full ${getBgColor(normalizedScore)}`}
          />
        </div>
        <div className="mt-3 flex items-center justify-between">
          <span className={`text-2xl font-bold ${getColor(normalizedScore)}`}>
            {normalizedScore}%
          </span>
          <span className="text-sm text-gray-400">{getLabel(normalizedScore)}</span>
        </div>
      </div>
    </div>
  );
};

export default RiskGauge;