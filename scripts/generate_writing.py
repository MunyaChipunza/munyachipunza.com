from __future__ import annotations

import html
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


ROOT = Path(r"C:\Users\Dell\OneDrive\100. Zee\Munyachipunza.com")
OLD_HOST = "www.munyachipunza.com"
OLD_IP = "185.230.63.171"
SITE_URL = "https://munyachipunza.com"
BLOG_APP_ID = "14bcded7-0066-7c35-14d7-466cb3f09103"
POSTS_PER_PAGE = 5
CONTACT_FORM_ACTION = "https://formsubmit.co/02774129a6ffd7df5b31b69ff0886e06"
CONTACT_FORM_AJAX = "https://formsubmit.co/ajax/02774129a6ffd7df5b31b69ff0886e06"
CONTACT_SUCCESS_URL = f"{SITE_URL}/thanks"

POST_CONFIG = {
    "the-weight-of-unspoken-words": {
        "route": "weight-of-unspoken-words",
        "tag": "Faith & Resilience",
    },
    "self-worth-how-much-do-you-value-yourself": {
        "route": "self-worth",
        "tag": "Identity",
    },
    "peace-can-be-safe-too": {
        "route": "peace-can-be-safe",
        "tag": "Peace",
    },
    "sometimes-it-s-ok-to-be-not-ok": {
        "route": "not-ok",
        "tag": "Resilience",
    },
    "when-all-seems-to-be-going-wrong": {
        "route": "when-all-goes-wrong",
        "tag": "Faith",
    },
    "when-the-enemy-is-the-inner-me": {
        "route": "enemy-inner-me",
        "tag": "Identity",
    },
    "the-power-of-thank-you": {
        "route": "the-power-of-thank-you",
        "tag": "Gratitude",
    },
    "words-that-build-not-break": {
        "route": "words-that-build-not-break",
        "tag": "Communication",
    },
    "from-burden-to-blessing-shifting-the-lens-of-leadership-and-life": {
        "route": "shifting-the-lens-of-leadership-and-life",
        "tag": "Leadership",
    },
    "when-the-leader-runs-empty": {
        "route": "when-the-leader-runs-empty",
        "tag": "Leadership",
    },
    "pressure-reveals-the-leader": {
        "route": "pressure-reveals-the-leader",
        "tag": "Leadership",
    },
    "dare-to-lead": {
        "route": "dare-to-lead",
        "tag": "Leadership",
    },
}


def run_curl(url: str, *, headers: dict[str, str] | None = None, method: str = "GET", data: str | None = None, resolve_old: bool = False) -> str:
    handle, output_path = tempfile.mkstemp(prefix="munya-wix-", suffix=".json")
    os.close(handle)
    args = ["curl.exe", "-sS", "-L", "--output", output_path]
    if resolve_old:
        args.extend(["-k", "--resolve", f"{OLD_HOST}:443:{OLD_IP}"])
    for name, value in (headers or {}).items():
        args.extend(["-H", f"{name}: {value}"])
    if method != "GET":
        args.extend(["-X", method])
    if data is not None:
        args.extend(["--data-binary", data])
    args.append(url)
    try:
        subprocess.run(args, check=True, capture_output=True, text=True, encoding="utf-8")
        return Path(output_path).read_text(encoding="utf-8")
    finally:
        Path(output_path).unlink(missing_ok=True)


def fetch_json(url: str, **kwargs) -> dict:
    return json.loads(run_curl(url, **kwargs))


def fetch_access_token() -> str:
    payload = fetch_json(f"https://{OLD_HOST}/_api/v1/access-tokens", resolve_old=True)
    return payload["apps"][BLOG_APP_ID]["accessToken"]


