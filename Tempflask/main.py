from flask import Flask, jsonify
from flask import request as flask_request
import logging

from ThirdPartyServerManager import ThirdPartyServerManager

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

third_party_server_manager = ThirdPartyServerManager()


@app.route('/api/register_third_party_server', methods=['POST'])
def register_third_party_server():
    server_name_label = flask_request.json['server_name_label']
    server_config_path = flask_request.json['server_config_path']

    try:
        ThirdPartyServerManager.add_server(server_name_label, server_config_path)
        return jsonify({'success': True, 'message': f'Server {server_name_label} registered successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to register server,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/unregister_third_party_server', methods=['POST'])
def unregister_third_party_server():
    server_name_label = flask_request.json['server_name_label']

    try:
        ThirdPartyServerManager.remove_server(server_name_label)
        return jsonify({'success': True, 'message': f'Server {server_name_label} unregistered successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to unregister server,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/start_third_party_server', methods=['POST'])
def start_third_party_server():
    server_name_label = flask_request.json['server_name_label']
    server_path = flask_request.json['server_path']

    try:
        ThirdPartyServerManager.run_server(server_path, server_name_label)
        return jsonify({'success': True, 'message': f'Server {server_name_label} started successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to start server,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/restart_third_party_server', methods=['POST'])
def restart_third_party_server():
    server_name_label = flask_request.json['server_name_label']
    server_path = flask_request.json['server_path']
    server_config_path = flask_request.json['server_config_path']

    try:
        ThirdPartyServerManager.restart_server(server_name_label, server_path, server_config_path)
        return jsonify({'success': True, 'message': f'Server {server_name_label} restarted successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to restart server,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/restart_all_third_party_servers', methods=['POST'])
def restart_all_third_party_servers():
    try:
        ThirdPartyServerManager.restart_all_servers()
        return jsonify({'success': True, 'message': 'All servers restarted successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to restart all servers,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stop_third_party_server', methods=['POST'])
def stop_third_party_server():
    server_name_label = flask_request.json['server_name_label']

    try:
        ThirdPartyServerManager.stop_server(server_name_label)
        return jsonify({'success': True, 'message': f'Server {server_name_label} stopped successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to stop server,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stop_all_third_party_servers', methods=['POST'])
def stop_all_third_party_servers():
    try:
        ThirdPartyServerManager.stop_all_servers()
        return jsonify({'success': True, 'message': 'All servers stopped successfully'}), 200
    except Exception as e:
        logger.error(f'Failed to stop all servers,error:{e}')
        return jsonify({'success': False, 'message': str(e)}), 500

app.run(debug=True)