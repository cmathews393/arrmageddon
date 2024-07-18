from flask import flash, redirect, render_template, url_for

from app.modules.confighandler.main import read_config
from arrmageddon.app.forms import BookSyncForm, TagSelectionForm
from arrmageddon.app.modules.book_tools import book_tools_bp
from arrmageddon.app.modules.book_tools.functions import (
    get_readarr_and_abs_books_by_tag,
    get_readarr_tags,
    sync_book,
)


@book_tools_bp.route("/")
def index():
    return render_template("book_tools.html.j2")


@book_tools_bp.route("/better_ui")
def better_ui():
    return render_template("book_tools/better_ui.html.j2")


import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@book_tools_bp.route("/abs_tag_sync", methods=["GET", "POST"])
def abs_tag_sync():
    tag_form = TagSelectionForm()
    sync_form = BookSyncForm()

    config_readarr = read_config("readarr")
    readarr_api_url = config_readarr.get("api_url")
    readarr_api_key = config_readarr.get("api_key")

    # Load tags for selection
    tags = get_readarr_tags(readarr_api_url, readarr_api_key)
    tag_form.tag.choices = [(tag["id"], tag["label"]) for tag in tags]

    if tag_form.validate_on_submit() and tag_form.submit.data:
        tag_id = tag_form.tag.data
        logger.debug(f"Tag ID selected: {tag_id}")
        book_pairs = get_readarr_and_abs_books_by_tag(tag_id)
        # Set choices for the sync form here
        for readarr_book, matches in book_pairs:
            sync_form.abs_book_id.choices = [
                (match["libraryItem"]["id"], match["title"]) for match in matches
            ]
        return render_template(
            "book_tools/abs_tag_sync.html.j2",
            book_pairs=book_pairs,
            sync_form=sync_form,
            tag_form=tag_form,
        )

    if sync_form.validate_on_submit() and sync_form.sync.data:
        readarr_book_id = sync_form.readarr_book_id.data
        abs_book_id = sync_form.abs_book_id.data
        logger.debug(
            f"Syncing Readarr book ID {readarr_book_id} with ABS book ID {abs_book_id}"
        )
        sync_book(readarr_book_id, abs_book_id)
        flash("Book synced successfully.", "success")
        return redirect(url_for("book_tools.abs_tag_sync"))

    return render_template(
        "book_tools/abs_tag_sync.html.j2",
        book_pairs=[],
        sync_form=sync_form,
        tag_form=tag_form,
    )
