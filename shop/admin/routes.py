from shop import app, db, bcrypt
from flask import render_template, request, session, redirect, url_for, flash, jsonify
import stripe
import re
from .forms import RegistrationForm, LoginForm, AdminRegistrationForm, ProductForm
from .models import User, Admin, Product, Order, OrderItem

# home page
@app.route("/")
def home():
    return render_template('pages/home.html', title='SecureCart Home Page')

# validate the password during registration
def validate_password(password):
    errors = [] # list for tracking errors

    if len(password) < 8: # password must be at least 8 characters
        errors.append('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password): # password must have one capital letter
        errors.append('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password): # password must have at least one lowercase letter
        errors.append('Password must contain at least one lowercase letter.')
    if not re.search(r'[0-9]', password): # password must contain at least one digit
        errors.append('Password must contain at least one digit.')
    if not re.search(r'[@$!%*?&]', password): # password must contain at least one special character
        errors.append('Password must contain at least one special character (@, $, !, %, *, ?, &).')
    return errors

# customer register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # validate the user's input into the form
        password_errors = validate_password(form.password.data) # run the validate_password function above
        # list all of the errors with the user's password
        if password_errors:
            for error in password_errors:
                flash(error, 'danger')
            return render_template('pages/register.html', form=form)

        existing_user = User.query.filter_by(username=form.username.data).first() # check if the username is already used

        # display to the user that their username is taken
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('pages/register.html', form=form)

        # display to the user that their email is taken
        existing_email = User.query.filter_by(email=form.email.data).first() # check if the email is already used
        if existing_email:
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('pages/register.html', form=form)

        # check passwords match
        if form.password.data.strip() != form.confirm.data.strip():
            flash('The passwords do not match. Please re-enter the passwords.', 'danger')
            return render_template('pages/register.html', form=form)

        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash and decode to string

        # adding the user's details to the database
        user = User(
            name=form.name.data.strip(),
            surname=form.surname.data.strip(),
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            password=hash_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Account successfully created!', 'success') # show the user their accunt was created
        return redirect(url_for('home')) # go back to the home page

    else:
        # display all errors if the user's input is wrong
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", 'danger') # display all the errors to the user
                return redirect(
                    url_for('register'))

    return render_template('pages/register.html', form=form) # display the register page

# customer login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # check in the database if the user's entered credentials match

        # authenticate the user if their credentials are correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # create session values for the user
            session['id'] = user.id
            session['username'] = form.username.data
            session['email'] = user.email
            return redirect(url_for('all_products'))
        else:
            # display to the user that their username or password was incorrect
            flash('Invalid username or password. Please try again.', 'danger')  # Flash message on failed login
            return redirect(url_for('login'))

    return render_template('pages/login.html', form=form, title="SecureCart Login Page")

# admin register page
@app.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegistrationForm(request.form)
    if form.validate_on_submit():
        password_errors = validate_password(form.password.data) # use the password_validation function

        # list all of the errors with the user's password
        if password_errors:
            for error in password_errors:
                flash(error, 'danger')
            return render_template('pages/admin-register.html', form=form)

        existing_admin = Admin.query.filter_by(username=form.username.data).first() # use the database to check if the username the admin has chosen is taken

        # tell the admin that their chosen username exists
        if existing_admin:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('pages/admin-register.html', form=form)

        # tell the admin that their chosen email exists
        existing_email = Admin.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('pages/admin-register.html', form=form)

        # check passwords match
        if form.password.data.strip() != form.confirm.data.strip():
            flash('The passwords do not match. Please re-enter the passwords.', 'danger')
            return render_template('pages/admin-register.html', form=form)

        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash and decode to string

        # add the admin's details to the Admin table of the database
        admin = Admin(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            password=hash_password
        )
        db.session.add(admin)
        db.session.commit()

        # create session values for the admin
        session['username'] = form.username.data

        # display a message to the admin that their account was successfully created
        flash('Account successfully created!', 'success')
        return redirect(url_for('home'))
    else:
        # display all errors if the admin's input is wrong
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", 'danger')
                return redirect(
                    url_for('admin_register'))

    return render_template('pages/admin-register.html', form=form)

# admin login page
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first() # check in the database if the admin's entered credentials match

        # display the admin's dashboard if their credentials are correct and create session values
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            # create session values for the user
            session['id'] = admin.id
            session['username'] = admin.username
            session['email'] = admin.email
            return redirect(url_for('admin_dashboard'))  # Or any page you want to redirect to
        else:
            # create session values for the user
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('admin_login'))  # Ensure this points to the correct route
    return render_template('pages/admin-login.html', form=form)

# admin dashboard page
@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'id' not in session: # if the user hasn't logged in
        flash('Admin access required.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else: # otherwise if the user has logged in
        products = Product.query.all() # gather all of the products from the database
        orders = Order.query.join(User).all() # gather all of the orders from the database
        order_items = OrderItem.query.all() # gather all of the items ordered from the database
        active_users = User.query.all() # gather all of the users that have registered from the database

        return render_template(
            'pages/admin-dashboard.html',
            products=products,
            orders=orders,
            order_items=order_items,
            active_users=active_users
        )

# page for adding new products for admins
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'id' not in session:  # if the admin hasn't logged in
        flash('Admin access required.', 'danger')  # display to the admin that they need to login
        return redirect(url_for('home'))
    else:  # otherwise if the admin has logged in
        form = ProductForm() # take the information that the admin submitted on the form

        # add the new product to the "Product" table on the database
        if form.validate_on_submit():
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                image_url=form.image_url.data.filename
            )
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))

        return render_template('pages/add-product.html', form=form)

