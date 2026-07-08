# cinema-systems.com — static site

Static site for Cinema Systems (custom home theater installation, Los Angeles & Orange County),
migrated from Weebly in July 2026. Hosted on GitHub Pages.

## Structure
- Root `*.html` — main pages (services, city pages, projects, contact)
- `blog/` — 171 blog posts plus archive/category/pagination pages
- `uploads/`, `files/` — images, theme CSS/JS, self-hosted videos (`files/videos/`)
- `cdn2.editmysite.com/` — vendored Weebly platform CSS/JS/fonts (Weebly's CDN will shut down)
- Legacy pretty-URL dirs (`services/…`, `contact-us/`, etc.) — redirect stubs preserving old backlinks
- `sitemap.xml`, `robots.txt`, `404.html`, `CNAME`

## DNS cutover (do this at your domain registrar / Cloudflare)
1. In the GitHub repo: Settings → Pages → confirm custom domain `www.cinema-systems.com` and enable **Enforce HTTPS** (after DNS propagates).
2. At your DNS provider:
   - `www` CNAME → `<github-username>.github.io`
   - Apex `cinema-systems.com` A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. **Do NOT touch MX records** — email for info@/johnkim@/jennykim@cinema-systems.com must keep working.
4. Verify, then cancel Weebly.

## Editing
Plain HTML — edit pages directly and push to `main`; GitHub Pages redeploys automatically.
