#!encoding=utf-8
import config

class TokenExist(Exception):
    pass
class TokenNotFound(Exception):
    pass

class AgentHandler(object):
    def __init__(self, token):
        self.token = token
        self.state = 0 # supervisor STOPPED
        self.name = config.SUPERVISOR_NAME_TEMPLATE.format(token=self.token)
        self.last_update = 0
        self.start_time = 0
        self.stop_time = 0
        self.error_text = ''
        return

class InfoHolder(object):
    def __init__(self, name):
        self.name = name
        self.agents = {}
        self.system_basic = {}
        self.system_status = {}
    def add_agent(self, token):
        if token in self.agents:
            raise TokenExist()

        new = AgentHandler(token)
        self.agents[token] = new
        return new

    def remove_agent(self, token):
        if token not in self.agents:
            raise TokenNotFound()
        ret = self.agents[token]
        del self.agents[token]

        return ret
