from flask import Blueprint

book_tools_bp = Blueprint("book_tools", __name__)

from arrmageddon.app.modules.book_tools import routes
