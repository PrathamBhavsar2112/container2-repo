from flask import Flask, request, jsonify
import os
import csv

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

        # ✅ Fix 1: Check if file exists before anything else
        if not os.path.exists(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404

        total_sum = 0
        with open(file_path, "r") as f:
            lines = f.readlines()

            # ✅ Fix 2: Normalize header (lowercase & remove spaces)
            header = lines[0].strip().lower().replace(" ", "")
            if header != "product,amount":
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

            # ✅ Fix 3: Validate each row strictly before processing
            csv_reader = csv.reader(lines[1:], delimiter=",")
            for row in csv_reader:
                if len(row) != 2:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                product, amount = row
                product = product.strip()
                amount = amount.strip()

                # Ensure amount is a valid integer
                if not amount.isdigit():
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                if product == product_name:
                    total_sum += int(amount)

        return jsonify({"file": file_name, "sum": total_sum}), 200

    except Exception:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
