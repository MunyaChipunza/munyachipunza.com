const body = document.body;
const navToggle = document.querySelector("[data-nav-toggle]");
const navLinks = document.querySelector("[data-nav-links]");

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const expanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!expanded));
    body.classList.toggle("nav-open", !expanded);
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navToggle.setAttribute("aria-expanded", "false");
      body.classList.remove("nav-open");
    });
  });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll(".will-reveal").forEach((element) => {
  revealObserver.observe(element);
});

document.querySelectorAll("[data-copy-link]").forEach((button) => {
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copyLink);
      const original = button.textContent;
      button.textContent = "Link copied";
      window.setTimeout(() => {
        button.textContent = original;
      }, 1600);
    } catch (error) {
      button.textContent = "Copy failed";
    }
  });
});

document.querySelectorAll("[data-contact-form], [data-subscribe-form]").forEach((form) => {
  const button = form.querySelector('button[type="submit"]');
  const note = form.parentElement?.querySelector("[data-form-status]");
  const ajaxAction = form.dataset.ajaxAction || form.getAttribute("action");
  const isSubscribe = form.hasAttribute("data-subscribe-form");
  const pendingMessage =
    form.dataset.pendingMessage || (isSubscribe ? "Saving your subscription..." : "Sending your note...");
  const successMessage =
    form.dataset.successMessage || (isSubscribe ? "Thank you. You're on the list." : "Thank you. Your message is on its way.");
  const errorMessage =
    form.dataset.errorMessage ||
    (isSubscribe ? "Subscription did not go through. Please try again in a moment." : "The message did not send. Please try again in a moment.");
  const successButtonLabel = form.dataset.successButtonLabel || (isSubscribe ? "Subscribed" : "Message sent");
  const errorButtonLabel = form.dataset.errorButtonLabel || "Try again";

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity() || !ajaxAction) {
      return;
    }

    const originalLabel = button?.textContent ?? "";
    if (button) {
      button.disabled = true;
      button.textContent = "Sending...";
    }

    if (note) {
      note.dataset.state = "";
      note.textContent = pendingMessage;
    }

    try {
      const response = await fetch(ajaxAction, {
        method: "POST",
        body: new FormData(form),
        headers: {
          Accept: "application/json",
        },
      });

      const payload = await response.json().catch(() => ({}));
      if (!response.ok || !["true", true].includes(payload.success)) {
        throw new Error("Submission failed");
      }

      form.reset();
      if (note) {
        note.dataset.state = "success";
        note.textContent = successMessage;
      }
      if (button) {
        button.textContent = successButtonLabel;
      }
    } catch (error) {
      if (note) {
        note.dataset.state = "error";
        note.textContent = errorMessage;
      }
      if (button) {
        button.textContent = errorButtonLabel;
      }
    } finally {
      window.setTimeout(() => {
        if (button) {
          button.disabled = false;
          button.textContent = originalLabel;
        }
      }, 1800);
    }
  });
});

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});
