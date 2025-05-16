// Constants
const RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY = 3000; // 3 seconds
const MESSAGE_TIMEOUT = 5000; // 5 seconds timeout for message acknowledgment

// Initialize Socket.IO with configuration
const socket = io({
  reconnection: true,
  reconnectionAttempts: RECONNECT_ATTEMPTS,
  reconnectionDelay: RECONNECT_DELAY,
  timeout: 10000,
  transports: ["websocket", "polling"], // Explicitly specify transport methods
  forceNew: true, // Force a new connection
  autoConnect: true, // Automatically connect
});

// DOM Elements
const chatHistory = document.getElementById("chat-history");
const targetUsername =
  document.getElementById("targetUsername")?.getAttribute("data-value") || "";
const room_id =
  document.getElementById("room_id")?.getAttribute("data-value") || "";
const messageInput = document.querySelector("textarea[name='message']");
const sendButton = document.querySelector("button[type='submit']");

// Message queue for handling failed messages
let messageQueue = [];
let isProcessingQueue = false;

// Initialize chat when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  if (chatHistory) {
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  // Request notification permission
  if ("Notification" in window && Notification.permission !== "granted") {
    Notification.requestPermission();
  }

  // Add event listeners
  if (sendButton) {
    sendButton.addEventListener("click", handleSendMessage);
  }
  if (messageInput) {
    messageInput.addEventListener("keypress", handleKeyPress);
  }
});

// Socket event handlers
socket.on("connect", function () {
  console.log("Connected to server");
  joinRoom();
  // Process any queued messages when reconnected
  processMessageQueue();
});

socket.on("disconnect", function (reason) {
  console.log("Disconnected from server:", reason);
  if (reason === "io server disconnect") {
    // Server initiated disconnect, try to reconnect
    socket.connect();
  }
});

socket.on("connect_error", function (error) {
  console.error("Connection error:", error);
});

socket.on("reconnect_attempt", function (attemptNumber) {
  console.log("Reconnection attempt:", attemptNumber);
});

socket.on("reconnect_failed", function () {
  console.error("Failed to reconnect after", RECONNECT_ATTEMPTS, "attempts");
  alert("Connection to chat server lost. Please refresh the page.");
});

// Process message queue
function processMessageQueue() {
  if (isProcessingQueue || messageQueue.length === 0) return;

  isProcessingQueue = true;
  const message = messageQueue.shift();

  sendMessageToServer(message)
    .then(() => {
      isProcessingQueue = false;
      if (messageQueue.length > 0) {
        processMessageQueue();
      }
    })
    .catch((error) => {
      console.error("Error processing queued message:", error);
      messageQueue.unshift(message); // Put the message back at the start of the queue
      isProcessingQueue = false;
    });
}

// Send message to server with timeout
function sendMessageToServer(messageData) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error("Message send timeout"));
    }, MESSAGE_TIMEOUT);

    socket.emit("message", messageData, (error) => {
      clearTimeout(timeout);
      if (error) {
        reject(error);
      } else {
        resolve();
      }
    });
  });
}

// Join room function
function joinRoom() {
  if (room_id) {
    console.log("Joining room:", room_id);
    socket.emit("join", {
      room: room_id,
      target_username: targetUsername,
    });
  }
}

// Show notification function
function showNotification(title, message) {
  if (Notification.permission === "granted") {
    const notification = new Notification(title, {
      body: message,
      icon: "/static/remchat_logo.png",
    });
    setTimeout(() => notification.close(), 5000);
  }
}

// Handle incoming messages
socket.on("message", function (data) {
  console.log("Message received:", data);

  if (!data || !data.msg || !data.user) {
    console.error("Invalid message format:", data);
    return;
  }

  const sessionUsername =
    document.getElementById("sessionUsername")?.getAttribute("data-username") ||
    "";

  try {
    const chatBox = document.createElement("div");
    chatBox.setAttribute("data-sender", data.user);

    // Sanitize message content
    const sanitizedMessage = DOMPurify.sanitize(data.msg);
    const timestamp = new Date().toLocaleString();

    chatBox.innerHTML = `
      <span class="message-content">${sanitizedMessage}</span><br />
      <small class="timestamp-info"><em>${timestamp}</em></small>
    `;

    chatBox.classList.add(
      "chat-box",
      data.user === sessionUsername ? "sent" : "received"
    );

    if (chatHistory) {
      chatHistory.appendChild(chatBox);
      chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    if (!document.hasFocus()) {
      showNotification("New message from " + data.user, data.msg);
    }
  } catch (error) {
    console.error("Error handling message:", error);
  }
});

// Handle send message
function handleSendMessage(event) {
  event.preventDefault();
  sendMessage();
}

// Handle key press (Enter to send)
function handleKeyPress(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

// Send message function
function sendMessage() {
  if (!messageInput || !messageInput.value.trim()) {
    return;
  }

  const message = messageInput.value.trim();
  const userId = chatHistory?.dataset.userId;

  if (!userId) {
    console.error("User ID not found");
    return;
  }

  const messageData = {
    msg: message,
    user_id: userId,
    room: room_id,
  };

  try {
    console.log("Sending message to room:", room_id);

    // Add message to queue
    messageQueue.push(messageData);

    // Try to send immediately if connected
    if (socket.connected) {
      processMessageQueue();
    }

    // Clear input field
    messageInput.value = "";
  } catch (error) {
    console.error("Error in sendMessage:", error);
    alert("An error occurred while sending the message.");
  }
}

// Cleanup on page unload
window.addEventListener("beforeunload", function () {
  if (socket) {
    socket.disconnect();
  }
});
