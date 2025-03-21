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

        # **Check if the file exists FIRST**
        if not os.path.exists(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404

        total_sum = 0
        with open(file_path, "r") as f:
            lines = f.readlines()

            # **Fix: Ensure the file has a valid CSV header**
            if not lines or not lines[0].strip().lower() == "product,amount":
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

            # **Fix: Validate each line before processing**
            for line in lines[1:]:
                parts = line.strip().split(",")

                # Ensure there are exactly 2 values and second value is numeric
                if len(parts) != 2 or not parts[1].strip().isdigit():
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                product, amount = parts
                if product.strip() == product_name:
                    total_sum += int(amount.strip())

        return jsonify({"file": file_name, "sum": total_sum}), 200

    except ValueError:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
    except Exception:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400  # Fix CSV format errors

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
