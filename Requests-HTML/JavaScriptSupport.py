# import pyppeteer
# import pyppeteer.chromium_downloader

# # Patch the revision and download URLs before requests_html imports
# REVISION = '1263111'
# pyppeteer.__chromium_revision__ = REVISION
# pyppeteer.chromium_downloader.__chromium_revision__ = REVISION
# pyppeteer.chromium_downloader.downloadURLs = {
#     'linux': f'https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/{REVISION}/chrome-linux.zip',
#     'mac': f'https://storage.googleapis.com/chromium-browser-snapshots/Mac/{REVISION}/chrome-mac.zip',
#     'win32': f'https://storage.googleapis.com/chromium-browser-snapshots/Win/{REVISION}/chrome-win.zip',
#     'win64': f'https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/{REVISION}/chrome-win.zip',
# }
from requests_html import HTMLSession

def search_site(base_url: str, query: str, link_pattern: str = "/?p=") -> list[str]:
    """Search a website and return matching article URLs."""
    session = HTMLSession()
    try:
        r = session.get(f"{base_url}?s={query}")
        r.html.render(sleep=5, timeout=30)
        article_urls = [l for l in r.html.absolute_links if link_pattern in l]
        return article_urls
    finally:
        session.close()

if __name__ == "__main__":
    urls = search_site("https://www.sinchew.com.my/", "大马公司委员会")
    print(f"Found {len(urls)} articles")
