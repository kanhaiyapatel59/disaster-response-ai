import React, { useState } from 'react';
import { Camera, Upload, MapPin, Users, Droplets, AlertTriangle, Loader } from 'lucide-react';
import { detectionAPI } from '../api/client';

const DetectionAgent = () => {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [location, setLocation] = useState('Mumbai');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = async () => {
    if (!image) {
      setError('Please upload an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('location', location);

      const response = await detectionAPI.analyze(formData);
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Camera size={28} className="text-cyan-400" />
          <span>Detection Agent</span>
        </h1>
        <p className="text-sm text-gray-400">AI-powered drone/CCTV image analysis</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📸 Upload Image</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                <MapPin size={16} className="inline mr-1" />
                Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2.5 text-gray-200 focus:outline-none focus:border-blue-500"
                placeholder="Enter location"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                <Upload size={16} className="inline mr-1" />
                Drone/CCTV Image
              </label>
              <label className="cursor-pointer">
                <div className="bg-dark-bg border-2 border-dashed border-dark-border rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
                  {imagePreview ? (
                    <img src={imagePreview} alt="Preview" className="max-h-48 mx-auto rounded-lg" />
                  ) : (
                    <div>
                      <Camera size={40} className="mx-auto text-gray-500" />
                      <p className="text-sm text-gray-400 mt-2">Click to upload image</p>
                      <p className="text-xs text-gray-500">JPG, PNG, WEBP supported</p>
                    </div>
                  )}
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                </div>
              </label>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading || !image}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center space-x-2">
                  <Loader size={18} className="animate-spin" />
                  <span>Analyzing...</span>
                </span>
              ) : (
                'Analyze Image'
              )}
            </button>

            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
                ❌ {error}
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        <div className="glass rounded-xl border border-dark-border p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4">📊 Detection Results</h3>
          
          {results ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">People Detected</p>
                  <p className="text-xl font-bold text-white">
                    {results.data?.analysis?.people_detected || 0}
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Flood Area</p>
                  <p className="text-xl font-bold text-yellow-500">
                    {results.data?.analysis?.flood_area_percent || 0}%
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Severity</p>
                  <p className={`text-xl font-bold ${
                    results.data?.analysis?.severity_level === 'CRITICAL' ? 'text-red-500' :
                    results.data?.analysis?.severity_level === 'HIGH' ? 'text-orange-500' :
                    results.data?.analysis?.severity_level === 'MEDIUM' ? 'text-yellow-500' :
                    'text-green-500'
                  }`}>
                    {results.data?.analysis?.severity_level || 'Unknown'}
                  </p>
                </div>
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400">Water Level</p>
                  <p className="text-sm font-medium text-white">
                    {results.data?.analysis?.water_level || 'Unknown'}
                  </p>
                </div>
              </div>

              {results.data?.recommendations && (
                <div className="bg-dark-bg/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-2">Recommendations</p>
                  <ul className="space-y-1">
                    {results.data.recommendations.map((rec, idx) => (
                      <li key={idx} className="text-sm text-gray-300">• {rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-gray-500">
              <Camera size={48} className="mb-3 opacity-20" />
              <p className="text-sm">Upload an image to see detection results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DetectionAgent;