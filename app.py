from flask import Flask, render_template, request, jsonify
from campus_graph import bfs, dfs, ucs, dls, ids, get_all_locations, CAMPUS_GRAPH, NODE_POSITIONS

app = Flask(__name__)


@app.route("/")
def index():
    locations = get_all_locations()
    edges = []
    seen = set()
    for node, neighbors in CAMPUS_GRAPH.items():
        for neighbor, weight in neighbors.items():
            key = tuple(sorted([node, neighbor]))
            if key not in seen:
                seen.add(key)
                edges.append({"from": node, "to": neighbor, "weight": weight})
    return render_template(
        "index.html",
        locations=locations,
        graph=CAMPUS_GRAPH,
        positions=NODE_POSITIONS,
        edges=edges,
    )


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    start = data.get("start")
    goal = data.get("goal")
    algorithm = data.get("algorithm", "bfs")

    if start not in CAMPUS_GRAPH or goal not in CAMPUS_GRAPH:
        return jsonify({"error": "Invalid location selected"}), 400

    extra = {}

    if algorithm == "bfs":
        path, visited, distance, explored_edges = bfs(CAMPUS_GRAPH, start, goal)
    elif algorithm == "dfs":
        path, visited, distance, explored_edges = dfs(CAMPUS_GRAPH, start, goal)
    elif algorithm == "ucs":
        path, visited, distance, explored_edges = ucs(CAMPUS_GRAPH, start, goal)
    elif algorithm == "dls":
        depth_limit = data.get("depth_limit", 3)
        path, visited, distance, explored_edges, cutoff = dls(
            CAMPUS_GRAPH, start, goal, depth_limit
        )
        extra["depth_limit"] = depth_limit
        extra["cutoff"] = cutoff
    elif algorithm == "ids":
        path, visited, distance, explored_edges, found_depth = ids(
            CAMPUS_GRAPH, start, goal
        )
        extra["found_at_depth"] = found_depth
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    edges_in_path = []
    if path:
        for i in range(len(path) - 1):
            edges_in_path.append({"from": path[i], "to": path[i + 1]})

    return jsonify(
        {
            "path": path,
            "visited_order": visited,
            "distance": distance,
            "algorithm": algorithm.upper(),
            "edges_in_path": edges_in_path,
            "explored_edges": explored_edges,
            **extra,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
