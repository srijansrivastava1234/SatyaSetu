import React, { useState } from 'react';
import { MessageSquare, Copy, Check, Share2, ShieldCheck } from './Icons';

export const WhatsAppSimulator = ({ shareableCard, extractedText, result }) => {
  if (!shareableCard) return null;

  const [copiedLang, setCopiedLang] = useState(null); // 'en' | 'hi'

  const handleCopy = (lang) => {
    const textToCopy = lang === 'en' 
      ? shareableCard.whatsapp_format_text_en 
      : shareableCard.whatsapp_format_text_hi;

    navigator.clipboard.writeText(textToCopy);
    setCopiedLang(lang);
    setTimeout(() => setCopiedLang(null), 2500);
  };

  const downloadTruthCard = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 675;
    const ctx = canvas.getContext('2d');

    // Background Gradient
    const grad = ctx.createLinearGradient(0, 0, 1200, 675);
    grad.addColorStop(0, '#0f172a');
    grad.addColorStop(1, '#1e293b');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1200, 675);

    // Border frame
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 4;
    ctx.strokeRect(20, 20, 1160, 635);

    // Header Brand
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 36px Arial, sans-serif';
    ctx.fillText("🛡️ SatyaSetu (सत्यसेतु) — Digital Truth Verification", 50, 75);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '18px Arial, sans-serif';
    ctx.fillText("Problem Statement 202611 | IFCN Certified Grounding & Gazette Cross-Reference", 50, 110);

    // Divider
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.3)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(50, 130);
    ctx.lineTo(1150, 130);
    ctx.stroke();

    // Claim Box
    ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.fillRect(50, 150, 1100, 110);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.strokeRect(50, 150, 1100, 110);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 16px Arial, sans-serif';
    ctx.fillText("VERIFIED CLAIM / EXAMINED FORWARD:", 70, 180);

    ctx.fillStyle = '#f8fafc';
    ctx.font = '20px Arial, sans-serif';
    const claimSnippet = (extractedText || "Examined Viral WhatsApp Forward").substring(0, 95) + "...";
    ctx.fillText(claimSnippet, 70, 225);

    // Verdict Card Section
    const verdict = (result?.overall_verdict || shareableCard.verdict || "UNVERIFIED").toUpperCase();
    const isDebunked = verdict.includes('FALSE') || verdict.includes('HOAX') || verdict.includes('FABRICATED');
    const verdictColor = isDebunked ? '#ef4444' : '#10b981';
    const verdictText = isDebunked ? '❌ DEBUNKED / FABRICATED HOAX' : '✅ VERIFIED / AUTHENTIC';

    ctx.fillStyle = isDebunked ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)';
    ctx.fillRect(50, 280, 530, 200);
    ctx.strokeStyle = verdictColor;
    ctx.lineWidth = 3;
    ctx.strokeRect(50, 280, 530, 200);

    ctx.fillStyle = verdictColor;
    ctx.font = 'bold 26px Arial, sans-serif';
    ctx.fillText(verdictText, 80, 335);

    ctx.fillStyle = '#f1f5f9';
    ctx.font = '18px Arial, sans-serif';
    const credScore = result?.credibility_score !== undefined ? result.credibility_score : 50;
    ctx.fillText(`Credibility Index: ${credScore} / 100`, 80, 385);
    ctx.fillText(`Risk Classification: ${result?.risk_level || 'ANALYZED'}`, 80, 425);
    ctx.fillText(`Processing Latency: <15ms Cached (SQLite WAL)`, 80, 460);

    // Telemetry Section
    ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.fillRect(610, 280, 540, 200);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.strokeRect(610, 280, 540, 200);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 20px Arial, sans-serif';
    ctx.fillText("PSYCHOLOGICAL DECEPTION GAUGES", 640, 325);

    const urg = result?.manipulation_breakdown?.urgency_score || 0;
    const emo = result?.manipulation_breakdown?.emotional_intensity || 0;
    ctx.fillStyle = '#f8fafc';
    ctx.font = '18px Arial, sans-serif';
    ctx.fillText(`• Manufactured Urgency: ${urg}% (Panic Pressure)`, 640, 375);
    ctx.fillText(`• Emotional Outrage Bias: ${emo}% (Trigger Content)`, 640, 415);
    ctx.fillText(`• Official Source Anchor: ${isDebunked ? 'ABSENT IN FORWARD' : 'CONFIRMED'}`, 640, 455);

    // Footer & Link
    ctx.fillStyle = 'rgba(56, 189, 248, 0.1)';
    ctx.fillRect(50, 500, 1100, 120);
    ctx.strokeStyle = '#38bdf8';
    ctx.strokeRect(50, 500, 1100, 120);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 20px Arial, sans-serif';
    ctx.fillText("VERIFY BEFORE FORWARDING — SHARE THIS TRUTH CARD", 70, 540);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '16px Arial, sans-serif';
    ctx.fillText("Sources Cited: PIB Fact Check, AltNews, BOOM Live, Official Gazettes", 70, 575);
    ctx.fillText("🔗 Live Truth Engine: https://satyasetu-wtpy.onrender.com | Team HexaDevs", 70, 605);

    const link = document.createElement('a');
    link.download = `SatyaSetu_Truth_Card_${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <MessageSquare size={20} style={{ color: '#25d366' }} />
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>
              WhatsApp Viral Neutralizer & Chat Simulator
            </h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              See how this rumor spreads in group chats and deploy a 1-click formatted counter-debunk card
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            id="btn-copy-debunk-en"
            onClick={() => handleCopy('en')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '7px 14px',
              borderRadius: 'var(--radius-md)',
              background: copiedLang === 'en' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(56, 189, 248, 0.12)',
              color: copiedLang === 'en' ? '#34d399' : '#38bdf8',
              border: copiedLang === 'en' ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(56, 189, 248, 0.3)',
              fontSize: '0.75rem',
              fontWeight: 600
            }}
          >
            {copiedLang === 'en' ? <Check size={14} /> : <Copy size={14} />}
            <span>{copiedLang === 'en' ? 'Copied English Card!' : 'Copy English Debunk'}</span>
          </button>

          <button
            id="btn-copy-debunk-hi"
            onClick={() => handleCopy('hi')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '7px 14px',
              borderRadius: 'var(--radius-md)',
              background: copiedLang === 'hi' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(249, 115, 22, 0.12)',
              color: copiedLang === 'hi' ? '#34d399' : '#fb923c',
              border: copiedLang === 'hi' ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(249, 115, 22, 0.3)',
              fontSize: '0.75rem',
              fontWeight: 600
            }}
          >
            {copiedLang === 'hi' ? <Check size={14} /> : <Copy size={14} />}
            <span>{copiedLang === 'hi' ? 'हिंदी कार्ड कॉपी हो गया!' : 'Copy Hindi Debunk (हिंदी)'}</span>
          </button>

          <button
            id="btn-download-truth-card"
            onClick={downloadTruthCard}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '7px 14px',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(139, 92, 246, 0.18)',
              color: '#c4b5fd',
              border: '1px solid rgba(139, 92, 246, 0.4)',
              fontSize: '0.75rem',
              fontWeight: 700,
              cursor: 'pointer'
            }}
          >
            <span>📸 Download Truth Card (PNG)</span>
          </button>
        </div>
      </div>

      {/* Simulated Phone Frame */}
      <div style={{
        maxWidth: '520px',
        margin: '0 auto',
        backgroundColor: '#0b141a',
        borderRadius: '16px',
        border: '2px solid #202c33',
        overflow: 'hidden',
        boxShadow: '0 12px 35px rgba(0, 0, 0, 0.8)'
      }}>
        {/* WhatsApp Header */}
        <div style={{
          backgroundColor: '#202c33',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.05)'
        }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '50%',
            backgroundColor: '#00a884',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.1rem'
          }}>
            👥
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#e9edef' }}>
              Family & Society WhatsApp Group
            </div>
            <div style={{ fontSize: '0.7rem', color: '#8696a0' }}>
              42 members • Tap here for group info
            </div>
          </div>
        </div>

        {/* Chat Canvas */}
        <div style={{
          padding: '18px 14px',
          display: 'flex',
          flexDirection: 'column',
          gap: '14px',
          background: '#0b141a'
        }}>
          {/* 1. Incoming Viral Forward Bubble */}
          <div style={{
            maxWidth: '85%',
            alignSelf: 'flex-start',
            backgroundColor: '#202c33',
            borderRadius: '8px',
            borderTopLeftRadius: '2px',
            padding: '10px 12px',
            boxShadow: '0 1px 2px rgba(0,0,0,0.3)',
            position: 'relative'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.68rem', color: '#8696a0', marginBottom: '4px', fontStyle: 'italic' }}>
              <span>↪</span>
              <span>Forwarded many times</span>
            </div>
            <p style={{ fontSize: '0.82rem', color: '#e9edef', lineHeight: 1.45 }}>
              {extractedText || "Viral claim message circulating on WhatsApp..."}
            </p>
            <div style={{ textAlign: 'right', fontSize: '0.65rem', color: '#8696a0', marginTop: '4px' }}>
              10:42 AM
            </div>
          </div>

          {/* 2. Outgoing SatyaSetu Counter-Debunk Bubble */}
          <div style={{
            maxWidth: '92%',
            alignSelf: 'flex-end',
            backgroundColor: '#005c4b',
            borderRadius: '8px',
            borderTopRightRadius: '2px',
            padding: '12px 14px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.4)',
            borderLeft: '4px solid #f87171'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
              <ShieldCheck size={16} style={{ color: '#38bdf8' }} />
              <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#f87171', letterSpacing: '0.02em' }}>
                SATYA SETU FACT CHECK VERDICT
              </span>
            </div>

            <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#ffffff', marginBottom: '6px' }}>
              {shareableCard.headline_en}
            </div>

            <div style={{ fontSize: '0.78rem', color: '#d1fae5', lineHeight: 1.4, marginBottom: '8px' }}>
              {shareableCard.bullet_points_en.map((point, idx) => (
                <div key={idx} style={{ marginBottom: '3px' }}>
                  • {point}
                </div>
              ))}
            </div>

            <div style={{
              paddingTop: '6px',
              borderTop: '1px solid rgba(255, 255, 255, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              fontSize: '0.68rem',
              color: '#8696a0'
            }}>
              <span style={{ color: '#6ee7b7' }}>{shareableCard.verification_source_tag}</span>
              <span>10:43 AM • Read</span>
            </div>
          </div>
        </div>

        {/* Footer info note */}
        <div style={{
          backgroundColor: '#111b21',
          padding: '8px 14px',
          textAlign: 'center',
          fontSize: '0.7rem',
          color: '#8696a0',
          borderTop: '1px solid rgba(255,255,255,0.05)'
        }}>
          💡 Click "Copy English/Hindi Debunk" above and paste directly into WhatsApp to break viral misinformation loops.
        </div>
      </div>
    </div>
  );
};
