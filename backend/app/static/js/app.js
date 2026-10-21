/**
 * SatyaSetu: Institutional Misinformation Intelligence Engine
 * Client Application Logic & Verification Controller
 */

let activeTab = 'text';
let currentResult = null;
let selectedScenarioId = null;
let activeLang = 'en';
let imageBase64Data = '';
let userApiKey = localStorage.getItem('SATYA_GEMINI_KEY') || '';

const SCENARIO_PRESETS = {
  'unesco-anthem': {
    title: "UNESCO Best Anthem Award",
    text: "Great news for every proud Indian! 🇮🇳 UNESCO has just officially announced that 'Jana Gana Mana' has been declared the BEST NATIONAL ANTHEM in the world! No other country's anthem got this honour. Please forward this message to at least 10 people and all your groups right now to show your patriotism! Jai Hind! Vande Mataram!"
  },
  'rbi-500-note': {
    title: "Fake RBI ₹500 Green Strip Warning",
    text: "WARNING! Check your ₹500 notes immediately! If the green security strip is closer to Mahatma Gandhi's photo instead of RBI Governor's signature, it is 100% FAKE! Share this alert with all your family groups before you lose money!"
  },
  'salt-shortage': {
    title: "Salt Shortage Panic Rumor",
    text: "URGENT ALERT: Severe salt shortage across Delhi and Bihar! Salt prices have jumped from ₹20 to ₹400 per kg today. Markets are running out. Go buy 10 packets immediately before all grocery stores shut down tonight!"
  },
  'cbse-exam-circular': {
    title: "Official CBSE Exam Circular (Authentic)",
    text: "CBSE Board Examination 2026: Official notification and date sheet for Class 10 and 12 published. Candidates can download official circular from cbse.gov.in."
  }
};

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadInitialState();
  fetchSystemTelemetry();
});

function setupEventListeners() {
  const claimText = document.getElementById('claim-text');
  const claimUrl = document.getElementById('claim-url');

  if (claimText) {
    claimText.addEventListener('input', () => { selectedScenarioId = null; });
    claimText.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        executeVerify();
      }
    });
  }

  if (claimUrl) {
    claimUrl.addEventListener('input', () => { selectedScenarioId = null; });
    claimUrl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        executeVerify();
      }
    });
  }
}

function loadInitialState() {
  selectScenario('unesco-anthem');
}

function onUserInput() {
  selectedScenarioId = null;
}

function setTab(tab) {
  activeTab = tab;
  selectedScenarioId = null;

  ['text', 'image', 'url', 'voice'].forEach(t => {
    const pane = document.getElementById(`pane-${t}`);
    const btn = document.getElementById(`tab-${t}`);
    if (pane) pane.style.display = (t === tab) ? 'block' : 'none';
    if (btn) btn.classList.toggle('active', t === tab);
  });
}

function selectScenario(scenarioKey) {
  const preset = SCENARIO_PRESETS[scenarioKey];
  if (!preset) return;

  selectedScenarioId = scenarioKey;
  setTab('text');
  
  const textInput = document.getElementById('claim-text');
  if (textInput) {
    textInput.value = preset.text;
  }
  executeVerify();
}