def fetch_posts(access_token: str) -> list[dict]:
    listing = fetch_json(
        "https://www.wixapis.com/blog/v3/posts?paging.limit=100",
        headers={"Authorization": access_token},
    )["posts"]
    detailed_posts = []

    for listed_post in listing:
        query = json.dumps(
            {
                "dataCollectionId": "Blog/Posts",
                "query": {"filter": {"slug": {"$eq": listed_post["slug"]}}},
            }
        )
        item = fetch_json(
            "https://www.wixapis.com/wix-data/v2/items/query",
            method="POST",
            data=query,
            headers={
                "Authorization": access_token,
                "Content-Type": "application/json",
            },
        )["dataItems"][0]["data"]

        config = POST_CONFIG[listed_post["slug"]]
        detailed_posts.append(
            {
                "old_slug": listed_post["slug"],
                "route": config["route"],
                "tag": config["tag"],
                "title": listed_post["title"],
                "excerpt": clean_excerpt(item.get("excerpt") or listed_post.get("excerpt") or ""),
                "published_date": item["publishedDate"]["$date"],
                "updated_date": item["lastPublishedDate"]["$date"],
                "minutes_to_read": int(round(item.get("timeToRead") or listed_post.get("minutesToRead") or 2)),
                "plain_content": item.get("plainContent", "").strip(),
                "rich_content": item.get("richContent", {}).get("nodes", []),
                "image_url": listed_post.get("media", {})
                .get("wixMedia", {})
                .get("image", {})
                .get("url", f"{SITE_URL}/assets/images/munya-home.jpg"),
            }
        )

    detailed_posts.sort(key=lambda post: post["published_date"], reverse=True)
    return detailed_posts


def clean_excerpt(text: str) -> str:
    text = normalize_text(text)
    text = " ".join(text.replace("\u00a0", " ").split())
    return text.replace("You ’re", "You’re").replace("you  ", "you ").replace("thank you  ", "thank you ").strip()


