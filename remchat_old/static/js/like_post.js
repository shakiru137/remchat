console.log("I am in the script");

var socket = io();

// Constants for button states.
const BUTTON_STATE_LIKE = "Like";
const BUTTON_STATE_LIKED = "Liked";

/**
 * Listens for 'like_response' events from the server.
 * @param {Object} data - Contains a message and status from the server.
 */
socket.on("like_response", function (data) {
  console.log(data.message);
  // Optionally, display the message to the user (alert, UI message, etc.)
});

/**
 * Updates the button state and like count in the UI.
 *
 * @param {HTMLElement} button - The button element for the like action.
 * @param {HTMLElement} likeCountElement - The element displaying the like count.
 * @param {number} count - The current like count.
 * @param {boolean} liked - Indicates if the post is currently liked.
 */
function updateLikeUI(button, likeCountElement, count, liked) {
  if (liked) {
    button.value = BUTTON_STATE_LIKED;
    likeCountElement.innerText = count + 1 + " Likes"; // Increment the like count
    button.style.backgroundColor = "#355839";
    button.style.color = "#fff";
  } else {
    button.value = BUTTON_STATE_LIKE;
    likeCountElement.innerText = (count > 0 ? count - 1 : 0) + " Likes"; // Decrement the like count
    button.style.backgroundColor = "#dcf8c6";
    button.style.color = "rgb(51, 204, 102)";
  }
}

/**
 * Handles the click event when a user likes or unlikes a post.
 * It updates the like button text and the displayed like count on the page.
 *
 * @param {number} post_id - The ID of the post to like/unlike.
 */
function like_post(post_id) {
  var button_value = document.getElementById("button_value_" + post_id);
  var like_count = document.getElementById("like-count-" + post_id);

  // Check if elements exist
  if (!button_value || !like_count) {
    console.error(
      "Button or like count element not found for post ID:",
      post_id
    );
    return; // Exit if elements are not found
  }

  // Extract the current like count by removing " Likes" from the inner text
  var count_value = parseInt(like_count.innerText.replace(" Likes", ""));

  // Clean up the button value by converting to lowercase and trimming spaces
  var button_text = button_value.value.toLowerCase().trim();

  // Determine if the post is currently liked and update the UI
  if (button_text === BUTTON_STATE_LIKE.toLowerCase()) {
    updateLikeUI(button_value, like_count, count_value, true);
  } else if (button_text === BUTTON_STATE_LIKED.toLowerCase()) {
    updateLikeUI(button_value, like_count, count_value, false);
  }

  // Emit the like event to the server via WebSocket
  socket.emit("like_post", { post_id: post_id });
}
