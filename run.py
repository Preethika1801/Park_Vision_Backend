#run.py
from app import create_app

# Create an instance of the app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
