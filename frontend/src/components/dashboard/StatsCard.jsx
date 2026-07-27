import React from 'react';
import { motion } from 'framer-motion';

const StatsCard = ({ title, value, icon, change, color = 'blue' }) => {
  const colors = {
    blue: 'from-blue-600 to-blue-400',
    cyan: 'from-cyan-600 to-cyan-400',
    green: 'from-green-600 to-green-400',
    red: 'from-red-600 to-red-400',
    yellow: 'from-yellow-600 to-yellow-400',
    purple: 'from-purple-600 to-purple-400',
  };

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      className="glass rounded-xl p-5 border border-dark-border"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {change !== undefined && (
            <p className={`text-xs mt-2 ${change > 0 ? 'text-green-500' : 'text-red-500'}`}>
              {change > 0 ? '↑' : '↓'} {Math.abs(change)}% from last update
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colors[color] || colors.blue} flex items-center justify-center`}>
          {icon}
        </div>
      </div>
    </motion.div>
  );
};

export default StatsCard;