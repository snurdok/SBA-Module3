import azure.functions as func
import json
import math
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CalculateArea", methods=["POST", "GET"])
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('CalculateArea function triggered.')

    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }

    # Handle preflight OPTIONS request
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            headers=headers
        )

    shape = body.get("shape", "").lower()

    if shape == "triangle":
        base = body.get("base")
        height = body.get("height")
        if base is None or height is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'base' or 'height' for triangle"}),
                status_code=400, headers=headers
            )
        result = 0.5 * float(base) * float(height)

    elif shape == "square":
        side = body.get("side")
        if side is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'side' for square"}),
                status_code=400, headers=headers
            )
        result = float(side) ** 2

    elif shape == "circle":
        radius = body.get("radius")
        if radius is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'radius' for circle"}),
                status_code=400, headers=headers
            )
        result = math.pi * float(radius) ** 2

    else:
        return func.HttpResponse(
            json.dumps({"error": f"Unknown shape: '{shape}'. Use 'triangle', 'square', or 'circle'."}),
            status_code=400, headers=headers
        )

    return func.HttpResponse(
        json.dumps({"shape": shape, "result": result}),
        status_code=200,
        headers=headers
    )
