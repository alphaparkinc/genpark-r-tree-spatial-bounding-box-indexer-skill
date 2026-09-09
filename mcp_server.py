"""MCP Server for KD-Tree Spatial Indexer Skill."""
import json
import sys
from client import KDTree2D

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "find_nearest_neighbor",
                            "description": "Find closest spatial entity to target coordinate using KD-Tree",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "entities": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "x": {"type": "number"},
                                                "y": {"type": "number"},
                                                "data": {}
                                            },
                                            "required": ["x", "y"]
                                        }
                                    },
                                    "target": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    }
                                },
                                "required": ["entities", "target"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                entities = [((e["x"], e["y"]), e.get("data", e)) for e in args["entities"]]
                tree = KDTree2D(entities)
                target = tuple(args["target"])
                pt, data, dist = tree.nearest_neighbor(target)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps({"nearest_point": pt, "data": data, "distance": dist})
                        }]
                    }
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
