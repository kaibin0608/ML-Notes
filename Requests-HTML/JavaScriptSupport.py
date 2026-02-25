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

session = HTMLSession()

try:
    # r = session.get('https://www.enanyang.my/?s=大马公司委员会')
    r = session.get('https://www.sinchew.com.my/?s=大马公司委员会')
    r.html.render(sleep=5, timeout=30)

    # Get article URLs from search results
    article_urls = [l for l in r.html.absolute_links if '/?p=' in l]
    print(f"Found {len(article_urls)} articles\n")

    # Visit each article and extract date
    for url in article_urls[:2]:  # limit to first 5 for testing
        page = session.get(url)
        # No need for render() here - dates are usually in static HTML

        # Try common date selectors
        date = None
        for sel in ['.article_date_meta', '.meta .time']:
                    # , '.entry-date', '.post-date', 'span.date', '.meta-date', '.published']:
            el = page.html.find(sel, first=True)
            if el:
                date = el.attrs.get('data-datestr', el.text)
                break

        title = page.html.find('title', first=True)
        title_text = title.text if title else 'No title'

        print(f"Title: {title_text}")
        print(f"el : {el}")
        print(f"Date:  {date}")
        print(f"URL:   {url}")
        print()


except Exception as e:
    print(f"Error: {e}")
finally:
    session.close()
