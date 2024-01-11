from flask import Flask, jsonify, request
from utils.database import connect
from config_loader import load_config


app = Flask(__name__)
config = load_config()

@app.route('/')
def index():
    return "Welcome to Bridge Legal Inbound Alert Tool!"


@app.route('/inbound/history', methods=['GET'])
def get_org_inbound_history():
    org_id = request.args.get('inOrganizationId', type=int)
    if org_id is None:
        return jsonify({"error": "Missing organization ID"}), 400
    
    conn, tunnel = connect(config)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bl_venture_openapi.bl_request_log WHERE organization_id=%s", (org_id,))
            request_list = cursor.fetchall()
            return jsonify(request_list)
    finally:
        conn.close()
        tunnel.stop()

@app.route('/inbound/history/detail', methods=['GET'])
def get_request_detail():
    request_id = request.args.get("id", type=int)
    if request_id is None:
        return jsonify({"error": "Missing request ID"}), 400

    conn, tunnel = connect(config)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bl_venture_openapi.bl_request_analyse_result WHERE request_log_id=%s", (request_id))
            request_detail = cursor.fetchall()
            return jsonify(request_detail)
    finally:
        conn.close()
        tunnel.stop()

if __name__ == '__main__':
    app.run(debug=True)
