import os
import requests
from dotenv import load_dotenv
load_dotenv()
headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}" }

def get_tasks():
    url = "https://api.airtable.com/v0/appwr95EmedjJLiUQ/tbls9MJ4uzGQ8lrNV"
    try:
       response = requests.get(url, headers=headers, timeout=10)
       response.raise_for_status()
       return response.json()
    
    except requests.exceptions.ConnectionError:
        print("The network is slow, couldn't load")
    except requests.exceptions.Timeout:
        print("Time session expired")
    except requests.exceptions.HTTPError:
        print("Invalid data")
    

def create_task():
    name = input("Enter task name: ")
    status = input("Enter task status(Started/Pending/Completed): ")
    notes = input("Add notes: ")
    url = "https://api.airtable.com/v0/appwr95EmedjJLiUQ/tbls9MJ4uzGQ8lrNV"
    body ={"records": [{"fields": {"Name" : name, "Status": status, "Notes": notes}}]}
    try:
       response = requests.post(url, json=body, headers=headers, timeout=10)
       response.raise_for_status()
       data = response.json()
       record = data["records"][0]
       print(f"Task created: {record['fields']['Name']} (ID: {record['id']})")
       return data
    except requests.exceptions.ConnectionError:
        print("The network is slow, couldn't load")
    except requests.exceptions.Timeout:
        print("Time session expired")
    except requests.exceptions.HTTPError as e:
          print(f"HTTP Error: {e}")
          print(f"Response body: {response.text}")

def show_tasks():
    data = get_tasks()
    target_keys = ['Name', 'Status', 'Notes']


    for idx, record in enumerate(data['records'], start=1):
       print(f"{idx}. ID: {record['id']}")
    
    
       fields = record['fields']
       for key in target_keys:
           if key in fields:
              print(f"   - {key}: {fields[key]}")
            
       print("====================")

    
def update_task():
    
    record_id = input("Which record id will you like to update?: ")
    field = input("Which field will you like to update(Name,Status, Notes): ").capitalize()
    if field == "Name":
        new_name = input("Enter the new name: ")
        body = {"fields": {"Name": new_name}}
    elif field == "Status":
        new_status = input("Which status are you now: ")
        body = {"fields": {"Status": new_status}}
    elif field == "Notes":
        new_note = input("Enter your new note: ")
        body = {"fields": {"Notes": new_note}}
    else:
        print("Invalid field. Choose Name, Status, or Notes.")
        return
    url = "https://api.airtable.com/v0/appwr95EmedjJLiUQ/tbls9MJ4uzGQ8lrNV"
    try: 
       response = requests.patch(f"{url}/{record_id}",json=body,headers=headers, timeout=10)
       response.raise_for_status()
       print("Data updated")
    except requests.exceptions.ConnectionError:
        print("The network is slow, couldn't load")
    except requests.exceptions.Timeout:
        print("Time session expired")
    except requests.exceptions.HTTPError as e:
          print(f"HTTP Error: {e}")
          print(f"Response body: {response.text}")

def delete_task():
    
    url = "https://api.airtable.com/v0/appwr95EmedjJLiUQ/tbls9MJ4uzGQ8lrNV"
    record_id = input("Which record id will you like to delete?: ")
    try: 
       response = requests.delete(f"{url}/{record_id}",headers=headers, timeout=10)
       response.raise_for_status()
       print("Data deleted!")
    except requests.exceptions.ConnectionError:
        print("The network is slow, couldn't load")
    except requests.exceptions.Timeout:
        print("Time session expired")
    except requests.exceptions.HTTPError as e:
          print(f"HTTP Error: {e}")
          print(f"Response body: {response.text}")

def menu():
    print("==============TODO MANAGER==============")
    print("1. Create Task")
    print("2. Show Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

def main():
    while True:
        menu()
        choice = input("What action will you like to perform on your todo?: ")
        if choice == "1":
            create_task()
        
        elif choice == "2":
            show_tasks()
        
        elif choice == "3":
            update_task()
        
        elif choice == "4":
            delete_task()
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()


    
    


    


    
    

    



