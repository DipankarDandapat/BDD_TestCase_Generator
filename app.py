from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
import shutil
import glob

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Import agents after Flask app is created
from agents import user_proxy, bdd_writer
CORS(app)  # Enable CORS for all routes

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    """Serve the main page"""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Generate BDD test cases from requirement"""
    try:
        data = request.get_json(force=True)
        requirement = data.get("requirement", "").strip()
        
        if not requirement:
            return jsonify({"error": "Requirement is empty"}), 400
        
        # Create unique run folder to avoid collisions
        run_id = str(uuid.uuid4())
        run_dir = os.path.join(OUTPUT_DIR, run_id)
        os.makedirs(run_dir, exist_ok=True)
        
        # Store current directory
        original_dir = os.getcwd()
        
        try:
            # Change to run directory
            os.chdir(run_dir)
            
            # Run the multi-agent chat
            user_proxy.initiate_chat(
                bdd_writer,
                message=f"Create a full BDD feature file for:\n\n{requirement}"
            )
            
            # Find the generated *.feature file
            feature_files = glob.glob("*.feature")
            if not feature_files:
                return jsonify({"error": "No feature file was generated"}), 500
            
            feature_file = feature_files[0]
            
            # Read the generated content
            with open(feature_file, "r", encoding="utf-8") as f:
                gherkin_text = f.read()
            
            # Copy file to output directory with run_id prefix for download
            download_filename = f"{run_id}_{feature_file}"
            shutil.copy(feature_file, os.path.join(original_dir, OUTPUT_DIR, download_filename))
            
            return jsonify({
                "gherkin": gherkin_text,
                "filename": download_filename,
                "run_id": run_id
            })
            
        except Exception as e:
            return jsonify({"error": f"Agent execution failed: {str(e)}"}), 500
        
        finally:
            # Always return to original directory
            os.chdir(original_dir)
            
    except Exception as e:
        return jsonify({"error": f"Request processing failed: {str(e)}"}), 500

@app.route("/download/<filename>")
def download(filename):
    """Download generated feature file"""
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "BDD Generator"})

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set!")
        print("Please set it before running the application.")
    
    app.run(host="0.0.0.0", port=5000, debug=True)

