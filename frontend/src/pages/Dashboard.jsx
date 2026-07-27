import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  MapPin, Users, Heart, Home, Cloud, AlertTriangle,
  TrendingUp, Activity, Clock, CheckCircle
} from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import StatsCard from '../components/dashboard/StatsCard';
import AgentStatus from '../components/dashboard/AgentStatus';
import ActivityFeed from '../components/dashboard/ActivityFeed';
import RiskGauge from '../components/dashboard/RiskGauge';
import { healthAPI } from '../api/client';

// Fix Leaflet default marker
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Dashboard = () => {
  const [stats, setStats] = useState({
    affectedAreas: 12,
    peopleAffected: 2847,
    peopleRescued: 1243,
    sheltersOpen: 23,
    weatherStatus: 'Critical',
    criticalAlerts: 4,
  });

  const [agents, setAgents] = useState([
    { name: 'Weather Agent', status: 'active' },
    { name: 'Detection Agent', status: 'active' },
    { name: 'Prediction Agent', status: 'waiting' },
    { name: 'Rescue Agent', status: 'waiting' },
    { name: 'Resource Agent', status: 'waiting' },
    { name: 'Medical Agent', status: 'waiting' },
    { name: 'Communication Agent', status: 'waiting' },
  ]);

  const [activities, setActivities] = useState([
    { icon: '🌤️', message: 'Weather Agent: Critical rainfall detected in Mumbai', time: '2 min ago' },
    { icon: '📸', message: 'Detection Agent: 35 people detected in flood zone', time: '5 min ago' },
    { icon: '🔮', message: 'Prediction Agent: Water level predicted to rise 25%', time: '8 min ago' },
    { icon: '🏥', message: 'Resource Agent: 3 shelters at 80% capacity', time: '12 min ago' },
    { icon: '🚁', message: 'Rescue Agent: 2 teams deployed to Bandra', time: '18 min ago' },
  ]);

  const [riskScore, setRiskScore] = useState(68);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await healthAPI.check();
        console.log('System health:', response.data);
      } catch (error) {
        console.error('Health check failed:', error);
      }
    };
    checkHealth();

    const interval = setInterval(() => {
      setAgents(prev => {
        const newAgents = [...prev];
        const idx = Math.floor(Math.random() * newAgents.length);
        const statuses = ['active', 'running', 'waiting', 'completed'];
        newAgents[idx].status = statuses[Math.floor(Math.random() * statuses.length)];
        return newAgents;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-sm text-gray-400">Real-time disaster monitoring and response</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatsCard
          title="Affected Areas"
          value={stats.affectedAreas}
          icon={<MapPin size={20} className="text-white" />}
          color="red"
          change={12}
        />
        <StatsCard
          title="People Affected"
          value={stats.peopleAffected.toLocaleString()}
          icon={<Users size={20} className="text-white" />}
          color="yellow"
          change={8}
        />
        <StatsCard
          title="People Rescued"
          value={stats.peopleRescued.toLocaleString()}
          icon={<Heart size={20} className="text-white" />}
          color="green"
          change={15}
        />
        <StatsCard
          title="Shelters Open"
          value={stats.sheltersOpen}
          icon={<Home size={20} className="text-white" />}
          color="cyan"
          change={3}
        />
        <StatsCard
          title="Weather Status"
          value={stats.weatherStatus}
          icon={<Cloud size={20} className="text-white" />}
          color="purple"
        />
        <StatsCard
          title="Critical Alerts"
          value={stats.criticalAlerts}
          icon={<AlertTriangle size={20} className="text-white" />}
          color="red"
          change={-5}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map - Takes 2/3 of space */}
        <div className="lg:col-span-2 glass rounded-xl border border-dark-border overflow-hidden h-[400px]">
          <div className="p-4 border-b border-dark-border">
            <h3 className="text-sm font-semibold text-gray-300">🗺️ Incident Map</h3>
          </div>
          <MapContainer
            center={[19.0760, 72.8777]}
            zoom={11}
            className="h-[calc(100%-52px)]"
          >
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            />
            <Circle
              center={[19.0760, 72.8777]}
              radius={3000}
              pathOptions={{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.2 }}
            />
            <Circle
              center={[19.1136, 72.8697]}
              radius={2000}
              pathOptions={{ color: '#f59e0b', fillColor: '#f59e0b', fillOpacity: 0.2 }}
            />
            <Circle
              center={[19.0556, 72.8401]}
              radius={1500}
              pathOptions={{ color: '#3b82f6', fillColor: '#3b82f6', fillOpacity: 0.2 }}
            />
            <Marker position={[19.0760, 72.8777]}>
              <Popup>
                <div className="text-sm">
                  <strong>Mumbai Central</strong>
                  <p className="text-gray-400">Critical Flooding</p>
                  <p className="text-xs text-gray-500">35 people affected</p>
                </div>
              </Popup>
            </Marker>
            <Marker position={[19.1136, 72.8697]}>
              <Popup>
                <div className="text-sm">
                  <strong>Andheri East</strong>
                  <p className="text-gray-400">High Water Level</p>
                  <p className="text-xs text-gray-500">20 people affected</p>
                </div>
              </Popup>
            </Marker>
          </MapContainer>
        </div>

        {/* Right Panel - Agent Status */}
        <div className="space-y-6">
          <AgentStatus agents={agents} />
          <RiskGauge score={riskScore} />
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ActivityFeed activities={activities} />
        </div>
        <div className="glass rounded-xl border border-dark-border p-5">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📊 Quick Stats</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-2 bg-dark-bg/50 rounded-lg">
              <span className="text-sm text-gray-400">Active Incidents</span>
              <span className="text-sm font-semibold text-white">8</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-dark-bg/50 rounded-lg">
              <span className="text-sm text-gray-400">Rescue Teams</span>
              <span className="text-sm font-semibold text-white">14</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-dark-bg/50 rounded-lg">
              <span className="text-sm text-gray-400">Ambulances</span>
              <span className="text-sm font-semibold text-white">23</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-dark-bg/50 rounded-lg">
              <span className="text-sm text-gray-400">Response Time</span>
              <span className="text-sm font-semibold text-green-500">4.2 min</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;