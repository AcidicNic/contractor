from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.PlantStore
plants = db.plants


@app.route('/')

def plants_index():
    return render_template('plants_index.html', plants=plants.find())


@app.route('/plants', methods=['POST'])
def plants_submit():
    plant = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    plant_id = plants.insert_one(plant).inserted_id
    return redirect(url_for('plants_show', plant_id=plant_id))


@app.route('/plants/<plant_id>', methods=['POST'])
def plants_update(plant_id):
    updated_plant = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    plants.update_one(
        {'_id': ObjectId(plant_id)},
        {'$set': updated_plant})
    return redirect(url_for('plants_show', plant_id=plant_id))


@app.route('/plants/new')
def plants_new():
    return render_template('plants_new.html', plant={}, title='Add a Plant!')


@app.route('/plants/<plant_id>/edit')
def plans_edit(plant_id):
    plant = plants.find_one({'_id': ObjectId(plant_id)})
    return render_template('plants_edit.html', plant=plant, title='Edit Listing')


@app.route('/plants/<plant_id>/delete', methods=['POST'])
def plants_delete(plant_id):
    plants.delete_one({'_id': ObjectId(plant_id)})
    return redirect(url_for('plants_index'))


@app.route('/plants/<plant_id>')
def plants_show(plant_id):
    plant = plants.find_one({'_id': ObjectId(plant_id)})
    return render_template('plants_show.html', plant=plant)


if __name__ == '__main__':
    app.run(debug=True, port=5454)