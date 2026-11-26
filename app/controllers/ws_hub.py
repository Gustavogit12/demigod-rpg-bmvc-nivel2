import json


class WebSocketHub:
    def __init__(self):
        self.clients = set()

    def register(self, ws):
        self.clients.add(ws)

    def unregister(self, ws):
        self.clients.discard(ws)

    def broadcast(self, payload: dict):
        message = json.dumps(payload, ensure_ascii=False)
        dead_clients = []
        for ws in list(self.clients):
            try:
                ws.send(message)
            except Exception:
                dead_clients.append(ws)
        for ws in dead_clients:
            self.unregister(ws)


hub = WebSocketHub()