def normalize_text(text: str, *, strip_edges: bool = True) -> str:
    text = text.replace("\u00a0", " ")
    leading_space = text[:1].isspace()
    trailing_space = text[-1:].isspace()
    text = re.sub(r"([.!?])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([.!?])([“\"'])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    if not strip_edges:
        if leading_space:
            text = f" {text}"
        if trailing_space:
            text = f"{text} "
    return text


def format_date(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    return f"{dt.day} {dt.strftime('%B %Y')}"


def iso_date(value: str) -> str:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def reading_time_label(minutes: int) -> str:
    return f"{minutes} min read"


def text_snippet(text: str, limit: int) -> str:
    text = clean_excerpt(text)
    if len(text) <= limit:
        return text
    sliced = text[:limit].rsplit(" ", 1)[0].strip()
    return f"{sliced}..."


def render_inline_node(node: dict) -> str:
    node_type = node.get("type")
    if node_type == "TEXT":
        rendered = html.escape(normalize_text(node.get("textData", {}).get("text", ""), strip_edges=False))
        for decoration in node.get("textData", {}).get("decorations", []):
            deco_type = decoration.get("type")
            if deco_type == "ITALIC":
                rendered = f"<em>{rendered}</em>"
            elif deco_type == "BOLD":
                rendered = f"<strong>{rendered}</strong>"
        return rendered

    children = "".join(render_inline_node(child) for child in node.get("nodes", []))
    if node_type == "LINK":
        link = node.get("linkData", {}).get("link", {})
        url = link.get("url")
        if url:
            return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{children}</a>'
    return children


def paragraph_text(post: dict) -> list[str]:
    paragraphs: list[str] = []
    for node in post["rich_content"]:
        if node.get("type") != "PARAGRAPH":
            continue
        content = "".join(render_inline_node(child) for child in node.get("nodes", []))
        content = content.strip()
        if content:
            paragraphs.append(content)
    if paragraphs:
        merged: list[str] = []
        for paragraph in paragraphs:
            if merged and should_join_paragraph(merged[-1], paragraph):
                merged[-1] = f"{merged[-1]} {paragraph}"
            else:
                merged.append(paragraph)
        return merged
    fallback = clean_excerpt(post["plain_content"])
    return [html.escape(fallback)] if fallback else []


def strip_markup(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def should_join_paragraph(previous: str, current: str) -> bool:
    prev_plain = strip_markup(previous).strip()
    curr_plain = strip_markup(current).strip()
    if not prev_plain or not curr_plain:
        return False
    if prev_plain[-1] in ".!?;:”\"'":
        return False
    return bool(re.match(r"^(and|or|but|because|so|that|it|you|we|they|the|a|an)\b", curr_plain, flags=re.IGNORECASE))


def first_paragraph_plain(post: dict) -> str:
    paragraphs = paragraph_text(post)
    if not paragraphs:
        return ""
    plain = (
        paragraphs[0]
        .replace("<em>", "")
        .replace("</em>", "")
        .replace("<strong>", "")
        .replace("</strong>", "")
    )
    return clean_excerpt(plain)


def render_article_body(post: dict) -> str:
    paragraphs = paragraph_text(post)
    blocks = []
    for index, paragraph in enumerate(paragraphs):
        class_attr = ' class="lead"' if index == 0 else ""
        blocks.append(f"<p{class_attr}>{paragraph}</p>")
    return "\n          ".join(blocks)


def article_description(post: dict) -> str:
    return text_snippet(first_paragraph_plain(post) or post["excerpt"], 158)


def article_intro(post: dict) -> str:
    return text_snippet(first_paragraph_plain(post) or post["excerpt"], 210)


def page_route(page_number: int) -> str:
    return "/writing" if page_number == 1 else f"/writing/page/{page_number}"


def page_title(page_number: int) -> str:
    return "Writing | Munya Chipunza" if page_number == 1 else f"Writing Page {page_number} | Munya Chipunza"


def archive_canonical(page_number: int) -> str:
    return f"{SITE_URL}{page_route(page_number)}"


def header(active: str, cta_href: str, cta_label: str) -> str:
    return f"""    <header class="site-header">
      <div class="nav-shell">
        <a class="brand-mark" href="/">
          <strong>Munya</strong>
          <span>Chipunza</span>
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Toggle navigation" data-nav-toggle>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
            <path d="M4 7h16M4 12h16M4 17h16"></path>
          </svg>
        </button>
        <ul class="nav-links" data-nav-links>
          <li><a href="/"{" class=\"active\"" if active == "home" else ""}>Home</a></li>
          <li><a href="/about"{" class=\"active\"" if active == "about" else ""}>About</a></li>
          <li><a href="/writing"{" class=\"active\"" if active == "writing" else ""}>Writing</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
        <div class="nav-actions">
          <a class="button button-secondary" href="{cta_href}">{cta_label}</a>
        </div>
      </div>
    </header>"""


FOOTER = """    <footer class="footer">
      <div class="footer-shell">
        <div class="footer-grid">
          <div>
            <strong>Munya Chipunza</strong>
            <p>Reflections on faith, resilience, and hope for anyone navigating a season that feels heavier than expected.</p>
          </div>
          <div>
            <div class="footer-heading">Navigate</div>
            <div class="footer-links">
              <a href="/">Home</a>
              <a href="/about">About</a>
              <a href="/writing">Writing</a>
            </div>
          </div>
          <div>
            <div class="footer-heading">Elsewhere</div>
            <div class="footer-social">
              <a class="social-link" href="https://www.facebook.com/chipunzamunya" target="_blank" rel="noopener" aria-label="Facebook">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"></path></svg>
              </a>
              <a class="social-link" href="https://x.com/Iam_munya" target="_blank" rel="noopener" aria-label="X">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"></path></svg>
              </a>
              <a class="social-link" href="https://www.tiktok.com/@munyachipunza" target="_blank" rel="noopener" aria-label="TikTok">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"></path></svg>
              </a>
              <a class="social-link" href="https://www.threads.com/@iam_munya" target="_blank" rel="noopener" aria-label="Threads">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"></path></svg>
              </a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <span>&copy; <span data-year></span> Munya Chipunza.</span>
          <span>Written in Cape Town, rooted in Zimbabwe.</span>
        </div>
      </div>
    </footer>"""


def contact_form_fields(subject: str) -> str:
    return f"""          <form class="signup-form full" name="contact" method="POST" action="{CONTACT_FORM_ACTION}" data-contact-form data-ajax-action="{CONTACT_FORM_AJAX}" id="contact-form">
            <input type="hidden" name="_subject" value="{html.escape(subject, quote=True)}">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="{CONTACT_SUCCESS_URL}">
            <p class="sr-only">
              <label>Do not fill this out if you are human <input name="_honey" tabindex="-1" autocomplete="off"></label>
            </p>
            <input type="text" name="name" placeholder="Your name" autocomplete="name" required>
            <input type="email" name="email" placeholder="Your email address" autocomplete="email" required>
            <textarea class="full-row" name="message" placeholder="Your message" required></textarea>
            <button class="button button-primary full-row" type="submit">Send message</button>
          </form>
          <p class="form-note" data-form-status aria-live="polite">Your note comes through privately and lands in Munya's inbox.</p>"""


FORM_SECTION = f"""      <section class="form-section" id="contact">
        <div class="form-panel will-reveal">
          <p class="eyebrow">Stay in touch</p>
          <h2>Send a note.</h2>
          <p>If something in the writing met you where you are, this is the simplest way to reach out.</p>
{contact_form_fields("New message from munyachipunza.com")}
        </div>
      </section>"""


def archive_cards(posts: list[dict]) -> str:
    cards = []
    for post in posts:
        cards.append(
            f"""        <a class="article-card will-reveal" href="/writing/{post["route"]}">
          <div>
            <p class="article-tag">{html.escape(post["tag"])}</p>
            <h2 class="article-card-title">{html.escape(post["title"])}</h2>
            <p>{html.escape(text_snippet(post["excerpt"] or first_paragraph_plain(post), 260))}</p>
          </div>
          <div class="article-meta">
            <div>{format_date(post["published_date"])}</div>
            <div>{reading_time_label(post["minutes_to_read"])}</div>
          </div>
        </a>"""
        )
    return "\n\n".join(cards)


def render_pagination(page_number: int, total_pages: int) -> str:
    page_links = []
    for number in range(1, total_pages + 1):
        if number == page_number:
            page_links.append(f'<span class="pagination-link is-current" aria-current="page">{number}</span>')
        else:
            page_links.append(f'<a class="pagination-link" href="{page_route(number)}">{number}</a>')

    previous_link = (
        f'<a class="pagination-button" href="{page_route(page_number - 1)}">Newer page</a>'
        if page_number > 1
        else '<span class="pagination-button is-disabled">Newer page</span>'
    )
    next_link = (
        f'<a class="pagination-button" href="{page_route(page_number + 1)}">Older page</a>'
        if page_number < total_pages
        else '<span class="pagination-button is-disabled">Older page</span>'
    )

    return f"""      <nav class="pagination" aria-label="Writing pages">
        <div class="pagination-row">
          {previous_link}
          <span class="pagination-label">Page {page_number} of {total_pages}</span>
          {next_link}
        </div>
        <div class="pagination-links">
          {' '.join(page_links)}
        </div>
      </nav>"""


def render_archive_page(page_posts: list[dict], page_number: int, total_pages: int, total_posts: int) -> str:
    title = page_title(page_number)
    description = "Editorial reflections on faith, identity, resilience, peace, and what it means to stay human in hard seasons."
    hero_line = "Short reflections on faith, identity, grief, peace, and the quiet interior work required to stay human under pressure."
    page_note = f"Page {page_number} of {total_pages} &middot; {total_posts} published reflections."
    canonical = archive_canonical(page_number)
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description, quote=True)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="Reflections on faith, identity, peace, grief, and staying steady.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE_URL}/assets/images/munya-home.jpg">
    <link rel="alternate" href="{SITE_URL}/blog-feed.xml" title="Munya Chipunza - RSS" type="application/rss+xml">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="stylesheet" href="/assets/css/style.css">
  </head>
  <body>
{header("writing", "/about", "About Munya")}

    <main>
      <section class="page-hero">
        <p class="eyebrow">All writing</p>
        <h1>Words for the road.</h1>
        <p>{hero_line}</p>
        <p class="archive-note">{page_note}</p>
      </section>

      <section class="article-list">
{archive_cards(page_posts)}
      </section>

{render_pagination(page_number, total_pages)}

{FORM_SECTION}
    </main>

{FOOTER}

    <script src="/assets/js/site.js"></script>
  </body>
</html>
"""


def render_article_nav(posts: list[dict], index: int) -> str:
    newer = posts[index - 1] if index > 0 else None
    older = posts[index + 1] if index + 1 < len(posts) else None

    left = (
        f"""        <a href="/writing/{newer["route"]}">
          <span>Newer reflection</span>
          <strong>{html.escape(newer["title"])}</strong>
        </a>"""
        if newer
        else "        <div></div>"
    )
    right = (
        f"""        <a href="/writing/{older["route"]}">
          <span>Older reflection</span>
          <strong>{html.escape(older["title"])}</strong>
        </a>"""
        if older
        else "        <div></div>"
    )

    return f"""      <nav class="article-nav">
{left}
{right}
      </nav>"""


def render_article_page(post: dict, posts: list[dict], index: int) -> str:
    canonical = f"{SITE_URL}/writing/{post['route']}"
    title = f"{post['title']} | Munya Chipunza"
    description = article_description(post)
    intro = article_intro(post)
    share_text = quote(f"{post['title']} by Munya Chipunza")
    share_url = quote(canonical, safe="")

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description, quote=True)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{html.escape(post['image_url'], quote=True)}">
    <meta property="article:published_time" content="{post['published_date']}">
    <meta property="article:modified_time" content="{post['updated_date']}">
    <link rel="alternate" href="{SITE_URL}/blog-feed.xml" title="Munya Chipunza - RSS" type="application/rss+xml">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="stylesheet" href="/assets/css/style.css">
  </head>
  <body>
{header("writing", "/writing", "All writing")}

    <main>
      <section class="article-hero">
        <a class="article-back" href="/writing">&larr; Back to all writing</a>
        <p class="post-tag">{html.escape(post["tag"])}</p>
        <h1>{html.escape(post["title"])}</h1>
        <p class="article-intro">{html.escape(intro)}</p>
        <div class="post-meta">
          <img src="/assets/images/munya-avatar.jpg" alt="Munya Chipunza">
          <span>Munya Chipunza</span>
          <span>{format_date(post["published_date"])}</span>
          <span>{reading_time_label(post["minutes_to_read"])}</span>
        </div>
      </section>

      <article class="article-body">
        <div class="prose">
          {render_article_body(post)}
        </div>
      </article>

      <section class="share-strip">
        <div class="share-list">
          <strong>Share</strong>
          <a href="https://twitter.com/intent/tweet?text={share_text}&amp;url={share_url}" target="_blank" rel="noopener">X</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" rel="noopener">LinkedIn</a>
          <button type="button" data-copy-link="{canonical}">Copy link</button>
        </div>
      </section>

{render_article_nav(posts, index)}

      <section class="form-section" id="contact">
        <div class="form-panel">
          <p class="eyebrow">Stay in touch</p>
          <h2>Send a note.</h2>
          <p>If this reflection met you where you are, you can respond here in plain words.</p>
{contact_form_fields(f"New message about {post['title']}")}
        </div>
      </section>
    </main>

{FOOTER}

    <script src="/assets/js/site.js"></script>
  </body>
</html>
"""


def render_redirect_page(destination: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <link rel="canonical" href="{SITE_URL}{destination}">
    <meta http-equiv="refresh" content="0; url={destination}">
    <script>window.location.replace("{destination}");</script>
  </head>
  <body>
    <p>Redirecting to <a href="{destination}">{destination}</a>.</p>
  </body>
</html>
"""


def feed_html(post: dict) -> str:
    paragraphs = paragraph_text(post)
    return "".join(f"<p>{paragraph}</p>" for paragraph in paragraphs)


def render_feed(posts: list[dict]) -> str:
    items = []
    for post in posts:
        url = f"{SITE_URL}/writing/{post['route']}"
        pub_date = datetime.fromisoformat(post["published_date"].replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S GMT")
        items.append(
            f"""<item>
<title><![CDATA[{post["title"]}]]></title>
<description><![CDATA[{post["excerpt"]}]]></description>
<link>{url}</link>
<guid isPermaLink="true">{url}</guid>
<pubDate>{pub_date}</pubDate>
<content:encoded><![CDATA[{feed_html(post)}]]></content:encoded>
<dc:creator><![CDATA[Munya Chipunza]]></dc:creator>
</item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title><![CDATA[Munya Chipunza]]></title>
<description><![CDATA[Munya Chipunza]]></description>
<link>{SITE_URL}/writing</link>
<generator>Static site feed</generator>
<lastBuildDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
<atom:link href="{SITE_URL}/blog-feed.xml" rel="self" type="application/rss+xml"/>
{''.join(items)}
</channel>
</rss>
"""


def render_sitemap(posts: list[dict], total_pages: int) -> str:
    urls = [
        (f"{SITE_URL}/", "daily"),
        (f"{SITE_URL}/about", "monthly"),
        (f"{SITE_URL}/writing", "weekly"),
    ]
    for page_number in range(2, total_pages + 1):
        urls.append((f"{SITE_URL}/writing/page/{page_number}", "weekly"))
    for post in posts:
        urls.append((f"{SITE_URL}/writing/{post['route']}", "monthly"))

    url_xml = "\n".join(
        f"""  <url>
    <loc>{loc}</loc>
    <changefreq>{freq}</changefreq>
  </url>"""
        for loc, freq in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_xml}
</urlset>
"""


def update_homepage_feature_dates(posts: list[dict]) -> None:
    home_path = ROOT / "index.html"
    home = home_path.read_text(encoding="utf-8")
    replacements = {
        "February 2026 &bull; 3 min read": f"{format_date(posts[0]['published_date'])} &bull; {reading_time_label(posts[0]['minutes_to_read'])}",
        "November 2025 &bull; 3 min read": f"{format_date(posts[1]['published_date'])} &bull; {reading_time_label(posts[1]['minutes_to_read'])}",
        "October 2025 &bull; 3 min read": f"{format_date(posts[2]['published_date'])} &bull; {reading_time_label(posts[2]['minutes_to_read'])}",
    }
    for old, new in replacements.items():
        home = home.replace(old, new)
    home_path.write_text(home, encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    access_token = fetch_access_token()
    posts = fetch_posts(access_token)
    total_pages = (len(posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE

    for page_number in range(1, total_pages + 1):
        start = (page_number - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        page_posts = posts[start:end]
        archive_html = render_archive_page(page_posts, page_number, total_pages, len(posts))
        if page_number == 1:
            write(ROOT / "writing" / "index.html", archive_html)
            write(ROOT / "blog" / "index.html", render_redirect_page("/writing"))
        else:
            write(ROOT / "writing" / "page" / str(page_number) / "index.html", archive_html)
            write(ROOT / "blog" / "page" / str(page_number) / "index.html", render_redirect_page(f"/writing/page/{page_number}"))

    for index, post in enumerate(posts):
        article_html = render_article_page(post, posts, index)
        write(ROOT / "writing" / f"{post['route']}.html", article_html)
        write(ROOT / "writing" / post["route"] / "index.html", article_html)
        write(ROOT / "blog" / post["route"] / "index.html", render_redirect_page(f"/writing/{post['route']}"))
        write(ROOT / "post" / post["old_slug"] / "index.html", render_redirect_page(f"/writing/{post['route']}"))

    write(ROOT / "blog-feed.xml", render_feed(posts))
    write(ROOT / "sitemap.xml", render_sitemap(posts, total_pages))
    update_homepage_feature_dates(posts)


if __name__ == "__main__":
    main()
