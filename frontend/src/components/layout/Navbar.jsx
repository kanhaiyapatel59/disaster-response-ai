import React, { useState } from 'react';
import { Menu, Bell, Search, User, ChevronDown } from 'lucide-react';

const Navbar = ({ toggleSidebar }) => {
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="bg-dark-card/80 backdrop-blur-md border-b border-dark-border sticky top-0 z-40">
      <div className="flex items-center justify-between px-6 py-3">
        <div className="flex items-center space-x-4">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-lg hover:bg-dark-border transition-colors"
          >
            <Menu size={20} className="text-gray-400" />
          </button>
          <div className="relative hidden md:block">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
            <input
              type="text"
              placeholder="Search incidents, locations..."
              className="bg-dark-bg border border-dark-border rounded-lg pl-10 pr-4 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-blue-500 w-64 transition-colors"
            />
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1 text-sm text-gray-400">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span className="hidden sm:inline">All Systems Go</span>
          </div>

          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 rounded-lg hover:bg-dark-border transition-colors"
          >
            <Bell size={20} className="text-gray-400" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          <div className="flex items-center space-x-2 pl-3 border-l border-dark-border">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-cyan-400 flex items-center justify-center">
              <span className="text-white text-sm font-medium">AD</span>
            </div>
            <ChevronDown size={16} className="text-gray-400" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;