# deleting a product from the system
@app.route('/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'id' not in session:  # if the admin hasn't logged in
        return jsonify({'error': 'Admin access required.'}), 403  # return a JSON error with 403 status code
    product = Product.query.get(product_id)

    if not product:  # if the product doesn't exist
        return jsonify({'error': 'Product not found.'}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True}), 200  # respond with success
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Error deleting product.'}), 500  # respond with error


# displays the store's products to the user
@app.route('/products')
def all_products():
    if 'id' not in session: # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else: # otherwise if the user has logged in
        products = Product.query.all()  # Fetch all products from the database
        return render_template('pages/all-products.html', products=products)

# add the items to the cart
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'id' not in session: # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else: # otherwise if the user has logged in

        # check if the cart has been created
        if 'cart' not in session:
            session['cart'] = {}

        cart = session['cart']
        quantity = int(request.form.get('quantity', 1)) # get the quantity of the product the user wants

        cart[str(product_id)] = quantity
        session.modified = True
        session['cart'] = cart
        return redirect(url_for('all_products'))

# view page
@app.route('/view-cart')
def view_cart():
    if 'id' not in session:  # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else:  # otherwise if the user has logged in
        cart_items = []
        total_items = 0
        total_price = 0

        if 'cart' in session:  # check if the cart exists in the session
            cart = session['cart']  # get the cart from the session
            product_ids = [int(pid) for pid in cart.keys()]  # convert product IDs to integers

            # fetch products matching the IDs in the cart
            products = Product.query.filter(Product.id.in_(product_ids)).all()

            # loop through each product to calculate totals
            for product in products:
                quantity = cart.get(str(product.id), 0)  # get the quantity for the product
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': product.price * quantity  # calculate subtotal for the product
                })
                total_items += quantity  # update total item count
                total_price += product.price * quantity  # update total price

            session['amount'] = total_price  # save total price in session
            session.modified = True  # mark session as updated

        return render_template('pages/view-cart.html', cart_items=cart_items, total_items=total_items, total_price=total_price)

# payments page
@app.route('/payments', methods=['GET'])
def payments():
    if 'id' not in session:  # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else:  # otherwise if the user has logged in
        cart_items = []
        total_items = 0
        total_price = 0

        if 'cart' in session:  # check if the cart exists in the session
            cart = session['cart']  # get the cart from the session
            product_ids = [int(pid) for pid in cart.keys()]  # convert product IDs to integers

            # fetch products matching the IDs in the cart
            products = Product.query.filter(Product.id.in_(product_ids)).all()

            # loop through each product to calculate totals
            for product in products:
                quantity = cart.get(str(product.id), 0)  # get the quantity for the product
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': product.price * quantity  # calculate subtotal for the product
                })
                total_items += quantity  # update total item count
                total_price += product.price * quantity  # update total price

            session['amount'] = total_price  # save total price in session
            session.modified = True  # mark session as updated
        else:
            flash("Please add items to the cart first.", "error")
            return redirect(url_for('all-products'))

        return render_template('pages/payments.html', cart_items=cart_items, total_items=total_items, total_price=total_price)