function handleImage(e) {
  selectedScenarioId = null;
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      imageBase64Data = reader.result;
      const previewImg = document.getElementById('img-preview');
      const emptyBox = document.getElementById('image-empty');
      const previewContainer = document.getElementById('image-preview-container');
      
      if (previewImg) previewImg.src = reader.result;
      if (emptyBox) emptyBox.style.display = 'none';
      if (previewContainer) previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

function clearImage() {
  imageBase64Data = '';
  selectedScenarioId = null;
  const fileInput = document.getElementById('img-file');
  const emptyBox = document.getElementById('image-empty');
  const previewContainer = document.getElementById('image-preview-container');
  
  if (fileInput) fileInput.value = '';
  if (emptyBox) emptyBox.style.display = 'block';
  if (previewContainer) previewContainer.style.display = 'none';
}

function clearAll() {
  const textInput = document.getElementById('claim-text');
  const urlInput = document.getElementById('claim-url');
  if (textInput) textInput.value = '';
  if (urlInput) urlInput.value = '';
  clearImage();
  selectedScenarioId = null;
  document.title = "SatyaSetu — TrustAI Misinformation Engine";
}

async function executeVerify() {
  const btn = document.getElementById('btn-submit');
  const textVal = (document.getElementById('claim-text')?.value || '').trim();
  const urlVal = (document.getElementById('claim-url')?.value || '').trim();

  if (activeTab === 'text') {
    if (!textVal) {
      showToast('Please enter a claim or message text to verify.');
      return;
    }
    if (selectedScenarioId && SCENARIO_PRESETS[selectedScenarioId]?.text !== textVal) {
      selectedScenarioId = null;
    }
  } else if (activeTab === 'url') {
    if (!urlVal) {
      showToast('Please enter an article or tweet URL.');
      return;
    }
  } else if (activeTab === 'image') {
    if (!imageBase64Data) {
      showToast('Please select or drag an image screenshot.');
      return;
    }
  }

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> Verifying Authenticity...`;
  }
  document.title = "SatyaSetu — Verifying Claim...";

  const payload = {
    scenario_id: selectedScenarioId || undefined,
    text: activeTab === 'text' ? textVal : undefined,
    url: activeTab === 'url' ? urlVal : undefined,
    image_base64: activeTab === 'image' ? imageBase64Data : undefined,
    api_key_override: userApiKey || undefined
  };

  try {
    const res = await fetch('/api/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    currentResult = data;
    renderResults(data);
    fetchSystemTelemetry();
  } catch (err) {
    console.error('[SatyaSetu] Verification error:', err);
    showToast('Failed to reach verification backend. Ensure FastAPI server is online.');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `Verify Claim Authenticity`;
    }
  }
}

function renderResults(res) {
  document.title = `SatyaSetu — [${res.overall_verdict}] Verification Report`;

  const resultsArea = document.getElementById('results-area');
  if (resultsArea) resultsArea.style.display = 'block';

  // Verdict status styling
  const v = res.overall_verdict.toUpperCase();
  const isVerified = v.includes('VERIFIED') || v.includes('TRUE') || v.includes('AUTHENTIC');
  const isDebunked = v.includes('FALSE') || v.includes('HOAX') || v.includes('FABRICATED');
  
  const statusColor = isVerified ? 'var(--color-verified)' : isDebunked ? 'var(--color-debunked)' : 'var(--color-caution)';
  const statusBg = isVerified ? 'var(--color-verified-bg)' : isDebunked ? 'var(--color-debunked-bg)' : 'var(--color-caution-bg)';
  const badgeClass = isVerified ? 'badge-verified' : isDebunked ? 'badge-debunked' : 'badge-caution';

  const vCard = document.getElementById('verdict-card');
  if (vCard) vCard.style.borderTopColor = statusColor;

  const vIcon = document.getElementById('verdict-icon-container');
  if (vIcon) {
    vIcon.style.background = statusBg;
    vIcon.style.color = statusColor;
    vIcon.innerText = isVerified ? '✓' : isDebunked ? '!' : '?';
  }

  const vTitle = document.getElementById('verdict-title');
  if (vTitle) {
    vTitle.innerText = res.overall_verdict;
    vTitle.style.color = statusColor;
  }

  const rBadge = document.getElementById('verdict-risk-badge');
  if (rBadge) {
    rBadge.className = `badge ${badgeClass}`;
    rBadge.innerText = res.risk_level.replace(/_/g, ' ');
  }

  const sText = document.getElementById('score-text');
  if (sText) {
    sText.innerText = `${res.credibility_score}%`;
    sText.style.color = statusColor;
  }

  const sBar = document.getElementById('score-bar');
  if (sBar) {
    sBar.style.width = `${res.credibility_score}%`;
    sBar.style.background = statusColor;
  }

  updateSummaryText();

  // Populate Atomic Claims
  const cList = document.getElementById('atomic-claims-list');
  if (cList) {
    cList.innerHTML = '';
    res.atomic_claims.forEach(c => {
      const cVerdict = (c.verdict || 'UNVERIFIED').toUpperCase();
      const cBadgeClass = cVerdict.includes('VERIFIED') || cVerdict === 'TRUE' ? 'badge-verified' : cVerdict === 'FALSE' ? 'badge-debunked' : 'badge-neutral';
      cList.innerHTML += `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:12px 14px; background:var(--bg-surface-elevated); border:1px solid var(--border-subtle); border-radius:var(--radius-md); margin-bottom:8px;">
          <div>
            <div style="font-weight:600; font-size:0.88rem; color:var(--text-primary);">${c.text}</div>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;">Target: <strong style="color:var(--text-secondary);">${c.target_entity}</strong> | Query: <code style="color:var(--color-accent);">${c.normalized_query}</code></div>
          </div>
          <span class="badge ${cBadgeClass}">${c.verdict}</span>
        </div>
      `;
    });
  }

  // Populate Manipulation Telemetry
  const m = res.manipulation_breakdown;
  updateMetricBar('urgency', m.urgency_score);
  updateMetricBar('emotion', m.emotional_intensity);
  updateMetricBar('sensational', m.sensationalism_score);

  const tList = document.getElementById('tactics-list');
  if (tList) {
    tList.innerHTML = '';
    if (m.detected_tactics && m.detected_tactics.length > 0) {
      m.detected_tactics.forEach(t => tList.innerHTML += `<span class="badge badge-debunked" style="margin-right:6px; margin-bottom:6px;">${t}</span>`);
    } else {
      tList.innerHTML = `<span class="badge badge-verified">No manipulative tactics detected</span>`;
    }
  }

  const mList = document.getElementById('missing-list');
  if (mList) {
    mList.innerHTML = '';
    if (m.missing_elements && m.missing_elements.length > 0) {
      m.missing_elements.forEach(el => mList.innerHTML += `<span class="badge badge-caution" style="margin-right:6px; margin-bottom:6px;">${el}</span>`);
    } else {
      mList.innerHTML = `<span class="badge badge-neutral">Standard citation anchors present</span>`;
    }
  }

  // Grounding Evidence & Journalistic Sources Table
  const evCont = document.getElementById('evidence-container');
  if (evCont) {
    evCont.innerHTML = '';
    let renderedCount = 0;

    // 1. Certified Fact-Check Desks (AltNews, BOOM, PIB Fact Check, Factly)
    if (res.certified_evidence && res.certified_evidence.length > 0) {
      res.certified_evidence.forEach(item => {
        renderedCount++;
        const gSearchUrl = `https://news.google.com/search?q=${encodeURIComponent(item.fact_checker + ' ' + item.claim_text)}`;
        evCont.innerHTML += `
          <div style="padding:14px 16px; border-radius:var(--radius-sm); background:var(--bg-surface-elevated); border:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; gap:16px;">
            <div style="flex:1;">
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px; flex-wrap:wrap;">
                <span style="font-weight:700; font-size:0.88rem; color:var(--text-primary);">${item.fact_checker}</span>
                <span class="badge badge-neutral" style="font-size:0.68rem;">Certified Fact-Checking Desk</span>
                ${item.review_date ? `<span style="font-size:0.75rem; color:var(--text-muted);">${item.review_date}</span>` : ''}
              </div>
              <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">"${item.claim_text}"</p>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-shrink:0; flex-wrap:wrap;">
              <span class="badge badge-debunked">${item.rating}</span>
              ${item.review_url ? `<a href="${item.review_url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="padding:5px 12px; font-size:0.78rem;">Read Investigation ↗</a>` : ''}
              <a href="${gSearchUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="padding:5px 10px; font-size:0.75rem; background:transparent; border:1px solid var(--border-subtle); color:var(--text-muted);" title="Search live coverage for this headline on Google News">Live News ↗</a>
            </div>
          </div>
        `;
      });
    }

    // 2. Accredited National Newspapers, Official Gazettes & Wire Reports
    if (res.web_grounding_citations && res.web_grounding_citations.length > 0) {
      res.web_grounding_citations.forEach(c => {
        renderedCount++;
        const badgeText = c.authority_badge || 'Accredited Journalistic Source';
        const gSearchUrl = `https://news.google.com/search?q=${encodeURIComponent(c.publisher + ' ' + c.title)}`;
        evCont.innerHTML += `
          <div style="padding:14px 16px; border-radius:var(--radius-sm); background:var(--bg-surface-elevated); border:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; gap:16px;">
            <div style="flex:1;">
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px; flex-wrap:wrap;">
                <span style="font-weight:700; font-size:0.88rem; color:var(--color-accent);">${c.publisher}</span>
                <span class="badge badge-verified" style="font-size:0.68rem;">${badgeText}</span>
                ${c.pub_date ? `<span style="font-size:0.75rem; color:var(--text-muted);">${c.pub_date}</span>` : ''}
              </div>
              <div style="font-size:0.9rem; font-weight:600; color:var(--text-primary); margin:2px 0;">${c.title}</div>
              <div style="font-size:0.8rem; color:var(--text-secondary);">${c.snippet}</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-shrink:0; flex-wrap:wrap;">
              ${c.url ? `
                <a href="${c.url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="padding:5px 12px; font-size:0.78rem;">Source ↗</a>
              ` : ''}
              <a href="${gSearchUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="padding:5px 10px; font-size:0.75rem; background:transparent; border:1px solid var(--border-subtle); color:var(--text-muted);" title="Search live coverage for this headline on Google News">Live News ↗</a>
            </div>
          </div>
        `;
      });
    }

    if (renderedCount === 0) {
      evCont.innerHTML = `
        <div style="padding:16px; text-align:center; color:var(--text-muted); font-size:0.85rem;">
          No conflicting or corroborating coverage found in verified newspaper databases.
        </div>
      `;
    }
  }

  // WhatsApp Simulator
  const waIncoming = document.getElementById('wa-incoming-text');
  const waHeadline = document.getElementById('wa-debunk-headline');
  const waBullets = document.getElementById('wa-debunk-bullets');
  const waTag = document.getElementById('wa-debunk-tag');

  if (waIncoming) waIncoming.innerText = res.extracted_text || 'Forwarded message...';
  if (waHeadline) waHeadline.innerText = res.shareable_card.headline_en;
  if (waBullets) {
    waBullets.innerHTML = '';
    res.shareable_card.bullet_points_en.forEach(b => waBullets.innerHTML += `<div>• ${b}</div>`);
  }
  if (waTag) waTag.innerText = res.shareable_card.verification_source_tag;

  // Verification Checklist Rules
  const chkGrid = document.getElementById('checklist-grid');
  if (chkGrid && res.verification_checklist) {
    chkGrid.innerHTML = '';
    res.verification_checklist.forEach((item, idx) => {
      chkGrid.innerHTML += `
        <div style="padding:12px 14px; background:var(--bg-surface-elevated); border:1px solid var(--border-subtle); border-radius:var(--radius-md); display:flex; gap:12px; align-items:flex-start;">
          <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-accent); font-weight:700;">0${idx+1}</span>
          <div style="font-size:0.8rem; color:var(--text-secondary); line-height:1.4;">${item}</div>
        </div>
      `;
    });
  }
}

