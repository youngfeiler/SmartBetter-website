from flask import Flask, render_template, jsonify, request
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import plotly.graph_objects as go
import plotly as plotly
from functionality.user import User
from functionality.raw_odds_data_holders import RawOddsHolders
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



def create_app():
    app = Flask(__name__, template_folder='static/templates', static_folder='static')
    # TODO: Put this key in the secret file
    app.secret_key = 'to_the_moon'
    app.db_manager = DBManager()
    app.db = database(app.db_manager)
    app.celery = celery
    return app


app = create_app()
app.config['STRIPE_PUBLIC_KEY'] = 'pk_live_51Nm0vBHM5Jv8uc5M5hu3bxlKg6soYb2v9xSg5O7a9sXi6JQJpl7nPWiNKrNHGlXf5g8PFnN6sn0wcLOrixvxF8VH00nVoyGtCk'
app.config['STRIPE_PRIVATE_KEY'] = os.environ.get("STRIPE_API_KEY")
stripe.api_key = app.config['STRIPE_PRIVATE_KEY']

@atexit.register
def close_db():
    app.db_manager.close()

@app.route('/')
def index():
    app.db.check_payments()
    return render_template('landing_page.html', 
                           checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])

@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/scenarios')
def scenarios():
    return render_template('scenarios.html')

@app.route('/pregame')
def pregame_beta():
    return render_template('pregame.html')

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
    if price_id == "price_1OG9CDHM5Jv8uc5MTtdQOZMv":
        price = 99
    else:
        price = 199
    trial_end_date = int((datetime.utcnow() + timedelta(days=7)).timestamp())

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
        success_url=url_for('register', _external=True) + '?session_id={CHECKOUT_SESSION_ID}' + f'&price={price}',
        cancel_url=url_for('index', _external=True),

    )
    return redirect(checkout_session.url,code=302)


@app.route('/checkout_free_trial/<string:price_id>')
def create_checkout_session_free_trial(price_id):
    if price_id == "price_1OG9CDHM5Jv8uc5MTtdQOZMv":
        price = 99
    else:
        price = 199
    trial_end_date = int((datetime.utcnow() + timedelta(days=7)).timestamp())

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
        success_url=url_for('register', _external=True) + '?session_id={CHECKOUT_SESSION_ID}' + f'&price={price}',
        cancel_url=url_for('index', _external=True),
        subscription_data = {
             'trial_end': trial_end_date
        }
    )
    return redirect(checkout_session.url,code=302)

@app.route('/test_func')
def test_func():
    tasks.start_dashboard_runner.delay()
    return render_template('nba.html')

@app.route('/home')
def home():
    return render_template('landing_page.html')

@app.route('/account')
def account():
  if 'user_id' in session:
        users = app.db.get_user_info(session['user_id'])
        return render_template('account_settings.html', users = users)
  else:
        return redirect(url_for('login'))

@app.route('/performance')
def show_performance():
    return render_template('performance.html')

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
        username = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = '+1' + str(request.form['phone_number'])
        bankroll = request.form['bankroll']
        sign_up_date = datetime.now()
        payed = False
        if username in users:
            print("if usrname in users")

            has_payed=app.db.check_duplicate_account(username)
            print("made it here")
            print(has_payed)
            if has_payed:
                payed = True
                app.db.add_user(first_name, last_name, username, password, phone, bankroll, sign_up_date, payed)
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
            app.db.add_user(first_name, last_name, username, password, phone, bankroll, sign_up_date, payed)
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
  if (user_id is not None):
      payed = my_db.check_account(user_id)
      if payed:
        return redirect(url_for('show_nba'))
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    login_allowed = my_db.check_login_credentials(username, password)

    print(f'{username} login result: {login_allowed}')
    
    if login_allowed:
        payed = my_db.check_account(username)
        session['user_id'] = username
        if not payed:
            flash('Your Free Trial Has Ended. Check Out Our Purchase Plans At The Bottom Of The Page', 'error')
            return redirect(url_for('index'))
        return redirect(url_for('show_nba'))
    elif not login_allowed:
        return render_template('login.html', incorrect_password=True, form_data=request.form)

  return render_template('login.html')

@app.route('/mlb')
def show_mlb():
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('mlb.html')
    else:
        return redirect(url_for('register'))
    
@app.route('/nfl')
def show_nfl():
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('nfl.html')
    else:
        return redirect(url_for('register'))
    
@app.route('/nba')
def show_nba():
    # Set to false for prod
    show_div = False

    referrer = request.referrer
    if referrer:
        if referrer.endswith('/login') or referrer.endswith('/register'):
            show_div = True
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('nba.html', show_div=show_div)
    else:
        return redirect(url_for('register'))

@app.route('/nhl')
def show_nhl():
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('nhl.html')
    else:
        return redirect(url_for('register'))   

@app.route('/nhl_pregame')
def show_nhl_pregame():
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('nhl_pregame.html')
    else:
        return redirect(url_for('register'))
    
@app.route('/nba_pregame')
def show_nba_pregame():
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('nba_pregame.html')
    else:
        return redirect(url_for('register'))

@app.route('/get_performance_data', methods=["POST", "GET"])
def get_performance_data():
    try:
        data = request.json
        dict_params = data['params']
        print(dict_params)
        db = database(app.db_manager)
        return_data = db.get_bet_tracker_dashboard_data(dict_params)        
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
    bankroll = app.db.calculate_user_bankroll(session["user_id"])
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

@app.route('/get_unsettled_bet_data', methods=['GET'])
def get_unsettled_bet_data():

    user = session['user_id']

    my_db = database(app.db_manager)

    data = my_db.get_unsettled_bet_data(user)

    grouped_data = data.groupby('game_id').apply(lambda x: x.to_dict(orient='records'))

    sorted_grouped_data = sorted(grouped_data.items(), key=lambda x: max(record['if_win'] for record in x[1]), reverse=True)

    sorted_dict = {game_id: records for game_id, records in sorted_grouped_data}


    return jsonify(sorted_dict)


@app.route('/bet_tracker')
def bet_tracker():
    try:
        if session['user_id'] is not None:
            return render_template('bet_tracker.html')
    except:
        return redirect(url_for('register'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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

if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)

    
