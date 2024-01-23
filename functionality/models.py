from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class ChatQuestions(Base):
    __tablename__ = 'chat_questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    worked_bool = Column(Boolean, nullable=True)

class MasterModelObservations(Base):
    __tablename__ = 'master_model_observations'
    new_column = Column(String(255), primary_key=True)
    sport_title = Column(String(255))
    completed = Column(Boolean)
    game_id = Column(String(255))
    game_date = Column(String(255))
    team = Column(String(255))
    minutes_since_commence = Column(Float)
    opponent = Column(String(255))
    snapshot_time = Column(String(255))
    ev = Column(Float)
    average_market_odds = Column(Float)
    highest_bettable_odds = Column(Float)
    sportsbooks_used = Column(Text)

class LoginInfo(Base):
    __tablename__ = 'login_info'
    firstname = Column(String(255))
    lastname = Column(String(255))
    username = Column(String(255), unique=True, primary_key=True)
    password = Column(String(255))
    phone = Column(String(255))
    bankroll = Column(String(255))
    payed = Column(Integer)
    date_signed_up = Column(String(255))

class MlbExtraInfo(Base):
    __tablename__ = 'mlb_extra_info'

    date = Column(Integer)
    my_id = Column(String(255), primary_key=True)
    number_of_game_today = Column(Integer)
    day_of_week = Column(String(255))
    away_team = Column(String(255))
    away_team_league = Column(String(255))
    away_team_game_number = Column(Integer)
    home_team = Column(String(255))
    home_team_league = Column(String(255))
    home_team_game_number = Column(Integer)
    day_night = Column(String(255))
    park_id = Column(String(255))

class PlacedBets(Base):
    __tablename__ = 'placed_bets'

    game_id = Column(String(255))
    average_market_odds = Column(String(255))
    team = Column(String(255))
    sportsbooks_used = Column(Text)
    bet_amount = Column(String(255))
    highest_bettable_odds = Column(String(255))
    minimum_acceptable_odds = Column(String(255))
    ev = Column(String(255))
    date = Column(String(255))
    time_difference_formatted = Column(String(255))
    user_name = Column(String(255))
    bet_profit = Column(Float)
    time_placed = Column(String(255), primary_key=True)

class Scores(Base):
    __tablename__ = 'scores'

    game_id = Column(String(255), primary_key=True)
    sport_title = Column(String(255))
    commence_time = Column(String(255))
    home_team = Column(String(255))
    away_team = Column(String(255))
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)
    winning_team = Column(String(255))