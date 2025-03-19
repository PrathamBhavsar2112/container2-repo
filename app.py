from flask import Flask, request, jsonify
import os

app = Flask(__name__)

PERSISTENT_VOLUME_PATH = "/pratham_PV_dir/"

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()
        if not data or "file" not in data or "product" not in data:
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400

        file_name = data["file"]
        product_name = data["product"]

        file_path = os.path.join(PERSISTENT_VOLUME_PATH, file_name)
        if not os.path.exists(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404

        total_sum = 0
        with open(file_path, "r") as f:
            lines = f.readlines()
            if not lines or "product, amount" not in lines[0].strip():
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 2:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
                product, amount = parts
                if product.strip() == product_name:
                    total_sum += int(amount.strip())

        return jsonify({"file": file_name, "sum": total_sum}), 200

    except ValueError:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
    except Exception:
        return jsonify({"file": file_name if 'file_name' in locals() else None, 
                        "error": "Error reading file."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)