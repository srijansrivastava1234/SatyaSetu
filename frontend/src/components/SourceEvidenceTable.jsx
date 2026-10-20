import React from 'react';
import { ShieldCheck, ExternalLink, LinkIcon } from './Icons';

export const SourceEvidenceTable = ({ evidence, webCitations }) => {
  const hasCertified = evidence && evidence.length > 0;
  const hasWeb = webCitations && webCitations.length > 0;

  if (!hasCertified && !hasWeb) return null;

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShieldCheck size={20} style={{ color: '#10b981' }} />
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>
              Credible-Source Verification & Evidence Provenance
            </h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Cross-referenced against certified IFCN signers, PIB Fact Check, and official records
            </p>
          </div>
        </div>
      </div>

      {/* Certified IFCN Evidence Cards */}
      {hasCertified && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#94a3b8', marginBottom: '10px' }}>
            Direct ClaimReview Matches ({evidence.length} certified debunks)
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {evidence.map((item, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '14px 18px',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-color)',
                  flexWrap: 'wrap',
                  gap: '12px'
                }}
              >
                <div style={{ flex: '1 1 300px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#38bdf8' }}>
                      {item.fact_checker}
                    </span>
                    <span className="badge badge-neutral" style={{ fontSize: '0.65rem' }}>
                      IFCN Signatory
                    </span>
                    {item.review_date && (
                      <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                        Reviewed: {item.review_date}
                      </span>
                    )}
                  </div>
                  <p style={{ fontSize: '0.82rem', color: '#e2e8f0', lineHeight: 1.4 }}>
                    "{item.claim_text}"
                  </p>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span className="badge badge-false" style={{ fontSize: '0.75rem', padding: '6px 12px' }}>
                    Rating: {item.rating}
                  </span>

                  {item.review_url && (
                    <a
                      href={item.review_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      id={`link-evidence-${idx}`}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '6px 12px',
                        borderRadius: 'var(--radius-sm)',
                        background: 'rgba(56, 189, 248, 0.12)',
                        color: '#38bdf8',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        textDecoration: 'none',
                        border: '1px solid rgba(56, 189, 248, 0.3)'
                      }}
                    >
                      <span>Read Full Debunk</span>
                      <ExternalLink size={14} />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Web Grounding & Official Gazette Citations */}
      {hasWeb && (
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#94a3b8', marginBottom: '10px' }}>
            Authoritative Institutional Cross-References
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
            {webCitations.map((cite, idx) => (
              <div
                key={idx}
                style={{
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(10, 15, 26, 0.5)',
                  border: '1px solid var(--border-color)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#10b981' }}>
                    {cite.publisher}
                  </span>
                  {cite.url && (
                    <a
                      href={cite.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: '#94a3b8', display: 'flex', alignItems: 'center' }}
                    >
                      <ExternalLink size={14} />
                    </a>
                  )}
                </div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f8fafc' }}>
                  {cite.title}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: 1.4 }}>
                  {cite.snippet}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
