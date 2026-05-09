const body = document.body;
const navToggle = document.querySelector("[data-nav-toggle]");
const navLinks = document.querySelector("[data-nav-links]");

const trackEvent = (eventName, parameters = {}) => {
  if (typeof window.gtag !== "function") {
    return;
  }

  window.gtag("event", eventName, {
    page_location: window.location.href,
    page_path: window.location.pathname,
    page_title: document.title,
    ...parameters,
  });
};

const analyticsFormSource = (form) =>
  form.dataset.analyticsSource ||
  form.querySelector('[name="metadata__source"], [name="source"]')?.value ||
  form.getAttribute("name") ||
  "unknown";

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
    const label = button.querySelector("[data-copy-text]");
    const originalLabel = label?.textContent || button.getAttribute("aria-label") || button.textContent;
    const setStatus = (message, state) => {
      if (label) {
        label.textContent = message;
      } else {
        button.textContent = message;
      }
      button.setAttribute("aria-label", message);
      button.setAttribute("title", message);
      button.classList.remove("is-copied", "is-error");
      if (state) {
        button.classList.add(state);
      }
    };

    try {
      await navigator.clipboard.writeText(button.dataset.copyLink);
      trackEvent("share_click", {
        share_platform: button.dataset.sharePlatform || "copy_link",
        link_url: button.dataset.copyLink,
      });
      setStatus("Link copied", "is-copied");
      window.setTimeout(() => {
        setStatus(originalLabel, "");
      }, 1600);
    } catch (error) {
      setStatus("Copy failed", "is-error");
      window.setTimeout(() => {
        setStatus(originalLabel, "");
      }, 1600);
    }
  });
});

document.querySelectorAll("a[data-share-platform]").forEach((link) => {
  link.addEventListener("click", () => {
    trackEvent("share_click", {
      share_platform: link.dataset.sharePlatform,
      link_url: link.href,
    });
  });
});

document.querySelectorAll("[data-contact-form], [data-subscribe-form]").forEach((form) => {
  const button = form.querySelector('button[type="submit"]');
  const note = form.parentElement?.querySelector("[data-form-status]");
  const isSubscribe = form.hasAttribute("data-subscribe-form");
  const isButtondownSubscribe = isSubscribe && form.action.includes("buttondown.com/api/emails/embed-subscribe/");
  const ajaxAction = form.dataset.ajaxAction;
  const pendingMessage =
    form.dataset.pendingMessage || (isSubscribe ? "Saving your subscription..." : "Sending your note...");
  const successMessage =
    form.dataset.successMessage ||
    (isSubscribe ? "Thank you. Please check your inbox to confirm your subscription." : "Thank you. Your message is on its way.");
  const errorMessage =
    form.dataset.errorMessage ||
    (isSubscribe ? "Subscription did not go through. Please try again in a moment." : "The message did not send. Please try again in a moment.");
  const successButtonLabel = form.dataset.successButtonLabel || (isSubscribe ? "Check your inbox" : "Message sent");
  const errorButtonLabel = form.dataset.errorButtonLabel || "Try again";

  if (isButtondownSubscribe) {
    // Let Buttondown's official embedded form handle validation, subscription,
    // confirmation, and any visible error state. A no-cors fetch hides failures.
    form.addEventListener("submit", () => {
      if (form.reportValidity()) {
        trackEvent("newsletter_subscribe_submit", {
          form_provider: "buttondown",
          form_source: analyticsFormSource(form),
        });
      }
    });
    return;
  }

  if (!ajaxAction) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity() || !ajaxAction) {
      return;
    }

    const eventPrefix = isSubscribe ? "newsletter_subscribe" : "contact_form";
    trackEvent(`${eventPrefix}_submit`, {
      form_provider: "formsubmit",
      form_source: analyticsFormSource(form),
    });

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
      trackEvent(`${eventPrefix}_success`, {
        form_provider: "formsubmit",
        form_source: analyticsFormSource(form),
      });
      if (note) {
        note.dataset.state = "success";
        note.textContent = successMessage;
      }
      if (button) {
        button.textContent = successButtonLabel;
      }
    } catch (error) {
      trackEvent(`${eventPrefix}_error`, {
        form_provider: "formsubmit",
        form_source: analyticsFormSource(form),
      });
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

const articleBody = document.querySelector(".article-body");
if (articleBody) {
  const sentDepths = new Set();
  const thresholds = [50, 90];
  let isQueued = false;

  const articleTitle = document.querySelector(".article-hero h1")?.textContent?.trim() || document.title;

  const checkReadDepth = () => {
    isQueued = false;

    const articleTop = articleBody.getBoundingClientRect().top + window.scrollY;
    const articleHeight = articleBody.offsetHeight;
    if (!articleHeight) {
      return;
    }

    const progress = Math.max(
      0,
      Math.min(100, ((window.scrollY + window.innerHeight - articleTop) / articleHeight) * 100)
    );

    thresholds.forEach((threshold) => {
      if (progress >= threshold && !sentDepths.has(threshold)) {
        sentDepths.add(threshold);
        trackEvent(`article_read_${threshold}`, {
          article_title: articleTitle,
          article_path: window.location.pathname,
          percent_scrolled: threshold,
        });
      }
    });

    if (sentDepths.size === thresholds.length) {
      window.removeEventListener("scroll", queueReadDepthCheck);
      window.removeEventListener("resize", queueReadDepthCheck);
    }
  };

  function queueReadDepthCheck() {
    if (isQueued) {
      return;
    }

    isQueued = true;
    window.requestAnimationFrame(checkReadDepth);
  }

  window.addEventListener("scroll", queueReadDepthCheck, { passive: true });
  window.addEventListener("resize", queueReadDepthCheck);
  queueReadDepthCheck();
}

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});
