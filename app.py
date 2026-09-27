from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Welcome route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Event Management API"
    })


# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])


# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Check that JSON data was provided
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Check that title was provided
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new ID
    new_id = max([event.id for event in events], default=0) + 1

    # Create and store the new event
    new_event = Event(new_id, title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Find the event
    for event in events:
        if event.id == event_id:
            event.title = title
            return jsonify(event.to_dict()), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return jsonify({
                "message": "Event deleted successfully"
            }), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)