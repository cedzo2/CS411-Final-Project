import pymongo

conn=pymongo.MongoClient()
db = conn.academicworld

def get_faculty_info(input_value):
    query = db.faculty.aggregate([
        {"$match": {"name":input_value}},
        {"$project":{"_id":0, "name":1, "position":1, "email":1, "phone":1, "researchInterest":1, "publications":{"$size":"$publications"}, "affiliation.name":1, "photoUrl":1}}
    ])

    faculty_dict = {}
    for x in query:
        for key in x.keys():
            if x[key] is None:
                faculty_dict[key] = "N/A"
            else:
                faculty_dict[key] = x[key]
                
    return faculty_dict

def get_universities():
    query = db.faculty.distinct("affiliation.name")
    return query

def get_faculty(input_value):
    query = db.faculty.distinct("name", {"affiliation.name": input_value})
    return query

# "Adalbert Gerald Soosai Raj"