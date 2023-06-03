from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Restaurant, MenuItem
from sqlalchemy import asc
from . import db
import re

main = Blueprint('main', __name__)

#Show all restaurants
@main.route('/')
@main.route('/restaurant/')
def showRestaurants():
  restaurants = db.session.query(Restaurant).order_by(asc(Restaurant.name))
  return render_template('restaurants.html', restaurants = restaurants)

#Create a new restaurant

@main.route('/restaurant/new/', methods=['GET','POST'])
@login_required
def newRestaurant():
  
  if request.method == 'POST':
    name = request.form['name']
    # Check if name contains only letters, spaces and '
    if not re.match("^[a-zA-Z ']*$", name):  
      flash('Valid name should only include letters, space and single quote.')
      return render_template('newRestaurant.html')
    newRestaurant = Restaurant(name=name)
    db.session.add(newRestaurant)
    flash('New Restaurant %s Successfully Created' % newRestaurant.name)
    db.session.commit()
    return redirect(url_for('main.showRestaurants'))
  else:
    return render_template('newRestaurant.html')


#Edit a restaurant
@main.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
@login_required
def editRestaurant(restaurant_id):
  editedRestaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      if request.form['name']:
        name = request.form['name']
        # Check if name contains only letters, spaces and '
        if not re.match("^[a-zA-Z ']*$", name):  
          flash('Invalid name. Name should only include letters, space and single quote.')
          return render_template('editRestaurant.html', restaurant = editedRestaurant)
        
        editedRestaurant.name = name
        flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
        db.session.commit()
        return redirect(url_for('main.showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant = editedRestaurant)



#Delete a restaurant
@main.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
@login_required
def deleteRestaurant(restaurant_id):
  restaurantToDelete = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
    db.session.delete(restaurantToDelete)
    flash('%s Successfully Deleted' % restaurantToDelete.name)
    db.session.commit()
    return redirect(url_for('main.showRestaurants', restaurant_id = restaurant_id))
  else:
    return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)

#Show a restaurant menu
@main.route('/restaurant/<int:restaurant_id>/')
@main.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', items = items, restaurant = restaurant)
     

#create new menu item
@main.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
@login_required
def newMenuItem(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      name = request.form['name']
      description = request.form['description']
      price = request.form['price']
      course = request.form['course']

      # Check if name contains only letters, spaces, numbers,single quotes and dash
      if not re.match("^[a-zA-Z0-9 '-]*$", name):  
          flash('validName only include letters, space, single quotes and number.')
          return render_template('newmenuitem.html', restaurant_id = restaurant_id)

      # Check if description contains only letters, numbers, single-quote, comma, fullstop, and dash
      if not re.match("^[a-zA-Z0-9 ',.-]*$", description):
          flash('valid description only include letters, numbers, single-quote, commas, full stops, and dashes.')
          return render_template('newmenuitem.html', restaurant_id = restaurant_id)

      # Check if price contains only digits
      if not price.isdigit():
          flash('Valid price should only include digits.')
          return render_template('newmenuitem.html', restaurant_id = restaurant_id)

      newItem = MenuItem(name = name, description = description, price = price, course = course, restaurant_id = restaurant_id)
      db.session.add(newItem)
      db.session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
  else:
      return render_template('newmenuitem.html', restaurant_id = restaurant_id)


#edit menu items
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
@login_required
def editMenuItem(restaurant_id, menu_id):

    editedItem = db.session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            #  name should contain only letters, spaces and '
            if not re.match("^[a-zA-Z ']*$", name):  
                flash('valid name only include letters, space, single quotes and number.')
                return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
            editedItem.name = name
        if request.form['description']:
            description = request.form['description']
            # description should contain only letters, numbers, ', comma, fullstop, and dash
            if not re.match("^[a-zA-Z0-9 ',.-]*$", description):
                flash('valid description only include letters, numbers, single-quote, commas, full stops, and dashes.')
                return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
            editedItem.description = description
        if request.form['price']:
            price = request.form['price']
            # price contains only digits
            if not price.isdigit():
                flash('Valid price should only include digits.')
                return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
            editedItem.price = price
        if request.form['course']:
            editedItem.course = request.form['course']
        db.session.add(editedItem)
        db.session.commit() 
        flash('Menu Item Successfully Edited')
        return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)



#Delete a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
@login_required
def deleteMenuItem(restaurant_id,menu_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    itemToDelete = db.session.query(MenuItem).filter_by(id = menu_id).one() 
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = itemToDelete)
