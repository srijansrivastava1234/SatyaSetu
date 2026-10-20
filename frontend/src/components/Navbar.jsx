import React, { useState } from 'react';
import { ShieldCheck, KeyIcon, Info, Activity } from './Icons';

export const Navbar = ({ apiKey, setApiKey }) => {
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [tempKey, setTempKey] = useState(apiKey || '');

  const handleSave = () => {
    setApiKey(tempKey);
    setShowKeyModal(false);
  };

  return (
    <>
      <header style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px 32px',
        borderBottom: '1px solid var(--border-color)',
        backgroundColor: 'rgba(7, 9, 14, 0.85)',
        backdropFilter: 'blur(12px)',
        position: 'sticky',
        top: 0,
        zIndex: 50
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #f97316 0%, #38bdf8 50%, #10b981 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(56, 189, 248, 0.3)'
          }}>
            <ShieldCheck size={26} className="" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '1.35rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#fff' }}>
                Satya<span style={{ color: '#38bdf8' }}>Setu</span>
              </h1>
              <span className="badge badge-neutral" style={{ fontSize: '0.65rem', padding: '2px 8px' }}>
                PS ID: 202611
              </span>
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              TrustAI Misinformation & WhatsApp Manipulation Intelligence Engine
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(16, 185, 129, 0.08)',
            border: '1px solid rgba(16, 185, 129, 0.2)',
            padding: '6px 14px',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.75rem',
            color: '#34d399'
          }}>
            <span className="status-indicator online"></span>
            <span>IFCN ClaimReview & PIB Engine Active</span>
          </div>

          <button
            id="btn-settings-apikey"
            onClick={() => setShowKeyModal(true)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '7px 14px',
              borderRadius: 'var(--radius-md)',
              background: apiKey ? 'rgba(56, 189, 248, 0.12)' : 'rgba(255, 255, 255, 0.05)',
              border: '1px solid ' + (apiKey ? 'rgba(56, 189, 248, 0.3)' : 'var(--border-color)'),
              color: apiKey ? '#38bdf8' : 'var(--text-secondary)',
              fontSize: '0.8rem',
              fontWeight: 600
            }}
          >
            <KeyIcon size={16} />
            <span>{apiKey ? 'API Key Configured' : 'Configure Gemini Key'}</span>
          </button>
        </div>
      </header>

      {/* API Key Modal */}
      {showKeyModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100
        }}>
          <div className="glass-panel" style={{ width: '480px', padding: '24px', position: 'relative' }}>
            <h3 style={{ fontSize: '1.15rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <KeyIcon size={20} />
              Optional Gemini API Key
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              SatyaSetu works 100% out-of-the-box using built-in linguistic heuristics, Google Fact Check tools, and pre-indexed verified datasets. To enable live multimodal Gemini 1.5 Flash Vision OCR on custom uploaded screenshots, provide an optional API key below.
            </p>
            <input
              type="password"
              placeholder="AIzaSy..."
              value={tempKey}
              onChange={(e) => setTempKey(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 14px',
                fontSize: '0.9rem',
                marginBottom: '18px'
              }}
            />
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button
                onClick={() => setShowKeyModal(false)}
                style={{
                  padding: '8px 16px',
                  borderRadius: 'var(--radius-md)',
                  background: 'transparent',
                  color: 'var(--text-secondary)',
                  border: '1px solid var(--border-color)'
                }}
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                style={{
                  padding: '8px 20px',
                  borderRadius: 'var(--radius-md)',
                  background: '#38bdf8',
                  color: '#07090e',
                  fontWeight: 700
                }}
              >
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
