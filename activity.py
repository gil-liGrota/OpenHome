import activity_constant

class Activity:
    type_of_activity = activity_constant.ACTIVITY_LIST[0]
    amount_of_people = 0
    date = "00/00/0000"

    def __init__(self,  type_of_activity, amount_of_people, date):
        self.type_of_activity = type_of_activity
        self.amount_of_people = amount_of_people
        self.date = date


