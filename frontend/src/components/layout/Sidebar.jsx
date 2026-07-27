import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Cloud,
  Camera,
  TrendingUp,
  Compass,
  Package,
  Heart,
  MessageSquare,
  FileText,
  History,
  Settings,
  AlertTriangle,
} from 'lucide-react';

const menuItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/weather', icon: Cloud, label: 'Weather Agent' },
  { path: '/detection', icon: Camera, label: 'Detection Agent' },
  { path: '/prediction', icon: TrendingUp, label: 'Prediction Agent' },
  { path: '/rescue', icon: Compass, label: 'Rescue Agent' },
  { path: '/resource', icon: Package, label: 'Resource Agent' },
  { path: '/medical', icon: Heart, label: 'Medical Agent' },
  { path: '/communication', icon: MessageSquare, label: 'Communication Agent' },
  { path: '/commander', icon: AlertTriangle, label: 'Commander Agent' },
  { path: '/reports', icon: FileText, label: 'Reports' },
  { path: '/history', icon: History, label: 'History' },
  { path: '/settings', icon: Settings, label: 'Settings' },
];

const Sidebar = ({ isOpen = true }) => {
  return (
    <motion.aside
      initial={{ x: -280 }}
      animate={{ x: isOpen ? 0 : -280 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="fixed top-0 left-0 h-full w-64 bg-dark-card border-r border-dark-border z-50 overflow-y-auto"
    >
      <div className="p-4 border-b border-dark-border">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-400 rounded-xl flex items-center justify-center">
            <AlertTriangle className="text-white" size={20} />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white">AI Command</h1>
            <p className="text-[10px] text-gray-400">Disaster Response</p>
          </div>
        </div>
      </div>

      <nav className="p-3 space-y-1">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-all duration-200 text-sm ${
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-600/30'
                  : 'text-gray-400 hover:bg-dark-border hover:text-gray-200'
              }`
            }
          >
            <item.icon size={18} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-dark-border">
        <div className="flex items-center space-x-2 text-xs text-gray-500">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span>System Online</span>
          <span className="ml-auto">v1.0.0</span>
        </div>
      </div>
    </motion.aside>
  );
};

export default Sidebar;