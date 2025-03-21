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

        # ✅ Fix 1: If file does not exist, return "File not found."
        if not os.path.exists(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404

        total_sum = 0
        with open(file_path, "r") as f:
            lines = f.readlines()

            # ✅ Fix 2: Normalize header (removes spaces and checks lowercase)
            header = lines[0].strip().lower().replace(" ", "")
            if header != "product,amount":
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

            # ✅ Fix 3: Check CSV row structure
            for line in lines[1:]:
                parts = line.strip().split(",")

                # Ensure every row has **exactly 2 columns**
                if len(parts) != 2:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                product, amount = parts

                # Ensure second column is a number
                if not amount.strip().isdigit():
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

                if product.strip() == product_name:
                    total_sum += int(amount.strip())

        return jsonify({"file": file_name, "sum": total_sum}), 200

    except Exception:
        # ✅ Fix 4: Ensure correct error message in case of unexpected errors
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
