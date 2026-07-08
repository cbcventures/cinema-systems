# Blog publishing tools

`python3 tools/new_post.py post.json` — publishes one post: creates the
post page from the theme template, prepends the blog.html index entry,
creates/updates the monthly archive page and sidebar links, and adds the
sitemap entry. See the docstring in new_post.py for the post.json schema.

Style guide for post bodies (match existing posts):
- 600-900 words of HTML: sections as
  `<h2 class="wsite-content-title" style="text-align:left;">...</h2>`,
  paragraphs as `<div class="paragraph">...</div>`
- Target custom home theater / smart home / home network keywords
- 2-4 internal links (service pages like /home-theater-installation.html,
  /home-automation.html, /surround-sound.html, city pages, related /blog/ posts)
- End with a call to action: phone <a href="tel:+12135456169">213-545-6169</a>
  and/or <a href="/contact.html">contact</a>
- Meta description under 160 chars; unique, keyword-bearing title
- img: pick a topically fitting file from uploads/1/4/9/4/149484915/
  (prefer *_orig.* full-size versions); write descriptive keyworded img_alt