# remove a product from the cart
@app.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'id' not in session:  # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else:  # otherwise if the user has logged in
        if 'cart' in session: # check if the cart exists in the session
            cart = session['cart'] # get the cart from the session
            if str(product_id) in cart:
                del cart[str(product_id)]  # remove the product from the cart
                session.modified = True  # mark the session as modified
                return redirect(url_for('view_cart'))
            else:
                flash('Please add items to the cart first.', 'danger')
                return redirect(url_for('all-products'))
        else: # if the cart isn't in the session
            flash('Cart is empty.', 'warning') # display a message to the user that the cart is empty
            return redirect(url_for('view_cart'))

# make payment
@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    if 'id' not in session:  # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else:  # otherwise if the user has logged in
        total_price = request.json.get('total_price') # get the total price from the webpage
        payment_intent = stripe.PaymentIntent.create(
            amount=total_price,
            currency='gbp',
        ) # initiate the payment
        cart = session.get('cart', {}) # get the products from the cart
        return jsonify({'client_secret': payment_intent.client_secret})

# success page
@app.route('/success')
def success():
    if 'id' not in session:  # if the user hasn't logged in
        flash('Please create an account with SecureCart first.', 'danger') # display to the user that they need to login
        return redirect(url_for('home'))
    else:  # otherwise if the user has logged in
        cart_items = []
        total_items = 0
        total_price = 0

        if 'id' in session:  # check if the user is logged in
            if 'cart' in session:
                cart = session['cart']  # get the cart from the session
                product_ids = [int(pid) for pid in cart.keys()]  # convert cart keys (product ids) to integers

                # get the products from the database that are in the cart
                products = Product.query.filter(Product.id.in_(product_ids)).all()

                # go through each product to calculate total quantities and prices
                for product in products:
                    product_id_str = str(product.id)  # make sure product id is a string (to match session keys)
                    quantity = cart.get(product_id_str, 0)  # get how many of this product are in the cart (default to 0)

                    # add product details and calculate the subtotal
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'subtotal': product.price * quantity  # subtotal for this product (price * quantity)
                    })

                    # add to total items and total price
                    total_items += quantity
                    total_price += product.price * quantity

                # create a new order in the database with the total price and user id
                new_order = Order(
                    total_price=total_price,
                    user_id=session.get('id')  # link the order to the user
                )
                db.session.add(new_order)  # add the new order to the database
                db.session.commit()  # save the new order

                # add each item from the cart to the order
                for cart_item in cart_items:
                    order_item = OrderItem(
                        order_id=new_order.id,  # link the item to the new order
                        product_id=cart_item['product'].id,  # product id from the cart
                        quantity=cart_item['quantity'],  # how many of this product
                        subtotal=cart_item['subtotal']  # subtotal for this product (price * quantity)
                    )
                    db.session.add(order_item)  # add the order item to the database

                db.session.commit()  # save all the order items

                # clear the cart and total amount from the session after the order
                session.pop('cart', None)  # remove the cart from the session
                session.pop('amount', None)  # remove the total amount from the session
            else:
                flash('Please add items to the cart first.', 'danger')
                return redirect(url_for('all-products'))
        else:
            flash('Please create an account with SecureCart first.',
                  'danger')  # display to the user that they need to login
            return redirect(url_for('home'))

        return render_template('pages/confirmation.html',
                               cart_items=cart_items,
                               total_items=total_items,
                               total_price=total_price)

# logout
@app.route('/logout')
def logout():
    if 'id' in session: # check if id is in session
        session.pop('id', None)  # remove from session
        session.pop('cart', None) # remove from session
        return redirect(url_for('home'))