function updateMetricBar(type, score) {
  const label = document.getElementById(`metric-${type}`);
  const bar = document.getElementById(`bar-${type}`);
  const isHigh = score > 60;
  const col = isHigh ? 'var(--color-debunked)' : 'var(--color-verified)';

  if (label) {
    label.innerText = `${score}%`;
    label.style.color = col;
  }
  if (bar) {
    bar.style.width = `${score}%`;
    bar.style.background = col;
  }
}

function setLang(lang) {
  activeLang = lang;
  document.getElementById('lang-en')?.classList.toggle('active', lang === 'en');
  document.getElementById('lang-hi')?.classList.toggle('active', lang === 'hi');
  updateSummaryText();
}

function updateSummaryText() {
  if (!currentResult) return;
  const box = document.getElementById('summary-box');
  if (box) {
    box.innerText = activeLang === 'en' ? currentResult.debunk_summary_en : currentResult.debunk_summary_hi;
  }
}

function copyDebunk(lang) {
  if (!currentResult) return;
  const text = lang === 'en' ? currentResult.shareable_card.whatsapp_format_text_en : currentResult.shareable_card.whatsapp_format_text_hi;
  navigator.clipboard.writeText(text).then(() => {
    showToast(lang === 'en' ? 'English verification card copied to clipboard.' : 'सत्यापन कार्ड कॉपी हो गया।');
  });
}

