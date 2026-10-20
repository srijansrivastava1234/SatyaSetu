import React from 'react';
import { Zap, AlertTriangle, ShieldCheck } from './Icons';

export const ScenarioPicker = ({ onSelectScenario, activeScenarioId, loading }) => {
  const scenarios = [
    {
      id: "unesco-anthem",
      tag: "Pride-Bait Hoax",
      icon: "🇮🇳",
      title: "UNESCO Best Anthem Award",
      desc: "Viral chain forward claiming India won #1 national anthem ranking worldwide."
    },
    {
      id: "rbi-500-note",
      tag: "Financial Panic",
      icon: "💵",
      title: "Fake RBI ₹500 Green Strip Notice",
      desc: "Warning message claiming ₹500 notes with green strip near Gandhi are counterfeit."
    },
    {
      id: "salt-shortage",
      tag: "Supply Panic",
      icon: "🧂",
      title: "Nationwide Salt Shortage Rumor",
      desc: "Panic-buying rumor alleging salt selling at ₹400/kg across northern states."
    },
    {
      id: "cbse-exam-circular",
      tag: "Authentic Benchmark",
      icon: "🏛️",
      title: "Official CBSE Exam Circular",
      desc: "Control case: Authentic government notification with formal administrative metadata."
    }
  ];

  return (
    <div style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap size={18} className="" style={{ color: '#f59e0b' }} />
          <span style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8' }}>
            Instant Pitch Showcase Scenarios (Zero-Latency Live Demo)
          </span>
        </div>
        <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
          Click to load realistic viral case
        </span>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
        gap: '12px'
      }}>
        {scenarios.map((sc) => {
          const isActive = activeScenarioId === sc.id;
          return (
            <button
              key={sc.id}
              id={`btn-scenario-${sc.id}`}
              onClick={() => onSelectScenario(sc.id)}
              disabled={loading}
              className="glass-panel-interactive"
              style={{
                padding: '14px 16px',
                textAlign: 'left',
                border: isActive ? '1px solid #38bdf8' : '1px solid var(--border-color)',
                boxShadow: isActive ? '0 0 15px rgba(56, 189, 248, 0.25)' : 'none',
                backgroundColor: isActive ? 'rgba(56, 189, 248, 0.08)' : 'var(--bg-card)',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px',
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '1.25rem' }}>{sc.icon}</span>
                <span className={`badge ${sc.id === 'cbse-exam-circular' ? 'badge-true' : 'badge-false'}`} style={{ fontSize: '0.65rem' }}>
                  {sc.tag}
                </span>
              </div>
              <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#f8fafc' }}>
                {sc.title}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: 1.35 }}>
                {sc.desc}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
