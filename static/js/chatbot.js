function toggleChatbot() {
  var chatBody = document.getElementById("chatbot-body");
  chatBody.style.display = chatBody.style.display === "none" ? "block" : "none";
}

function sendMessage() {
  var input = document.getElementById("chat-input");
  var message = input.value;
  input.value = "";

  fetch("/chatbot", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `message=${encodeURIComponent(message)}`,
  })
    .then((response) => response.json())
    .then((data) => {
      var chatMessages = document.getElementById("chat-messages");
      chatMessages.innerHTML += `<div class="message-user">Tu: ${message}</div>`;
      chatMessages.innerHTML += `<div class="message-bot">Bot: ${data.response}</div>`;
      chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch((error) => console.error("Error: ", error));
}

// Añade esta función para manejar el evento de teclado
function handleEnter(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevenir el comportamiento predeterminado del formulario
    sendMessage(); // Llama a sendMessage cuando se presiona Enter
  }
}

// Añade el controlador de eventos al cargar la página
window.onload = function () {
  var chatInput = document.getElementById("chat-input");
  chatInput.addEventListener("keypress", handleEnter);
};
