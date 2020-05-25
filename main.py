"""
File: main.py
------------------
Program to track screenshots to change in technical documentation.
"""

import json
import requests

MISSING_VALUE = []

def main():
    # TODO: Test that a project name is valid
    # TODO: Test that a project file (reading a file) exists, if not, return an empty dictionary
    # TODO: Improve project name stuff (don't require a file type, give a user a list of projects to choose from)
    # TODO: If there is a visual diff for a path, return the path name for the user, along with a list of screenshots associated with that path name
    # TODO: Tell the user there are changes to path and to check screenshots
    # TODO: If there is no visual diff for a path, return a message to the user to let her know there are no changes

    while True:
        # Ask the user what they would like to do in the program, and capture that as a variable
        user_selects = int(input("What would you like to do? \n 1. Manage Projects \n 2. Manage screenshot inventory \n 3. Check a diff for changes to URLs \n 4. Exit \n"))

        # When the user wants to "Manage projects":
        if user_selects == 1:
            # Ask the user what they'd like to do
            project_action = int(input("What would you like to do? \n 1. Create a new project \n 2. View project details \n 3. Edit a project's details \n"))
            if project_action == 1:
                # Create an empty dictionary for the project
                project_dict = {}
                # Prompt the user for inputs
                name = input("What would you like to name your project? ")
                base_url = input("What is the base URL for your project, as you've entered it in Diffy? ")
                screenshots_in_external_library = int(input("How many screenshots are currently in your external library? "))
                diffy_project_id = int(input("What is the project ID in Diffy? "))
                # Store inputs in the project metadata dictionary
                project_metadata = {"name": name, "base_url": base_url, "screenshots_in_external_library": screenshots_in_external_library, "diffy_project_id": diffy_project_id}
                # Add the project metadata to the project dict
                project_dict = add_project_metadata_to_dict(project_metadata, project_dict)
                # Create an empty placeholder dictionary for the screenshot inventory
                screenshot_inventory = {}
                # Add the screenshot inventory to the project dict
                project_dict = add_screenshot_inventory_to_dict(screenshot_inventory, project_dict)
                # Write the dictionary to a new file
                save_project(name, project_dict)
                # Print a success message for the user
                print("Your new project has been created.")
                # Print the project metadata for the user
                print_dictionary(project_metadata)

            if project_action == 2:
                # Ask the user to specify the project where they want to view details
                project_name = get_project_name()
                # Retrieve the project dictionary from the specified filename
                project_dictionary = open_project(project_name)
                # Extract the project metadata from the dictionary
                project_metadata = extract_project_metadata(project_dictionary)
                # Print the project metadata for the user
                print_dictionary(project_metadata)

            if project_action == 3:
                # Ask the user to specify the project where they want to view details
                project_name = get_project_name()
                # Retrieve the project dictionary from the specified filename
                project_dictionary = open_project(project_name)
                # Extract the product metadata from the dictionary
                project_metadata = extract_project_metadata(project_dictionary)
                print("The current details for the " + project_name + " project are: ")
                print_dictionary(project_metadata)
                # Ask the user what project detail they'd like to change, store the data to the corresponding variable, and update the dict
                key_to_change = int(input("Which details would you like to edit? \n 1. Project Name \n 2. The base URL for the project \n 3. The number of screenshots in the external library \n 4. The project ID in Diffy \n"))
                if key_to_change == 1:
                    name = input("What is the new name you'd like to use for your project? ")
                    project_metadata["name"] = name
                if key_to_change == 2:
                    base_url = input("What is the new base URL you'd like to use in your project? ")
                    project_metadata["base_url"] = base_url
                if key_to_change == 3:
                    screenshots_in_external_library = int(input("What is the updated number of screenshots in your external library? "))
                    project_metadata["screenshots_in_external_library"] = screenshots_in_external_library
                if key_to_change == 4:
                    diffy_project_id = int(input("What is the new project ID in Diffy? "))
                    project_metadata["diffy_project_id"] = diffy_project_id
                # Add the updated project metadata to the project dictionary
                project_dictionary = add_project_metadata_to_dict(project_metadata, project_dictionary)
                # Write the updated dict to the file
                save_project(project_name, project_dictionary)
                # Print the new project details for the user, along with a success message
                print(project_name + " has been updated. Your new project details are: ")
                print_dictionary(project_metadata)


        # When the user wants to "Manage screenshot inventory":
        if user_selects == 2:
            # Ask the user for a project name
            project_name = get_project_name()
            # Open the JSON file and extract the dictionary
            project_dictionary = open_project(project_name)
            # Extract the project metadata from the dictionary
            project_metadata = extract_project_metadata(project_dictionary)
            # Extract the dictionary of URLs and screenshots from the project dictionary
            screenshot_inventory = extract_screenshot_inventory(project_dictionary)
            # Extract the Diffy project ID from the project metadata
            project_id = extract_project_id(project_metadata)
            # Ask the user what they'd like to do with the screenshot inventory
            manage_inventory = int(input("What would you like to do with the screenshot inventory? \n 1. Add or remove URLs \n 2. Add or remove screenshots \n 3. Check project inventory coverage \n"))

            if manage_inventory == 1:
                # Show the user a list of URLs that are currently in the inventory
                current_urls = extract_urls(screenshot_inventory)
                print("These are the URLs that are currently in your inventory: ")
                print(current_urls)
                option = int(input("What would you like to do with URLs? \n 1. Add URLs \n 2. Remove URLs \n 3. Populate URLs from Diffy \n"))
                # If the user wants to add URLs to the list:
                if option == 1:
                    urls_to_watch = add_urls(current_urls)
                    print("Updating URLs in Diffy...")
                    response = update_urls_in_diffy(urls_to_watch, project_id)
                    print(human_readable_status_codes(response))
                # If the user wants to remove URLs from the list:
                if option == 2:
                    urls_to_watch = remove_urls(current_urls)
                    print("Updating URLs in Diffy...")
                    response = update_urls_in_diffy(urls_to_watch, project_id)
                    print(human_readable_status_codes(response))
                if option == 3:
                    urls_to_watch = populate_urls_from_diffy(project_id)


                # Give the user a success message
                print("You have successfully updated the URLs in your inventory.")
                # Print the current list of URLs that the user is watching
                print("The current URL list is: ")
                print('\n'.join(map(str, urls_to_watch)))
                # Update the list of URLs in the screenshot inventory
                screenshot_inventory = update_urls_to_watch(urls_to_watch, screenshot_inventory)
                # Add the updated screenshot inventory to the project dictionary
                project_dictionary = add_screenshot_inventory_to_dict(screenshot_inventory, project_dictionary)
                # Write the updated dict to the file
                save_project(project_name, project_dictionary)

            if manage_inventory == 2:
                # Show the user a list of URLs that are currently in the inventory
                current_urls = extract_urls(screenshot_inventory)
                print("These are the URLs that are currently in your inventory: ")
                print(current_urls)
                # Ask the user which URL (key) they want to update screenshots for?
                key = input("For which URL would you like to update screenshots? ")
                # Show the user a list of screenshots (values) currently associated with that URL
                print("These are the screenshots currently associated with this URL: ")
                screenshots_for_key = screenshot_inventory.get(key, MISSING_VALUE)
                print(screenshots_for_key)
                # Ask the user what they'd like to do with screenshots?
                add_or_remove_screenshots = int(input("What would you like to do with screenshots? \n 1. Add screenshots \n 2. Remove screenshots \n"))
                # If the user wants to add screenshots:
                if add_or_remove_screenshots == 1:
                    # Get input from user for new screenshots to watch, append them to the current list of screenshots
                    screenshots_for_key = add_screenshots(screenshots_for_key)
                    # Overwrite the list of screenshots as values for the key (URL) in screenshot inventory dictionary
                    screenshot_inventory[key] = screenshots_for_key

                # If the user wants to remove screenshots:
                if add_or_remove_screenshots == 2:
                    # Get input from the user for screenshots they want to remove, remove them from the current list of screenshots
                    screenshots_for_key = remove_screenshots(screenshots_for_key)
                    # Overwrite the list of screenshots as values for the key (URL) in screenshot inventory dictionary
                    screenshot_inventory[key] = screenshots_for_key

                # Give the user a success message
                print("You have successfully updated screenshots for " + key)
                print("The new screenshots are: ")
                print(screenshots_for_key)
                # Update the screenshot inventory in the project dictionary
                project_dictionary = add_screenshot_inventory_to_dict(screenshot_inventory, project_dictionary)
                # Write the updated dict to the file
                save_project(project_name, project_dictionary)

                # Calculate screenshot inventory coverage
                # Extract the number of items in the external inventory from the project metadata
                external_inventory_size = get_inventory_size(project_metadata)
                # Calculate the number of screenshots in the app currently, the difference between that and the external
                # library, and the percent coverage of the external library, and print it for the user
                calculate_inventory_coverage(external_inventory_size, screenshot_inventory)

            if manage_inventory == 3:
                # Calculate screenshot inventory coverage
                # Extract the number of items in the external inventory from the project metadata
                external_inventory_size = get_inventory_size(project_metadata)
                # Calculate the number of screenshots in the app currently, the difference between that and the external
                # library, and the percent coverage of the external library, and print it for the user
                calculate_inventory_coverage(external_inventory_size, screenshot_inventory)



        # When the user wants to "Check a diff for changes to the URLs"
        if user_selects == 3:
            # Ask the user for a project name
            project_name = get_project_name()
            # Open the JSON file and extract the dictionary
            project_dictionary = open_project(project_name)
            # Extract the dictionary of URLs and screenshots from the project dictionary
            screenshot_inventory = extract_screenshot_inventory(project_dictionary)
            # Extract the project metadata from the dictionary
            project_metadata = extract_project_metadata(project_dictionary)
            # Get the base URL from the project metadata
            base_url = project_metadata.get("base_url")
            # Extract the Diffy project ID from the project metadata
            project_id = extract_project_id(project_metadata)

            # Give the user two options:
            user_diff_pref = int(input(
                "Which diff would you like to check for changes? \n 1. Check the most recent diff \n 2. Specify a diff to check \n"))
                # Check most recent diff
            if user_diff_pref == 1:
                # Get list of diffs from Diffy, store the ID from the most recent
                headers = get_default_headers_from_diffy()
                diff_id = get_most_recent_diff_id(headers, project_id)
            # Specify a diff
            if user_diff_pref == 2:
                # Get input from the user, store it to a var
                diff_id = input("What is the ID of the diff you'd like to check? ")
            # Get diff data from Diffy
            diffy_data_dump = get_diff_data_from_diffy(diff_id)
            # Extract URLs and scores from Diffy's diff data
            diffy_dict = dict_urls_and_scores_from_diffy(diffy_data_dump)
            # Create a list of only URLs with changes from the diff
            urls_with_changes = generate_list_of_changed_urls(diffy_dict)
            # Append list of changed URLs from diffy to base URL from project
            processed_changed_urls = add_base_url(urls_with_changes, base_url)
            print("These URLs contain changes: ")
            print('\n'.join(map(str, processed_changed_urls)))
            print("Review these screenshots for each changed URL: ")
            # Pass the list of URLs to the screenshot inventory dictionary as keys, and print the keys and the values (screenshots)
            print_screenshots_for_urls(processed_changed_urls, screenshot_inventory)

        if user_selects == 4:
            break

