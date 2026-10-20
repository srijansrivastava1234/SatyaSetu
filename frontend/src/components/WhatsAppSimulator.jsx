import React, { useState } from 'react';
import { MessageSquare, Copy, Check, Share2, ShieldCheck } from './Icons';

export const WhatsAppSimulator = ({ shareableCard, extractedText }) => {
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
          background: 'radial-gradient(circle, #0b141a 0%, #080f14 100%)'
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
