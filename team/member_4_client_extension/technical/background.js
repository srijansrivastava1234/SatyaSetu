// SatyaSetu Chrome Extension - Background Service Worker (Manifest V3)

const API_ENDPOINT = "http://127.0.0.1:8000/api/verify";

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
      const response = await fetch(API_ENDPOINT, {
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
      const verdict = (data.verdict || "UNKNOWN").toUpperCase();
      if (verdict.includes("FALSE") || verdict.includes("HOAX")) {
        chrome.action.setBadgeText({ text: "HOAX" });
        chrome.action.setBadgeBackgroundColor({ color: "#ef4444" }); // Red
      } else if (verdict.includes("VERIFIED") || verdict.includes("TRUE")) {
        chrome.action.setBadgeText({ text: "TRUE" });
        chrome.action.setBadgeBackgroundColor({ color: "#10b981" }); // Green
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