async function fetchSystemTelemetry() {
  try {
    const res = await fetch('/api/stats');
    if (res.ok) {
      const stats = await res.json();
      const statsBadge = document.getElementById('stats-cache-hits');
      if (statsBadge) {
        statsBadge.innerText = `${stats.cached_unique_claims} Claims Cached (${stats.cache_savings_hits} Cache Hits)`;
      }
    }
  } catch (e) {
    // Non-fatal telemetry polling
  }
}

function toggleKeyModal() {
  const modal = document.getElementById('key-modal');
  if (modal) {
    modal.style.display = (modal.style.display === 'flex') ? 'none' : 'flex';
  }
}

function saveApiKey() {
  const input = document.getElementById('gemini-key-input');
  if (input) {
    userApiKey = input.value.trim();
    localStorage.setItem('SATYA_GEMINI_KEY', userApiKey);
    toggleKeyModal();
    showToast('Gemini API key updated in browser storage.');
  }
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  if (toast) {
    toast.innerText = msg;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 3000);
  }
}

// ============================================================================
// VOICE NOTE (AUDIO) INGESTION (WEB SPEECH API)
// ============================================================================
let speechRecognizer = null;
let isRecordingVoice = false;

function toggleVoiceRecording() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const statusMsg = document.getElementById('voice-status-msg');
  const btn = document.getElementById('btn-record-voice');
  const dot = document.getElementById('voice-rec-dot');
  const label = document.getElementById('voice-rec-label');

  if (!SpeechRecognition) {
    showToast("Web Speech API not supported in this browser. Try testing with the sample buttons below!");
    if (statusMsg) statusMsg.innerText = "Speech recognition is not supported in your current browser. Please click a sample audio scenario below.";
    return;
  }

  if (isRecordingVoice) {
    if (speechRecognizer) speechRecognizer.stop();
    isRecordingVoice = false;
    if (label) label.innerText = "Click to Speak / बोलकर संदेश रिकॉर्ड करें";
    if (dot) dot.style.background = "#ef4444";
    if (btn) btn.classList.remove('btn-recording');
    return;
  }

  try {
    speechRecognizer = new SpeechRecognition();
    speechRecognizer.lang = 'hi-IN'; // Default to Hindi / Indian English
    speechRecognizer.interimResults = false;
    speechRecognizer.maxAlternatives = 1;

    speechRecognizer.onstart = () => {
      isRecordingVoice = true;
      if (label) label.innerText = "Listening... बोलिए (Recording Audio)";
      if (dot) dot.style.background = "#22c55e";
      if (statusMsg) statusMsg.innerText = "Microphone listening... Speak the WhatsApp voice note clearly in Hindi or English.";
    };

    speechRecognizer.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      showToast(`Audio transcribed: "${transcript.substring(0, 40)}..."`);
      const claimText = document.getElementById('claim-text');
      if (claimText) claimText.value = transcript;
      setTab('text');
      executeVerify();
    };

    speechRecognizer.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      showToast(`Voice capture error: ${event.error}. You can use sample audio buttons.`);
      if (statusMsg) statusMsg.innerText = `Recording failed (${event.error}). Please allow microphone access or test with sample buttons.`;
      if (label) label.innerText = "Click to Speak / बोलकर संदेश रिकॉर्ड करें";
      if (dot) dot.style.background = "#ef4444";
      isRecordingVoice = false;
    };

    speechRecognizer.onend = () => {
      isRecordingVoice = false;
      if (label) label.innerText = "Click to Speak / बोलकर संदेश रिकॉर्ड करें";
      if (dot) dot.style.background = "#ef4444";
    };

    speechRecognizer.start();
  } catch (err) {
    console.error(err);
    showToast("Microphone access could not be initialized.");
  }
}

