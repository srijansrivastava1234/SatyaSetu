import React from 'react';
import { Activity, Check, Clock } from './Icons';

export const PipelineVisualizer = ({ steps, totalLatency, sourceMode }) => {
  if (!steps || steps.length === 0) return null;

  return (
    <div className="glass-panel" style={{ padding: '20px 24px', marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={18} style={{ color: '#38bdf8' }} />
          <h3 style={{ fontSize: '0.9rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em', color: '#cbd5e1' }}>
            Multi-Tier Verification Pipeline Execution
          </h3>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
            Source Mode: <strong style={{ color: '#38bdf8' }}>{sourceMode || 'Hybrid Tier 1 + RAG'}</strong>
          </span>
          <span className="badge badge-neutral" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Clock size={12} />
            {totalLatency}ms total
          </span>
        </div>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '12px'
      }}>
        {steps.map((step, idx) => (
          <div
            key={idx}
            style={{
              padding: '12px 14px',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(255, 255, 255, 0.02)',
              border: '1px solid rgba(255, 255, 255, 0.06)',
              display: 'flex',
              flexDirection: 'column',
              gap: '4px'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#38bdf8' }}>
                Stage 0{idx + 1}
              </span>
              <span style={{
                fontSize: '0.65rem',
                fontFamily: 'var(--font-mono)',
                color: '#64748b',
                background: 'rgba(255, 255, 255, 0.04)',
                padding: '2px 6px',
                borderRadius: '4px'
              }}>
                {step.elapsed_ms}ms
              </span>
            </div>
            <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#f1f5f9' }}>
              {step.name}
            </div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8', lineHeight: 1.3 }}>
              {step.detail}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
