#!/usr/bin/env python3
"""Generate a small static portfolio from public GitHub profile data."""
import argparse, json, os, sys
from html import escape
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_json(url, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "github-portfolio-builder"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def render(profile, repos, lang):
    english = lang == "en"
    labels = {
        "bio": "About" if english else "Hakkında",
        "projects": "Projects" if english else "Projeler",
        "followers": "followers" if english else "takipçi",
        "stars": "stars" if english else "yıldız",
        "visit": "Visit repository" if english else "Depoyu ziyaret et",
    }
    cards = []
    for repo in repos:
        cards.append(
            f'<article class="card"><h3><a href="{escape(repo["html_url"])}">{escape(repo["name"])}</a></h3>'
            f'<p>{escape(repo.get("description") or "")}</p>'
            f'<small>{escape(repo.get("language") or "—")} · {repo.get("stargazers_count", 0)} {labels["stars"]}</small>'
            f'<a class="button" href="{escape(repo["html_url"])}">{labels["visit"]}</a></article>'
        )
    avatar = escape(profile.get("avatar_url", ""))
    name = escape(profile.get("name") or profile.get("login", ""))
    bio = escape(profile.get("bio") or "")
    return f"""<!doctype html>
<html lang="{"en" if english else "tr"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — Portfolio</title><style>
:root{{--bg:#0b1020;--panel:#121a2d;--ink:#f4f7ff;--muted:#aab5cf;--accent:#73e0a9}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at top right,#1d3b54,var(--bg) 45%);color:var(--ink);font:16px/1.6 system-ui,sans-serif}}
main{{max-width:1000px;margin:auto;padding:64px 24px}}header{{display:flex;gap:24px;align-items:center;border-bottom:1px solid #28334e;padding-bottom:32px}}
img{{width:96px;height:96px;border-radius:24px;border:3px solid var(--accent)}}h1{{margin:0;font-size:clamp(2rem,5vw,4rem)}}h2{{margin-top:48px}}.muted,small{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}.card{{background:var(--panel);padding:20px;border:1px solid #28334e;border-radius:18px;display:flex;flex-direction:column;gap:8px}}a{{color:var(--accent)}}.button{{margin-top:auto;text-decoration:none;font-weight:700}}footer{{margin-top:48px;color:var(--muted)}}
</style></head><body><main><header><img src="{avatar}" alt="{name}"><div><h1>{name}</h1><p class="muted">@{escape(profile.get("login", ""))} · {profile.get("followers", 0)} {labels["followers"]}</p></div></header>
<section><h2>{labels["bio"]}</h2><p>{bio}</p></section><section><h2>{labels["projects"]}</h2><div class="grid">{"".join(cards) or "<p>Henüz public proje bulunamadı.</p>"}</div></section>
<footer>Generated with GitHub Portfolio Builder · <a href="{escape(profile.get("html_url", "#"))}">GitHub</a></footer></main></body></html>"""


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--user", required=True, help="GitHub username")
    p.add_argument("--out", default="portfolio.html")
    p.add_argument("--token", default=os.getenv("GITHUB_TOKEN"))
    p.add_argument("--lang", choices=["tr", "en"], default="tr")
    args = p.parse_args()
    try:
        profile = get_json(f"https://api.github.com/users/{args.user}", args.token)
        repos = get_json(f"https://api.github.com/users/{args.user}/repos?sort=updated&per_page=12", args.token)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"GitHub API error: {exc}", file=sys.stderr)
        return 1
    html = render(profile, repos, args.lang)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Portfolio written to {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
