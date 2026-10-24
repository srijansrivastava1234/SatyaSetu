// SatyaSetu Chrome Extension - Background Service Worker (Manifest V3)

const PROD_API_ENDPOINT = "https://satyasetu-wtpy.onrender.com/api/verify";
const LOCAL_API_ENDPOINT = "http://127.0.0.1:8000/api/verify";

async function getApiEndpoint() {
  try {
    const store = await chrome.storage.local.get("customApiEndpoint");
    if (store && store.customApiEndpoint) {
      return store.customApiEndpoint;
    }
  } catch (e) {}

  // Auto-detect: if local dev server is up, use it; otherwise use live production cloud
  try {
    const ping = await fetch("http://127.0.0.1:8000/api/health", { method: "GET", signal: AbortSignal.timeout(800) });
    if (ping.ok) return LOCAL_API_ENDPOINT;
  } catch (e) {}

  return PROD_API_ENDPOINT;
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "satyasetu-verify-selection",
    title: "Verify with SatyaSetu (सत्यसेतु)",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "satyasetu-verify-selection" && info.selectionText) {
    const textToVerify = info.selectionText.trim();
    
    // Set badge to searching state
    chrome.action.setBadgeText({ text: "..." });
    chrome.action.setBadgeBackgroundColor({ color: "#f59e0b" }); // Amber

    try {
      const endpoint = await getApiEndpoint();
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textToVerify })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      // Store latest result in chrome.storage.local
      await chrome.storage.local.set({
        latestVerification: {
          query: textToVerify,
          result: data,
          timestamp: Date.now()
        }
      });

      // Update badge based on verdict
      const verdict = (data.overall_verdict || data.verdict || "UNKNOWN").toUpperCase();
      if (verdict.includes("FALSE") || verdict.includes("HOAX") || verdict.includes("FABRICATED")) {
        chrome.action.setBadgeText({ text: "HOAX" });
        chrome.action.setBadgeBackgroundColor({ color: "#ef4444" }); // Red
      } else if (verdict.includes("VERIFIED") || verdict.includes("TRUE") || verdict.includes("AUTHENTIC")) {
        chrome.action.setBadgeText({ text: "TRUE" });
        chrome.action.setBadgeBackgroundColor({ color: "#10b981" }); // Green
      } else if (verdict.includes("SUSPICIOUS") || verdict.includes("UNVERIFIED")) {
        chrome.action.setBadgeText({ text: "WARN" });
        chrome.action.setBadgeBackgroundColor({ color: "#f59e0b" }); // Amber
      } else {
        chrome.action.setBadgeText({ text: "?" });
        chrome.action.setBadgeBackgroundColor({ color: "#6b7280" }); // Gray
      }

    } catch (err) {
      console.error("[SatyaSetu] Extension Verification Error:", err);
      chrome.action.setBadgeText({ text: "ERR" });
      chrome.action.setBadgeBackgroundColor({ color: "#ef4444" });
    }
  }
});
