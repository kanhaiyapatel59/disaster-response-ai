import React from 'react';
import { FileText, Calendar, Download, Eye } from 'lucide-react';

const Reports = () => {
  const mockReports = [
    { id: 'DIS-20260127-0001', title: 'Mumbai Flood Incident', date: '2026-01-27', status: 'Complete' },
    { id: 'DIS-20260126-0002', title: 'Andheri Flood Assessment', date: '2026-01-26', status: 'Complete' },
    { id: 'DIS-20260126-0001', title: 'Bandra Rescue Operation', date: '2026-01-26', status: 'In Progress' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <FileText size={28} className="text-cyan-400" />
          <span>Reports</span>
        </h1>
        <p className="text-sm text-gray-400">Generated incident reports and documents</p>
      </div>

      <div className="glass rounded-xl border border-dark-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-dark-bg border-b border-dark-border">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Report ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border">
              {mockReports.map((report) => (
                <tr key={report.id} className="hover:bg-dark-bg/50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-300 font-mono">{report.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-300">{report.title}</td>
                  <td className="px-6 py-4 text-sm text-gray-400">{report.date}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      report.status === 'Complete' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {report.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <button className="p-1 rounded hover:bg-dark-border transition-colors">
                        <Eye size={16} className="text-gray-400" />
                      </button>
                      <button className="p-1 rounded hover:bg-dark-border transition-colors">
                        <Download size={16} className="text-gray-400" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Reports;