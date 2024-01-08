from functionality.db_manager import DBManager
import pandas as pd 
from openai import OpenAI
import os


class Chat():
    def __init__(self):
        self.DB = DBManager()

        try:
            self.session = self.DB.create_session()
            # self.df2 = pd.read_sql_table('nba_extra_info', con=self.DB.get_engine())
        except Exception as e:
            print(e)
        finally:
            self.session.close()

        self.client = OpenAI(api_key='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')


    def create_table_definition_prompt(self):
        prompt = '''### sql table, with its properties:
        #
        # props_data(active, date, points_scored, plus_minus, team, location, opponent, outcome, seconds_played, made_field_goals, attempted_field_goals, made_three_point_field_goals, attempted_three_point_field_goals, made_free_throws, attempted_free_throws, offensive_rebounds, defensive_rebounds, assists, steals, blocks, turnovers, personal_fouls, game_score, player)
        #
        '''
        return prompt


    def create_another_table_definition_prompt(self):
        prompt2 = '''### And another sql table, with its properties:
        #
        # nba_extra_info(active, date, points_scored, plus_minus, team, location, opponent, outcome, seconds_played, made_field_goals, attempted_field_goals, made_three_point_field_goals, attempted_three_point_field_goals, made_free_throws, attempted_free_throws, offensive_rebounds, defensive_rebounds, assists, steals, blocks, turnovers, personal_fouls, game_score, player)
        #
        '''
        return prompt2


    def combine_prompts(self, query_prompt):
        definition = self.create_table_definition_prompt()
        second_def = self.create_another_table_definition_prompt()
        query_init_string = f'### A query using one or more of the tables provided to answer: {query_prompt}\nSELECT'
        return definition + second_def + query_init_string
    
    def handle_response(self, query):
        if query.startswith(' '):
            query = 'SELECT' + query
        return query
    
    def generate_combined_response(self, user_prompt, response):
            new_query = f"""Create a nice answer using the prompt and the response.
            prompt: {user_prompt}
            response: {response}
            """

            print(new_query)

            # Use GPT-3 to generate the combined response
            completion = self.client.completions.create(
                model="text-davinci-003",
                prompt=new_query,
                temperature=0,
                max_tokens=150,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            
            return completion.choices[0].text.strip()

    def ask(self, prompt):

        nlp_text = prompt

        prompt = self.combine_prompts(nlp_text)

        print(prompt)       

        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["#", ";"]
        )

        # Access the generated text
        generated_text = response.choices[0].text

        print(generated_text)

        generated_text = self.handle_response(generated_text)

        try:
            result_df = pd.read_sql_query(generated_text, con=self.DB.get_engine())
            print("Query executed successfully. Results:")
            print(result_df)
            
            value_to_convert = result_df.iloc[0, 0]
            print("++++++++++")
            print(value_to_convert) 

            final_response = self.generate_combined_response(nlp_text, value_to_convert)

            return final_response


        except Exception as e:
            print("Error executing the query:")
            print(e)
        