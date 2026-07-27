import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Layout from './components/layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import WeatherAgent from './pages/WeatherAgent';
import DetectionAgent from './pages/DetectionAgent';
import PredictionAgent from './pages/PredictionAgent';
import RescueAgent from './pages/RescueAgent';
import ResourceAgent from './pages/ResourceAgent';
import MedicalAgent from './pages/MedicalAgent';
import CommunicationAgent from './pages/CommunicationAgent';
import CommanderAgent from './pages/CommanderAgent';
import Reports from './pages/Reports';
import History from './pages/History';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/weather" element={<WeatherAgent />} />
            <Route path="/detection" element={<DetectionAgent />} />
            <Route path="/prediction" element={<PredictionAgent />} />
            <Route path="/rescue" element={<RescueAgent />} />
            <Route path="/resource" element={<ResourceAgent />} />
            <Route path="/medical" element={<MedicalAgent />} />
            <Route path="/communication" element={<CommunicationAgent />} />
            <Route path="/commander" element={<CommanderAgent />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;