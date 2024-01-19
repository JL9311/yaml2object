from config_reader import field, yaml_to_object, json_to_object


class ApplicationConfig:
    @field(name='server.name', required=True)
    def name(self):
        return self.name

    @field(name='server.version', required=True)
    def version(self):
        return self.version

    @field(name='server.port', required=True)
    def port(self):
        return self.port

    @field(name='server.host', required=True)
    def host(self):
        return self.host

    def __init__(self, name=None, version=None, port=None, host=None):
        self.name = name
        self.version = version
        self.port = port
        self.host = host


class JsonConfig:
    @field(name='llm.model', required=True)
    def model(self):
        return self.model

    @field(name='llm.api_key', required=True)
    def api_key(self):
        return self.api_key

    @field(name='auth.access_token', required=False)
    def access_token(self):
        return self.access_token

    @field(name='auth.refresh_token', required=True)
    def refresh_token(self):
        return self.refresh_token

    def __init__(self, model=None, api_key=None, access_token=None, refresh_token=None):
        self.model = model
        self.api_key = api_key
        self.access_token = access_token
        self.refresh_token = refresh_token


if __name__ == '__main__':
    config_file = open("application.yaml", encoding='utf-8')
    application_config = yaml_to_object(ApplicationConfig, config_file.read())
    print(application_config.name)
    print(application_config.version)
    print(application_config.port)
    print(application_config.host)

    json_file = open("application.json", encoding='utf-8')
    json_config = json_to_object(JsonConfig, json_file.read())
    print(json_config.model)
    print(json_config.api_key)
    print(json_config.access_token)
    print(json_config.refresh_token)
