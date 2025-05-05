document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("input-form");
  const input = document.getElementById("input");
  const terminal = document.getElementById("terminal");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userInput = input.value.trim();
    if (!userInput) return;

    appendToTerminal(`> ${userInput}`);
    input.value = "";

    try {
      const response = await fetch("http://localhost:5000/game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: userInput }),
      });

      const data = await response.json();
      appendToTerminal(data.response);
    } catch (err) {
      appendToTerminal("Error: Could not connect to server.");
    }
  });

  function appendToTerminal(text) {
    terminal.innerHTML += `<div>${text}</div>`;
    terminal.scrollTop = terminal.scrollHeight;
  }
});
