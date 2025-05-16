// Constants
const FLASH_MESSAGE_DURATION = 5000; // Duration before fading out flash messages
const FLASH_FADE_OUT_DURATION = 1000; // Duration for fade out effect

document.addEventListener("DOMContentLoaded", (event) => {
  // Initialize form handling
  initializeForms();

  // Initialize flash messages
  initializeFlashMessages();

  // Initialize navigation
  initializeNavigation();

  // Initialize scroll position handling
  initializeScrollPosition();
});

function initializeForms() {
  // Clear form data on page reload
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.reset();

    // Add form validation
    form.addEventListener("submit", (e) => {
      if (!form.checkValidity()) {
        e.preventDefault();
        const invalidInputs = form.querySelectorAll(":invalid");
        invalidInputs.forEach((input) => {
          input.classList.add("invalid");
          input.addEventListener(
            "input",
            () => {
              input.classList.remove("invalid");
            },
            { once: true }
          );
        });
      }
    });
  });

  // Prevent form resubmission on refresh
  if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }
}

function initializeFlashMessages() {
  const flashes = document.querySelectorAll(".flashes .alert");
  if (flashes.length === 0) return;

  // Add role="alert" to flash messages for screen readers
  flashes.forEach((flash) => {
    flash.setAttribute("role", "alert");
  });

  // Fade out flash messages
  setTimeout(() => {
    flashes.forEach((flash) => {
      flash.style.transition = `opacity ${FLASH_FADE_OUT_DURATION}ms ease-out`;
      flash.style.opacity = 0;
      setTimeout(() => {
        flash.remove();
      }, FLASH_FADE_OUT_DURATION);
    });
  }, FLASH_MESSAGE_DURATION);
}

function initializeNavigation() {
  const navToggle = document.querySelector(".nav-toggle");
  const navbar = document.querySelector(".navbar");

  if (navToggle && navbar) {
    navToggle.addEventListener("click", function () {
      const isExpanded = navbar.classList.toggle("show");
      navToggle.setAttribute("aria-expanded", isExpanded);
    });

    // Close navigation when clicking outside
    document.addEventListener("click", (e) => {
      if (!navbar.contains(e.target) && !navToggle.contains(e.target)) {
        navbar.classList.remove("show");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });

    // Close navigation on escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navbar.classList.contains("show")) {
        navbar.classList.remove("show");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }
}

function initializeScrollPosition() {
  // Save scroll position and page URL before unloading the page
  window.addEventListener("beforeunload", saveScrollPosition);
  window.addEventListener("pagehide", saveScrollPosition);

  // Restore scroll position on pageshow
  window.addEventListener("pageshow", restoreScrollPosition);
}

function saveScrollPosition() {
  localStorage.setItem("scrollPosition", window.scrollY);
  localStorage.setItem("pageURL", window.location.href);
}

function restoreScrollPosition() {
  const scrollPosition = localStorage.getItem("scrollPosition");
  const savedPageURL = localStorage.getItem("pageURL");

  if (scrollPosition && savedPageURL === window.location.href) {
    window.scrollTo(0, parseInt(scrollPosition));
  }
}
