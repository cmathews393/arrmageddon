from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx


class ReadarrAPI:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}

    def get_books(self) -> list[dict]:
        url = f"{self.base_url}/api/v1/book"
        try:
            response = httpx.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
        return []

    def get_book_files(self, book_id: int) -> list[dict]:
        url = f"{self.base_url}/api/v1/bookfile"
        params = {"bookId": [book_id]}
        try:
            response = httpx.get(url, headers=self.headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
        return []

    def update_book_monitor_status(self, book_ids: list[int], monitored: bool) -> None:
        url = f"{self.base_url}/api/v1/book/monitor"
        payload = {"bookIds": book_ids, "monitored": monitored}
        try:
            response = httpx.put(url, headers=self.headers, json=payload, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")


def main() -> None:
    base_url = "http://192.168.1.222:8787"  # Replace with your Readarr instance URL
    api_key = "ee1f89479edc4c48aa4e0818cf40826a"  # Replace with your Readarr API key
    readarr = ReadarrAPI(base_url, api_key)

    print("Fetching books...")
    books = readarr.get_books()
    book_ids_to_unmonitor = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(readarr.get_book_files, book["id"]): book["id"]
            for book in books
        }

        for future in as_completed(futures):
            book_id = futures[future]
            try:
                files = future.result()
                if not files:
                    print(f"No files found for book ID: {book_id}")
                    book_ids_to_unmonitor.append(book_id)
                else:
                    print(f"Files found for book ID: {book_id}")
            except Exception as e:
                print(f"Error checking files for book ID: {book_id} - {e}")

    if book_ids_to_unmonitor:
        inputchoice = input(
            "No files found for some books. Do you want to unmonitor these books? (Y/N): ",
        )
        if inputchoice.upper() == "Y":
            print("Updating monitor status...")
            readarr.update_book_monitor_status(book_ids_to_unmonitor, monitored=False)
            print(f"Unmonitored books with IDs: {book_ids_to_unmonitor}")
        else:
            print("No changes made.")
    else:
        print("No books found without files.")


if __name__ == "__main__":
    main()
