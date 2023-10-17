import requests
import sqlite3

conn = sqlite3.connect('smartbetter.db')
c = conn.cursor()

c.execute('SELECT firstname, lastname, username, phone FROM login_info')
rows = c.fetchall()

url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
headers = {
    'Authorization': 'Bearer pat-na1-b8906562-368d-4935-aeec-0e040483f740'
}

for row in rows:
    first_name = row[0]
    last_name = row[1]
    email = row[2]
    phone = row[3]

    # Create the search payload to find a contact by email
    search_payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "email",
                        "value": email,
                        "operator": "EQ"
                    }
                ]
            }
        ]
    }

    # Send a GET request to search for the contact
    search_response = requests.post(url, json=search_payload, headers=headers)

    if search_response.status_code == 200:
        search_data = search_response.json()
        contacts = search_data.get('results', [])

        if contacts:
            # Contact already exists, update it
            contact_id = contacts[0]['id']
            update_url = f"{url}/{contact_id}"
            update_payload = {
                "properties": {
                    "firstname": first_name,
                    "lastname": last_name,
                    "phone": phone
                }
            }
            update_response = requests.put(update_url, json=update_payload, headers=headers)

            if update_response.status_code == 200:
                print(f"Updated contact with email {email}")
            else:
                print(f"Error updating contact: {update_response.status_code}")
        else:
            # Contact doesn't exist, create a new one
            payload = {
                "properties": {
                    "firstname": first_name,
                    "lastname": last_name,
                    "email": email,
                    "phone": phone
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"Created contact with email {email}")
            else:
                print(f"Error creating contact: {response.status_code}")
    else:
        print(f"Error searching contact: {search_response.status_code}")
