import React, { useState } from 'react';
import { History as HistoryIcon, Search, Filter, Calendar, Clock } from 'lucide-react';

const History = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const mockHistory = [
    { id: 1, location: 'Mumbai Central', date: '2026-01-27 14:30', type: 'Flood', severity: 'Critical', agents: 5 },
    { id: 2, location: 'Andheri East', date: '2026-01-27 12:15', type: 'Flood', severity: 'High', agents: 4 },
    { id: 3, location: 'Bandra West', date: '2026-01-26 18:45', type: 'Flood', severity: 'Medium', agents: 3 },
    { id: 4, location: 'Powai', date: '2026-01-26 09:00', type: 'Flood', severity: 'High', agents: 4 },
    { id: 5, location: 'Dadar', date: '2026-01-25 22:30', type: 'Flood', severity: 'Low', agents: 2 },
  ];

  const filteredHistory = mockHistory.filter(item =>
    item.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <HistoryIcon size={28} className="text-cyan-400" />
          <span>History</span>
        </h1>
        <p className="text-sm text-gray-400">Past incident analyses and responses</p>
      </div>

      <div className="glass rounded-xl border border-dark-border p-6">
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
            <input
              type="text"
              placeholder="Search incidents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-dark-bg border border-dark-border rounded-lg pl-10 pr-4 py-2 text-gray-200 focus:outline-none focus:border-blue-500"
            />
          </div>
          <button className="bg-dark-bg border border-dark-border rounded-lg px-4 py-2 text-gray-400 hover:text-white transition-colors flex items-center space-x-2">
            <Filter size={16} />
            <span>Filter</span>
          </button>
        </div>

        <div className="space-y-3">
          {filteredHistory.map((item) => (
            <div key={item.id} className="bg-dark-bg/50 rounded-lg p-4 hover:bg-dark-border/50 transition-colors">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-sm font-medium text-white">{item.location}</h4>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className="text-xs text-gray-400 flex items-center space-x-1">
                      <Calendar size={12} />
                      <span>{item.date}</span>
                    </span>
                    <span className="text-xs text-gray-400">{item.type}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      item.severity === 'Critical' ? 'bg-red-500/20 text-red-400' :
                      item.severity === 'High' ? 'bg-orange-500/20 text-orange-400' :
                      item.severity === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-green-500/20 text-green-400'
                    }`}>
                      {item.severity}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs text-gray-500">{item.agents} agents</span>
                  <button className="block text-xs text-blue-400 hover:text-blue-300 mt-1">
                    View Details →
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default History;