# These are commands that deal with getting a project name from the user, and opening/writing to files

def get_project_name():
    # Ask the user what project they'd like to open
    return input(str("Which project would you like to open? "))

def open_project(project_name):
    # Using the project name that the user entered, create a filename
    filename = str(project_name + ".json")
    # Using the filename, open the project file and convert the JSON to a Python dictionary.
    # Returns a Python dictionary containing URLs and screenshots to main.
    with open(filename, "r") as current_project:
        existing_content = json.load(current_project)
        return existing_content

def save_project(project_name, project_dictionary):
    # Using the project name that the user entered, create a filename
    filename = str(project_name + ".json")
    # Using the filename, convert the Python dictionary to JSON and write it to the file
    with open(filename, 'w') as savefile:
        json.dump(project_dictionary, savefile)

# Status messages

def invalid_selection():
    return "You have made an invalid selection. Please specify only the number for the action you'd like to take."

def human_readable_status_codes(status_code):
    missing_value = "Diffy returned an unrecognized response."
    human_readable = {"200": "Your URLs were successfully updated in Diffy", "400": "The domain in one of your URLs did not match the production domain in Diffy", "401": "There was a problem authenticating with Diffy"}
    return human_readable.get(status_code, missing_value)

# These commands are for dealing with project dictionaries

