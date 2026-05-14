import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.parse import urlparse


Fetcher = Any


@dataclass(frozen=True)
class FragranticaImageCandidate:
    name: str
    page_url: str
    image_url: str


@dataclass
class BackfillResult:
    checked: int = 0
    updated: int = 0
    unmatched: list[str] | None = None

    def __post_init__(self) -> None:
        if self.unmatched is None:
            self.unmatched = []


def fetch_designer_catalog(designer_url: str, fetcher: Fetcher | None = None) -> dict[str, FragranticaImageCandidate]:
    html_text = fetch_html(designer_url, fetcher)
    return parse_designer_catalog(html_text, base_url=designer_url)


def fetch_html(url: str, fetcher: Fetcher | None = None) -> str:
    if fetcher is not None:
        return fetcher(url)

    try:
        from scrapling.fetchers import Fetcher as ScraplingFetcher
    except ImportError as exc:
        raise RuntimeError("Scrapling fetchers are not installed") from exc

    response = ScraplingFetcher.get(
        url,
        impersonate="chrome",
        http3=False,
        stealthy_headers=True,
        timeout=30,
        retries=2,
    )
    if response.status >= 400:
        raise RuntimeError(f"Scrapling fetch failed with HTTP {response.status}: {response.reason}")
    return response.body.decode("utf-8", "ignore")


def parse_designer_catalog(html_text: str, *, base_url: str) -> dict[str, FragranticaImageCandidate]:
    catalog: dict[str, FragranticaImageCandidate] = {}
    for card in re.findall(r"<a\b[^>]*\bprefumeHbox\b.*?</a>", html_text, flags=re.I | re.S):
        href = extract_attr(card, "href")
        image_url = extract_image_url(card)
        name = extract_perfume_name(card)
        if not href or not image_url or not name:
            continue

        candidate = FragranticaImageCandidate(
            name=name,
            page_url=urljoin(base_url, html.unescape(href)),
            image_url=html.unescape(image_url),
        )
        catalog[normalize_name(name)] = candidate
    return catalog


def parse_product_page_image_url(html_text: str) -> str:
    for script_body in re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_text,
        flags=re.I | re.S,
    ):
        try:
            data = json.loads(html.unescape(script_body.strip()))
        except json.JSONDecodeError:
            continue
        image_url = image_url_from_json_ld(data)
        if image_url and "favicon" not in image_url.lower():
            return image_url

    for attr in ("property", "name"):
        pattern = (
            rf'<meta\b[^>]*{attr}=["\'](?:og:image|twitter:image)["\'][^>]*'
            rf'content=["\']([^"\']+)["\']'
        )
        match = re.search(pattern, html_text, flags=re.I | re.S)
        if match and "favicon" not in match.group(1).lower():
            return html.unescape(match.group(1).strip())

    return ""


def image_url_from_json_ld(data: Any) -> str:
    if isinstance(data, list):
        for item in data:
            image_url = image_url_from_json_ld(item)
            if image_url:
                return image_url
        return ""

    if not isinstance(data, dict):
        return ""

    image = data.get("image")
    if isinstance(image, str):
        return image.strip()
    if isinstance(image, list):
        for item in image:
            if isinstance(item, str) and item.strip():
                return item.strip()
            if isinstance(item, dict):
                value = item.get("url") or item.get("contentUrl")
                if isinstance(value, str) and value.strip():
                    return value.strip()
    if isinstance(image, dict):
        value = image.get("url") or image.get("contentUrl")
        if isinstance(value, str):
            return value.strip()

    graph = data.get("@graph")
    if graph:
        return image_url_from_json_ld(graph)

    return ""


def extract_image_url(card_html: str) -> str:
    image_src = ""
    img_match = re.search(r"<img\b[^>]*>", card_html, flags=re.I | re.S)
    if img_match:
        image_src = extract_attr(img_match.group(0), "src")
    if image_src:
        return image_src

    jpeg_match = re.search(
        r'<source\b[^>]*type=["\']image/jpeg["\'][^>]*srcset=["\']([^"\']+)["\']',
        card_html,
        flags=re.I | re.S,
    )
    if not jpeg_match:
        return ""
    return jpeg_match.group(1).split(",", 1)[0].strip().split(" ", 1)[0]


def extract_perfume_name(card_html: str) -> str:
    match = re.search(
        r'<h3\b[^>]*class=["\'][^"\']*tw-grid-perfume-title[^"\']*["\'][^>]*>(.*?)</h3>',
        card_html,
        flags=re.I | re.S,
    )
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(text).strip()


def extract_attr(tag_html: str, attr: str) -> str:
    match = re.search(rf'\b{re.escape(attr)}=["\']([^"\']+)["\']', tag_html, flags=re.I)
    return match.group(1).strip() if match else ""


def normalize_name(value: object) -> str:
    text = html.unescape(str(value or "")).strip().lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[\u2018\u2019\u201a\u201b]", "'", text)
    text = re.sub(r"[\u201c\u201d\u201e\u201f]", '"', text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def designer_url_from_record(record: dict[str, Any]) -> str:
    product_url = str(record.get("product_url") or "")
    path_parts = [part for part in urlparse(product_url).path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[0].lower() == "perfume":
        return f"https://www.fragrantica.com/designers/{title_slug(path_parts[1])}.html"

    brand = str(record.get("brand") or "")
    return f"https://www.fragrantica.com/designers/{title_slug(brand.replace(' ', '-'))}.html"


def title_slug(slug: str) -> str:
    return "-".join(part[:1].upper() + part[1:] for part in slug.strip("/").split("-") if part)


def backfill_raw_files(
    raw_dir: str | Path,
    *,
    fetcher: Fetcher | None = None,
    limit: int | None = None,
    dry_run: bool = False,
) -> BackfillResult:
    result = BackfillResult()
    catalogs: dict[str, dict[str, FragranticaImageCandidate]] = {}

    for json_path in sorted(Path(raw_dir).glob("*_fragrance_data.json")):
        records = json.loads(json_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            continue

        changed = False
        for record in records:
            if not isinstance(record, dict):
                continue
            if str(record.get("image_url") or "").strip():
                continue
            if not str(record.get("product_url") or "").strip():
                continue
            if limit is not None and result.checked >= limit:
                break

            result.checked += 1
            source = str(record.get("source") or "").lower()
            if source == "fragrantica":
                designer_url = designer_url_from_record(record)
                if designer_url not in catalogs:
                    catalogs[designer_url] = fetch_designer_catalog(designer_url, fetcher)

                key = normalize_name(record.get("english_name") or record.get("normalized_name") or record.get("korean_name"))
                candidate = catalogs[designer_url].get(key)
                if not candidate:
                    result.unmatched.append(str(record.get("english_name") or key))
                    continue
                record["image_url"] = candidate.image_url
                record["product_url"] = candidate.page_url
            else:
                image_url = parse_product_page_image_url(fetch_html(str(record.get("product_url")), fetcher))
                if not image_url:
                    result.unmatched.append(str(record.get("english_name") or record.get("product_url")))
                    continue
                record["image_url"] = image_url
            result.updated += 1
            changed = True

        if changed and not dry_run:
            json_path.write_text(
                json.dumps(records, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    return result
