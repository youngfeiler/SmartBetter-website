from flask import Flask, render_template, jsonify, request
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import Flask-CORS
from flask_wtf.csrf import CSRFProtect
from flask import make_response
import plotly.graph_objects as go
import plotly as plotly
from functionality.user import User
from functionality.database import database
from functionality.result_updater import result_updater
from functionality.live_dashboard_runner import live_dashboard_runner
import functionality.tasks as tasks
from functionality.util import american_to_decimal, decimal_to_american
import pandas as pd
from functionality.tasks import celery
import json
from datetime import timedelta
from datetime import datetime
import os
import stripe
import time
import atexit
from functionality.db_manager import DBManager
from functionality.models import LoginInfo  
from functionality.models import VerificationCode
import warnings
warnings.filterwarnings("ignore")
from flask_socketio import SocketIO
from chat import Chat
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from threading import Thread
import time
import pandas as pd
import flock as flock
# from amplitude import Amplitude
# from amplitude import BaseEvent



def create_app():
    app = Flask(__name__, template_folder='static/templates', static_folder='static')
    # TODO: Put this key in the secret file
    app.secret_key = 'to_the_moon'
    app.db_manager = DBManager()
    app.db = database(app.db_manager)
    app.celery = celery
    # app.chat = Chat()
    app.chat = Chat()
    # app.amplitude = Amplitude("f3e43aeacf3279a00145b345a0fc8861")
    # app.amplitude.include_utm = True
    # app.amplitude.include_referrer = True
    # app.amplitude.include_gclid = True
    # app.amplitude.include_fbclid = True

    return app

app = create_app()

socketio = SocketIO(app)


app.config['STRIPE_PUBLIC_KEY'] = 'pk_live_51Nm0vBHM5Jv8uc5M5hu3bxlKg6soYb2v9xSg5O7a9sXi6JQJpl7nPWiNKrNHGlXf5g8PFnN6sn0wcLOrixvxF8VH00nVoyGtCk'
app.config['STRIPE_PRIVATE_KEY'] = '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'
stripe.api_key = app.config['STRIPE_PRIVATE_KEY']

@atexit.register
def close_db():
    app.db_manager.close()

@app.route('/')
def index():
    is_logged_in = True if 'user_id' in session else False

    return render_template('landing_page.html', 
                           checkout_public_key=app.config['STRIPE_PUBLIC_KEY'],
                           is_logged_in = is_logged_in)

@app.route('/about')
def about():
    is_logged_in = True if 'user_id' in session else False

    return render_template('about_us.html', is_logged_in = is_logged_in)

@app.route('/how_it_works')
def how_it_works():
    is_logged_in = True if 'user_id' in session else False

    return render_template('how_it_works.html', is_logged_in = is_logged_in)

@app.route('/product')
def product():
    is_logged_in = True if 'user_id' in session else False

    return render_template('product.html', is_logged_in = is_logged_in)

@app.route('/scenarios')
def scenarios():
    is_logged_in = True if 'user_id' in session else False

    return render_template('scenarios.html', is_logged_in = is_logged_in)

@app.route('/pregame')
def pregame_beta():
    is_logged_in = True if 'user_id' in session else False

    return render_template('pregame.html', is_logged_in = is_logged_in)

@app.route('/positive_ev')
def positive_ev():
    is_logged_in = True if 'user_id' in session else False
    return render_template('positive_ev_dashboard.html', is_logged_in = is_logged_in)

@app.route('/arbitrage')
def arbitrage():
    is_logged_in = True if 'user_id' in session else False
    return render_template('arbitrage.html', is_logged_in = is_logged_in)

@app.route('/get_team_vals_for_scenarios', methods=['GET', 'POST'])
def get_team_vals_for_scenarios():
       teams = pd.read_csv('../extra_info_sheets/teams.csv')
       teams.sort_values(by="team", inplace=True)
       return teams.to_json(orient='records', date_format='iso')

@app.route('/get_divisions_teams_from_conference', methods=['GET', 'POST'])
def get_divisions_teams_from_conference():
    try: 
        data = request.json
        input_conference = data['conference']
        teams = pd.read_csv('../extra_info_sheets/teams.csv')
        return_df = teams[teams['conference'] == input_conference]
        
        return return_df.to_json(orient='records', date_format='iso')
    except Exception as e:
        print(e)

