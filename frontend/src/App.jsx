import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ScenarioPicker } from './components/ScenarioPicker';
import { ClaimInputModal } from './components/ClaimInputModal';
import { PipelineVisualizer } from './components/PipelineVisualizer';
import { CredibilityMeter } from './components/CredibilityMeter';
import { ManipulationBreakdown } from './components/ManipulationBreakdown';
import { SourceEvidenceTable } from './components/SourceEvidenceTable';
import { WhatsAppSimulator } from './components/WhatsAppSimulator';
import { VerificationChecklist } from './components/VerificationChecklist';

const API_BASE = import.meta.env.VITE_API_BASE || 
  (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? "http://127.0.0.1:8000/api"
    : "https://satyasetu-wtpy.onrender.com/api");

export default function App() {
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeScenarioId, setActiveScenarioId] = useState(null);
  const [rawText, setRawText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Load initial demo scenario by default so judges see results immediately
  useEffect(() => {
    handleSelectScenario('unesco-anthem');
  }, []);

  const handleSelectScenario = async (scenarioId) => {
    setActiveScenarioId(scenarioId);
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario_id: scenarioId })
      });

      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      setResult(data);
      if (data.extracted_text) {
        setRawText(data.extracted_text);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to fetch verification result. Ensure backend server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async ({ text, url, image_base64, scenario_id }) => {
    setLoading(true);
    setError(null);

    try {
      const payload = {
        text: text || undefined,
        url: url || undefined,
        image_base64: image_base64 || undefined,
        scenario_id: scenario_id || undefined,
        api_key_override: apiKey || undefined
      };

      const res = await fetch(`${API_BASE}/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Could not complete verification pipeline. Check network or backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar apiKey={apiKey} setApiKey={setApiKey} />

      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px', width: '100%', flex: 1 }}>
        {/* Hero Pitch Headline */}
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            padding: '4px 14px',
            borderRadius: 'var(--radius-full)',
            background: 'rgba(56, 189, 248, 0.1)',
            border: '1px solid rgba(56, 189, 248, 0.25)',
            fontSize: '0.78rem',
            color: '#38bdf8',
            fontWeight: 700,
            marginBottom: '12px',
            letterSpacing: '0.04em',
            textTransform: 'uppercase'
          }}>
            CIVIC TRUST & INFORMATION INTEGRITY
          </div>
          <h2 style={{
            fontSize: 'clamp(1.8rem, 4vw, 2.5rem)',
            fontWeight: 800,
            letterSpacing: '-0.02em',
            lineHeight: 1.2,
            marginBottom: '12px'
          }}>
            Tackling Digital Misinformation & WhatsApp Viral Panics
          </h2>
          <p style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            maxWidth: '720px',
            margin: '0 auto',
            lineHeight: 1.6
          }}>
            Multimodal OCR extraction, certified IFCN ClaimReview grounding, and linguistic deception diagnostics engineered to stop viral fake news at the source.
          </p>
        </div>

        {/* 1. Quick Showcase Scenarios */}
        <ScenarioPicker
          onSelectScenario={handleSelectScenario}
          activeScenarioId={activeScenarioId}
          loading={loading}
        />

        {/* 2. Custom Input Component */}
        <ClaimInputModal
          onVerify={handleVerify}
          loading={loading}
          rawText={rawText}
          setRawText={setRawText}
          scenarioId={activeScenarioId}
          setScenarioId={setActiveScenarioId}
        />

        {error && (
          <div style={{
            padding: '16px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            color: '#f87171',
            marginBottom: '24px',
            fontSize: '0.9rem'
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* 3. Real-Time Pipeline Visualizer */}
        {result && (
          <PipelineVisualizer
            steps={result.pipeline_steps}
            totalLatency={result.total_latency_ms}
            sourceMode={result.data_source_mode}
          />
        )}

        {/* 4. Verification Results Layout */}
        {result && (
          <div>
            {/* Top Credibility Banner & Summary */}
            <CredibilityMeter result={result} />

            {/* Psychological & Linguistic Manipulation Breakdown */}
            <ManipulationBreakdown manipulation={result.manipulation_breakdown} />

            {/* Dual Grid: Evidence Provenance vs. WhatsApp Debunk Simulator */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px' }}>
              <SourceEvidenceTable
                evidence={result.certified_evidence}
                webCitations={result.web_grounding_citations}
              />
              <WhatsAppSimulator
                shareableCard={result.shareable_card}
                extractedText={result.extracted_text}
                result={result}
              />
            </div>

            {/* 5. Citizen Verification Checklist */}
            <VerificationChecklist customChecklist={result.verification_checklist} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        padding: '24px',
        borderTop: '1px solid var(--border-color)',
        textAlign: 'center',
        fontSize: '0.8rem',
        color: 'var(--text-muted)',
        backgroundColor: 'rgba(7, 9, 14, 0.95)'
      }}>
        <div>
          <strong>SatyaSetu</strong> • TrustAI Misinformation & Viral Disinformation Intelligence Engine
        </div>
        <div style={{ marginTop: '4px', fontSize: '0.75rem', color: '#64748b' }}>
          Combines Google Fact Check Tools API (IFCN Schema) • Multimodal Vision OCR • Regional Indian Civic Grounding
        </div>
      </footer>
    </div>
  );
}
