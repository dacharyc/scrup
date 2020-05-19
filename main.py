"""
File: main.py
------------------
Program to track screenshots to change in technical documentation.
"""

import json

def main():
    # TODO: Get a URL (Page in app path) from user, store it
    # TODO: Get a list of screenshots associated with that URL from user, store it
    # TODO: Get a second URL to diff against primary URL from user, store it
    # TODO: Check with Diffy (API?) to verify whether there's a visual diff for original path vs. new path
    # TODO: If there is a visual diff for a path, return the path name for the user, along with a list of screenshots associated with that path name
    # TODO: Tell the user there are changes to path and to check screenshots
    # TODO: If there is no visual diff for a path, return a message to the user to let her know there are no changes

    user_selects = int(input("What would you like to do? \n 1. Add a URL to a project \n 2. Diff URLs \n"))

    if user_selects == 1:
        project_name = get_project_name()
        existing_content = open_project(project_name)
        to_watch = add_urls_and_screenshots(existing_content)
        print("You have added these URLs and screenshots to watch: ")
        print_to_watch(to_watch)
        save_project(to_watch, project_name)

def get_project_name():
    return input(str("Which project would you like to open? "))

def open_project(filename):
    with open(filename, "r") as current_project:
        existing_content = json.load(current_project)
        return existing_content

def save_project(project_dictionary, project_filename):
    with open(project_filename, 'w') as savefile:
        json.dump(project_dictionary, savefile)

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


def print_to_watch(to_watch):
    '''
    Prints all of the URLs and associated screenshots in the to_watch list.
    '''

    for url_to_watch in to_watch:
        print(url_to_watch, "->", to_watch[url_to_watch])


if __name__ == '__main__':
    main()