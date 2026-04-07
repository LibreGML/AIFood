import requests


r = requests.post('http://127.0.0.1:5000/api/register_third_party_server', json={
    'server_name_label': 'Qwen2.5_Cot-494M-F16',
    'server_config_path': './ThirdPartyServerConfig.ini'
})
print(r.json())

r2 = requests.post('http://127.0.0.1:5000/api/start_third_party_server', json={
    'server_name_label': 'Qwen2.5_Cot-494M-F16',
    'server_path': './llama_cpp_utils/llama-server.exe'
})
print(r2.json())