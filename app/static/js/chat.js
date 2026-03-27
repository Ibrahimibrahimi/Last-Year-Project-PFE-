// ─────────────────────────────────────────────
// LearnCode — Chatbot UI logic
// Pairs with: templates/chatbot.html
// Calls:      POST /chat  { message: "..." }
// ─────────────────────────────────────────────

(function () {
  "use strict";

  const messagesEl = document.getElementById("chat-messages");
  const formEl     = document.getElementById("chat-form");
  const inputEl    = document.getElementById("chat-input");
  const sendBtn    = document.getElementById("chat-send");

  // ── Helpers ───────────────────────────────

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** Minimal markdown: bold, inline code, fenced code blocks */
  function renderMarkdown(text) {
    // Fenced code blocks  ```lang\n...\n```
    text = text.replace(/```(\w*)\n?([\s\S]*?)```/g, function (_, lang, code) {
      const langLabel = lang ? `<span class="chat-code-lang">${escapeHtml(lang)}</span>` : "";
      return `<div class="chat-code-block">${langLabel}<pre><code>${escapeHtml(code.trim())}</code></pre></div>`;
    });
    // Inline code  `...`
    text = text.replace(/`([^`]+)`/g, "<code>$1</code>");
    // Bold  **...**
    text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    // Line breaks
    text = text.replace(/\n/g, "<br>");
    return text;
  }

  function appendMessage(role, text, isLoading = false) {
    const wrapper = document.createElement("div");
    wrapper.className = `chat-message chat-message--${role}`;
    if (isLoading) wrapper.id = "chat-typing";

    const bubble = document.createElement("div");
    bubble.className = "chat-bubble";

    if (isLoading) {
      bubble.innerHTML = `<span class="chat-typing-dots"><span></span><span></span><span></span></span>`;
    } else {
      bubble.innerHTML = renderMarkdown(text);
    }

    wrapper.appendChild(bubble);
    messagesEl.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  function removeTypingIndicator() {
    const el = document.getElementById("chat-typing");
    if (el) el.remove();
  }

  function setLoading(on) {
    sendBtn.disabled  = on;
    inputEl.disabled  = on;
    sendBtn.innerHTML = on
      ? `<span class="spinner-border spinner-border-sm" role="status"></span>`
      : `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
           <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11Z"/>
         </svg>`;
  }

  // ── Main send flow ─────────────────────────

  async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;

    appendMessage("user", text);
    inputEl.value = "";
    inputEl.style.height = "auto";
    setLoading(true);
    appendMessage("bot", "", true); // typing indicator

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      removeTypingIndicator();

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        appendMessage("bot", `⚠️ Error: ${err.error || res.statusText}`);
        return;
      }

      const data = await res.json();
      appendMessage("bot", data.reply || "(no response)");

    } catch (err) {
      removeTypingIndicator();
      appendMessage("bot", `⚠️ Network error: ${err.message}`);
    } finally {
      setLoading(false);
      inputEl.focus();
    }
  }

  // ── Event listeners ────────────────────────

  formEl.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage();
  });

  // Auto-grow textarea
  inputEl.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 150) + "px";
  });

  // Ctrl+Enter or Enter (without Shift) to send
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // ── Welcome message ────────────────────────
  appendMessage("bot", "👋 Hi! I'm your **LearnCode AI Tutor**. Ask me anything about programming — concepts, debugging, exercises, you name it!");

})();