from db_config import db

class Host:
    def __init__(self, name, phone, address, is_vegan, is_religious, is_vegetarian, bio, activity_list=None):
        self.name = name
        self.phone = phone
        self.address = address
        self.is_vegan = is_vegan
        self.is_vegetarian = is_vegetarian
        self.is_religious = is_religious
        self.bio = bio
        self.activity_list = activity_list if activity_list is not None else []

    def add_host_to_db(self):
        doc_ref = db.collection('hosts').document(self.name)
        doc_ref.set({
            "phone": self.phone,
            "address": self.address,
            "is_vegan": self.is_vegan,
            "is_vegetarian": self.is_vegetarian,
            "is_religious": self.is_religious,
            "bio": self.bio,
            "activity_list": self.activity_list
        })

    def add_activity_to_db(self, activity):
        activity_data = {
            "host_name": self.name,
            "type of activity": activity.type_of_activity,
            "amount of people": activity.amount_of_people,
            "date": activity.date,
            "pending_guests": [],
            "approved_guests": []
        }

        new_doc_ref = db.collection('activities').add(activity_data)[1]
        activity_data['doc_id'] = new_doc_ref.id

        self.activity_list.append(activity_data)
        db.collection('hosts').document(self.name).update({
            "activity_list": self.activity_list
        })

    def add_activity(self, activity):
        self.add_activity_to_db(activity)