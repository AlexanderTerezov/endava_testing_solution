import requests

BASE_URL = "https://reqres.in/api/users"
API_KEY = "reqres-free-v1"
headers = {
    "x-api-key" : API_KEY
}

def list_users(page=1):
    params = {
        "page" : page
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    assert response.status_code == 200, f"Request failed. Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "data" in data, "There is no \"data\" field in response"
    assert isinstance(data["data"], list), "\"data\" is not a list"

    return data["data"]

# Extract first user details
def extract_single_user_details(users):
    assert users, "User list is empty"
    first_user = users[0]

    assert "id" in  first_user and "email" in  first_user, "User is missing id or email fields"
    user_id = first_user["id"]
    user_email = first_user["email"]
    

    print(f"Extracted user id: {user_id}, Email: {user_email}\n")

    return {"id": first_user["id"],"email": first_user["email"]}

# (Optional) Extract all users, sort them by First Name alphabetically. Print sorted collection.
def print_sorted_users(users):
    assert users, "User list is empty"
    
    sorted_users = sorted(users, key=lambda user : user["first_name"])
    print("Sorted Users:")
    for user in sorted_users:
        print(f"{user["id"]} {user["first_name"]} {user["last_name"]} - {user["email"]}")

def get_extracted_user_details(user_id):
    params = {
        "id" : user_id
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    assert response.status_code == 200, f"Request failed. Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "data" in data, "There is no \"data\" field in response"

    return data

def get_nonexistent_user():
    nonexistent_id = 9999
    params = {
        "id" : nonexistent_id
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    
    assert response.status_code == 404, f"Request failed. Expected status code 404, got {response.status_code}"
    

def create_unique_user():
    new_user = {
        "email": "morpheus@testmail.com",
        "first_name": "Morpheus",
        "last_name": "NoIdea"
    }

    response = requests.post(BASE_URL, headers=headers , data=new_user)
    assert response.status_code == 201, f"Request failed. Expected status code 201, got {response.status_code}"

    data = response.json()
    return data

def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/{user_id}", headers=headers)
    assert response.status_code == 204, f"Request failed. Expected status code 204, got {response.status_code}"

if __name__ == "__main__":
    users = list_users()
    first_user_id_email = extract_single_user_details(users)
    print_sorted_users(users)
    get_extracted_user_details(first_user_id_email["id"])
    get_nonexistent_user()
    unique_user = create_unique_user()
    delete_user(unique_user["id"])