from flask import flash, redirect, render_template, url_for

from arrmageddon.app.modules.book_tools import book_tools_bp
from arrmageddon.app.modules.book_tools.functions import get_readarr_tags, sync_tags
from arrmageddon.app.modules.confighandler.main import read_config


@book_tools_bp.route("/")
def index():
    return render_template("book_tools.html.j2")


@book_tools_bp.route("/better_ui")
def better_ui():
    return render_template("book_tools/better_ui.html.j2")


from arrmageddon.app.forms import TagSyncForm


@book_tools_bp.route("/abs_tag_sync", methods=["GET", "POST"])
def abs_tag_sync():
    config_readarr = read_config("readarr")
    api_url_readarr = config_readarr.get("api_url")
    api_key_readarr = config_readarr.get("api_key")
    form = TagSyncForm()
    tags = get_readarr_tags(api_url_readarr, api_key_readarr)
    form.tag.choices = [(tag["id"], tag["label"]) for tag in tags]

    if form.validate_on_submit():
        tag_id = form.tag.data
        tag_name = next(tag["label"] for tag in tags if tag["id"] == int(tag_id))

        sync_tags(tag_name)

        flash("Tag sync completed successfully.", "success")
        return redirect(url_for("book_tools.abs_tag_sync"))

    return render_template("book_tools/abs_tag_sync.html.j2", form=form)
