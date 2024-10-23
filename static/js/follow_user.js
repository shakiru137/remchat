var socket = io();

// Constants for button states
const BUTTON_STATE_FOLLOW = "Follow";
const BUTTON_STATE_FOLLOWING = "Following";

// Set up Socket.IO listener outside the function to avoid duplicate listeners
socket.on("follow_response", function (data) {
  console.log(data.message);
  const buttonValue = document.getElementById("button_value_" + data.user_id);

  if (buttonValue) {
    // Update the button state based on the response
    buttonValue.value = data.is_following
      ? BUTTON_STATE_FOLLOWING
      : BUTTON_STATE_FOLLOW;
  }
});

// Function to toggle follow/unfollow status
function toggleFollowStatus(user_id) {
  const buttonValue = document.getElementById("button_value_" + user_id); // Get button for this user

  if (!buttonValue) {
    console.error("Button not found for user ID:", user_id);
    return;
  }

  const isFollowing = buttonValue.value === BUTTON_STATE_FOLLOW;

  if (isFollowing) {
    socket.emit("follow", { user_id: user_id }); // Send follow request
    buttonValue.value = BUTTON_STATE_FOLLOWING; // Optimistically update the UI
  } else {
    socket.emit("unfollow", { user_id: user_id }); // Send unfollow request
    buttonValue.value = BUTTON_STATE_FOLLOW; // Optimistically update the UI
  }
}