def extract_project_metadata(dictionary):
    project_metadata = dictionary["project_metadata"]
    return project_metadata

def add_project_metadata_to_dict(project_metadata, project_dictionary):
    project_dictionary["project_metadata"] = project_metadata
    return project_dictionary

def extract_screenshot_inventory(dictionary):
    screenshot_inventory = dictionary["screenshot_inventory"]
    return screenshot_inventory

def add_screenshot_inventory_to_dict(screenshot_inventory, project_dictionary):
    project_dictionary["screenshot_inventory"] = screenshot_inventory
    return project_dictionary

def print_dictionary(dictionary):
    for key,value in dictionary.items():
        print(key,value)

def add_urls(url_list):
    updated_urls = url_list
    while True:
        new_urls = input("What URL do you want to watch? ")
        if new_urls == "":
            break
        updated_urls.append(new_urls)
    return updated_urls

def remove_urls(url_list):
    remove_url = input("Which URL do you want to remove? ")
    while remove_url in url_list:
        url_list.remove(remove_url)
        return url_list
    else:
        print("That is not a valid URL in the inventory.")

def add_screenshots(current_screenshots):
    updated_screenshots = current_screenshots
    while True:
        screenshot = input("What is a new screenshot associated with this URL? ")
        if screenshot == "":
            break
        updated_screenshots.append(screenshot)
    return updated_screenshots

