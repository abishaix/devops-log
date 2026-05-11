from flask import Flask, jsonify

app = Flask(__name__)

# Root route — confirms the reverse proxy is working end to end
@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Hello from the private backend!",
        "server": "Flask running on private EC2 @ 10.0.131.56"
    })

# Info route — documents the architecture for your practice log
@app.route('/info')
def info():
    return jsonify({
        "architecture": "Nginx reverse proxy → Flask backend",
        "public_server_public_ip": "3.108.40.11",
        "public_server_private_ip": "10.0.12.155",
        "backend_private_ip": "10.0.131.56",
        "backend_port": 5000,
        "note": "This response came through Nginx — Flask has no public IP"
    })

# Run on 0.0.0.0 so Nginx can reach it from within the VPC.
# Never expose port 5000 to the internet — only Nginx should call this.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
