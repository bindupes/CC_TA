from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store registered nodes and their CPU details
nodes = {}

@app.route('/register_node', methods=['POST'])
def register_node():
    data = request.get_json()

    if "node_id" not in data or "cpu_limit" not in data:
        return jsonify({"error": "Missing node_id or cpu_limit"}), 400

    node_id = data["node_id"]
    cpu_limit = data["cpu_limit"]

    # Initialize CPU usage to 0
    nodes[node_id] = {
        "cpu_limit": cpu_limit,
        "cpu_usage": 0
    }

    return jsonify({"message": f"Node {node_id} registered with CPU limit {cpu_limit}!"})

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    return jsonify(nodes)
@app.route('/update_cpu_usage', methods=['POST'])
def update_cpu_usage():
    data = request.get_json()

    if "node_id" not in data or "cpu_usage" not in data:
        return jsonify({"error": "Missing node_id or cpu_usage"}), 400

    node_id = data["node_id"]
    cpu_usage = data["cpu_usage"]

    if node_id not in nodes:
        return jsonify({"error": "Node not found"}), 404

    # Update CPU usage
    nodes[node_id]["cpu_usage"] = cpu_usage

    # Check if CPU usage exceeds the limit
    if cpu_usage > nodes[node_id]["cpu_limit"]:
        return jsonify({"warning": f"Node {node_id} exceeded CPU limit!"}), 200

    return jsonify({"message": f"CPU usage for {node_id} updated to {cpu_usage}"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
