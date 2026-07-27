import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { motion } from 'framer-motion';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-dark-bg">
      <Sidebar isOpen={sidebarOpen} />
      
      <div className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-0'}`}>
        <Navbar toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
        
        <motion.main
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="p-6"
        >
          {children}
        </motion.main>
      </div>
    </div>
  );
};

export default Layout;