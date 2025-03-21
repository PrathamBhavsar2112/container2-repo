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

        # Check if the file exists
        if not os.path.exists(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404

        # Open the file and check the CSV format
        with open(file_path, "r") as f:
            lines = f.readlines()

            # Check if the file is empty or the header is incorrect
            if not lines or not lines[0].strip().lower() == "product, amount":
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

            # Process the file content
            total_sum = 0
            for line in lines[1:]:
                parts = line.strip().split(",")

                # Check if the line has exactly 2 parts and the second part is a valid number
                if len(parts) != 2 or not parts[1].strip().isdigit():
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                product, amount = parts
                if product.strip() == product_name:
                    total_sum += int(amount.strip())

        return jsonify({"file": file_name, "sum": total_sum}), 200

    except Exception:
        # Catch any unexpected errors and return the correct error message
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)