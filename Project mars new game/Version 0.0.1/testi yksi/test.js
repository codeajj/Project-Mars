document.addEventListener('DOMContentLoaded', () => {
  const terminal = document.getElementById('terminal');
  const buttons = document.querySelectorAll('.action-button');
  let selectedIndex = 0;

  const printToTerminal = (message) => {
    terminal.innerHTML += `<div>> ${message}</div>`;
    terminal.scrollTop = terminal.scrollHeight;
  };

  const callAPI = (action) => {
    const url = `http://localhost:5000/${action}`;
    console.log("Calling API URL:", url); // Debug: Logs the requested URL

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => printToTerminal(data.message))
      .catch(err => printToTerminal(`Error: ${err.message}`));
  };

  buttons.forEach((button, index) => {
    button.addEventListener('click', () => {
      callAPI(button.dataset.action);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
      buttons[selectedIndex].classList.remove('selected');
      selectedIndex = (selectedIndex + 1) % buttons.length;
      buttons[selectedIndex].classList.add('selected');
    } else if (e.key === 'ArrowLeft') {
      buttons[selectedIndex].classList.remove('selected');
      selectedIndex = (selectedIndex - 1 + buttons.length) % buttons.length;
      buttons[selectedIndex].classList.add('selected');
    } else if (e.key === 'Enter') {
      callAPI(buttons[selectedIndex].dataset.action);
    }
  });
});
