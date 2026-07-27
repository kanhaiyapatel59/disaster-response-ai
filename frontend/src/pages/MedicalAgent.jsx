import React from 'react';
import { Heart, Stethoscope, Pill, Activity, Truck, Users } from 'lucide-react';

const MedicalAgent = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Heart size={28} className="text-cyan-400" />
          <span>Medical Agent</span>
        </h1>
        <p className="text-sm text-gray-400">Medical resource tracking and ambulance dispatch</p>
      </div>
      <div className="glass rounded-xl border border-dark-border p-6">
        <div className="flex flex-col items-center justify-center py-12 text-gray-500">
          <Stethoscope size={64} className="mb-4 opacity-20" />
          <p className="text-lg">Medical Agent</p>
          <p className="text-sm">Hospital beds, ambulances, and medical supplies</p>
          <p className="text-xs text-gray-600 mt-4">Coming soon in Day 2</p>
        </div>
      </div>
    </div>
  );
};

export default MedicalAgent;