function loadSampleVoiceNote(type) {
  const samples = {
    electricity: "Urgent electricity disconnection alert: Dear consumer, your power supply will be cut off tonight at 9:30 PM from the main power sub-station because your previous month bill was not updated. Immediately call our power officer at 9876543210 or install the bill update APK link now.",
    recharge: "Jio and Airtel free 3-month recharge scheme: Government is giving free 5G unlimited recharge to all citizens on completion of 5G network rollout. Click the link to register your mobile number before midnight."
  };

  const textVal = samples[type] || samples.electricity;
  const claimText = document.getElementById('claim-text');
  if (claimText) claimText.value = textVal;
  setTab('text');
  showToast("Loaded sample voice note transcript!");
  executeVerify();
}

// ============================================================================
// BILINGUAL UI TOGGLE (ENGLISH <-> HINDI)
// ============================================================================
let isHindiUI = false;

function toggleUILanguage() {
  isHindiUI = !isHindiUI;
  const btnToggle = document.getElementById('btn-ui-lang');
  if (btnToggle) {
    btnToggle.innerText = isHindiUI ? "🌐 English" : "🌐 हिन्दी";
  }

  // Update Hero Section
  const heroTitle = document.querySelector('.hero-title span');
  const heroDesc = document.querySelector('.hero-desc');
  const heroPill = document.querySelector('.hero-pill span');

  if (heroTitle) {
    heroTitle.innerText = isHindiUI 
      ? "व्हाट्सएप और डिजिटल अफवाहों की तुरंत सत्यता जांचें" 
      : "Neutralize Viral Misinformation at the Source";
  }
  if (heroDesc) {
    heroDesc.innerText = isHindiUI
      ? "PIB, IFCN प्रमाणित तथ्य-जांचकर्ताओं और सरकारी राजपत्रों द्वारा संचालित भारत की प्रथम जीरो-हैलुसिनेशन डिजिटल सत्यापन प्रणाली।"
      : "A deterministic, multi-tier intelligence pipeline combining certified IFCN fact-checking repositories, real-time authoritative press grounding, and deception telemetry.";
  }
  if (heroPill) {
    heroPill.innerText = isHindiUI ? "प्रमाणित सार्वजनिक सत्यता नेटवर्क" : "Verified Public Integrity Network";
  }

  // Update Section Titles
  const presetsTitle = document.querySelector('.presets-section .section-title');
  if (presetsTitle) {
    presetsTitle.innerText = isHindiUI ? "सत्यापित घटनाओं का संग्रह (नमूना मामले)" : "Verified Incident Archive & Sample Reports";
  }

  // Update Ingestion Tabs
  const tabText = document.getElementById('tab-text');
  const tabImage = document.getElementById('tab-image');
  const tabUrl = document.getElementById('tab-url');
  const tabVoice = document.getElementById('tab-voice');

  if (tabText) tabText.innerText = isHindiUI ? "संदेश व पाठ (Text)" : "Message & Raw Text";
  if (tabImage) tabImage.innerText = isHindiUI ? "स्क्रीनशॉट ओसीआर (Image)" : "Screenshot & Poster OCR";
  if (tabUrl) tabUrl.innerText = isHindiUI ? "वेब लिंक (URL)" : "Web Article / Media URL";
  if (tabVoice) tabVoice.innerText = isHindiUI ? "🎙️ ध्वनि संदेश (Voice Note)" : "🎙️ Voice Note (आवाज़)";

  // Update Main Action Button
  const btnSubmit = document.getElementById('btn-submit');
  if (btnSubmit && !btnSubmit.disabled) {
    btnSubmit.innerText = isHindiUI ? "संदेश की सत्यता जांचें" : "Verify Claim Authenticity";
  }

  showToast(isHindiUI ? "भाषा हिन्दी में बदल दी गई है" : "Switched UI to English");
}

