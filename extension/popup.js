// SatyaSetu Chrome Extension - Popup Logic

document.addEventListener("DOMContentLoaded", async () => {
  const verdictBadge = document.getElementById("verdictBadge");
  const queryText = document.getElementById("queryText");
  const explanationText = document.getElementById("explanationText");
  const copyBtn = document.getElementById("copyDebunkBtn");
  const toast = document.getElementById("toast");

  let debunkMessage = "";

  // Load latest stored verification from storage
  const data = await chrome.storage.local.get("latestVerification");
  if (data && data.latestVerification) {
    const item = data.latestVerification;
    const res = item.result || {};
    
    queryText.innerText = item.query ? `"${item.query}"` : "No recent query.";
    explanationText.innerText = res.explanation || res.summary || "Verification complete.";

    const verdict = (res.verdict || "UNVERIFIED").toUpperCase();
    verdictBadge.innerText = verdict;

    if (verdict.includes("FALSE") || verdict.includes("HOAX")) {
      verdictBadge.className = "badge badge-false";
    } else if (verdict.includes("VERIFIED") || verdict.includes("TRUE")) {
      verdictBadge.className = "badge badge-true";
    } else {
      verdictBadge.className = "badge badge-pending";
    }

    debunkMessage = `🚨 *SatyaSetu Fact-Check Alert* 🚨\n\n*Claim*: "${item.query}"\n*Verdict*: ${verdict}\n*Analysis*: ${explanationText.innerText}\n\n*Verified via certified IFCN sources.* Please verify before forwarding!`;
  }

  copyBtn.addEventListener("click", () => {
    if (!debunkMessage) {
      debunkMessage = "SatyaSetu Fact-Check: Always verify before forwarding unconfirmed WhatsApp messages!";
    }
    navigator.clipboard.writeText(debunkMessage).then(() => {
      toast.style.display = "block";
      setTimeout(() => { toast.style.display = "none"; }, 2500);
    });
  });
});
