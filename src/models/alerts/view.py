from flask import Blueprint, render_template, session, url_for, redirect, request

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as users_decorators
alert_blueprint = Blueprint('alerts',__name__)

@alert_blueprint.route('/')
@users_decorators.requires_login
def index():
    return render_template("alerts/alert_home.html")


@alert_blueprint.route('/new',methods=['GET','POST'])
@users_decorators.requires_login
def create_alert():
    if request.method =='POST':
        name = request.form['name']
        url = request.form['url']
        price_limit =float(request.form['price-li'])
        print(url, name, price_limit)
        item = Item(name, url)
        item.save_to_mongo()
        alert = Alert(session['email'],price_limit, item._id)
        alert.load_item_price()
        return redirect(url_for('users.user_alerts'))
    return render_template('alerts/create_alert.html')
@alert_blueprint.route('/edit/<string:alert_id>',methods=['GET','POST'])
@users_decorators.requires_login
def edit_alert(alert_id):
    if request.method =='POST':

        price_limit =float(request.form['price-li'])
        alert=Alert.find_by_id(alert_id)
        alert.price_limit=price_limit
        alert.save_to_mongo()
        return redirect(url_for('users.user_alerts'))
    return render_template('alerts/edit_alert.html',alert=Alert.find_by_id(alert_id))



@alert_blueprint.route('/deactivate/<string:alert_id>')
@users_decorators.requires_login
def deactivate_activate_alert(alert_id):
    alert = Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/delete/<string:alert_id>')
@users_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))



@alert_blueprint.route('/<string:alert_id>')
def get_alert_page(alert_id):
    alert=Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html', alert=alert)
@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass
@alert_blueprint.route('/check_alert/<string:alert_id>')
def check_price(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.load_item_price()
    return  redirect(url_for('alerts.get_alert_page',alert_id=alert._id))