@app.route('/get_teams_from_division', methods=['GET', 'POST'])
def get_teams_from_division():
    try: 
        data = request.json
        input_division = data['division']
        input_conference = data['conference']
        teams = pd.read_csv('../extra_info_sheets/teams.csv')
        return_df = teams[teams['division'] == input_division]
        return_df = return_df[return_df['conference'] == input_conference]
        
        return return_df.to_json(orient='records', date_format='iso')
    except Exception as e:
        print(e)
    
@app.route('/get_scenario_data', methods=['GET', 'POST'])
def get_scenario_data():
    try:
        data = request.json
        print(data)
        db = database()
        start = time.time()

        graph_data = db.get_scenario_results(app.config['raw_odds_data'], data)
        
        print(graph_data)

        end = time.time()

        print(f"time to run: {end - start}")

        return graph_data

        # response = {'status_code': 'success', 'message': f'Sport recieved: {sport}'}
    except Exception as e:
        print(e)
        response = {'status_code': 'error', 'message': str(e)}

    return response

@app.route('/checkout/<string:price_id>')
def create_checkout_session(price_id):
    if price_id == "price_1OZhXvHM5Jv8uc5MyZO28LI1":
        price = 15
    elif price_id == "price_1OZhdhHM5Jv8uc5MaLORELDu":
        price = 50
    else:
        price = 20
    trakdesk_cid = request.args.get('client_reference_id')

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        allow_promotion_codes=True,
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='subscription',
        client_reference_id=trakdesk_cid,
       success_url=url_for('success_checkout', _external=True) + '?session_id={CHECKOUT_SESSION_ID}' + f'&price={price}',
        cancel_url=url_for('index', _external=True),

    )
    return redirect(checkout_session.url,code=302)

