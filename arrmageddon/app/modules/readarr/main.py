import httpx
from typing import List, Dict
from urllib.parse import urlencode
import os
import dotenv

dotenv.load_dotenv()


def get_tag_id(api_url: str, api_key: str, tag_name: str) -> int:
    """Get the tag ID for a specific tag name in Readarr."""
    url = f"{api_url}/api/v1/tag"
    headers = {"X-Api-Key": api_key}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    tags = response.json()
    for tag in tags:
        if tag["label"] == tag_name:
            return tag["id"]

    raise ValueError(f"Tag '{tag_name}' not found")


def get_authors_with_tag(api_url: str, api_key: str, tag_id: int) -> List[Dict]:
    """Get a list of authors tagged with a specific tag ID in Readarr."""
    url = f"{api_url}/api/v1/author"
    headers = {"X-Api-Key": api_key}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    authors = response.json()
    tagged_authors = [author for author in authors if tag_id in author.get("tags", [])]
    return tagged_authors


def get_book_ids_for_authors(
    api_url: str, api_key: str, authors: List[Dict]
) -> tuple[List[int], List[str]]:
    """Get a list of book IDs for the given authors in Readarr."""
    headers = {"X-Api-Key": api_key}
    book_ids = []
    book_titles = []
    for author in authors:
        author_id = author["id"]
        url = f"{api_url}/api/v1/book?authorId={author_id}&includeAllAuthorBooks=false"
        response = httpx.get(url, headers=headers)
        response.raise_for_status()

        books = response.json()

        for book in books:
            if book.get("statistics", {}).get("bookFileCount", 0) == 0:
                book_ids.append(book["id"])
            if book.get("statistics", {}).get("bookFileCount") != 0:
                book_titles.append(book["title"])
    return book_ids, book_titles


def force_search(api_url: str, api_key: str, book_ids: List[int]) -> None:
    """Force a search for all books with the given IDs in Readarr."""
    url = f"{api_url}/api/v1/command"
    headers = {"X-Api-Key": api_key}
    for book_id in book_ids:
        data = {"name": "BookSearch", "bookIds": [book_id]}
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()


def get_audiobookshelf_books(api_url: str, api_key: str) -> List[Dict]:
    """Get a list of books from Audiobookshelf."""
    url = f"{api_url}/api/items"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    return response.json()["items"]


def get_abs_book_id(api_url: str, api_key: str, book_title: str) -> str:
    """Get the Audiobookshelf library item ID for the first result of a specific book title."""
    query_params = urlencode({"q": book_title})
    url = f"{api_url}/api/libraries/9e0f554f-3a38-498d-9ae3-991358e8e076/search?{query_params}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    abs_books = response.json()
    if abs_books.get("book"):
        abs_id = abs_books["book"][0]["libraryItem"]["id"]
        return abs_id

    else:
        print(f"book missing {book_title}")


def add_tag_to_audiobookshelf_book(
    api_url: str, api_key: str, book_id: str, tag: str
) -> None:
    """Add a tag to a book in Audiobookshelf."""
    url = f"{api_url}/api/items/{book_id}/media"
    print(url)
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"tags": [tag]}
    response = httpx.patch(url, json=data, headers=headers)
    response.raise_for_status()


def main(
    api_url_readarr: str,
    api_key_readarr: str,
    api_url_abs: str,
    api_key_abs: str,
    tag_names: List[str],
) -> None:
    for tag_name in tag_names:
        tag_id = get_tag_id(api_url_readarr, api_key_readarr, tag_name)
        tagged_authors = get_authors_with_tag(api_url_readarr, api_key_readarr, tag_id)
        book_ids, book_titles = get_book_ids_for_authors(
            api_url_readarr, api_key_readarr, tagged_authors
        )
        force_search(api_url_readarr, api_key_readarr, book_ids)

        for book in book_titles:
            abs_id = get_abs_book_id(
                api_key=api_key_abs, api_url=api_url_abs, book_title=book
            )
            if abs_id:
                add_tag_to_audiobookshelf_book(
                    api_url_abs, api_key_abs, abs_id, tag_name
                )

    print("Operation completed.")


if __name__ == "__main__":
    API_URL_READARR = os.getenv("API_URL_READARR")
    API_KEY_READARR = os.getenv("API_KEY_READARR")
    API_URL_ABS = os.getenv("API_URL_ABS")
    API_KEY_ABS = os.getenv("API_KEY_ABS")
    TAG_NAMES = os.getenv("TAG_NAMES").split(", ")

    main(API_URL_READARR, API_KEY_READARR, API_URL_ABS, API_KEY_ABS, TAG_NAMES)