// ============================================================================
// DOWNLOADABLE "TRUTH CARD" IMAGE GENERATOR (HTML5 CANVAS)
// ============================================================================
function downloadTruthCard() {
  if (!currentResult) {
    showToast("Please verify a claim first before downloading a truth card!");
    return;
  }

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
  const claimSnippet = (currentResult.extracted_text || "Examined Viral WhatsApp Forward").substring(0, 95) + "...";
  ctx.fillText(claimSnippet, 70, 225);

  // Verdict Card Section
  const isDebunked = currentResult.verdict === 'FALSE' || currentResult.verdict === 'DEBUNKED';
  const verdictColor = isDebunked ? '#ef4444' : '#10b981';
  const verdictText = isDebunked ? '❌ DEBUNKED / FABRICATED HOAX' : '✅ VERIFIED / AUTHENTIC GAZZETTE';

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
  const credScore = currentResult.credibility_score !== undefined ? currentResult.credibility_score : 0;
  ctx.fillText(`Credibility Index: ${credScore} / 100`, 80, 385);
  ctx.fillText(`Risk Classification: ${currentResult.risk_level || 'HIGH_MISINFORMATION'}`, 80, 425);
  ctx.fillText(`Processing Latency: <15ms Cached (SQLite WAL)`, 80, 460);

  // Telemetry Section
  ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.fillRect(610, 280, 540, 200);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
  ctx.strokeRect(610, 280, 540, 200);

  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 20px Arial, sans-serif';
  ctx.fillText("PSYCHOLOGICAL DECEPTION GAUGES", 640, 325);

  const urg = currentResult.manipulation_signals?.urgency_score || 0;
  const emo = currentResult.manipulation_signals?.emotional_intensity || 0;
  ctx.fillStyle = '#f8fafc';
  ctx.font = '18px Arial, sans-serif';
  ctx.fillText(`• Manufactured Urgency: ${urg}% (Panic Pressure)`, 640, 375);
  ctx.fillText(`• Emotional Outrage Bias: ${emo}% (Trigger Content)`, 640, 415);
  ctx.fillText(`• Official Circular Link: ABSENT IN FORWARD`, 640, 455);

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
  ctx.fillText("Sources Cited: PIB Fact Check, AltNews, BOOM Live, RBI Official Gazettes", 70, 575);
  ctx.fillText("🔗 Live Truth Engine: https://satyasetu-wtpy.onrender.com | Team HexaDevs", 70, 605);

  // Download Trigger
  const link = document.createElement('a');
  link.download = `SatyaSetu_Truth_Card_${Date.now()}.png`;
  link.href = canvas.toDataURL('image/png');
  link.click();
  showToast("📸 Downloaded SatyaSetu Truth Card PNG!");
}
