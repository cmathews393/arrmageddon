from urllib.parse import urlencode

import httpx

from arrmageddon.app.modules.confighandler.main import read_config


def get_tag_id(readarr_api_url: str, readarr_api_key: str, tag_name: str) -> int:
    """Get the tag ID for a specific tag name in Readarr."""
    url = f"{readarr_api_url}/api/v1/tag"
    headers = {"X-Api-Key": readarr_api_key}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    tags = response.json()
    for tag in tags:
        if tag["label"] == tag_name:
            return tag["id"]

    raise ValueError(f"Tag '{tag_name}' not found")


def get_readarr_tags(readarr_api_url: str, readarr_api_key: str):
    """Fetch tags from Readarr."""
    url = f"{readarr_api_url}/api/v1/tag"
    headers = {"X-Api-Key": readarr_api_key}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_authors_with_tag(
    readarr_api_url: str,
    readarr_api_key: str,
    tag_id: int,
) -> list[dict]:
    """Get a list of authors tagged with a specific tag ID in Readarr."""
    url = f"{readarr_api_url}/api/v1/author"
    headers = {"X-Api-Key": readarr_api_key}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    authors = response.json()

    # Ensure authors is a list and not a dict
    if isinstance(authors, dict):
        authors = [authors]
    tagged_authors = [author for author in authors if tag_id in author.get("tags", [])]
    print("Tagged Authors:", tagged_authors)

    return tagged_authors


def get_book_ids_for_authors(
    readarr_api_url: str,
    readarr_api_key: str,
    authors: list[dict],
) -> tuple[list[int], list[str]]:
    """Get a list of book IDs for the given authors in Readarr."""
    headers = {"X-Api-Key": readarr_api_key}
    book_ids = []
    book_titles = []
    for author in authors:
        author_id = author["id"]
        url = f"{readarr_api_url}/api/v1/book?authorId={author_id}&includeAllAuthorBooks=false"
        response = httpx.get(url, headers=headers)
        response.raise_for_status()

        books = response.json()

        for book in books:
            if book.get("statistics", {}).get("bookFileCount", 0) == 0:
                book_ids.append(book["id"])
            if book.get("statistics", {}).get("bookFileCount") != 0:
                book_titles.append(book["title"])
    return book_ids, book_titles


def force_search(
    readarr_api_url: str,
    readarr_api_key: str,
    book_ids: list[int],
) -> None:
    """Force a search for all books with the given IDs in Readarr."""
    url = f"{readarr_api_url}/api/v1/command"
    headers = {"X-Api-Key": readarr_api_key}
    for book_id in book_ids:
        data = {"name": "BookSearch", "bookIds": [book_id]}
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()


def get_abs_book_id(
    abs_api_url: str,
    abs_api_key: str,
    abs_library_id: str,
    book_title: str,
) -> str:
    """Get the Audiobookshelf library item ID for the first result of a specific book title."""
    query_params = urlencode({"q": book_title})
    url = f"{abs_api_url}/api/libraries/{abs_library_id}/search?{query_params}"
    headers = {"Authorization": f"Bearer {abs_api_key}"}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    abs_books = response.json()

    if abs_books.get("book"):
        abs_id = abs_books["book"][0]["libraryItem"]["id"]
        return abs_id

    else:
        print(f"book missing {book_title}")


def add_tag_to_audiobookshelf_book(
    abs_api_url: str,
    abs_api_key: str,
    book_id: str,
    tag: str,
) -> None:
    """Add a tag to a book in Audiobookshelf."""
    url = f"{abs_api_url}/api/items/{book_id}/media"
    print(url)
    headers = {"Authorization": f"Bearer {abs_api_key}"}
    data = {"tags": [tag]}
    response = httpx.patch(url, json=data, headers=headers)
    response.raise_for_status()


def get_readarr_and_abs_books_by_tag(tag_id: int) -> list[tuple[dict, list[dict]]]:
    """Get books from Readarr by tag and their possible matches in Audiobookshelf."""
    config_readarr = read_config("readarr")
    config_abs = read_config("audiobookshelf")

    readarr_api_url = config_readarr.get("api_url")
    readarr_api_key = config_readarr.get("api_key")
    abs_api_url = config_abs.get("api_url")
    abs_api_key = config_abs.get("api_key")
    abs_library_id = config_abs.get("library_id")

    authors = get_authors_with_tag(readarr_api_url, readarr_api_key, tag_id)
    book_pairs = []

    for author in authors:
        author_id = author["id"]
        books_url = f"{readarr_api_url}/api/v1/book?authorId={author_id}&includeAllAuthorBooks=false"
        headers = {"X-Api-Key": readarr_api_key}
        response = httpx.get(books_url, headers=headers)
        response.raise_for_status()

        books = response.json()
        for book in books:
            book_id = book["id"]
            book_title = book["title"]
            abs_books = []
            try:
                abs_id = get_abs_book_id(
                    abs_api_url,
                    abs_api_key,
                    abs_library_id,
                    book_title,
                )
                abs_books.append({"libraryItem": {"id": abs_id}, "title": book_title})
            except Exception as e:
                print(f"Could not find ABS book for {book_title}: {e}")

            book_pairs.append((book, abs_books))

    return book_pairs


def sync_book(readarr_book_id: int, abs_book_id: str) -> None:
    """Sync a Readarr book with an Audiobookshelf book by adding a tag."""
    config_abs = read_config("audiobookshelf")

    abs_api_url = config_abs.get("api_url")
    abs_api_key = config_abs.get("api_key")
    abs_library_id = config_abs.get("library_id")

    tag = "Synced"
    add_tag_to_audiobookshelf_book(abs_api_url, abs_api_key, abs_book_id, tag)
