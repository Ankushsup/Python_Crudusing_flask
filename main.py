from flask import Flask, jsonify, request, abort
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ankush:root@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100))
    pet_type = db.Column(db.String(100))
    pet_age = db.Column(db.Integer())
    pet_description = db.Column(db.String(100))

    def __repr__(self):
        return "<Pet %r>" % self.pet_name

    def to_dict(self):
        return dict(id=self.id, pet_name=self.pet_name, pet_type=self.pet_type, pet_age=self.pet_age,
                    pet_description=self.pet_description)


# db.create_all()
@cross_origin()
@app.route('/pets', methods=["POST"])
def index():
    pet_data = request.get_json()
    id = pet_data.get('id')
    pet_name = pet_data.get('pet_name')
    pet_type = pet_data.get('pet_type')
    pet_age = pet_data['pet_age']
    pet_description = pet_data['pet_description']

    pet = Pet(id=id, pet_name=pet_name, pet_type=pet_type, pet_age=pet_age, pet_description=pet_description)
    db.session.add(pet)
    db.session.commit()
    return jsonify({"success": True, "response": "Pet address"})


@cross_origin()
@app.route("/pets/<int:pet_id>", methods=['PUT'])
def upd(pet_id):
    pet = Pet.query.get(pet_id)
    pet_age = request.json['pet_age']
    pet_description = request.json['pet_description']
    if pet is None:
        abort(404)
    else:
        pet.pet_age = pet_age
        pet.pet_description = pet_description
        db.session.add(pet)
        db.session.commit()
        return jsonify({"success": True, "response": "Pet details updates"})

@cross_origin()
@app.route("/pets/<int:pet_id>",methods=['DELETE'])
def dele(pet_id):
    pet=Pet.query.get(pet_id)
    if pet is None:
        abort(402)
    else:
        Pet.query.filter(Pet.id == pet_id).delete()
        db.session.commit()
        return jsonify({"Deleted Succesfully pet_id":True})


@cross_origin()
@app.route('/pets', methods=['GET'])
def get():
    all_pets = []
    pets = db.session.query(Pet).all()
    for pet in pets:
        all_pets.append(pet.to_dict())
    return jsonify(all_pets)


if __name__ == '__main__':
    app.run(debug=True)