class Host:
    name = ""
    phone = ""
    address = ""
    is_vegan = False
    is_vegetarian = False
    is_religious = False
    bio = ""
    activity_list = []


    def __init__(self, name, phone, address, allergies, is_vegan, is_religious, bio, is_vegetarian):
        self.name = name
        self.phone = phone
        self.address = address
        self.allergies = allergies
        self.is_vegan = is_vegan
        self.is_vegetarian = is_vegetarian
        self.is_religious = is_religious
        self.bio = bio

    def add_activity(self, activity):
        self.activity_list.append(activity)

