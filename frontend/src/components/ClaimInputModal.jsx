import React, { useState } from 'react';
import { MessageSquare, ImageIcon, LinkIcon, Search, RefreshCw, Sparkles, Mic } from './Icons';

export const ClaimInputModal = ({ onVerify, loading, rawText, setRawText, scenarioId, setScenarioId }) => {
  const [activeTab, setActiveTab] = useState('text'); // 'text' | 'image' | 'url' | 'voice'
  const [urlInput, setUrlInput] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [imageBase64, setImageBase64] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recordingStatus, setRecordingStatus] = useState('');

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
      text: (activeTab === 'text' || activeTab === 'voice') ? rawText : '',
      url: activeTab === 'url' ? urlInput : '',
      image_base64: activeTab === 'image' ? imageBase64 : '',
      scenario_id: scenarioId
    });
  };

  const handleToggleVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Microphone recognition requires Google Chrome or Chromium browser.");
      return;
    }

    if (isRecording) {
      setIsRecording(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = 'hi-IN'; // Indian Hindi / English
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setIsRecording(true);
        setRecordingStatus('Listening... बोलिए (Recording WhatsApp audio)');
      };

      recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        setRawText(transcript);
        setScenarioId(null);
        setActiveTab('text');
        setIsRecording(false);
        setRecordingStatus(`Captured: "${transcript}"`);
      };

      recognition.onerror = (e) => {
        setIsRecording(false);
        setRecordingStatus(`Microphone capture error: ${e.error}`);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognition.start();
    } catch (err) {
      console.error(err);
      setIsRecording(false);
    }
  };

  const handleClear = () => {
    setRawText('');
    setUrlInput('');
    setImagePreview(null);
    setImageBase64('');
    setScenarioId(null);
    setIsRecording(false);
    setRecordingStatus('');
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
        marginBottom: '20px',
        flexWrap: 'wrap'
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

        <button
          id="tab-btn-voice"
          type="button"
          onClick={() => setActiveTab('voice')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: activeTab === 'voice' ? 'rgba(34, 197, 94, 0.15)' : 'transparent',
            border: activeTab === 'voice' ? '1px solid rgba(34, 197, 94, 0.3)' : '1px solid transparent',
            color: activeTab === 'voice' ? '#4ade80' : 'var(--text-secondary)',
            fontWeight: 600,
            fontSize: '0.85rem'
          }}
        >
          <Mic size={16} />
          🎙️ Voice Note (आवाज़)
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

        {activeTab === 'voice' && (
          <div style={{
            border: '2px dashed rgba(34, 197, 94, 0.4)',
            borderRadius: 'var(--radius-md)',
            padding: '36px 20px',
            textAlign: 'center',
            background: 'rgba(34, 197, 94, 0.04)'
          }}>
            <button
              type="button"
              onClick={handleToggleVoice}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '10px',
                padding: '12px 24px',
                borderRadius: '9999px',
                background: isRecording ? '#ef4444' : '#22c55e',
                color: '#ffffff',
                border: 'none',
                fontSize: '0.95rem',
                fontWeight: 700,
                cursor: 'pointer',
                boxShadow: isRecording ? '0 0 20px rgba(239, 68, 68, 0.6)' : '0 0 15px rgba(34, 197, 94, 0.4)'
              }}
            >
              <Mic size={20} />
              {isRecording ? "Stop Recording (रोकें)" : "Speak / बोलकर रिकॉर्ड करें"}
            </button>
            <p style={{ marginTop: '14px', fontSize: '0.85rem', color: isRecording ? '#ef4444' : 'var(--text-secondary)' }}>
              {recordingStatus || "Click the microphone and speak a WhatsApp forward or rumor in Hindi or English."}
            </p>
            {rawText && (
              <div style={{
                marginTop: '16px',
                padding: '12px',
                background: 'rgba(15, 23, 42, 0.6)',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                fontSize: '0.9rem',
                color: '#f8fafc',
                textAlign: 'left'
              }}>
                <strong>Transcribed Speech:</strong> "{rawText}"
              </div>
            )}
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
              borderRadius: 'var(--radius-sm)',
              background: loading ? '#30363d' : 'var(--color-brand)',
              color: '#ffffff',
              fontWeight: 600,
              fontSize: '0.9rem',
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
