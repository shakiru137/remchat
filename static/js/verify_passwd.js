document.getElementById("myForm").addEventListener("submit", function (e) {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const errorMessage = document.getElementById("errorMessage");

  // Check if passwords match.
  if (password !== confirmPassword) {
    e.preventDefault(); // Prevent form submission
    errorMessage.textContent = "Passwords do not match!";

    // Clear the error message after 3 seconds
    setTimeout(() => {
      errorMessage.textContent = "";
    }, 3000);
  } else {
    errorMessage.textContent = ""; // Clear error message if passwords match
  }
});

// Clear error message on input
const passwordField = document.getElementById("password");
const confirmPasswordField = document.getElementById("confirmPassword");

passwordField.addEventListener("input", () => {
  document.getElementById("errorMessage").textContent = "";
});

confirmPasswordField.addEventListener("input", () => {
  document.getElementById("errorMessage").textContent = "";
});
