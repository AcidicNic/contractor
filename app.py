from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

#with heroku
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/PlantStore')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

# without heroku
# client = MongoClient()
# db = client.PlantStore

plants = db.plants


@app.route('/')
def plants_index():
    ''' home page, lists all of the plant lsitings '''
    return render_template('plants_index.html', plants=plants.find())


@app.route('/plants/<plant_id>')
def plants_show(plant_id):
    ''' shows the info for one individual plant '''
    plant = plants.find_one({'_id': ObjectId(plant_id)})
    return render_template('plants_show.html', plant=plant)


@app.route('/plants/new')
def plants_new():
    ''' form to create a listing '''
    return render_template('plants_new.html', plant={}, title='Add a Plant!')


@app.route('/plants', methods=['POST'])
def plants_submit():
    ''' add new plant to the database and redirect to that plant's page '''
    plant = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    plant_id = plants.insert_one(plant).inserted_id
    return redirect(url_for('plants_show', plant_id=plant_id))


@app.route('/plants/<plant_id>/edit')
def plans_edit(plant_id):
    ''' form to edit a plant's listing '''
    plant = plants.find_one({'_id': ObjectId(plant_id)})
    return render_template('plants_edit.html', plant=plant, title='Edit Listing')


@app.route('/plants/<plant_id>', methods=['POST'])
def plants_update(plant_id):
    ''' add updated info of a plant to the database and redirect to that plant's page '''
    updated_plant = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    plants.update_one(
        {'_id': ObjectId(plant_id)},
        {'$set': updated_plant})
    return redirect(url_for('plants_show', plant_id=plant_id))


@app.route('/plants/<plant_id>/delete', methods=['POST'])
def plants_delete(plant_id):
    ''' delete a plant from the database, redirect to the home page '''
    plants.delete_one({'_id': ObjectId(plant_id)})
    return redirect(url_for('plants_index'))


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
