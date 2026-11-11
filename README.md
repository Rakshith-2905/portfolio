# Rakshith Subramanyam — personal site

A Jekyll site. GitHub Pages builds it automatically — you don't run a build step to publish.

## Publish a new post (the whole workflow)

1. Create a file in `_posts/` named `YYYY-MM-DD-your-slug.md`.
2. Put this at the top (the front matter):

   ```
   ---
   layout: post
   kind: Opinion        # Opinion or Project
   title: "Your title"
   date: 2026-08-01
   excerpt: "One or two sentences shown on the cards."
   ---

   Write the post in Markdown here.
   ```

3. Commit and push. That's it — the post appears at `/writing/your-slug/`, on the
   Writing page, and in the "latest 3" on the homepage automatically (newest first).

`kind` controls the little tag: **Opinion** (navy) or **Project** (gold). Add more kinds
by adding a matching class in `assets/css/main.css` (see `.n-kind.opinion` / `.n-kind.project`).

## Linking a project card to its post

The applied-project cards on the Research timeline (in `index.html`) link to posts by URL,
e.g. `href="{{ '/writing/certifying-real-images/' | relative_url }}"`. If you rename a post's
slug, update that link too.

## Files worth knowing

- `index.html` — the homepage (hero, both timelines, writing teaser, about).
- `writing.html` — the Writing index (`/writing/`).
- `_layouts/` — `default` (shell), `post` (a single post).
- `_includes/` — `head`, `header` (nav), `footer`.
- `assets/css/main.css` — all styles.
- `assets/img/rakshith.jpg` — headshot.
- `assets/files/Rakshith_Subramanyam_Resume.pdf` — the résumé the buttons point to.
  Replace this file (same name) to update your résumé.
- `_config.yml` — name, links, email, résumé path.

## Deploy on GitHub Pages

1. Push these files to your repo.
2. Repo → **Settings → Pages** → set **Source** to *Deploy from a branch*, pick your
   branch (e.g. `main`) and `/ (root)`.
3. Wait ~1 minute; your site is live.

### One setting to get right: `baseurl`

- **Custom domain** (e.g. `rakshithsubri.com`): leave `baseurl: ""` in `_config.yml`.
- **Project URL** (`rakshith-2905.github.io/portfolio`): set `baseurl: "/portfolio"`.

Every internal link uses `relative_url`, so once `baseurl` is right, all links and images work.

## Run locally (optional)

```
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```

## Things to update before you go live

- Trajectory **dates** in `index.html` (Lead / Head / VP) — set to your real ones.
- Applied-project **years** (2025 / 2025 / 2026) — confirm.
- **DECIDER** and **CREPE** links currently point to Google Scholar — swap in the paper URLs.
- Fill in the four draft posts in `_posts/` when you're ready.