def remove_screenshots(current_screenshots):
    remove_screenshot = input("Which screenshot do you want to remove? ")
    if remove_screenshot in current_screenshots:
        current_screenshots.remove(remove_screenshot)
    return current_screenshots

def extract_urls(urls_in_project):
    '''Create an empty list, and then loop through the keys in the dictionary - in this case, URLs, adding them
    to the empty list.
    :param urls_in_project: This is a dictionary containing all of the URLs and screenshots in the project.
    :return: The list of keys (URLs) that we've extracted from the dictionary.'''
    return list(urls_in_project.keys())

def update_urls_to_watch(urls_to_watch, screenshot_inventory):
    for url in urls_to_watch:
        # Add new URLs to dictionary
        if not screenshot_inventory.get(url):
            screenshot_inventory[url] = []
    # Remove URLs from the dictionary
    urls_to_delete = [url for url in screenshot_inventory.keys() if url not in urls_to_watch]
    for url in urls_to_delete:
        del screenshot_inventory[url]
    return screenshot_inventory

def print_screenshots_for_urls(urls, screenshot_inventory):
    for url in urls:
        screenshots = screenshot_inventory.get(url, MISSING_VALUE)
        if len(screenshots) > 0:
            print("For the URL " + url + ": \n Review these screenshots:")
            for screenshot in screenshots:
                print("\t * " + screenshot)
        else:
            print("There were no screenshots found for " + url)

def get_inventory_size(project_metadata):
    external_inventory_size = project_metadata["screenshots_in_external_library"]
    return external_inventory_size

def extract_project_id(project_metadata):
    project_id = project_metadata["diffy_project_id"]
    return project_id

# These commands are for calculating screenshot inventory coverage

def calculate_inventory_coverage(external_inventory, screenshot_inventory_dict):
    '''
    :param external_inventory: This is how many screenshots the user has in their external library, and it comes from
    the get_inventory_size() method
    :param screenshot_inventory_dict: This param passes the project dictionary into the calculate_project_inventory_size
    method, so the method can loop through each screenshot and increment a counter, counting the number of screenshots
    that have currently been inventoried in the app.
    :return: Give the user a print statement telling them how many screenshots they have inventoried in the app so far,
    the difference between the app's inventory and their external screenshot library, and the percentage of coverage of
    that library.
    '''
    # Calculate the number of screenshots that are currently in the project
    number_of_screenshots_in_project = calculate_project_inventory_size(screenshot_inventory_dict)
    # Calculate the difference between the number of screenshots in the external library and the number of screenshots
    # that have been entered into the app.
    number_of_screenshots_to_inventory = external_inventory - number_of_screenshots_in_project
    # Calculate the percent of coverage of the external library based on how many screenshots have been entered into
    # the app.
    percent_of_screenshots_inventoried = int((number_of_screenshots_in_project / external_inventory) * 100)
    # Convert ints to strings and give the user a message containing details of the calculations.
    return print("You have inventoried " + str(number_of_screenshots_in_project) + " screenshots. \n "
                    "You have " + str(number_of_screenshots_to_inventory) + " remaining screenshots to inventory. \n "
                    "You have inventoried " + str(percent_of_screenshots_inventoried) + "% of your total screenshots.")

def calculate_project_inventory_size(screenshot_inventory):
    '''
    Loop through all of the screenshots in the project dictionary, and increment a counter, to create a count of the
    current number of screenshots the user has inventoried.
    :param total_screenshots: This is the project dictionary containing all of the URLs and screenshots in the project.
    :return: An int that represents the total number of screenshots currently inventoried in the app.
    '''
    total = 0
    for screenshots in screenshot_inventory.values():
        for screenshot in screenshots:
            total += 1
    return total

# These commands are for using the Diffy API