@app.route('/checkout_free_trial/<string:price_id>')
def create_checkout_session_free_trial(price_id):
    if price_id == "price_1OZhXvHM5Jv8uc5MyZO28LI1":
        price = 15
    elif price_id == "price_1OZhdhHM5Jv8uc5MaLORELDu":
        price = 50
    else:
        price = 20
    trial_end_date = int((datetime.utcnow() + timedelta(days=8)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    trakdesk_cid = request.args.get('client_reference_id')
    print(trakdesk_cid)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        allow_promotion_codes=True,
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='subscription',
        client_reference_id=trakdesk_cid,
        success_url=url_for('free_success_checkout', _external=True) + '?session_id={CHECKOUT_SESSION_ID}' + f'&price={price}',
        cancel_url=url_for('index', _external=True),
        subscription_data = {
             'trial_end': trial_end_date
        }
    )
    return redirect(checkout_session.url,code=302)

@app.route('/free_success_checkout')
def free_success_checkout():
    checkout_session_id = request.args.get('session_id')
    price = request.args.get('price')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer_email = checkout_session['customer_details']['email']


    # app.amplitude.track(
    #     BaseEvent(
    #         event_type="Sign Up",
    #         device_id=customer_email,
    #         event_properties={
    #             "price": 'free',
    #             "checkout_id": checkout_session_id,
    #             "customer_email": customer_email
    #         }
    #     )
    # )
    return redirect(url_for('register', _external=True) + f'?session_id={checkout_session_id}&price={price}')

@app.route('/success_checkout')
def success_checkout():
    checkout_session_id = request.args.get('session_id')
    price = request.args.get('price')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer_email = checkout_session['customer_details']['email']

    # app.amplitude.track(
    #     BaseEvent(
    #         event_type="Sign Up",
    #         device_id=customer_email,
    #         event_properties={
    #             "price": 'free',
    #             "checkout_id": checkout_session_id,
    #             "customer_email": customer_email
    #         }
    #     )
    # )
    return redirect(url_for('register', _external=True) + f'?session_id={checkout_session_id}&price={price}')


@app.route('/get_positive_ev_data')
def get_positive_ev_data():

    data = request.get_json()
    sport_title = data.get('sport_title', '')

    try:
        bankroll = app.db.get_user_bank_roll(session["user_id"])
    except:
        bankroll = 5000
    print(bankroll)

    data = app.db.get_live_dash_data(session['user_id'], sport_title)

    print(data)
    if data.empty:
        data = pd.DataFrame(columns=['bankroll', 'update'])
        data = data.append({'bankroll': bankroll, 'update': False}, ignore_index=True)
    else:
        data['bankroll'] = bankroll
    data_json = data.to_dict(orient='records')

    return jsonify(data_json)

@app.route('/get_arbitrage_dash_data', methods=['POST'])
def get_arbitrage_dash_data():

    data = request.get_json()
    
    filters = data.get('filters', '')

    try:
        bankroll = app.db.get_user_bank_roll(session["user_id"])
    except KeyError:
        bankroll = 5000

    data = app.db.get_arbitrage_dash_data(filters, bankroll)
    
    if data.empty:
        data = pd.DataFrame(columns=['bankroll', 'update'])
        data = data.append({'bankroll': bankroll, 'update': False}, ignore_index=True)
    else:
        data['bankroll'] = bankroll
    data_json = data.to_dict(orient='records')

    return jsonify(data_json)

@app.route('/test_func')
def test_func():
    tasks.start_dashboard_runner.delay()
    return render_template('nba.html')

@app.route('/home')
def home():
    is_logged_in = True if 'user_id' in session else False

    return render_template('landing_page.html', is_logged_in = is_logged_in)

@app.route('/account')
def account():
  is_logged_in = True if 'user_id' in session else False

  if 'user_id' in session:
        users = app.db.get_user_info(session['user_id'])
        return render_template('account_settings.html', users = users, is_logged_in = is_logged_in)
  else:
        return redirect(url_for('login'))

@app.route('/performance')
def show_performance():
  is_logged_in = True if 'user_id' in session else False

  return render_template('performance.html', is_logged_in = is_logged_in)

    
@app.route('/update_bankroll', methods=['POST'])
def update_bankroll():
    if request.method == 'POST':
        new_bankroll = request.form.get('Name-5')
        success = app.db.update_bankroll(session['user_id'], new_bankroll)
        if success:
            flash('Your bankroll has been updated!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Your bankroll was not updated. Please try again.', 'error')
            return redirect(url_for('account'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    app.db.get_all_usernames()
    app.db.check_payments()
    users = app.db.users
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['email'].lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = '+1' + str(request.form['phone_number'])
        bankroll = request.form['bankroll']
        sign_up_date = datetime.now()
        payed = False
        how_heard = request.form['how_heard']
        referral_name = request.form['referral_name']
        other_source = request.form['other_source']
        if username in users:

            has_payed=app.db.check_duplicate_account(username)

            if has_payed:
                payed = True
                app.db.add_user(first_name, last_name, username, password, phone, bankroll, sign_up_date, payed, how_heard, referral_name, other_source)
                print("add_user complete")

                users = app.db.users
                print("users complete")

                login_allowed = app.db.check_login_credentials(username, password)
                print("login_allowed complete")

                if login_allowed:
                    session['user_id'] = username
                    return redirect(url_for('show_nba'))
                elif not login_allowed:
                    error_message = "Email or password incorrect. Please try again."
                    return render_template('register.html', incorrect_password=True, form_data=request.form, error_message=error_message)     
        
            else:
                error_message = "Account with this Email already exists. Please try again."
                return render_template('register.html', username_exists=True, form_data=request.form,error_message=error_message)
        elif password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render_template('register.html', username_exists=False, form_data=request.form, error_message=error_message)
        else:
            app.db.add_user(first_name, last_name, username, password, phone, bankroll, sign_up_date, payed, how_heard, referral_name, other_source)
            login_allowed = app.db.check_login_credentials(username, password)
            print(f'{username} login result: {login_allowed}')
            if login_allowed:
                session['user_id'] = username
                return redirect(url_for('show_nba'))
            elif not login_allowed:
                error_message = "Email or password incorrect. Please try again."
                return render_template('register.html', incorrect_password=True, form_data=request.form, error_message=error_message)     
    
    return render_template('register.html', username_exists=False, form_data={})

@app.route('/login', methods=['GET', 'POST'])  
def login():
  user_id = session.get('user_id')
  my_db = database(app.db_manager)
  remember_token = request.cookies.get('remember_token')
  print(remember_token, 'is here')
  if remember_token:
        my_db = database(app.db_manager)
        username = my_db.get_username_by_remember_token(remember_token)
        if username:
             print(username, 'is here')
             permission = my_db.get_permission(username.lower())
             session['user_id'] = username
             session['permission'] = permission
             return redirect(url_for('positive_ev'))




  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')
    
    login_allowed = my_db.check_login_credentials(username, password)
    
    print(f'{username} login result: {login_allowed}')
    
    if login_allowed:
        permission = my_db.get_permission(username.lower())
        print(f"username: {username}")
        print(f"app permission: {permission}")
        session['user_id'] = username
        session['permission'] = permission
        if remember:
            remember_token = my_db.generate_secure_token()
            my_db.store_remember_token(username, remember_token)
            response = make_response(redirect(url_for('positive_ev')))
            response.set_cookie('remember_token', remember_token, max_age=60 * 60 * 24 * 10)
            return response
        else:
            return redirect(url_for('positive_ev'))
    
    elif not login_allowed:
        return render_template('login.html', incorrect_password=True, form_data=request.form)

  return render_template('login.html')

@app.route('/mlb')
def show_mlb():
    is_logged_in = True if 'user_id' in session else False

    return render_template('mlb.html', is_logged_in = is_logged_in)

@app.route('/nfl')
def show_nfl():
    is_logged_in = True if 'user_id' in session else False

    return render_template('nfl.html', is_logged_in = is_logged_in)
    
@app.route('/nba')
def show_nba():
    is_logged_in = True if 'user_id' in session else False

    # Set to false for prod only if we want to show the loom video 
    show_div = False

    #Uncomment only if we want to show the loom video
    # if request.referrer and (request.referrer.endswith('/login') or request.referrer.endswith('/register')):
    #     show_div = True

    return render_template('nba.html', show_div=show_div, is_logged_in = is_logged_in)
   
@app.route('/chat')
def show_chat():
    is_logged_in = True if 'user_id' in session else False
    return render_template('chat.html', is_logged_in = is_logged_in)

@app.route('/handle_chat', methods = ["GET", "POST"])
def handle_chat():

    text = request.form['text']

    response = app.chat.ask(text)
    
    return f"{response} "

@app.route('/nhl')
def show_nhl():
    is_logged_in = True if 'user_id' in session else False

    return render_template('nhl.html', is_logged_in = is_logged_in)
    
@app.route('/get_performance_data', methods=["POST", "GET"])
def get_performance_data():
    print("-------------------")   

    try:
        data = request.json
        dict_params = data['params']
        print(dict_params)
        db = database(app.db_manager)
        return_data = db.get_bet_tracker_dashboard_data(dict_params)     
        print(jsonify(return_data))
    except Exception as e:
        print(e)
    return jsonify(return_data)

@app.route('/add_saved_bet', methods=['POST'])
def add_saved_bet():
    try:
        data = request.json 
        user = session['user_id']
        data['user_name'] = user
        myDatabase = database(app.db_manager)
        myDatabase.add_made_bet_to_db(data)
        response = {'status_code': 'success', 'message': 'Bet saved successfully'}
    except Exception as e:
        response = {'status_code': 'error', 'message': str(e)}

    return jsonify(response)

@app.route('/get_live_dash_data', methods=['POST'])
def get_live_dash_data():
    data = request.get_json()
    sport_title = data.get('sport_title', '')
    # wrong calculation

    try:
        bankroll = app.db.get_user_bank_roll(session["user_id"])
    except KeyError:
        bankroll = 5000

    data = app.db.get_live_dash_data(bankroll, sport_title)

    if data.empty:
        data = pd.DataFrame(columns=['bankroll', 'update'])
        data = data.append({'bankroll': bankroll, 'update': False}, ignore_index=True)
    else:
        data['bankroll'] = bankroll
    data_json = data.to_dict(orient='records')

    return jsonify(data_json)

@app.route('/get_positive_ev_dash_data', methods=['POST'])
def get_positive_ev_dash_data():

    data = request.get_json()
    
    filters = data.get('filters', '')

    try:
        bankroll = app.db.get_user_bank_roll(session["user_id"])
    except KeyError:
        bankroll = 5000

    data = app.db.get_positive_ev_dash_data(filters, bankroll)
    
    if data.empty:
        data = pd.DataFrame(columns=['bankroll', 'update'])
        data = data.append({'bankroll': bankroll, 'update': False}, ignore_index=True)
    else:
        data['bankroll'] = bankroll
    data_json = data.to_dict(orient='records')

    return jsonify(data_json)

@app.route('/get_unsettled_bet_data', methods=['GET'])
def get_unsettled_bet_data():

    user = session['user_id']

    my_db = database(app.db_manager)

    data = my_db.get_unsettled_bet_data(user)

    grouped_data = data.groupby('game_id').apply(lambda x: x.to_dict(orient='records'))

    sorted_grouped_data = sorted(grouped_data.items(), key=lambda x: max(record['if_win'] for record in x[1]), reverse=True)

    sorted_dict = {game_id: records for game_id, records in sorted_grouped_data}


    return jsonify(sorted_dict)

@app.route('/get_filter_dropdown_values', methods=["GET"])
def get_filter_dropwdown_values():
    data = app.db.get_filter_dropdown_values()
    return data

@app.route('/bet_tracker')
def bet_tracker():

    is_logged_in = True if 'user_id' in session else False

    try:
        if session['user_id'] is not None:
            return render_template('bet_tracker.html', is_logged_in = is_logged_in)
    except:
        return redirect(url_for('register'))
    
@app.route('/market_view')
def market_view():

    is_logged_in = True if 'user_id' in session else False

    try:
        if session['user_id'] is not None:
            return render_template('market_view.html', is_logged_in = is_logged_in)
    except:
        return redirect(url_for('register'))

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))
@app.route('/logout')
def logout():
    # session.pop('user_id', None)
    # session.pop('permission', None)
    session.clear()

    # if 'remember_token' in request.cookies:
    #     response = make_response(redirect(url_for('login')))
    #     response.set_cookie('remember_token', '', expires=0)  # Delete the remember token cookie
    #     return response
    # else:
    
    return redirect(url_for('index'))

@app.route('/change_account')
def change_account():
    session.pop('user_id', None)
    session.pop('permission', None)
    session.clear()

    if 'remember_token' in request.cookies:
        response = make_response(redirect(url_for('login')))
        response.set_cookie('remember_token', '', expires=0)  # Delete the remember token cookie
        return response
    else:
        return redirect(url_for('login'))


@app.route('/learn')
def learn():
    include_header_css = False
    return render_template('learning_center.html', include_header_css=include_header_css)

@app.route('/faq')
def faq():
    return render_template('learn.html')
    
@app.route("/cancel_subscription", methods=["POST"])
def cancel_subscription():
    # Perform the subscription cancellation logic here
    action = request.get_json().get("action")

    if action == "cancel":
        # Implement the subscription cancellation process here
        # You can interact with your subscription service or database
        db = database(app.db_manager)
        db.cancel_subscription(session['user_id'])
        return redirect(url_for('logout'))
    else:
        return jsonify({"success": False})

@app.route("/get_user_permission", methods=['GET'])
def get_user_permission():
     
     if 'user_id' in session:
        print(app.db.get_permission(session['user_id']))
        return jsonify({'permission': app.db.get_permission(session['user_id'])['permission']})
     else:
         return jsonify({'permission': 'free'})
     
@app.route('/reset_password_page')
def reset_password_page():
    msg = request.args.get('msg')
    if msg and 'successfully' in msg:
        return redirect(url_for('password_update_successful'))
    else:
        return render_template('reset_password.html', msg = msg)
    

@app.route('/reset_password', methods=['POST','GET'])
def reset_password():
    my_db = database(app.db_manager)
    username = request.form.get('username')
    def generate_random_code():
    # Generate a random 6-digit code
        return str(random.randint(100000, 999999))

    def send_email(email, code):
        sender_email = 'admin@smartbettor.ai'
        sender_password = os.environ.get("email_pass")

    # Create a MIMEText object for the email body
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = f'Your Smartbettor Verification Code: {code}'
        body = f"""Hey Valued SmartBettor User,

        To verify your password reset request please enter the following code when prompted:

        {code}

        Please note that this code is only valid for the next 5 minutes.

        Thank you!
        """
        
    # Attach the body to the email
        message.attach(MIMEText(body, 'plain'))

    # Establish a connection to the SMTP server
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        print(f"Verification code sent to {username}")

    def password_function(email):
        try:
            session = app.db_manager.create_session()
            user = session.query(LoginInfo).filter_by(username=username).first()
            print(user)
            if user != None:
                code = generate_random_code()
                send_email(email, code)
                return code
            else:
                #TODO: test
                return 0
        except Exception as e:
            print(e)
            return str(e)
        finally:
            session.close()
    def set_reset_instance(code,username):
        if code != 0:
            try:
            # Create a session
                session = app.db_manager.create_session()
                current_datetime = datetime.now()

    # Add 5 minutes to the current datetime
                time_plus_5 = current_datetime + timedelta(minutes=5)

                new_code = VerificationCode(username=username, code=code, time_allowed=time_plus_5, used = False)


                # Add the new user to the session and commit the transaction
                session.add(new_code)
                session.commit()
            except Exception as e:
                print(e)
                return str(e)
            finally:
                session.close()


    code = password_function(username)
    if code == 0:
        error_message = "Email not found in the database. If you have paid through stripe, please complete registration."
        return render_template('register.html', incorrect_password=True, form_data={}, error_message=error_message) 
    set_reset_instance(code,username)
    return redirect(url_for('confirm_password', username=username))

@app.route('/confirm_password')
def confirm_password():
    username = request.args.get('username')
    try:
        msg = request.args.get('msg')
    except:
        msg = ''

    if request.referrer and 'reset_password' in request.referrer:
        return render_template('confirm_password.html', username = username)
    
    elif request.referrer and 'confirm_password' in request.referrer:
        return render_template('confirm_password.html', username = username, msg = msg)
    else:
        # Redirect to login page if the referrer is not reset_password
        return redirect(url_for('login'))
    
@app.route('/confirm_password_button/<string:username>/<string:code>', methods=['GET', 'POST'])
def confirm_password_button(username, code):
    try:
        session = app.db_manager.create_session()
        code = int(code)

        # Fetch the verification code from the database
        verification_code = session.query(VerificationCode).filter_by(username=username, code=code).first()

        if verification_code:
            current_datetime = datetime.now()

            # Check if the code is still valid
            if verification_code.time_allowed > current_datetime and not verification_code.used:
                # Set the code as used and commit the transaction
                session.delete(verification_code)
                session.commit()
                return redirect(url_for('set_new_password', username=username))
            else:
                #TODO: test
                msg = "Code expired or already used"
                return redirect(url_for('reset_password_page',msg=msg))
        else:
            msg= "Invalid code for the given username"
            return redirect(url_for('confirm_password',msg=msg, username=username))
      

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": str(e)})
    finally:
        session.close()

@app.route('/set_new_password')
def set_new_password():
    username = request.args.get('username')
    if request.referrer and 'confirm_password' in request.referrer:
        # Proceed with the confirm password logic
        return render_template('set_new_password.html', username = username)
    else:
        # Redirect to login page if the referrer is not reset_password
        return redirect(url_for('login'))
    
@app.route('/set_new_password_db/<string:username>/<string:password>', methods=['GET', 'POST'])
def set_new_password_db(username, password):
    try:
        # Create a session
        session = app.db_manager.create_session()

        # Fetch the user from the database
        this_user = session.query(LoginInfo).filter_by(username=username).first()

        if this_user:
            # Set the new password for the user
            this_user.password = generate_password_hash(password)  # Use your preferred password hashing method

            # Commit the transaction
            session.commit()

            # Flash success message and redirect to login or any other page
            msg = "Password updated successfully please return to Smartbettor.ai home page and log in with new credentials."
            return redirect(url_for('reset_password_page',msg=msg))

        else:
            # Flash error message for invalid username
            flash("Invalid username", "error")

    except Exception as e:
        print(e)
        flash(str(e), "error")

    finally:
        session.close()

    # Redirect to an appropriate page on failure
    return redirect(url_for('login'))  # Change 'login' to the appropriate endpoin

@app.route('/password_update_successful')
def password_update_successful():
    return render_template('password_update_successful.html')

@app.route('/load_initial_market_view_data', methods=['GET', 'POST'])
def load_initial_market_view_data():

    with open('market_view_data/market_view_data.csv', 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            df = pd.read_csv(f)

    df['hashable_id_copy'] = df['hashable_id'].copy()

    df.set_index('hashable_id_copy', inplace=True)

    return df.to_json(orient='records')


    
def get_team_vals_for_scenarios():
       teams = pd.read_csv('../extra_info_sheets/teams.csv')
       teams.sort_values(by="team", inplace=True)
       return teams.to_json(orient='records', date_format='iso')


def get_all_market_view_data():
    try:

        filename = 'market_view_data/market_view_data.csv'

        with open(filename, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
    
         with lock:
            df = pd.read_csv(f)

        if df.empty or len(df.columns) == 0:
            print("DataFrame is empty or has no columns.")
            return get_all_market_view_data()

        df['hashable_id_copy'] = df['hashable_id'].copy()
        df.set_index('hashable_id_copy', inplace=True)

        return df

    except pd.errors.EmptyDataError:
        print("File 'market_view_data/market_view_data.csv' is empty.")
        return get_all_market_view_data()

    except pd.errors.ParserError:
        print("Error parsing 'market_view_data/market_view_data.csv'.")
        return get_all_market_view_data()

    except Exception as e:
        print(f"An error occurred: {e}")
        return get_all_market_view_data()


def find_modified_rows(df1, df2):
    # Find common indices
    common_indices = df1['hashable_id'].isin(df2['hashable_id'])

    # Initialize an empty DataFrame to store modified rows
    modified_rows_df2 = pd.DataFrame(columns=df2.columns)

    # Iterate through common indices and compare rows
    for idx in df1.loc[common_indices, 'hashable_id']:
        row_df1 = df1[df1['hashable_id'] == idx].iloc[0]
        row_df2 = df2[df2['hashable_id'] == idx].iloc[0]

        # Compare rows
        if not row_df1.equals(row_df2):
            modified_rows_df2 = modified_rows_df2.append(row_df2)

    return modified_rows_df2

def compare_dataframes(df1, df2):
    if 'hashable_id' not in df1.columns or 'hashable_id' not in df2.columns:
        raise ValueError("Both DataFrames must have a 'hashable_id' column.")

    added_rows = df2.loc[~df2.index.isin(df1.index)]

    deleted_rows = df1.loc[~df1.index.isin(df2.index)]

    changed_rows = find_modified_rows(df1, df2)

    return {
        'added_rows': added_rows,
        'deleted_rows': deleted_rows,
        'changed_rows': changed_rows
    }

def listen_for_updates():

    old_data = get_all_market_view_data()

    old_data['hashable_id_copy'] = old_data['hashable_id'].copy()

    old_data.set_index('hashable_id_copy', inplace=True)

    while True:

        start_time = time.time()

        new_data = get_all_market_view_data()

        differences = compare_dataframes(old_data, new_data)

        try:
            json_dfs = {
                key: value.to_json(orient='records') if isinstance(value, pd.DataFrame) else None
                for key, value in differences.items()
            }

            socketio.emit('update_data', json_dfs, namespace='/')
        except AttributeError as e:
            print(f"Unable to send data: {e}")

        old_data = new_data.copy()

        end_time = time.time()

        elapsed_time = end_time - start_time

        print("Elapsed time:", elapsed_time, "seconds")

        time.sleep(1)  # Polling interval

@socketio.on('connect')
def handle_connect():
    print("-------------")
    print('Client connected 65')
    print("-------------")

if __name__ == '__main__':
    # Start background thread for listening to updates
    update_listener_thread = Thread(target=listen_for_updates)
    update_listener_thread.daemon = True
    update_listener_thread.start()

    socketio.run(app, debug=True, port=5000, use_reloader=False)


    # Start Flask application
    # socketio.run(app, debug=True)

    
