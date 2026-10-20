import React, { useState } from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle, Info } from './Icons';

export const CredibilityMeter = ({ result }) => {
  if (!result) return null;

  const [activeLang, setActiveLang] = useState('en'); // 'en' | 'hi'

  const {
    overall_verdict,
    credibility_score,
    risk_level,
    debunk_summary_en,
    debunk_summary_hi,
    atomic_claims
  } = result;

  const isFalse = overall_verdict.includes('FALSE') || overall_verdict.includes('FABRICATED') || overall_verdict.includes('HOAX');
  const isTrue = overall_verdict.includes('TRUE') || overall_verdict.includes('AUTHENTIC');
  const isWarning = !isFalse && !isTrue;

  const statusColor = isFalse ? '#ef4444' : isTrue ? '#10b981' : '#f59e0b';
  const statusBg = isFalse ? 'rgba(239, 68, 68, 0.12)' : isTrue ? 'rgba(16, 185, 129, 0.12)' : 'rgba(245, 158, 11, 0.12)';
  const statusBorder = isFalse ? 'rgba(239, 68, 68, 0.3)' : isTrue ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.3)';

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '28px', borderTop: `4px solid ${statusColor}` }}>
      {/* Top Verdict Header */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '16px',
        paddingBottom: '20px',
        borderBottom: '1px solid var(--border-color)',
        marginBottom: '20px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: 'var(--radius-md)',
            background: statusBg,
            border: `1px solid ${statusBorder}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: statusColor
          }}>
            {isFalse ? <AlertTriangle size={28} /> : isTrue ? <CheckCircle size={28} /> : <Info size={28} />}
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '1.4rem', fontWeight: 800, color: statusColor, letterSpacing: '-0.01em' }}>
                {overall_verdict}
              </span>
              <span className={`badge ${isFalse ? 'badge-false' : isTrue ? 'badge-true' : 'badge-warning'}`} style={{ fontSize: '0.7rem' }}>
                {risk_level.replace(/_/g, ' ')}
              </span>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Deterministic cross-reference against Certified IFCN Fact-Check Archive
            </p>
          </div>
        </div>

        {/* Credibility Dial / Numerical Badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid var(--border-color)',
          padding: '10px 18px',
          borderRadius: 'var(--radius-lg)'
        }}>
          <div>
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
              Credibility Index
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: statusColor, fontFamily: 'var(--font-mono)' }}>
                {credibility_score}
              </span>
              <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>/ 100</span>
            </div>
          </div>

          <div style={{
            width: '64px',
            height: '8px',
            background: '#1e293b',
            borderRadius: '4px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: `${credibility_score}%`,
              height: '100%',
              background: statusColor,
              borderRadius: '4px',
              transition: 'width 0.8s ease'
            }} />
          </div>
        </div>
      </div>

      {/* Debunk Summary with Language Selector */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em', color: '#cbd5e1' }}>
            Executive Fact-Check Synthesis
          </h4>
          <div style={{ display: 'flex', gap: '6px' }}>
            <button
              onClick={() => setActiveLang('en')}
              style={{
                padding: '4px 10px',
                borderRadius: '6px',
                fontSize: '0.75rem',
                fontWeight: 600,
                background: activeLang === 'en' ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                color: activeLang === 'en' ? '#38bdf8' : 'var(--text-muted)',
                border: activeLang === 'en' ? '1px solid rgba(56, 189, 248, 0.4)' : '1px solid transparent'
              }}
            >
              English
            </button>
            <button
              onClick={() => setActiveLang('hi')}
              style={{
                padding: '4px 10px',
                borderRadius: '6px',
                fontSize: '0.75rem',
                fontWeight: 600,
                background: activeLang === 'hi' ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                color: activeLang === 'hi' ? '#38bdf8' : 'var(--text-muted)',
                border: activeLang === 'hi' ? '1px solid rgba(56, 189, 248, 0.4)' : '1px solid transparent'
              }}
            >
              हिंदी (Hindi)
            </button>
          </div>
        </div>

        <div style={{
          padding: '16px 20px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(10, 15, 26, 0.6)',
          border: '1px solid var(--border-color)',
          fontSize: '0.95rem',
          lineHeight: 1.65,
          color: '#f8fafc'
        }}>
          {activeLang === 'en' ? debunk_summary_en : debunk_summary_hi}
        </div>
      </div>

      {/* Atomic Claims Dissection */}
      {atomic_claims && atomic_claims.length > 0 && (
        <div>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em', color: '#cbd5e1', marginBottom: '10px' }}>
            Atomic Claim Deconstruction ({atomic_claims.length} claims identified)
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {atomic_claims.map((claim) => (
              <div
                key={claim.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                  fontSize: '0.85rem'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flex: 1 }}>
                  <span style={{
                    width: '22px',
                    height: '22px',
                    borderRadius: '50%',
                    background: 'rgba(56, 189, 248, 0.15)',
                    color: '#38bdf8',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.75rem',
                    fontWeight: 700
                  }}>
                    {claim.id}
                  </span>
                  <div>
                    <span style={{ color: '#f1f5f9', fontWeight: 500 }}>{claim.text}</span>
                    <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>
                      Target Entity: <strong style={{ color: '#94a3b8' }}>{claim.target_entity}</strong> | Query: <code style={{ color: '#38bdf8' }}>{claim.normalized_query}</code>
                    </div>
                  </div>
                </div>
                <span className={`badge ${claim.verdict === 'FALSE' ? 'badge-false' : claim.verdict === 'TRUE' ? 'badge-true' : 'badge-neutral'}`} style={{ fontSize: '0.65rem' }}>
                  {claim.verdict}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
