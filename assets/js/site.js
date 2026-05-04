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

document.querySelectorAll('form[name="newsletter"]').forEach((form) => {
  const emailInput = form.querySelector('input[type="email"]');
  const button = form.querySelector('button[type="submit"]');
  const note = form.parentElement?.querySelector(".form-note");

  if (button) {
    button.textContent = "Open email app";
  }

  if (note) {
    note.innerHTML =
      'This opens your email app and pre-fills a note to <a href="mailto:info@munyachipunza.com">info@munyachipunza.com</a>.';
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!form.reportValidity()) {
      return;
    }

    const email = emailInput?.value.trim() ?? "";
    const subject = "Next reflection request";
    const lines = [
      "Hello Munya,",
      "",
      "Please keep me posted when your next reflection is published.",
      email ? `My email address: ${email}` : "",
    ].filter(Boolean);

    window.location.href =
      `mailto:info@munyachipunza.com?subject=${encodeURIComponent(subject)}` +
      `&body=${encodeURIComponent(lines.join("\n"))}`;

    if (button) {
      const originalLabel = button.textContent;
      button.textContent = "Email app opened";
      window.setTimeout(() => {
        button.textContent = originalLabel;
      }, 1600);
    }
  });
});

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});