def get_default_headers_from_diffy():
    payload = {"key": "816e6d80f424c910b4f05cf1e34d994c"}
    response = requests.post("https://app.diffy.website/api/auth/key", data=json.dumps(payload))
    token = json.loads(response.text)["token"]
    abt = "Bearer " + token
    default_header = {"Authorization": abt}
    return default_header

def update_project(header, url_list, project_id):
    url = str("https://app.diffy.website/api/projects/" + str(project_id))
    response = requests.get(url, headers=header)
    project_dict = json.loads(response.text)
    project_dict['urls'] = url_list
    r = requests.post(url, headers=header, data=json.dumps(project_dict))
    return str(r.status_code)

def update_urls_in_diffy(list_of_urls, project_id):
    headers = get_default_headers_from_diffy()
    update_status = update_project(headers, list_of_urls, project_id)
    return update_status

def get_most_recent_diff_id(header, project_id):
    url = str("https://app.diffy.website/api/projects/" + str(project_id) + "/diffs")
    response = requests.get(url, headers=header)
    diff_list = json.loads(response.text)['diffs']
    diff_id = diff_list[0]['id']
    return diff_id

def get_diff_data_from_diffy(diff_id):
    url = "https://app.diffy.website/api/diffs/" + str(diff_id)
    header = get_default_headers_from_diffy()
    response = requests.get(url, headers=header)
    response = json.loads(response.text)
    return response

def dict_urls_and_scores_from_diffy(response):
    diffs_dict = response["diffs"]
    urls_and_scores = {}
    for url in diffs_dict.keys():
        scores = []
        # Rewrite this with the d.items() method that returns keys and values
        sizes_dictionary = diffs_dict[url]
        for size in sizes_dictionary.keys():
            specific_size_dict = sizes_dictionary[size]
            scores.append(specific_size_dict['diff']['score'])
        urls_and_scores[url] = scores
    return urls_and_scores

def check_for_changed_url(scores):
    return any(x != 0 for x in scores)

def generate_list_of_changed_urls(urls_and_scores):
    list_of_changed_urls = []
    for url,scores in urls_and_scores.items():
        if check_for_changed_url(scores):
            list_of_changed_urls.append(url)
    return list_of_changed_urls

def populate_urls_from_diffy(project_id):
    header = get_default_headers_from_diffy()
    diffy_dict = get_project_info_from_diffy(project_id, header)
    diffy_urls = diffy_dict["urls"]
    return diffy_urls


def get_project_info_from_diffy(project_id, header):
    url = str("https://app.diffy.website/api/projects/" + str(project_id))
    response = requests.get(url, headers=header)
    diffy_dict = json.loads(response.text)
    return diffy_dict

def add_base_url(urls_from_diffy, base_url):
    processed_urls = []
    for url in urls_from_diffy:
        full_url = str(base_url + url)
        processed_urls.append(full_url)
    return processed_urls

''' Deprecated methods: The Junkyard

def convert_urls_for_diffy(url_list):
    To update the URLs in the project using Diffy's API, we must POST a list of all of the URLs in the project in a
    specific format. This function calls the add_slashes method, passing in the list of all the URLs that the user has
    entered, so they can be formatted to the manner that Diffy requires.
    :param url_list: This function receives a list of all of the URLs that are currently in the project.
    :return: The list of processed URLs that are ready to be converted to JSON and POSTed to Diffy.
    project_urls = url_list
    processed_urls = add_slashes(project_urls)
    return processed_urls

def add_slashes(base_urls):
    Diffy requires a list of URLs that contains a \ before every /. This function takes the URLs that the user has entered,
    and adds a \ before every URL per Diffy's requirements. https://www.google.com/ would become https:\/\/www.google.com\/
    :param base_urls: This is the list of URLs in the project, passed in as the project_urls list from the
    convert_urls_for_diffy method.
    :return: List of URLs that have been processed to contain the extra \.
    # Create an empty list to store the modified strings
    urls_with_slashes = []
    # Loop through all of the URLs in the base_urls list, replacing the "/" with a "\/" and then appending it to the
    # new list created above. NOTE: the extra \ is required because Python treats the single \ as an escape. When printing
    # these converted URLs for debugging, they will appear to contain two backslashes before every forward slash
    # i.e. "\\/" - but using len() to verify the length of these strings confirms that is a display issue and the strings
    # are actually correctly formatted for passing to Diffy.
    for url in base_urls:
        new_url = url.replace("/", '\\/')
        urls_with_slashes.append(new_url)
    return urls_with_slashes
'''


if __name__ == '__main__':
    main()