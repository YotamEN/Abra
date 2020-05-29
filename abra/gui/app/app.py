from abra.common import *
from flask import render_template, Blueprint, request, current_app, send_from_directory
from json import loads
import requests


app_bp = Blueprint('app_bp', __name__, template_folder='templates', static_folder='static')


@app_bp.route('/', methods=['GET'])
def homepage():
    return render_template("main.html")


@app_bp.route(f'/users/', methods=['GET'])
def users_page():
    gui_url, api_url = get_urls()

    users_out = []
    if request.method == 'GET':
        response = requests.get(api_url + f'/users')
        users = response.json()
        for user_json in users:
            user_json = loads(user_json)
            users_out.append({
                USER_ID_KEY: user_json[USER_ID_KEY],
                USERNAME_KEY: user_json[USERNAME_KEY],
                USER_URL_KEY: f'{gui_url}/users/{user_json[USER_ID_KEY]}',
                USER_SNAPSHOTS_URL_KEY: f'{gui_url}/users/{user_json[USER_ID_KEY]}/snapshots'
            })
        return render_template("users.html", users=users_out)


@app_bp.route("/users/<int:user_id>/", methods=['GET'])
def user_page(user_id):
    gui_url, api_url = get_urls()

    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}')
        user_info = response.json()
        user_info[USER_SNAPSHOTS_URL_KEY] = f'/users/{user_id}/snapshots'
        return render_template("user.html", user=user_info)


@app_bp.route("/users/<int:user_id>/snapshots/", methods=['GET'])
def user_snapshots(user_id):
    gui_url, api_url = get_urls()

    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}/snapshots')
        snapshots = response.json()
        return render_template("user_snapshots.html", snapshots=snapshots, user_id=user_id)


@app_bp.route("/users/<int:user_id>/snapshots/<snapshot_id>/", methods=['GET'])
def snapshot_page(user_id, snapshot_id):
    gui_url, api_url = get_urls()
    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}/snapshots/{snapshot_id}')
        snapshot = response.json()
        snapshot[USER_ID_KEY] = user_id
        return render_template("snapshot.html", data=snapshot)


@app_bp.route("/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>/", methods=['GET'])
def result_page(user_id, snapshot_id, result_name):
    gui_url, api_url = get_urls()

    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}/snapshots/{snapshot_id}/{result_name}')
        result = response.json()
        if result is None:
            print(f"Error while trying to get result. Possibly available results: {TOPICS}")
        result[RESULT_NAME_KEY] = result_name
        image_path = f"{gui_url}/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data/"
        return render_template("result.html", result=result, image_path=image_path)


@app_bp.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data/', methods=['GET'])
def get_image(user_id, snapshot_id, result_name):
    gui_url, api_url = get_urls()

    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}/snapshots/{snapshot_id}/{result_name}')
        result = response.json()
        path = result[RESULT_URL_KEY]
        path = path.split("/")
        img_dir, img_file = "/".join(path[:-1]), path[-1]
        return send_from_directory(img_dir, img_file)


def get_urls():
    gui_host = current_app.config['gui_host']
    gui_port = current_app.config['gui_port']
    api_host = current_app.config['api_host']
    api_port = current_app.config['api_port']
    gui_url = f'http://{gui_host}:{gui_port}'
    api_url = f'http://{api_host}:{api_port}'
    return gui_url, api_url
