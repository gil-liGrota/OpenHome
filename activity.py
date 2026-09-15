import activity_constant
from host import Host

class Activity:
    hosting_details = Host
    type_of_activity = activity_constant.ACTIVITY_LIST[0]
    amount_of_people = 0
    date = "00/00/0000"

    def __init__(self, hosting_details, type_of_activity, amount_of_people, date):
        self.hosting_details = hosting_details
        self.type_of_activity = type_of_activity
        self.amount_of_people = amount_of_people
        self.date = date


