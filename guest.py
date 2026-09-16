from db_config import db

class Guest:
    def __init__(self, name, phone, address, allergies, is_vegan, is_religious, bio, is_vegetarian):
        self.name = name
        self.phone = phone
        self.address = address
        self.allergies = allergies
        self.is_vegan = is_vegan
        self.is_vegetarian = is_vegetarian
        self.is_religious = is_religious
        self.bio = bio

    def add_guest_to_db(self):
        doc_ref = db.collection('guests').document(self.name)
        doc_ref.set({
            "phone": self.phone,
            "address": self.address,
            "allergies": self.allergies,
            "is_vegan": self.is_vegan,
            "is_vegetarian": self.is_vegetarian,
            "is_religious": self.is_religious,
            "bio": self.bio
        })
        print("Guest successfully added to DB!")