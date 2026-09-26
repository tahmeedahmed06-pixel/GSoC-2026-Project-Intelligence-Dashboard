from flask import Flask, jsonify, request, send_file
from search_api import search

app = Flask(__name__)


@app.get("/")
def dashboard():
    return send_file("dashboard.html")


@app.get("/api/search")
def api_search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    try:
        result = search(query, limit=50)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("=" * 70)
    print("GSoC 2026 SEARCH SERVER")
    print("=" * 70)
    print()
    print("Dashboard: http://127.0.0.1:5000/")
    print("Search:    http://127.0.0.1:5000/api/search?q=Rust")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )