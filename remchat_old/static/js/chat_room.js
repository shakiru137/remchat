document.addEventListener("DOMContentLoaded", function () {
  const chatHistory = document.getElementById("chat-history");

  if (chatHistory) {
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  // Checks if the browser supports notifications
  if ("Notification" in window && Notification.permission !== "granted") {
    Notification.requestPermission();
  }
});

const socket = io(); // Initialize Socket.IO

const targetUsername =
  document.getElementById("targetUsername")?.getAttribute("data-value") || "";
const room_id =
  document.getElementById("room_id")?.getAttribute("data-value") || "";

socket.on("connect", function () {
  console.log("Joining room: " + room_id);
  socket.emit("join", {
    room: room_id,
    target_username: targetUsername,
  });
});

// Function to show notifications
function showNotification(title, message) {
  if (Notification.permission === "granted") {
    const notification = new Notification(title, {
      body: message,
      icon: iconUrl,
    });

    // Set the notification to disappear after 5 seconds
    setTimeout(() => notification.close(), 5000); // 5 seconds
  }
}

// Listen for incoming messages
socket.on("message", function (data) {
  console.log("Message received: ", data);

  const sessionUsername =
    document.getElementById("sessionUsername")?.getAttribute("data-username") ||
    "";
  const chatHistory = document.getElementById("chat-history");
  const chatBox = document.createElement("div");

  // Add data attributes to store sender and receiver information
  chatBox.setAttribute("data-sender", data.user);

  // Sanitize message content using DOMPurify
  const sanitizedMessage = DOMPurify.sanitize(data.msg);

  // Format timestamp
  const timestamp = new Date().toLocaleString();

  // Message structure using correct class names
  chatBox.innerHTML = `
    <span class="message-content">${sanitizedMessage}</span><br />
    <small class="timestamp-info"><em>${timestamp}</em></small>
  `;

  // Check if the sender is the current user and align accordingly
  chatBox.classList.add(
    "chat-box",
    data.user === sessionUsername ? "sent" : "received"
  );

  // Append the new message to the chat history
  if (chatHistory) {
    chatHistory.appendChild(chatBox);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  // Show a notification if the window is not in focus
  if (!document.hasFocus()) {
    showNotification("New message from " + data.user, data.msg);
  }
});

function sendMessage() {
  const message = document
    .querySelector("textarea[name='message']")
    .value.trim();
  const userId = document.getElementById("chat-history").dataset.userId;

  if (message) {
    console.log("Sending message: ", message + " to " + room_id);
    socket.emit("message", { msg: message, user_id: userId, room: room_id });

    document.querySelector("textarea[name='message']").value = ""; // Clear input
  } else {
    alert("Message cannot be empty."); // Alert user if empty
  }
}
