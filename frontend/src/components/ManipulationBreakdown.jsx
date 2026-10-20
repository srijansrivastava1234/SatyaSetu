import React from 'react';
import { AlertTriangle, Info, Zap } from './Icons';

export const ManipulationBreakdown = ({ manipulation }) => {
  if (!manipulation) return null;

  const {
    urgency_score,
    emotional_intensity,
    sensationalism_score,
    credibility_index,
    detected_tactics,
    linguistic_markers,
    missing_elements
  } = manipulation;

  const getMetricColor = (val) => {
    if (val >= 70) return '#ef4444'; // Red
    if (val >= 40) return '#f59e0b'; // Amber
    return '#10b981'; // Green
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '18px' }}>
        <Zap size={20} style={{ color: '#f59e0b' }} />
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>
            Psychological Manipulation & Deception Analysis
          </h3>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Deep linguistic markers explaining WHY this message was engineered to trigger immediate viral sharing
          </p>
        </div>
      </div>

      {/* 3 Metric Gauges */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '16px',
        marginBottom: '20px'
      }}>
        {/* Urgency */}
        <div style={{
          padding: '14px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid var(--border-color)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#cbd5e1' }}>Manufactured Urgency</span>
            <span style={{ fontSize: '0.85rem', fontWeight: 800, color: getMetricColor(urgency_score), fontFamily: 'var(--font-mono)' }}>
              {urgency_score}%
            </span>
          </div>
          <div style={{ height: '6px', background: '#1e293b', borderRadius: '3px', overflow: 'hidden' }}>
            <div style={{ width: `${urgency_score}%`, height: '100%', background: getMetricColor(urgency_score), borderRadius: '3px' }} />
          </div>
          <span style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '6px', display: 'block' }}>
            {urgency_score > 60 ? 'Forces reader to act without thinking' : 'Normal descriptive pacing'}
          </span>
        </div>

        {/* Emotional Outrage/Fear */}
        <div style={{
          padding: '14px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid var(--border-color)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#cbd5e1' }}>Emotional Intensity</span>
            <span style={{ fontSize: '0.85rem', fontWeight: 800, color: getMetricColor(emotional_intensity), fontFamily: 'var(--font-mono)' }}>
              {emotional_intensity}%
            </span>
          </div>
          <div style={{ height: '6px', background: '#1e293b', borderRadius: '3px', overflow: 'hidden' }}>
            <div style={{ width: `${emotional_intensity}%`, height: '100%', background: getMetricColor(emotional_intensity), borderRadius: '3px' }} />
          </div>
          <span style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '6px', display: 'block' }}>
            {emotional_intensity > 60 ? 'Appeals to panic, outrage, or pride' : 'Balanced, objective tone'}
          </span>
        </div>

        {/* Sensationalism */}
        <div style={{
          padding: '14px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid var(--border-color)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#cbd5e1' }}>Sensational Punctuation</span>
            <span style={{ fontSize: '0.85rem', fontWeight: 800, color: getMetricColor(sensationalism_score), fontFamily: 'var(--font-mono)' }}>
              {sensationalism_score}%
            </span>
          </div>
          <div style={{ height: '6px', background: '#1e293b', borderRadius: '3px', overflow: 'hidden' }}>
            <div style={{ width: `${sensationalism_score}%`, height: '100%', background: getMetricColor(sensationalism_score), borderRadius: '3px' }} />
          </div>
          <span style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '6px', display: 'block' }}>
            {sensationalism_score > 60 ? 'Heavy ALL-CAPS and exclamation marks' : 'Standard journalistic syntax'}
          </span>
        </div>
      </div>

      {/* Breakdown Chips */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px'
      }}>
        {/* Detected Tactics */}
        <div style={{
          padding: '14px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(239, 68, 68, 0.04)',
          border: '1px solid rgba(239, 68, 68, 0.15)'
        }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#f87171', marginBottom: '8px' }}>
            Identified Deception Tactics
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {detected_tactics.map((tactic, idx) => (
              <span key={idx} className="badge badge-false" style={{ fontSize: '0.7rem' }}>
                {tactic}
              </span>
            ))}
          </div>
        </div>

        {/* Missing Elements */}
        <div style={{
          padding: '14px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(245, 158, 11, 0.04)',
          border: '1px solid rgba(245, 158, 11, 0.15)'
        }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#fbbf24', marginBottom: '8px' }}>
            Missing Journalistic Anchors
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {missing_elements.map((elem, idx) => (
              <span key={idx} className="badge badge-warning" style={{ fontSize: '0.7rem' }}>
                {elem}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
