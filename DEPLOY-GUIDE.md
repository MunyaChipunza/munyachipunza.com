# Munya Chipunza Site Deploy Guide

This site is a plain static website. You do not need Wix hosting for it.

## What is already prepared

- The live site files are in the root of this folder.
- `index.html`, `about.html`, `writing/`, `assets/`, `netlify.toml`, and the SEO files are already set up.
- Netlify clean URLs are already configured.
- The old Claude export folder `munyachipunza/` is ignored by `.gitignore` so it does not get pushed by mistake.

## Before you start

Your domain `munyachipunza.com` currently points to Wix nameservers:

- `ns6.wixdns.net`
- `ns7.wixdns.net`

That means you can stop paying for Wix site hosting, but you still need to either:

1. keep the domain at Wix and update the DNS there, or
2. transfer the domain to another registrar later.

The cheapest low-friction path is usually:

1. deploy the site on Netlify
2. point the existing Wix-managed domain to Netlify
3. cancel only the Wix site subscription after the new site is live

## Step 1: Create a GitHub repository

1. Create a free GitHub account if you do not already have one.
2. Create a new repository.
3. Upload the contents of this folder to that repository.

Important:

- Upload the root site files, not the parent `100. Zee` folder.
- If you use Git locally, the `.gitignore` file will keep `qa/`, logs, and the old `munyachipunza/` export out of the repo.

## Step 2: Deploy on Netlify

1. Create a free Netlify account.
2. Click `Add new site` -> `Import an existing project`.
3. Connect GitHub.
4. Select your repository.
5. Use these settings if Netlify asks:
   - Build command: leave blank
   - Publish directory: `.`
6. Click deploy.

Because this is a static site, the first deploy should be simple.

## Step 3: Test the Netlify preview URL

Before touching the domain, open the Netlify-generated URL and check:

- Home page loads
- About page loads
- Writing page loads
- At least one article opens
- Navigation works
- Newsletter form submits to the thank-you page

## Step 4: Connect the custom domain

1. In Netlify, open `Domain management`.
2. Add `munyachipunza.com`.
3. Add `www.munyachipunza.com` as well if you want both versions to work.
4. Netlify will show the exact DNS records it wants.

Because your nameservers are still at Wix, copy the DNS records from Netlify into the Wix DNS manager.

Do not guess these values. Use the exact records Netlify shows for your site.

## Step 5: Wait for DNS to update

After saving the DNS changes in Wix:

1. Wait for propagation.
2. Recheck the site in Netlify.
3. Recheck `munyachipunza.com`.
4. Confirm that the custom domain is marked verified in Netlify.

## Step 6: Cancel Wix hosting only after the new site works

Do not cancel first.

Cancel the Wix site subscription only when:

- the Netlify site is live
- the custom domain is working
- you have checked the main pages on desktop and mobile

You may still keep the domain registered there for now if that is the easiest option.

## Updating the site later

### Edit copy or layout

Update these files directly:

- `index.html`
- `about.html`
- `writing/index.html`
- `writing/*.html`
- `assets/css/style.css`
- `assets/js/site.js`

### Add a new article

1. Duplicate one of the files in `writing/`.
2. Rename it with the new slug.
3. Update the article title, intro, body, meta, and prev/next links.
4. Add the article card to `writing/index.html`.
5. If you want it featured on the homepage, update `index.html`.
6. Add the new URL to `sitemap.xml`.
7. Commit and push to GitHub.
8. Netlify will redeploy automatically.

## Folder map

- `assets/css/style.css` -> shared site styling
- `assets/js/site.js` -> navigation, reveal animations, copy-link button
- `assets/images/` -> local site images
- `writing/` -> writing index and article pages
- `netlify.toml` -> clean URL rules and headers
- `robots.txt`, `sitemap.xml`, `site.webmanifest`, `favicon.svg` -> SEO and browser metadata

## If you want the old nested folder removed

There is an older extracted folder named `munyachipunza/` still sitting inside this directory as a backup copy of the first Claude export.

It is not part of the new build.

If you want, remove it only after you are satisfied with the new site and have backed up anything you still need from it.
