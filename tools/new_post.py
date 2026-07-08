#!/usr/bin/env python3
"""Publish a new blog post into the cinema-systems.com static site.

Usage:  python3 tools/new_post.py post.json

post.json:
{
  "slug": "kebab-case-url-slug",
  "title": "Post Title",
  "desc": "Meta description, <=160 chars.",
  "iso": "2026-07-14",
  "img": "some-image-750x500_orig.jpg",
  "img_alt": "Descriptive alt text with keywords",
  "body": "<h2 class=\"wsite-content-title\" ...>...</h2><div class=\"paragraph\">...</div>..."
}

Handles: post page from theme template, blog.html index entry, monthly
archive page (creates if new month), archive sidebar links on every blog
page, sitemap.xml entry. Run from the repo root. Refuses to overwrite an
existing post.
"""
import re, os, sys, json, glob, html as H

BASE = "https://www.cinema-systems.com"
UPDIR = "uploads/1/4/9/4/149484915/"
MONTHNAMES = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
              6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
              11: "November", 12: "December"}

def die(msg):
    print("ERROR:", msg); sys.exit(1)

def main():
    if len(sys.argv) != 2:
        die("usage: python3 tools/new_post.py post.json")
    p = json.load(open(sys.argv[1]))
    for k in ("slug", "title", "desc", "iso", "img", "img_alt", "body"):
        if not p.get(k): die(f"missing field: {k}")
    if not re.fullmatch(r"[a-z0-9-]+", p["slug"]): die("slug must be kebab-case")
    yy, mm, dd = (int(x) for x in p["iso"].split("-"))
    date = f"{mm}/{dd}/{yy}"
    mkey, mlabel = f"{mm:02d}-{yy}", f"{MONTHNAMES[mm]} {yy}"
    img_rel = "/" + UPDIR + p["img"]
    post_path = f"blog/{p['slug']}.html"

    if not os.path.exists("blog") or not os.path.exists("tools/post_template.html"):
        die("run from the repo root")
    if os.path.exists(post_path): die(f"post already exists: {post_path}")
    if not os.path.exists(UPDIR + p["img"]): die(f"image not found: {UPDIR}{p['img']}")
    if len(p["desc"]) > 170: die("desc too long (>170 chars)")

    def fill(doc):
        return (doc.replace("{{TITLE}}", H.escape(p["title"], quote=False))
                   .replace("{{SLUG}}", p["slug"])
                   .replace("{{DESC}}", H.escape(p["desc"], quote=True))
                   .replace("{{IMG_ALT}}", H.escape(p["img_alt"], quote=True))
                   .replace("{{IMG}}", img_rel)
                   .replace("{{DATE}}", date)
                   .replace("{{ISO}}", p["iso"])
                   .replace("{{BODY}}", p["body"].strip()))

    open(post_path, "w", encoding="utf-8").write(
        fill(open("tools/post_template.html", encoding="utf-8").read()))

    lead = (f'<div><div class="wsite-image wsite-image-border-none" '
            f'style="padding-top:10px;padding-bottom:10px;margin-left:0;margin-right:0;text-align:center">'
            f' <img src="{img_rel}" alt="{H.escape(p["img_alt"], quote=True)}" style="width:auto;max-width:100%" /> </div></div>')
    def entry(href_prefix):
        return f'''<div id="blog-post-{p['iso'].replace('-','')}{p['slug'][:8]}" class="blog-post">
\t<div class="blog-header">
\t\t<h2 class="blog-title"><a class="blog-title-link blog-link" href="{href_prefix}{p['slug']}.html">{H.escape(p['title'], quote=False)}</a></h2>
\t\t<p class="blog-date"><span class="date-text">{date}</span></p>
\t</div>
\t<div class="blog-content">
\t\t{lead}
\t\t<div class="paragraph">{H.escape(p['desc'], quote=False)} <a href="{href_prefix}{p['slug']}.html"><strong>Read More &raquo;</strong></a></div>
\t</div>
</div>
<div class="blog-post-separator"></div>
'''
    idx = open("blog.html", encoding="utf-8").read()
    first = re.search(r'<div id="blog-post-[^"]*" class="blog-post">', idx).start()
    open("blog.html", "w", encoding="utf-8").write(idx[:first] + entry("blog/") + idx[first:])

    apath = f"blog/archives/{mkey}.html"
    if os.path.exists(apath):
        doc = open(apath, encoding="utf-8").read()
        m = re.search(r'<div id="blog-post-[^"]*" class="blog-post">', doc)
        doc = doc[:m.start()] + entry("../") + doc[m.start():]
        open(apath, "w", encoding="utf-8").write(doc)
        new_month = False
    else:
        doc = open("tools/archive_template.html", encoding="utf-8").read()
        doc = doc.replace("{{MKEY}}", mkey).replace("{{MLABEL}}", mlabel).replace("{{ENTRIES}}", entry("../"))
        doc = doc.replace(f'{mkey}.html" class="blog-link">', f'{mkey}.html" class="blog-link active">', 1)
        open(apath, "w", encoding="utf-8").write(doc)
        new_month = True

    patched = 0
    if new_month:
        months = []
        for f in glob.glob("blog/archives/??-????.html"):
            k = os.path.basename(f)[:-5]
            if k != mkey: months.append((int(k[3:]), int(k[:2]), k))
        prev_key = max(months)[2]
        prev_label = f"{MONTHNAMES[int(prev_key[:2])]} {prev_key[3:]}"
        for f in glob.glob("**/*.html", recursive=True):
            doc = open(f, encoding="utf-8", errors="replace").read()
            if 'class="blog-archive-list"' not in doc or f"{mkey}.html" in doc: continue
            m = re.search(rf'<a href="([^"]*?){prev_key}\.html" class="blog-link( active)?">{prev_label}</a>', doc)
            if not m: continue
            link = f'<a href="{m.group(1)}{mkey}.html" class="blog-link">{mlabel}</a>\n\t\t<br />\n\t\t'
            doc = doc.replace(m.group(0), link + m.group(0), 1)
            open(f, "w", encoding="utf-8").write(doc)
            patched += 1

    sm = open("sitemap.xml", encoding="utf-8").read()
    if f"/blog/{p['slug']}<" not in sm:
        sm = sm.replace("</urlset>",
                        f"  <url><loc>{BASE}/blog/{p['slug']}</loc><lastmod>{p['iso']}</lastmod></url>\n</urlset>")
        open("sitemap.xml", "w", encoding="utf-8").write(sm)

    doc = open(post_path, encoding="utf-8").read()
    import re as _re
    if _re.search(r"\{\{[A-Z_]+\}\}", doc): die("unfilled template token in generated post")
    for m in re.finditer(r'(?:src|href)="(/[^"]+)"', doc):
        u = m.group(1).split("#")[0].split("?")[0].lstrip("/")
        if u and not os.path.exists(u) and not os.path.exists(u + ".html"):
            die(f"broken reference in post: /{u}")
    print(f"published: {post_path}")
    print(f"index + sitemap updated; archive {apath}" + (f" created, {patched} sidebars updated" if new_month else " updated"))

if __name__ == "__main__":
    main()
