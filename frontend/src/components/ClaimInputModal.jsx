import React, { useState } from 'react';
import { MessageSquare, ImageIcon, LinkIcon, Search, RefreshCw, Sparkles } from './Icons';

export const ClaimInputModal = ({ onVerify, loading, rawText, setRawText, scenarioId, setScenarioId }) => {
  const [activeTab, setActiveTab] = useState('text'); // 'text' | 'image' | 'url'
  const [urlInput, setUrlInput] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [imageBase64, setImageBase64] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
        setImageBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (loading) return;

    if (activeTab === 'text' && !rawText.trim()) return;
    if (activeTab === 'url' && !urlInput.trim()) return;
    if (activeTab === 'image' && !imageBase64) return;

    onVerify({
      text: activeTab === 'text' ? rawText : '',
      url: activeTab === 'url' ? urlInput : '',
      image_base64: activeTab === 'image' ? imageBase64 : '',
      scenario_id: scenarioId
    });
  };

  const handleClear = () => {
    setRawText('');
    setUrlInput('');
    setImagePreview(null);
    setImageBase64('');
    setScenarioId(null);
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '28px' }}>
      {/* Tab Switcher */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        borderBottom: '1px solid var(--border-color)',
        paddingBottom: '14px',
        marginBottom: '20px'
      }}>
        <button
          id="tab-btn-text"
          type="button"
          onClick={() => setActiveTab('text')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: activeTab === 'text' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
            border: activeTab === 'text' ? '1px solid rgba(56, 189, 248, 0.3)' : '1px solid transparent',
            color: activeTab === 'text' ? '#38bdf8' : 'var(--text-secondary)',
            fontWeight: 600,
            fontSize: '0.85rem'
          }}
        >
          <MessageSquare size={16} />
          WhatsApp Message / Text
        </button>

        <button
          id="tab-btn-image"
          type="button"
          onClick={() => setActiveTab('image')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: activeTab === 'image' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
            border: activeTab === 'image' ? '1px solid rgba(56, 189, 248, 0.3)' : '1px solid transparent',
            color: activeTab === 'image' ? '#38bdf8' : 'var(--text-secondary)',
            fontWeight: 600,
            fontSize: '0.85rem'
          }}
        >
          <ImageIcon size={16} />
          Screenshot / Poster OCR
        </button>

        <button
          id="tab-btn-url"
          type="button"
          onClick={() => setActiveTab('url')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: activeTab === 'url' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
            border: activeTab === 'url' ? '1px solid rgba(56, 189, 248, 0.3)' : '1px solid transparent',
            color: activeTab === 'url' ? '#38bdf8' : 'var(--text-secondary)',
            fontWeight: 600,
            fontSize: '0.85rem'
          }}
        >
          <LinkIcon size={16} />
          Social / News Link
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {activeTab === 'text' && (
          <div>
            <textarea
              id="input-claim-text"
              rows={4}
              value={rawText}
              onChange={(e) => {
                setRawText(e.target.value);
                setScenarioId(null);
              }}
              placeholder="Paste suspicious WhatsApp forward, viral message, or claim text here (e.g. 'UNESCO declared Indian national anthem best in the world...')"
              style={{
                width: '100%',
                padding: '14px 18px',
                fontSize: '0.95rem',
                lineHeight: 1.6,
                resize: 'vertical'
              }}
            />
          </div>
        )}

        {activeTab === 'image' && (
          <div style={{
            border: '2px dashed var(--border-color)',
            borderRadius: 'var(--radius-md)',
            padding: '30px',
            textAlign: 'center',
            background: 'rgba(10, 15, 26, 0.4)',
            position: 'relative'
          }}>
            {imagePreview ? (
              <div>
                <img
                  src={imagePreview}
                  alt="Screenshot Preview"
                  style={{ maxHeight: '220px', borderRadius: '8px', marginBottom: '12px', border: '1px solid var(--border-color)' }}
                />
                <div>
                  <button
                    type="button"
                    onClick={() => { setImagePreview(null); setImageBase64(''); }}
                    style={{ fontSize: '0.8rem', color: '#f87171', background: 'transparent' }}
                  >
                    Remove Image
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <ImageIcon size={38} className="" style={{ color: 'var(--color-brand)', margin: '0 auto 12px auto' }} />
                <p style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '6px' }}>
                  Upload or drop WhatsApp forward screenshot / newspaper clipping
                </p>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
                  SatyaSetu extracts text via Vision OCR and passes extracted claims to the verification engine
                </p>
                <label
                  htmlFor="file-upload"
                  style={{
                    display: 'inline-block',
                    padding: '8px 18px',
                    borderRadius: 'var(--radius-md)',
                    background: 'rgba(56, 189, 248, 0.15)',
                    color: '#38bdf8',
                    border: '1px solid rgba(56, 189, 248, 0.3)',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  Browse Image
                </label>
                <input
                  id="file-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  style={{ display: 'none' }}
                />
              </div>
            )}
          </div>
        )}

        {activeTab === 'url' && (
          <div>
            <div style={{ position: 'relative' }}>
              <input
                id="input-claim-url"
                type="url"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://twitter.com/... or https://news-source.com/article..."
                style={{
                  width: '100%',
                  padding: '14px 18px',
                  fontSize: '0.95rem'
                }}
              />
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '8px' }}>
              Extracts title and content body to identify claims and check IFCN ClaimReview records.
            </p>
          </div>
        )}

        {/* Action Controls */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginTop: '16px'
        }}>
          <button
            type="button"
            onClick={handleClear}
            style={{
              padding: '8px 14px',
              borderRadius: 'var(--radius-md)',
              background: 'transparent',
              color: 'var(--text-muted)',
              fontSize: '0.8rem'
            }}
          >
            Clear Input
          </button>

          <button
            id="btn-verify-claim"
            type="submit"
            disabled={loading}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              padding: '12px 28px',
              borderRadius: 'var(--radius-md)',
              background: loading ? '#334155' : 'linear-gradient(135deg, #38bdf8 0%, #2563eb 100%)',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '0.95rem',
              boxShadow: loading ? 'none' : '0 4px 20px rgba(56, 189, 248, 0.35)',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? (
              <>
                <RefreshCw size={18} className="" style={{ animation: 'spin 1s linear infinite' }} />
                <span>Interrogating Claim Database...</span>
              </>
            ) : (
              <>
                <Sparkles size={18} />
                <span>Verify Authenticity & Dissect Manipulation</span>
              </>
            )}
          </button>
        </div>
      </form>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};
