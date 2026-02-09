from flask import Flask, request, jsonify

app = Flask(__name__)

inventory = {}
next_id = 1

@app.route("/sell/", methods=["POST"])

def sell_book():
    
    global next_id

    data = request.get_json()

    book = {
        "title": data["title"],
        "author": data["author"],
        "year_of_publication": data["year_of_publication"]
    }

    book_id = next_id
    inventory[book_id] = book
    next_id += 1

    print("Current inverntory:", inventory)

    return jsonify({
        "status": "ok",
        "id": book_id
    })

@app.route("/list/", methods=["GET"])

def list_books():
    books = []

    for book_id, book_data in inventory.items():

        books.append({
            "id": book_id,
            "title": book_data["title"],
            "author": book_data["author"],
            "year_of_publication": book_data["year_of_publication"]
        })

    return jsonify(books)

@app.route("/purchase/<int:item_id>/", methods=["GET"])

def purchase_book(item_id):
    if item_id in inventory:
        inventory.pop(item_id)
        return jsonify({"status": "ok", "purchase_id": item_id})

    return jsonify({"status": "not found", "requested_id": item_id})

if __name__ == "__main__":
    app.run(debug=True)