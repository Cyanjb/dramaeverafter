#!/usr/bin/env python3
"""Tell Bing (and every IndexNow engine) which pages changed.

    python3 generator/indexnow.py --changed <git ref>   URLs whose files changed since <ref>
    python3 generator/indexnow.py --all                 every sitemap URL (first run, or a reset)
    python3 generator/indexnow.py --urls <file>         one URL or path per line
    add --dry-run to print the list and send nothing

Born 10 Sep 2026. Google demoted the site on 29 Aug and the second door is
AI search: ChatGPT search and Perplexity lean on Bing's index, and Bing has
no verdict against us. IndexNow is Bing's push channel (shared with Yandex,
Naver, Seznam, Yep): one POST names the URLs, the engines crawl them within
minutes instead of whenever they get round to the sitemap. Deleted or
redirected URLs go in the same list, so the old where-to-watch pages drop
out of Bing as fast as the new title pages go in.

The key: a 32-hex file at the site root whose content is its own name
(<key>.txt). Public by design, that is how the engine verifies the host.
This script finds it; nothing else needs to know the value. The weekly
workflow runs --changed after its push; a failure here never blocks a
publish, it only costs Bing a few days of noticing.
"""
import glob, json, os, re, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://dramaeverafter.com"
HOST = "dramaeverafter.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
SECTIONS = ("titles", "actors", "tropes", "apps", "where-to-watch", "chinese")
BATCH = 10000  # the protocol's per-request maximum


def key():
    for p in glob.glob(os.path.join(ROOT, "*.txt")):
        stem = os.path.basename(p)[:-4]
        if re.fullmatch(r"[0-9a-f]{32}", stem) and open(p).read().strip() == stem:
            return stem
    sys.exit("no IndexNow key file at the site root (<32 hex>.txt containing its own name)")


def is_site_page(path):
    path = path.replace(os.sep, "/")
    if path.startswith((".", "generator/", "data/", "references/", "design-system/")):
        return False
    if path.endswith(".html") and path != "404.html":
        return path.count("/") == 0 or path.split("/")[0] in SECTIONS
    return False


def indexable(path):
    """A page that still exists and carries noindex is not worth Bing's fetch;
    a page that no longer exists IS sent, so the engine drops it."""
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return True
    return 'content="noindex"' not in open(full, encoding="utf-8").read()


def to_url(path):
    return f"{DOMAIN}/{path.replace(os.sep, '/')}"


def from_sitemap():
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", sm)


def since(ref):
    out = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=ADMR", ref, "HEAD"],
                                  cwd=ROOT, text=True)
    return [to_url(p) for p in out.split("\n") if p and is_site_page(p) and indexable(p)]


def from_file(path):
    urls = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line if line.startswith("http") else to_url(line.lstrip("/")))
    return urls


def submit(urls, dry_run):
    urls = sorted(set(u for u in urls if u.startswith(DOMAIN + "/")))
    if not urls:
        print("IndexNow: nothing to send")
        return 0
    k = key()
    print(f"IndexNow: {len(urls):,} URLs" + (" (dry run, nothing sent)" if dry_run else ""))
    for u in urls[:8]:
        print("  " + u)
    if len(urls) > 8:
        print(f"  ... {len(urls) - 8:,} more")
    if dry_run:
        return 0
    rc = 0
    for i in range(0, len(urls), BATCH):
        body = json.dumps({"host": HOST, "key": k,
                           "keyLocation": f"{DOMAIN}/{k}.txt",
                           "urlList": urls[i:i + BATCH]}).encode()
        req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print(f"  batch {i // BATCH + 1}: HTTP {r.status} (200/202 = accepted)")
        except urllib.error.HTTPError as e:
            print(f"  batch {i // BATCH + 1}: HTTP {e.code} {e.read().decode(errors='replace')[:200]}")
            rc = 1
        except Exception as e:  # network: report, never raise; a publish must not fail on this
            print(f"  batch {i // BATCH + 1}: {e}")
            rc = 1
    return rc


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    if "--all" in args:
        urls = from_sitemap()
    elif "--changed" in args:
        urls = since(args[args.index("--changed") + 1])
    elif "--urls" in args:
        urls = from_file(args[args.index("--urls") + 1])
    else:
        sys.exit(__doc__)
    sys.exit(submit(urls, dry))
