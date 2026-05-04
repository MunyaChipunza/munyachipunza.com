# Munya Chipunza Site Deploy Guide

This site is now set up as a static GitHub Pages website on `munyachipunza.com`.

## What is already done

- The live site files are in the root of this folder.
- GitHub repository created: `MunyaChipunza/munyachipunza.com`
- GitHub Pages repository created: `MunyaChipunza/MunyaChipunza.github.io`
- Custom domain configured: `munyachipunza.com`
- Wix DNS updated to point the domain at GitHub Pages

## What this means

- You no longer need Wix site hosting for this website.
- The domain can stay registered at Wix for now.
- If you want to stop paying Wix completely later, transfer the domain to another registrar after the site has been stable for a while.

## Current hosting setup

- Live domain: `https://munyachipunza.com`
- Preferred domain: apex, not `www`
- `www.munyachipunza.com` is configured to point back to the apex site
- GitHub Pages serves the site

## One thing that may still be catching up

GitHub Pages issues the SSL certificate separately after DNS is correct.

DNS is already correct and GitHub is already serving the site on HTTP. If HTTPS is not active yet, that is a propagation delay on GitHub's side, not a site-code problem.

## Updating the site later

Edit these files directly:

- `index.html`
- `about.html`
- `writing/index.html`
- `writing/*.html`
- `assets/css/style.css`
- `assets/js/site.js`

## Publishing future changes

1. Edit the files locally in this folder.
2. Commit the changes to Git.
3. Push to the GitHub Pages repository.
4. GitHub Pages republishes the site automatically.

## Newsletter behavior

This site is hosted on GitHub Pages, which does not provide built-in form handling.

To avoid a fake signup form, the email capture buttons now open the visitor's email app and pre-fill a message to `info@munyachipunza.com`.

If you later want true subscriber collection without using Wix, add a separate form service such as Buttondown, ConvertKit, MailerLite, or Formspree.

## Files that are still here on purpose

- `munyachipunza/` is the older Claude export kept as a local backup.
- `qa/` contains local verification screenshots.
- `netlify.toml` is a leftover config file from the earlier Netlify direction and is not used by GitHub Pages.

## Safe cleanup later

Once you are satisfied with the live site, you can remove:

- `munyachipunza/`
- `qa/`
- old local log files

Do not remove them if you still want the backup or QA evidence.
