"""
File: main.py
------------------
Program to track screenshots to change in technical documentation.
"""

import json
import requests

def main():
    # TODO: Test that a project name is valid
    # TODO: Test that a project file (reading a file) exists, if not, return an empty dictionary
    # TODO: Improve project name stuff (don't require a file type, give a user a list of projects to choose from)
    # TODO: Check with Diffy (API?) to verify whether there's a visual diff for original path vs. new path
    # TODO: If there is a visual diff for a path, return the path name for the user, along with a list of screenshots associated with that path name
    # TODO: Tell the user there are changes to path and to check screenshots
    # TODO: If there is no visual diff for a path, return a message to the user to let her know there are no changes

    # Ask the user what they would like to do in the program, and capture that as a variable
    user_selects = int(input("What would you like to do? \n 1. Add a URL to a project \n 2. Diff URLs \n 3. Calculate screenshot inventory coverage \n"))

    # When the user wants to "Add a URL to a project":
    if user_selects == 1:
        # Ask the user for a project name
        project_name = get_project_name()
        # Open the JSON file and extract the dictionary of URLs and screenshots
        existing_content = open_project(project_name)
        # Solicit new URLs and screenshots from the user, and add those to the dictionary
        to_watch = add_urls_and_screenshots(existing_content)
        # Give the user a success message letting them know what URLs and screenshots they've added to the project
        print("You have added these URLs and screenshots to watch: ")
        print_to_watch(to_watch)
        # Extract a list of all of the keys (URLs) contained in the dictionary
        list_of_urls = extract_urls(to_watch)
        # Update the URLs in Diffy
        headers = get_default_headers_from_diffy()
        update_status = update_project(headers, list_of_urls)
        # Translate the API response code to something meaningful to the user, and print it
        print(human_readable_status_codes(update_status))
        # Convert the dictionary to JSON, and save it using the project name the user entered above
        save_project(to_watch, project_name)



    # When the user wants to "Diff URLs"
    if user_selects == 2:
        # Ask the User for a project name, and then get the list of URLs that are in that project
        url_list = get_list_of_urls_for_project()
        print(url_list) # Print the list of URLs for verification/debugging
        # Perform a Get request using Diffy's REST API to retreive Project Info, and convert it to a Python dictionary
        # stored as my_dictionary
        my_dictionary = suck_in_stuff_from_api()
        # Replace the value for the "urls" key in the dictionary with the list of URLs that has been updated for Diffy
        my_dictionary["urls"] = processed_urls
        print(processed_urls)  # For debugging
        print(json.dumps(processed_urls)) # For debugging
        # Convert the dictionary back to JSON, and POST it to Diffy, giving Diffy the current list of URLs to watch
        # add_urls_to_diffy(converted_urls)

    # When the user wants to calculate screenshot inventory coverage
    if user_selects == 3:
        # Ask the User for a project name
        project_name = get_project_name()
        # Get the dictionary of URLs and screenshots from the project whose name the user has entered
        project_inventory_size = open_project(project_name)
        # Ask the user for the number of screenshots in their external library
        external_inventory_size = get_inventory_size()
        # Calculate the number of screenshots in the app currently, the difference between that and the external
        # library, and the percent coverage of the external library, and print it for the user
        calculate_inventory_coverage(external_inventory_size, project_inventory_size)


# These are commands that deal with getting a project name from the user, and opening/writing to files

def get_project_name():
    # Ask the user what project they'd like to open - i.e. filename
    return input(str("Which project would you like to open? "))

def open_project(filename):
    # Using the filename that the user entered, open the project file and convert the JSON to a Python dictionary.
    # Returns a Python dictionary containing URLs and screenshots to main.
    with open(filename, "r") as current_project:
        existing_content = json.load(current_project)
        return existing_content

def save_project(project_dictionary, project_filename):
    # Using the filename that the user entered, convert the Python dictionary to JSON and write it to the file
    with open(project_filename, 'w') as savefile:
        json.dump(project_dictionary, savefile)

# These commands are for adding URLs and screenshots to the project inventory

def add_urls_and_screenshots(existing_content):
    '''
    Asks the user for URLs to watch, and any screenshots associated with that URL.
    Returns the dictionary of things to watch.
    '''

    to_watch = existing_content

    while True:
        url_to_watch = input("What URL do you want to watch? " )
        if url_to_watch == "":
            break
        screenshot_urls = []  # Create an empty list of screenshots
        while True:
            screenshot = input("What is a screenshot associated with this URL? ")
            if screenshot == "":
                break
            screenshot_urls.append(screenshot)
        to_watch[url_to_watch] = screenshot_urls
    return to_watch


# These commands deal with getting data out of the dictionary

