import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()


headers = {
    "Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"
}


BASE_URL = "https://api.airtable.com/v0/appwr95EmedjJLiUQ/tbls9MJ4uzGQ8lrNV"


def make_request(method, url, **kwargs):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = requests.request( method, url,**kwargs)

            if response.status_code == 429:
                print(
                    f"Rate limited. "
                    f"Waiting 30 seconds... "
                    f"Retry {attempt + 1}/{max_retries}"
                )

                time.sleep(30)
                continue

            response.raise_for_status()

            return response

        except requests.exceptions.ConnectionError:
            print("The network is slow, couldn't load")
            return None
            

        except requests.exceptions.Timeout:
            print("Time session expired")
            return None
            

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response body: {response.text}")
            return None
            

    print("Maximum retries reached. Request failed.")
    return None


def get_tasks():
    all_records = []

    params = {
        "pageSize": 100
    }

    while True:
        response = make_request("GET", BASE_URL, headers=headers, params=params, timeout=10)

        if response is None:
            return None

        data = response.json()

        all_records.extend(data["records"])

        if "offset" not in data:
            break

        params["offset"] = data["offset"]

    return {
        "records": all_records
    }


def create_task():
    name = input("Enter task name: ")

    status = input("Enter task status (Started/Pending/Completed): ")

    notes = input("Add notes: ")

    body = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "Status": status,
                    "Notes": notes
                }
            }
        ]
    }

    response = make_request("POST", BASE_URL, json=body, headers=headers, timeout=10)

    if response is None:
        return

    data = response.json()
    record = data["records"][0]

    print(
        f"Task created: {record['fields']['Name']} (ID: {record['id']}) ")


def show_tasks():
    data = get_tasks()

    if data is None:
        return

    target_keys = ["Name", "Status", "Notes"]

    for idx, record in enumerate(data["records"], start=1):
        print(f"{idx}. ID: {record['id']}")

        fields = record["fields"]

        for key in target_keys:
            if key in fields:
                print(f"   - {key}: {fields[key]}")

        print("====================")


def update_task():
    record_id = input("Which record id would you like to update?: ")

    field = input("Which field would you like to update(Name, Status, Notes): ").capitalize()

    if field == "Name":
        new_name = input("Enter the new name: ")

        body = {
            "fields": {
                "Name": new_name
            }
        }

    elif field == "Status":
        new_status = input("Which status are you now?: ")

        body = {
            "fields": {
                "Status": new_status
            }
        }

    elif field == "Notes":
        new_note = input("Enter your new note: ")

        body = {
            "fields": {
                "Notes": new_note
            }
        }

    else:
        print("Invalid field. Choose Name, Status, or Notes.")
        return

    response = make_request("PATCH",f"{BASE_URL}/{record_id}",json=body,headers=headers,timeout=10)

    if response is None:
        return

    print("Data updated")


def delete_task():
    record_id = input("Which record id would you like to delete?: ")

    response = make_request("DELETE",f"{BASE_URL}/{record_id}",headers=headers,timeout=10)

    if response is None:
        return

    print("Data deleted!")


def menu():
    print("============== TODO MANAGER ==============")
    print("1. Create Task")
    print("2. Show Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")


def main():
    while True:
        menu()

        choice = input("What action would you like to perform on your todo?: ")

        if choice == "1":
            create_task()

        elif choice == "2":
            show_tasks()

        elif choice == "3":
            update_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()