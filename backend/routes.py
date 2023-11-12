from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """ Returns list of urls of pictures"""
    if len(data) > 0:
        return [i["pic_url"] for i in data], 200
    return {"message": "Internal server error"}, 500


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """ Return a picture by id"""
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "Picture not found"}, 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        new_picture = request.json
        if any(picture['id'] == new_picture['id'] for picture in data):
            return {"Message": f"picture with id {new_picture['id']} already present"}, 302
        data.append(new_picture)
        return jsonify(new_picture), 201
    except NameError:
        return {"Message": "Data not defined"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    try:
        updated_picture = request.json
        for i, picture in enumerate(data):
            if picture["id"] == updated_picture["id"]:
                data[i] = updated_picture  # Update the original list
                return jsonify(updated_picture), 200
        return {"Message": "Picture not found"}, 404
    except NameError:
        return {"Message": "Data not defined"}, 500



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return {"Message": f"{id}"}, 204
    return {"Message": "picture not found"}, 404