def print_to_watch(to_watch):
    '''
    Prints all of the URLs and associated screenshots in the to_watch list.
    '''

    for url_to_watch in to_watch:
        print(url_to_watch, "->", to_watch[url_to_watch])

def extract_urls(urls_in_project):
    '''Create an empty list, and then loop through the keys in the dictionary - in this case, URLs, adding them
    to the empty list.
    :param urls_in_project: This is a dictionary containing all of the URLs and screenshots in the project.
    :return: The list of keys (URLs) that we've extracted from the dictionary.'''
    list_of_urls = []
    for keys in urls_in_project.keys():
         list_of_urls.append(keys)
    return list_of_urls

# These commands are for calculating screenshot inventory coverage

def get_inventory_size():
    '''
    Ask the user how many screenshots they have in their external library.
    :return: The user's answer.
    '''
    return int(input("How many screenshots are in your library? "))

def calculate_inventory_coverage(external_inventory, in_project_inventory_dict):
    '''
    :param external_inventory: This is how many screenshots the user has in their external library, and it comes from
    the get_inventory_size() method
    :param in_project_inventory_dict: This param passes the project dictionary into the calculate_project_inventory_size
    method, so the method can loop through each screenshot and increment a counter, counting the number of screenshots
    that have currently been inventoried in the app.
    :return: Give the user a print statement telling them how many screenshots they have inventoried in the app so far,
    the difference between the app's inventory and their external screenshot library, and the percentage of coverage of
    that library.
    '''
    # Calculate the number of screenshots that are currently in the project
    number_of_screenshots_in_project = calculate_project_inventory_size(in_project_inventory_dict)
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

def calculate_project_inventory_size(total_screenshots):
    '''
    Loop through all of the screenshots in the project dictionary, and increment a counter, to create a count of the
    current number of screenshots the user has inventoried.
    :param total_screenshots: This is the project dictionary containing all of the URLs and screenshots in the project.
    It comes from "in_project_inventory_dict" param that was passed to the calculate_inventory_coverage method from main.
    :return: An int that represents the total number of screenshots currently inventoried in the app.
    '''
    total = 1
    for screenshots in total_screenshots.values():
        for screenshot in screenshots:
            total += 1
    return total

# These commands are for using the Diffy API

'''
def get_list_of_urls_for_project():
    Ask the user what project they want to open, open the project, convert the JSON to a Python dictionary, extract
    the list of all the URLs contained in the dictionary.
    :return: The list of all the keys (URLs) contained in the project dictionary.
    # Ask the user to enter a project name, and store it as a variable
    project_name = get_project_name()
    # Use the filename that the user entered to open the project file and convert the JSON to a Python dictionary
    project_dict = open_project(project_name)
    # Extract a list of all of the keys (URLs) contained in the dictionary
    url_list = extract_urls(project_dict)
    return url_list
'''

def convert_urls_for_diffy(url_list):
    '''
    To update the URLs in the project using Diffy's API, we must POST a list of all of the URLs in the project in a
    specific format. This function calls the add_slashes method, passing in the list of all the URLs that the user has
    entered, so they can be formatted to the manner that Diffy requires.
    :param url_list: This function receives a list of all of the URLs that are currently in the project.
    :return: The list of processed URLs that are ready to be converted to JSON and POSTed to Diffy.
    '''
    project_urls = url_list
    processed_urls = add_slashes(project_urls)
    return processed_urls

def add_slashes(base_urls):
    '''
    Diffy requires a list of URLs that contains a \ before every /. This function takes the URLs that the user has entered,
    and adds a \ before every URL per Diffy's requirements. https://www.google.com/ would become https:\/\/www.google.com\/
    :param base_urls: This is the list of URLs in the project, passed in as the project_urls list from the
    convert_urls_for_diffy method.
    :return: List of URLs that have been processed to contain the extra \.
    '''
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

def update_project(header, url_list):
    url = "https://app.diffy.website/api/projects/2470"
    response = requests.get(url, headers=header)
    project_dict = json.loads(response.text)
    project_dict['urls'] = url_list
    r = requests.post(url, headers=header, data=json.dumps(project_dict))
    return str(r.status_code)

def get_default_headers_from_diffy():
    payload = {"key": "816e6d80f424c910b4f05cf1e34d994c"}
    response = requests.post("https://app.diffy.website/api/auth/key", data=json.dumps(payload))
    token = json.loads(response.text)["token"]
    abt = "Bearer " + token
    default_header = {"Authorization": abt}
    return default_header

def human_readable_status_codes(status_code):
    missing_value = "Diffy returned an unrecognized response."
    human_readable = {"200": "Your URLs were successfully updated in Diffy", "400": "The domain in one of your URLs did not match the production domain in Diffy", "401": "There was a problem authenticating with Diffy"}
    return human_readable.get(status_code, missing_value)

if __name__ == '__main__':
    main()