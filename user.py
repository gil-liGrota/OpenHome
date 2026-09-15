class User:
    name = ""
    phone = ""
    address = ""
    allergies = ""
    is_vegan = False
    is_vegetarian = False
    is_religious = False
    bio = ""

    def __init__(self, name, phone, address, gender, is_hosting, allergies, is_vegan, is_religious, bio, is_vegetarian):
        self.name = name
        self.phone = phone
        self.address = address
        self.allergies = allergies
        self.is_vegan = is_vegan
        self.is_vegetarian = is_vegetarian
        self.is_religious = is_religious
        self.bio = bio


    def __str__(self):
        return str(self.name)
