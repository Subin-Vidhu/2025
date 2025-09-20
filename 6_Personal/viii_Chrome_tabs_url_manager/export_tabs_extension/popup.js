async function listTabs() {
  try {
    const tabs = await chrome.tabs.query({});
    const urls = tabs.map(t => t.url).filter(Boolean);
    const text = urls.join("\n");
    document.getElementById("out").value = text;
    return { urls, text };
  } catch (e) {
    document.getElementById("out").value = "Error: " + e;
    return { urls: [], text: "" };
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const { urls, text } = await listTabs();

  document.getElementById("copy").onclick = async () => {
    try {
      await navigator.clipboard.writeText(text);
      alert("Copied " + urls.length + " URLs to clipboard");
    } catch (e) {
      alert("Copy failed: " + e);
    }
  };

  document.getElementById("download").onclick = () => {
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download =
      "tabs-urls-" +
      new Date().toISOString().replace(/[:.]/g, "-") +
      ".txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  document.getElementById("close").onclick = () => window.close();
});
