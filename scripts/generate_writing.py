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
SITE_DESCRIPTION = "Personal essays by Munya Chipunza on faith, resilience, fatherhood, grief, leadership, and finding hope in hard seasons."
BLOG_APP_ID = "14bcded7-0066-7c35-14d7-466cb3f09103"
POSTS_PER_PAGE = 5
ASSET_VERSION = "20260509a"
GOOGLE_ANALYTICS_TAG = """    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4J3RHW9XRZ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-4J3RHW9XRZ');
    </script>"""
ICON_LINKS = """    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">"""
SUBSCRIBE_MODE = "buttondown"  # Use "holding" while Buttondown account review is pending.
CONTACT_FORM_ACTION = "https://formsubmit.co/02774129a6ffd7df5b31b69ff0886e06"
CONTACT_FORM_AJAX = "https://formsubmit.co/ajax/02774129a6ffd7df5b31b69ff0886e06"
CONTACT_SUCCESS_URL = f"{SITE_URL}/thanks"
BUTTONDOWN_USERNAME = "munyachipunza"
BUTTONDOWN_SUBSCRIBE_ACTION = f"https://buttondown.com/api/emails/embed-subscribe/{BUTTONDOWN_USERNAME}"

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

LOCAL_POSTS = [
    {
        "old_slug": "the-people-who-stay",
        "route": "the-people-who-stay",
        "tag": "Friendship",
        "title": "The People Who Stay",
        "summary": "A reflection on rare friendship, costly loyalty, and the people God sends so we do not carry hard seasons alone.",
        "excerpt": "A reflection on rare friendship, costly loyalty, and the people God sends so we do not carry hard seasons alone. The people who stay when it costs something are rare.",
        "published_date": "2026-05-08T12:00:00Z",
        "updated_date": "2026-05-08T12:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "There is a kind of friendship that only reveals itself in the hard seasons.",
            "Not the friendship of convenience. Not the kind that shows up when things are easy and the room is full of good news. The kind that walks toward you when everyone else is quietly walking away.",
            "I have been thinking about those people this week.",
            "The ones who did not wait to be asked. Who showed up in the middle of something they had no obligation to enter. Who rearranged their lives, quietly and without ceremony, because they had decided a long time ago that you were worth showing up for.",
            "I think about Jonathan.",
            "In a season where loyalty to David could have cost him everything - his position, his father's favour, his own claim to a future - Jonathan stayed. He warned David of danger. He covered for him. He made a covenant not because it was strategic but because something deep in him had decided: this person matters.",
            "The Bible says Jonathan loved David as his own soul.",
            "That is not a feeling. That is a decision.",
            "I think about Ruth.",
            "When Naomi told her daughters-in-law to go back to their own people, Orpah left. Reasonably. Understandably. It made sense to go. But Ruth stayed. And what she said to Naomi has outlasted both of them: where you go I will go. Where you die I will die.",
            "Ruth did not stay because the situation looked promising. She stayed because the relationship was worth more than the circumstances.",
            "I think about Paul and Silas, side by side in a prison at midnight. No plan. No exit strategy. Just two people who had decided to go through it together. And they sang.",
            "Some of us are in seasons where we need people like that.",
            "Not people with answers. Not people who can fix the thing that is broken. Just people who will sit in the midnight with you and not make it feel like you are alone in it.",
            "If you have even one person like that - a friend who drives across a city, a spouse who keeps showing up, a sibling who calls when it gets quiet, someone who played a role they had no obligation to play just because you needed it - do not take that lightly.",
            "That person is not an accident in your life.",
            "They are a gift from a God who knows exactly how heavy the seasons get, and who has always believed you should not carry them alone.",
            "Tend those relationships. Honour them. Show up for those people the way they show up for you.",
            "Because the world will always have rooms full of people who know your name.",
            "But the people who stay when it costs something - those are rare.",
            "And they are worth everything.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-day-you-did-everything-right",
        "route": "the-day-you-did-everything-right",
        "tag": "Faith",
        "title": "The Day You Did Everything Right",
        "summary": "A reflection for the days when you gave your best, the result did not come, and the quiet question rose: was any of it worth it?",
        "excerpt": "A reflection for the days when you gave your best, the result did not come, and the quiet question rose: was any of it worth it? You were seen today.",
        "published_date": "2026-05-07T12:00:00Z",
        "updated_date": "2026-05-07T12:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "Some days you do everything right.",
            "And it still doesn't work out.",
            "You gave what you had. You showed up when it cost you something. You chose the harder, better thing - and the result you needed did not come. The door stayed closed. The person didn't respond. The situation didn't shift. The morning looked exactly like the one before it.",
            "And somewhere in the quiet, a question rises.",
            "Was any of it worth it?",
            "I have sat with that question. I think most of us have, if we are honest.",
            "There is a kind of tired that has nothing to do with sleep. It is the tired that comes from giving your best and finding the world unmoved. From doing right when wrong would have been easier, and receiving nothing for it. From holding on, quietly, faithfully, while no one is watching and nothing is changing.",
            "That tired is real. And it deserves to be named.",
            "But I have come to believe something about those days.",
            "There is a woman in the Bible who had been suffering for twelve years. She had tried everything available to her. Nothing worked. Everything she had was gone. By every measure, her situation was unchanged.",
            "And then she stopped waiting for the right circumstance to rescue her.",
            "She pushed through a crowd and reached.",
            "Not loudly. Not with a speech or a demand. Just a reach. A quiet, desperate, faithful reach toward the only one she believed could actually help her.",
            "And everything changed.",
            "Not because she finally earned it.",
            "Because she finally reached in the right direction.",
            "Some seasons are not asking you to do more.",
            "They are asking you to reach differently. To stop measuring your worth by what the day returned to you. To remember that the most important witness to your life is not the one who did not notice, did not respond, did not show up.",
            "You were seen today.",
            "In the reaching. In the showing up. In the quiet faithfulness that nobody applauded and nobody counted.",
            "Every bit of it was seen.",
            "And the one who saw it - the one who has always seen it - has never once looked at your life and found it lacking. Not on the hard days. Not on the empty ones. Not on the days you drove home in silence wondering if you were enough.",
            "You were enough then. You are enough now.",
            "Rest in that.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "what-they-see-first",
        "route": "what-they-see-first",
        "tag": "Identity",
        "title": "What They See First",
        "summary": "A reflection on being judged by the surface, and the steady comfort of being seen by God more truthfully than people ever do.",
        "excerpt": "A reflection on being judged by the surface, and the steady comfort of being seen by God more truthfully than people ever do. What people see first is rarely what God sees at all.",
        "published_date": "2026-05-06T12:00:00Z",
        "updated_date": "2026-05-06T12:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "There are people who will form their opinion before the story is finished.",
            "They will look at what is immediately visible - the obvious difficulty, the thing that makes you move differently - and they will decide there. Before the numbers. Before the output. Before they have stayed long enough to understand what they are actually looking at.",
            "I watched someone be reduced to their surface today.",
            "And it did something to me. Not just frustration. Something older than that. A kind of grief that comes from witnessing a person be unseen when their life is quietly telling a different story.",
            "I kept thinking about David.",
            "When Samuel came to Jesse's house to anoint the next king of Israel, the sons lined up. Tall. Strong. Impressive. The kind of men you look at and immediately believe. And Samuel nearly got it wrong. He looked at what was standing in front of him and thought, this must be the one.",
            "But God said: I do not see as man sees. Man looks at the outward appearance. I look at the heart.",
            "David was still in the fields. Nobody had even thought to call him in.",
            "The one God had already chosen was the one nobody considered worth presenting.",
            "I wonder if you have ever been that person. Left in the field. Not called into the room. Measured by what is immediately visible before anyone asked what you are actually made of.",
            "The quiet output that nobody is tracking. The resilience that does not announce itself. The work happening beneath the surface that the loudest voice in the room has not noticed yet.",
            "It does not mean you are invisible.",
            "It means you are being seen by a different set of eyes.",
            "The ones that matter most have always looked past the surface. They looked at a shepherd boy and saw a king. They looked at a widow with almost nothing and called it abundance. They looked at a man in chains and wrote letters that are still changing lives.",
            "Your story is not finished.",
            "What people see first is rarely what God sees at all.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "blank-page-was-still-there",
        "route": "blank-page-was-still-there",
        "tag": "Resilience",
        "title": "The Blank Page Was Still There",
        "summary": "A quiet return after a season of silence, and a reminder that some pauses are survival, not failure.",
        "excerpt": "A quiet return after a season of silence, and a reminder that some pauses are survival, not failure. The blank page does not hold your absence against you. It just opens.",
        "published_date": "2026-05-05T12:00:00Z",
        "updated_date": "2026-05-05T12:00:00Z",
        "minutes_to_read": 2,
        "paragraphs": [
            "I didn't plan to disappear.",
            "That's the thing about going quiet — it rarely starts with a decision. It starts with one week being harder than usual. Then that week becomes two. And somewhere in the middle of it, writing stops feeling like something you do and starts feeling like something you owe people. A debt you're not ready to pay.",
            "So you stay silent. And the longer the silence, the heavier the return feels.",
            "I've been away from this page for a while. Not because I ran out of things to say — if anything, the opposite. Life handed me more than I knew how to write about. Some seasons are like that. They're too full, too raw, too close to the bone to turn into words while you're still inside them.",
            "But here's what I came back to find: the blank page was still there. Waiting. Not accusing. Just waiting.",
            "There's a version of this story I used to believe — that if you stop, you forfeit something. That consistency is the price of being taken seriously. That the gap in your timeline is proof of something. Weakness, maybe. Or lack of discipline.",
            "I don't believe that anymore.",
            "I think some pauses are not failures. They're survival. They're you doing what needed to be done — holding things together, showing up where it mattered most, getting through the part of life that doesn't pause just because you need it to.",
            "The writing will still be here when you come back.",
            "I don't know who needs to hear this today. Maybe you stopped writing. Or praying. Or going to the gym. Or calling the people who matter. Maybe you put something down weeks ago — something that used to give you life — because the weight of everything else was too much.",
            "I want to tell you: the return doesn't have to be an event. You don't need to announce it. You don't need to explain the gap. You don't need to come back louder or more polished to make up for the time away.",
            "You just need to start again. Quietly, if that's all you have.",
            "One sentence. One prayer. One kilometre. One message.",
            "The blank page doesn't hold the absence against you. It just opens.",
            "I'm back. And whatever you put down — whenever you're ready — so are you.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    }
]


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


def decode_html_entities(text: str) -> str:
    text = str(text)
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    return text


def clean_excerpt(text: str) -> str:
    text = normalize_text(text)
    text = " ".join(text.replace("\u00a0", " ").split())
    return text.replace("You ’re", "You’re").replace("you  ", "you ").replace("thank you  ", "thank you ").strip()


def normalize_text(text: str, *, strip_edges: bool = True) -> str:
    text = decode_html_entities(text)
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


def escape_text(text: str, *, strip_edges: bool = True) -> str:
    return html.escape(normalize_text(text, strip_edges=strip_edges), quote=False)


def escape_attr(text: str, *, strip_edges: bool = True) -> str:
    # Double-quoted attributes only need double quotes escaped; apostrophes should
    # remain readable so they never appear on-page as encoded leftovers.
    return html.escape(normalize_text(text, strip_edges=strip_edges), quote=True).replace("&#x27;", "'")


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
        rendered = escape_text(node.get("textData", {}).get("text", ""), strip_edges=False)
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
            return f'<a href="{escape_attr(url)}" target="_blank" rel="noopener">{children}</a>'
    return children


def paragraph_text(post: dict) -> list[str]:
    if post.get("paragraphs"):
        return [escape_text(paragraph) for paragraph in post["paragraphs"] if paragraph.strip()]

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
    return [escape_text(fallback)] if fallback else []


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


def summary_source(post: dict) -> str:
    return clean_excerpt(post.get("summary") or first_paragraph_plain(post) or post["excerpt"])


def render_article_body(post: dict) -> str:
    paragraphs = paragraph_text(post)
    blocks = []
    for index, paragraph in enumerate(paragraphs):
        class_attr = ' class="lead"' if index == 0 else ""
        blocks.append(f"<p{class_attr}>{paragraph}</p>")
    return "\n          ".join(blocks)


def article_description(post: dict) -> str:
    return text_snippet(summary_source(post), 158)


def article_intro(post: dict) -> str:
    return text_snippet(summary_source(post), 210)


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
              <a class="social-link" href="https://www.instagram.com/iam_munya/" target="_blank" rel="noopener" aria-label="Instagram">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"></path></svg>
              </a>
              <a class="social-link" href="https://www.linkedin.com/in/munya-chipunza-73a1a039/" target="_blank" rel="noopener" aria-label="LinkedIn">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452H16.893V14.87c0-1.333-.027-3.045-1.856-3.045-1.858 0-2.142 1.45-2.142 2.948v5.68H9.34V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.124 2.062 2.062 0 0 1 0 4.124zM7.119 20.452H3.555V9H7.12v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
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


def contact_form_fields(subject: str, source: str = "contact") -> str:
    return f"""          <form class="signup-form full" name="contact" method="POST" action="{CONTACT_FORM_ACTION}" data-contact-form data-ajax-action="{CONTACT_FORM_AJAX}" data-analytics-source="{escape_attr(source)}" id="contact-form">
            <input type="hidden" name="_subject" value="{escape_attr(subject)}">
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


def subscribe_form_fields(subject: str, source: str) -> str:
    if SUBSCRIBE_MODE == "buttondown":
        return f"""          <form class="signup-form subscribe-form" name="subscribe" method="POST" action="{BUTTONDOWN_SUBSCRIBE_ACTION}" data-subscribe-form data-analytics-source="{escape_attr(source)}">
            <input type="hidden" value="1" name="embed">
            <input type="hidden" name="metadata__source" value="{escape_attr(source)}">
            <input type="email" name="email" placeholder="Your email address" autocomplete="email" aria-label="Your email address" required>
            <button class="button button-primary" type="submit">Subscribe</button>
          </form>
          <p class="form-note" data-form-status aria-live="polite">Occasional reflections. Please check your inbox to confirm.</p>"""

    if SUBSCRIBE_MODE == "holding":
        return f"""          <form class="signup-form subscribe-form" name="subscribe" method="POST" action="{CONTACT_FORM_ACTION}" data-subscribe-form data-ajax-action="{CONTACT_FORM_AJAX}" data-analytics-source="{escape_attr(source)}" data-pending-message="Saving your subscription..." data-success-message="Thank you. You're on the list." data-success-button-label="Subscribed">
            <input type="hidden" name="_subject" value="{escape_attr(subject)}">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="form_type" value="newsletter_subscription">
            <input type="hidden" name="status" value="holding until Buttondown account review is approved">
            <input type="hidden" name="interest" value="New reflections by email">
            <input type="hidden" name="source" value="{escape_attr(source)}">
            <p class="sr-only">
              <label>Do not fill this out if you are human <input name="_honey" tabindex="-1" autocomplete="off"></label>
            </p>
            <input type="email" name="email" placeholder="Your email address" autocomplete="email" aria-label="Your email address" required>
            <button class="button button-primary" type="submit">Subscribe</button>
          </form>
          <p class="form-note" data-form-status aria-live="polite">Occasional reflections. No noise.</p>"""

    raise ValueError(f"Unsupported SUBSCRIBE_MODE: {SUBSCRIBE_MODE}")


def render_subscribe_section(title: str, description: str, source: str) -> str:
    return f"""      <section class="subscribe-section">
        <div class="subscribe-panel will-reveal">
          <div class="subscribe-copy">
            <p class="eyebrow">By email</p>
            <h2>{escape_text(title)}</h2>
            <p>{escape_text(description)}</p>
          </div>
          <div class="subscribe-form-shell">
{subscribe_form_fields("New writing subscriber from munyachipunza.com", source)}
          </div>
        </div>
      </section>"""


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
            <p class="article-tag">{escape_text(post["tag"])}</p>
            <h2 class="article-card-title">{escape_text(post["title"])}</h2>
            <p>{escape_text(text_snippet(post["excerpt"] or first_paragraph_plain(post), 260))}</p>
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
    description = SITE_DESCRIPTION
    hero_line = "Short reflections on faith, identity, grief, peace, and the quiet interior work required to stay human under pressure."
    page_note = f"Page {page_number} of {total_pages} &middot; {total_posts} published reflections."
    canonical = archive_canonical(page_number)
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_text(title)}</title>
    <meta name="description" content="{escape_attr(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{escape_attr(title)}">
    <meta property="og:description" content="{escape_attr(description)}">
    <meta property="og:site_name" content="Munya Chipunza">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE_URL}/assets/images/munya-home.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_attr(title)}">
    <meta name="twitter:description" content="{escape_attr(description)}">
    <meta name="twitter:image" content="{SITE_URL}/assets/images/munya-home.jpg">
    <link rel="alternate" href="{SITE_URL}/blog-feed.xml" title="Munya Chipunza - RSS" type="application/rss+xml">
{ICON_LINKS}
    <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/assets/css/style.css">
{GOOGLE_ANALYTICS_TAG}
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

{render_subscribe_section("Get new reflections by email.", "Prefer email to scrolling? Join the list and I'll send the next reflection quietly when it is ready.", f"writing archive page {page_number}")}

{FORM_SECTION}
    </main>

{FOOTER}

    <script src="/assets/js/site.js?v={ASSET_VERSION}"></script>
  </body>
</html>
"""


def render_article_nav(posts: list[dict], index: int) -> str:
    newer = posts[index - 1] if index > 0 else None
    older = posts[index + 1] if index + 1 < len(posts) else None

    left = (
        f"""        <a href="/writing/{newer["route"]}">
          <span>Newer reflection</span>
          <strong>{escape_text(newer["title"])}</strong>
        </a>"""
        if newer
        else "        <div></div>"
    )
    right = (
        f"""        <a href="/writing/{older["route"]}">
          <span>Older reflection</span>
          <strong>{escape_text(older["title"])}</strong>
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
    <title>{escape_text(title)}</title>
    <meta name="description" content="{escape_attr(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{escape_attr(title)}">
    <meta property="og:description" content="{escape_attr(description)}">
    <meta property="og:site_name" content="Munya Chipunza">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{escape_attr(post['image_url'])}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_attr(title)}">
    <meta name="twitter:description" content="{escape_attr(description)}">
    <meta name="twitter:image" content="{escape_attr(post['image_url'])}">
    <meta property="article:published_time" content="{post['published_date']}">
    <meta property="article:modified_time" content="{post['updated_date']}">
    <link rel="alternate" href="{SITE_URL}/blog-feed.xml" title="Munya Chipunza - RSS" type="application/rss+xml">
{ICON_LINKS}
    <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/assets/css/style.css">
{GOOGLE_ANALYTICS_TAG}
  </head>
  <body>
{header("writing", "/writing", "All writing")}

    <main>
      <section class="article-hero">
        <a class="article-back" href="/writing">&larr; Back to all writing</a>
        <p class="post-tag">{escape_text(post["tag"])}</p>
        <h1>{escape_text(post["title"])}</h1>
        <p class="article-intro">{escape_text(intro)}</p>
        <div class="post-meta">
          <img src="/assets/images/munya-avatar.webp" alt="Munya Chipunza" width="256" height="256" decoding="async">
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

{render_subscribe_section("Get the next reflection by email.", "If this piece stayed with you, the next one can meet you in your inbox.", f"article: {post['route']}")}

      <section class="share-strip">
        <div class="share-list">
          <strong>Share</strong>
          <div class="share-actions">
            <a class="share-icon" href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" rel="noopener" data-share-platform="facebook" aria-label="Share on Facebook" title="Share on Facebook">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"></path></svg>
            </a>
            <a class="share-icon" href="https://www.threads.com/intent/post?text={share_text}%20{share_url}" target="_blank" rel="noopener" data-share-platform="threads" aria-label="Share on Threads" title="Share on Threads">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"></path></svg>
            </a>
            <a class="share-icon" href="https://twitter.com/intent/tweet?text={share_text}&amp;url={share_url}" target="_blank" rel="noopener" data-share-platform="x" aria-label="Share on X" title="Share on X">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"></path></svg>
            </a>
            <a class="share-icon" href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" rel="noopener" data-share-platform="linkedin" aria-label="Share on LinkedIn" title="Share on LinkedIn">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452H16.893V14.87c0-1.333-.027-3.045-1.856-3.045-1.858 0-2.142 1.45-2.142 2.948v5.68H9.34V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.124 2.062 2.062 0 0 1 0 4.124zM7.119 20.452H3.555V9H7.12v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
            </a>
            <button class="share-icon share-copy" type="button" data-copy-link="{canonical}" data-share-platform="copy_link" aria-label="Copy article link" title="Copy article link">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 7a3 3 0 0 1 3-3h6a3 3 0 0 1 0 6h-2v-2h2a1 1 0 1 0 0-2h-6a1 1 0 1 0 0 2v2a3 3 0 0 1-3-3Zm6 10a3 3 0 0 1-3 3H6a3 3 0 1 1 0-6h2v2H6a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2v-2a3 3 0 0 1 3 3Zm-8-4h10v-2H7v2Z"></path></svg>
              <span class="sr-only" data-copy-text>Copy article link</span>
            </button>
          </div>
        </div>
      </section>

{render_article_nav(posts, index)}

      <section class="form-section" id="contact">
        <div class="form-panel">
          <p class="eyebrow">Stay in touch</p>
          <h2>Send a note.</h2>
          <p>If this reflection met you where you are, you can respond here in plain words.</p>
{contact_form_fields(f"New message about {post['title']}", f"article: {post['route']}")}
        </div>
      </section>
    </main>

{FOOTER}

    <script src="/assets/js/site.js?v={ASSET_VERSION}"></script>
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


def render_homepage_feature_grid(posts: list[dict]) -> str:
    lead_post = posts[0]
    side_posts = posts[1:3]
    main_excerpt = text_snippet(lead_post.get("summary") or lead_post["excerpt"] or first_paragraph_plain(lead_post), 165)

    side_cards = []
    for post in side_posts:
        side_cards.append(
            f"""            <a class="mini-card will-reveal" href="/writing/{post["route"]}">
              <span class="mini-tag">{escape_text(post["tag"])}</span>
              <h3 class="mini-title">{escape_text(post["title"])}</h3>
              <p>{escape_text(text_snippet(post.get("summary") or post["excerpt"] or first_paragraph_plain(post), 110))}</p>
              <div class="feature-meta">{format_date(post["published_date"])} &bull; {reading_time_label(post["minutes_to_read"])}</div>
            </a>"""
        )

    return f"""        <div class="feature-grid">
          <a class="feature-card will-reveal" href="/writing/{lead_post["route"]}">
            <span class="feature-tag">{escape_text(lead_post["tag"])}</span>
            <h3 class="feature-title">{escape_text(lead_post["title"])}</h3>
            <p class="feature-excerpt">
              {escape_text(main_excerpt)}
            </p>
            <div class="feature-meta">{format_date(lead_post["published_date"])} &bull; {reading_time_label(lead_post["minutes_to_read"])}</div>
          </a>

          <div class="feature-side">
{chr(10).join(side_cards)}
          </div>
        </div>"""


def update_homepage_sections(posts: list[dict]) -> None:
    home_path = ROOT / "index.html"
    home = home_path.read_text(encoding="utf-8")
    home = re.sub(
        r'        <div class="feature-grid">.*?        </div>\r?\n      </section>',
        f"{render_homepage_feature_grid(posts)}\n      </section>",
        home,
        count=1,
        flags=re.S,
    )
    home = re.sub(
        r'      <section class="subscribe-section">.*?      </section>',
        render_subscribe_section(
            "Get new reflections by email.",
            "If the writing helps, subscribe here and I will send the next reflection quietly when it is ready.",
            "homepage",
        ),
        home,
        count=1,
        flags=re.S,
    )
    home_path.write_text(home, encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    access_token = fetch_access_token()
    posts = fetch_posts(access_token) + [dict(post) for post in LOCAL_POSTS]
    posts.sort(key=lambda post: post["published_date"], reverse=True)
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
        if post.get("old_slug"):
            write(ROOT / "post" / post["old_slug"] / "index.html", render_redirect_page(f"/writing/{post['route']}"))

    write(ROOT / "blog-feed.xml", render_feed(posts))
    write(ROOT / "sitemap.xml", render_sitemap(posts, total_pages))
    update_homepage_sections(posts)


if __name__ == "__main__":
    main()
