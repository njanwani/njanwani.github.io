# CLAUDE.md

Personal academic website for Neil Janwani, served via GitHub Pages at `njanwani.github.io`.

## Running locally

The page uses `fetch()` to pull in HTML sections and JSON, so it **must** be served over HTTP — opening `index.html` directly via `file://` will fail (CORS).

```
cd /Users/neiljanwani/Documents/njanwani.github.io
python3 -m http.server 8000
# open http://localhost:8000
# Ctrl+C to stop
```

After editing, refresh the browser (hard refresh `Cmd+Shift+R` to bypass cache).

## Deploy

GitHub Pages repo — pushing to the `main` branch publishes automatically. No build step.

## Structure

- `index.html` — shell + styling + JS. Inline `<style>` defines the academic theme (Lato font, custom tags like `<name>`, `<heading>`, `<papertitle>`, `<abs>`). JS at the bottom does the dynamic loading.
- `sections/intro.html` — fetched into `#intro`. Contains the bio, a `<div id="news">` placeholder, and the Research blurb.
- `sections/news.html` — the **News** list. Fetched into `#news` (which lives inside the intro markup) once intro is in the DOM. Edit news items here.
- `sections/papers.html` — fetched into `#papers`; just a `<div id="papers-container">` populated by JS.
- `sections/projects.html` — fetched into `#projects`; a "Projects" heading + `<div id="projects-container">` populated by JS. Same card layout as papers.
- `data/papers.json` — publication list (title, authors, venue, year, thumbnail, abstract, links). Edit this to add/update papers.
- `data/projects.json` — projects list, same schema as `papers.json`. Currently holds a placeholder (the MO-Playground entry). Edit this to add/update projects.
- `data/njanwani.pdf` — CV linked from the intro.
- `images/`, `videos/`, `pres/`, `js/` — assets. `js/hidebib.js` + inline `loadPapers()`/`hideallabs()` handle the collapsible abstracts.

## How loading works

`index.html` calls `loadSection` for `intro`, `papers`, and `projects`. When the intro finishes loading, `loadSection` chains a load of `sections/news.html` into the `#news` div (which only exists after intro is injected). The papers and projects sections trigger `loadPapers()` / `loadProjects()`, both thin wrappers over the shared `loadEntries(jsonFile, containerId)`, which fetches the JSON and builds a card row per entry. Abstracts are hidden by default (`hideallabs`) and toggled via `toggleblock`.

## Conventions / notes

- Layout is old-school `<table>`-based (design originally courtesy of Jon Barron). Match that style when editing.
- **News section** (`sections/intro.html`): two-column table — month/year on the left (gray, `color:#888`, bold), text on the right. Ordered newest-first. The table is wrapped in a scrollable `<div>` (`max-height:150px; overflow-y:auto`, bordered) that shows ~3 items at a time. Some months were inferred (2024 entries only had years; ICRA 2026 set to Jun) — confirm with Neil before treating them as authoritative.
- To add a news item, add a `<tr>` at the top of the News table (inside the scroll `<div>`) following the existing pattern.
- To add a publication, prepend an entry to `data/papers.json`.
