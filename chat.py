from functionality.db_manager import DBManager
import pandas as pd 
DB = DBManager()

try:
    session = DB.create_session()
    df =  pd.read_sql_table('placed_bets', con=DB.get_engine())
except Exception as e:
    print(e)
finally:
    session.close()
print(df.head())
from openai import OpenAI

client = OpenAI(api_key='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')
def create_table_definition_prompt(df):
   prompt = '''### sql table, with its properties:
#
# placed_bets({})
#
'''.format(', '.join(str(x) for x in df.columns))
   return prompt
print(create_table_definition_prompt(df))

def prompt_input():
    nlp_prompt = input("Enter your prompt: ")
    return nlp_prompt
nlp_text = prompt_input()   
def combine_prompts(df, query_prompt):
    definition = create_table_definition_prompt(df)
    query_init_string = f'### A query to answer: {query_prompt}\nSELECT'
    return definition + query_init_string
prompt = combine_prompts(df, nlp_text)

# Make the API call using OpenAI's new method
response = client.completions.create(
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
def handle_response(query):
    if query.startswith(' '):
        query = 'SELECT' + query
    return query

print(generated_text)

generated_text = handle_response(generated_text)
try:
    result_df = pd.read_sql_query(generated_text, con=DB.get_engine())
    print("Query executed successfully. Results:")
    print(result_df)
except Exception as e:
    print("Error executing the query:")
    print(e)