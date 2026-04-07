import subprocess
import configparser
from typing import NoReturn

from ConfigChecker import check_config

class ThirdPartyServerManager:

    __configs_and_status_dict = {}
    __now_running_dict = {}
    __now_exist_ports = []
    __last_running = None

    @classmethod
    def add_server(cls, model_name_label, config_path) -> None | NoReturn:
        if model_name_label == '':
            cls.stop_all_servers()
            raise Exception('model_name_label cannot be empty string')

        if model_name_label in cls.__configs_and_status_dict.keys():
            cls.stop_all_servers()
            raise Exception('This Server already exists.')

        try:
            configs = configparser.ConfigParser()
            configs.read(config_path)
            secs = configs.sections()
        except Exception as e:
            cls.stop_all_servers()
            raise Exception(f'Exception occurs while reading config file, exception: {e}')

        if model_name_label not in secs:
            cls.stop_all_servers()
            raise Exception('This model is not in configs.')

        is_config_checked_pass, missing_keys = check_config(dict(configs[model_name_label]), ['model_path', 'port'])
        if not is_config_checked_pass:
            cls.stop_all_servers()
            raise Exception(f'This config file {config_path} is invalid.Missing key(keys): {",".join(missing_keys)}')

        if configs[model_name_label].get('port') in cls.__now_exist_ports:
            cls.stop_all_servers()
            raise Exception('Ports conflicts.This port is already exist,please fix the config file ThirdPartyServerConfig.ini')

        cls.__now_exist_ports.append(configs[model_name_label].get('port'))

        cls.__configs_and_status_dict[model_name_label] = {
            'configs': configs[model_name_label],
            'status': 'offline',
            'process': None
        }

    @classmethod
    def remove_server(cls, model_name_label) -> None | NoReturn:
        if model_name_label == '':
            cls.stop_all_servers()
            raise Exception('model_name_label cannot be empty string')

        if model_name_label not in cls.__configs_and_status_dict.keys():
            cls.stop_all_servers()
            raise Exception('This Server does not exist.')

        if cls.__configs_and_status_dict.get(model_name_label).get('status') == 'online':
            cls.stop_all_servers()
            raise Exception('This Server is running.Please stop it before removing it')

        cls.__now_exist_ports.remove(
            cls.__configs_and_status_dict[model_name_label]['configs'].get('port')
        )
        del cls.__configs_and_status_dict[model_name_label]

    @classmethod
    def run_server(cls, server_path, model_name_label) -> None | NoReturn:
        if model_name_label == '':
            cls.stop_all_servers()
            raise Exception('model_name_label cannot be empty string')

        if model_name_label not in cls.__configs_and_status_dict.keys():
            cls.stop_all_servers()
            raise Exception('This Server does not exist.')

        if model_name_label in cls.__now_running_dict.keys():
            cls.stop_all_servers()
            raise Exception('This Server is already running.')

        cls.__configs_and_status_dict[model_name_label]['status'] = 'online'
        cls.__last_running = subprocess.Popen(
            f'{server_path} -m '
            f'{cls.__configs_and_status_dict[model_name_label]["configs"].get("model_path")} '
            f'--port {cls.__configs_and_status_dict[model_name_label]["configs"].get("port")} '
        )
        cls.__configs_and_status_dict[model_name_label]['process'] = cls.__last_running
        cls.__now_running_dict[model_name_label] = cls.__last_running

    @classmethod
    def stop_server(cls, model_name_label) -> None | NoReturn:
        if model_name_label == '':
            cls.stop_all_servers()
            raise Exception('model_name_label cannot be empty string')

        if model_name_label not in cls.__configs_and_status_dict.keys():
            cls.stop_all_servers()
            raise Exception('This Server does not exist.')

        if model_name_label not in cls.__now_running_dict.keys():
            cls.stop_all_servers()
            raise Exception('This Server is already stopped.')

        cls.__configs_and_status_dict[model_name_label]['status'] = 'offline'
        del cls.__now_running_dict[model_name_label]
        cls.__last_running = cls.__now_running_dict[list(cls.__now_running_dict.keys())[-1]] if list(
            cls.__now_running_dict.keys()) else None
        cls.__configs_and_status_dict[model_name_label]['process'].terminate()
        cls.__configs_and_status_dict[model_name_label]['process'] = None

    @classmethod
    def stop_all_servers(cls) -> None | NoReturn:
        for i in cls.__now_running_dict:
            cls.__now_running_dict[i].terminate()
        cls.__now_running_dict = {}
        for i in cls.__configs_and_status_dict:
            if cls.__configs_and_status_dict[i]['process']:
                cls.__configs_and_status_dict[i]['status'] = 'offline'
                cls.__configs_and_status_dict[i]['process'] = None
        cls.__last_running = None

    @classmethod
    def restart_server(cls, model_name_label, server_path, config_path) -> None | NoReturn:
        if model_name_label == '':
            cls.stop_all_servers()
            raise Exception('model_name_label cannot be empty string')

        cls.stop_server(model_name_label)
        cls.remove_server(model_name_label)
        cls.add_server(model_name_label, config_path)
        cls.run_server(server_path, model_name_label)

    @classmethod
    def restart_all_servers(cls) -> None | NoReturn:
        cls.__now_running_dict = {}
        cls.__last_running = None
        for i in cls.__configs_and_status_dict:
            if cls.__configs_and_status_dict[i]['status'] == 'online':
                cls.__configs_and_status_dict[i]['status'] = 'offline'
                cache_server_path = cls.__configs_and_status_dict[i]['process'].args.split()[0]
                cache_model_name_label = i
                cls.__configs_and_status_dict[i]['process'].terminate()
                cls.__configs_and_status_dict[i]['process'] = None
                cls.run_server(cache_server_path, cache_model_name_label)

    @classmethod
    def get_server_port(cls, model_name_label) -> None | NoReturn:
        if model_name_label == '':
            cls.stop_all_servers()
            raise Exception('model_name_label cannot be empty string')

        if model_name_label not in cls.__now_running_dict.keys():
            cls.stop_all_servers()
            raise Exception('This server is not running.')

        return cls.__now_running_dict[model_name_label].args.split()[-1]

    def __del__(self) -> None | NoReturn:
        self.stop_all_servers()

    def __delete__(self) -> None | NoReturn:
        self.stop_all_servers()

    @property
    def now_running_list(self) -> list[str]:
        return list(self.__now_running_dict.keys())

    @property
    def now_registered_models(self) -> list[str]:
        return list(self.__configs_and_status_dict.keys())

    @property
    def configs_and_status_dict(self) -> dict:
        return self.__configs_and_status_dict

    @property
    def last_running(self) -> subprocess.Popen:
        return self.__last_running

    @property
    def now_exist_ports(self) -> list[str]:
        return self.__now_exist_ports


    def extend_now_exist_ports(self, value: str | list) -> None | NoReturn:
        # 对外提供修改端口的接口，防止与其它服务冲突
        if type(value) == str:
            if value not in self.__now_exist_ports:
               self.__now_exist_ports.append(value)
        elif type(value) == list:
            self.__now_exist_ports.extend(value)
            self.__now_exist_ports = list(set(self.__now_exist_ports))  # 过滤已存在的端口
        else:
            self.stop_all_servers()
            raise TypeError('value must be str or list')
