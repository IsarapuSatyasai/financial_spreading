from flask import Flask, render_template, request, send_file
from pathlib import Path
import fitz


app = Flask(__name__)


# Change this to your PDF folder
PDF_FOLDER = (
    Path(__file__).resolve().parent.parent
    / "test_data"
)


@app.route("/")
def viewer():

    pdf_name = request.args.get("pdf")
    page = int(request.args.get("page", 1))
    keyword = request.args.get("keyword", "")

    pdf_path = PDF_FOLDER / pdf_name

    if not pdf_path.exists():
        return f"PDF not found: {pdf_path}", 404

    return render_template(
        "viewer.html",
        pdf_name=pdf_name,
        page=page,
        keyword=keyword,
    )


@app.route("/pdf/<path:filename>")
def pdf(filename):

    pdf_path = PDF_FOLDER / filename

    if not pdf_path.exists():
        return "PDF not found", 404

    return send_file(
        pdf_path,
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )