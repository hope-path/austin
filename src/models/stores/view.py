from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from src.models.stores.store import Store
import src.models.users.decorators as user_decorators
store_blueprint = Blueprint('stores',__name__)

@store_blueprint.route('/')
def index():
    stores=Store.all()
    return render_template("stores/store_list.html",stores=stores)

@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    store=Store.get_by_id(store_id)
    return render_template("stores/store.html", store=store)


@store_blueprint.route('/load/<string:store_id>')
def load_page(store_id):
    store = Store.get_by_id(store_id)
    return redirect(store.url_prefix)


@store_blueprint.route('/create_store',methods=['POST','GET'])
@user_decorators.requires_admin_permission
def create_store():
    if request.method =='POST':
        name=request.form['name']
        url_prefix=request.form['url_prefix']
        tagname=request.form['tagname']

        quer =request.form['query']
        query=eval(quer)
        store=Store(name,url_prefix,tagname,query)
        store.save_to_mongo()
        return redirect(url_for("stores.index"))
    return render_template("stores/create_store.html")


@store_blueprint.route('/delete/<string:stores_id>')
@user_decorators.requires_admin_permission

def delete(stores_id):
    store = Store.get_by_id(stores_id)
    store.delete()
    return redirect(url_for('stores.index'))


@store_blueprint.route('/edit_store/<string:stores_id>',methods=['POST','GET'])
@user_decorators.requires_admin_permission

def edit_store(stores_id):
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tagname = request.form['tagname']
        quer = request.form['query']
        query = eval(quer)
        store = Store(name, url_prefix, tagname, query,stores_id)
        store.update_to_mongo()
        return redirect(url_for("stores.index"))
    return render_template("stores/edit_store.html", store=Store.get_by_id(stores_id))