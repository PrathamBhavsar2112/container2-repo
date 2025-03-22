from flask import Flask, request, jsonify
import os

app = Flask(__name__)
# test 2
PERSISTENT_VOLUME_PATH = "/pratham_PV_dir/"

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    if not data or "file" not in data or "product" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data["file"]
    product = data["product"]
    file_path = os.path.join(PERSISTENT_VOLUME_PATH, file_name)

    if not os.path.isfile(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    try:
        total_sum = 0
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines or "product,amount" not in lines[0].replace(" ", "").lower():
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 2:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                row_product, amount = parts
                if not amount.strip().isdigit():
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                if row_product.strip() == product:
                    total_sum += int(amount.strip())

        return jsonify({"file": file_name, "sum": total_sum}), 200

    except Exception:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)