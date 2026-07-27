import React from 'react';
import { motion } from 'framer-motion';

const ActivityFeed = ({ activities }) => {
  return (
    <div className="glass rounded-xl border border-dark-border p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">🔄 Recent Activity</h3>
      <div className="space-y-3 max-h-64 overflow-y-auto">
        {activities.map((activity, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: idx * 0.05 }}
            className="flex items-start space-x-3 p-2 rounded-lg hover:bg-dark-border/50 transition-colors"
          >
            <span className="text-lg">{activity.icon}</span>
            <div className="flex-1">
              <p className="text-sm text-gray-300">{activity.message}</p>
              <p className="text-xs text-gray-500 mt-0.5">{activity.time}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ActivityFeed;