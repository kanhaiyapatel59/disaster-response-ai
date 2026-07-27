import React from 'react';
import { Compass, MapPin, Users, Ship, Truck, Loader } from 'lucide-react';

const RescueAgent = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Compass size={28} className="text-cyan-400" />
          <span>Rescue Agent</span>
        </h1>
        <p className="text-sm text-gray-400">Route planning and rescue team deployment</p>
      </div>
      <div className="glass rounded-xl border border-dark-border p-6">
        <div className="flex flex-col items-center justify-center py-12 text-gray-500">
          <Compass size={64} className="mb-4 opacity-20" />
          <p className="text-lg">Rescue Agent</p>
          <p className="text-sm">Team deployment and route optimization</p>
          <p className="text-xs text-gray-600 mt-4">Coming soon in Day 2</p>
        </div>
      </div>
    </div>
  );
};

export default RescueAgent;