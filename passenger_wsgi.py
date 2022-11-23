from app import app
from app.frontend.lib.template_filter import format_date_indo
from waitress import serve


if __name__ == "__main__":
    serve(app)
