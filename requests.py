
class Request:

    status = "Pending"

    def __init__(self,status):
        self.status = status

    def update_status(host_phone, status, requests_dict):
        requests_dict[host_phone] = status



