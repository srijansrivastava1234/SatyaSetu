import React, { useState } from 'react';
import { CheckCircle, ShieldCheck } from './Icons';

export const VerificationChecklist = ({ customChecklist }) => {
  const defaultItems = [
    {
      id: 1,
      title: "Check for Primary Institutional Identifiers",
      desc: "Legitimate announcements from RBI, CBSE, or Ministries always contain an official Circular/Notice Reference Number and link to an authentic .gov.in or .nic.in domain."
    },
    {
      id: 2,
      title: "Diagnose Artificial Urgency & Coercion",
      desc: "If a message commands you to 'SHARE BEFORE IT GETS DELETED' or 'FORWARD TO 10 GROUPS TO PROVE PATRIOTISM', it is almost certainly a manufactured viral hoax."
    },
    {
      id: 3,
      title: "Verify on Certified Fact-Checking Portals",
      desc: "Before forwarding, enter the core keywords into factcheck.pib.gov.in or certified IFCN outlets (AltNews, BOOM, Vishvas News)."
    },
    {
      id: 4,
      title: "Perform an Emotional Gut-Check",
      desc: "Misinformation is engineered to hijack fear, religious tension, or financial panic. When you feel a sudden surge of alarm, PAUSE rather than forward."
    }
  ];

  const items = customChecklist && customChecklist.length > 0
    ? customChecklist.map((text, idx) => ({ id: idx + 1, title: `Verification Rule 0${idx + 1}`, desc: text }))
    : defaultItems;

  const [checkedIds, setCheckedIds] = useState([]);

  const toggleCheck = (id) => {
    setCheckedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
        <ShieldCheck size={20} style={{ color: '#38bdf8' }} />
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>
            Pre-Forwarding Citizen Protocol (S.A.T.Y.A. Verification Checklist)
          </h3>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Mandatory hygiene steps every user must execute before forwarding unverified media
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
        {items.map((item) => {
          const isDone = checkedIds.includes(item.id);
          return (
            <div
              key={item.id}
              onClick={() => toggleCheck(item.id)}
              className="glass-panel-interactive"
              style={{
                padding: '14px 16px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: isDone ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                border: isDone ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid var(--border-color)',
                cursor: 'pointer',
                display: 'flex',
                gap: '12px'
              }}
            >
              <div style={{
                width: '24px',
                height: '24px',
                borderRadius: '6px',
                backgroundColor: isDone ? '#10b981' : 'rgba(255, 255, 255, 0.05)',
                border: isDone ? 'none' : '1px solid #475569',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                fontSize: '0.8rem',
                flexShrink: 0
              }}>
                {isDone ? '✓' : ''}
              </div>

              <div>
                <div style={{ fontSize: '0.85rem', fontWeight: 700, color: isDone ? '#34d399' : '#f1f5f9', marginBottom: '4px' }}>
                  {item.title}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: 1.4 }}>
                  {item.desc}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
