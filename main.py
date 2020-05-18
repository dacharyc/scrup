"""
File: main.py
------------------
Program to track screenshots to change in technical documentation.
"""

def main():
    # TODO: Get a URL (Page in app path) from user, store it
    # TODO: Get a list of screenshots associated with that URL from user, store it
    # TODO: Get a second URL to diff against primary URL from user, store it
    # TODO: Check with Diffy (API?) to verify whether there's a visual diff for original path vs. new path
    # TODO: If there is a visual diff for a path, return the path name for the user, along with a list of screenshots associated with that path name
    # TODO: Tell the user there are changes to path and to check screenshots
    # TODO: If there is no visual diff for a path, return a message to the user to let her know there are no changes

    user_selects = int(input("What would you like to do? \n 1. Create a new project \n 2. Add a URL to a project \n "
                             "3. Add a screenshot to a URL \n 4. Diff URLs \n"))


    if user_selects == 1:
        create_project()
    if user_selects == 2:
        open_project = input(str("Which project would you like to open? "))
        to_watch = add_url_to_project()
        print("You have added these URLs and screenshots to watch: ")
        print_to_watch(to_watch)
        save_url_to_project(open_project, to_watch)


def create_project():
    file = open(input(str("Name your project: ")), "x")

def add_url_to_project():
    '''
    Asks the user for URLs to watch, and any screenshots associated with that URL.
    Returns the dictionary of things to watch.
    '''



    to_watch = {}

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

def save_url_to_project(open_project, to_watch):
    current_project = open(open_project, "a")
    current_project.write(str(to_watch))
    current_project.close

'''
def open_project():
    open_project = input(str("Which project would you like to open? "))
    return open_project

def get_url_path():
    open_project = open(input(str("Which project would you like to open? ")), "a")
    urls_in_project = {}  # Create an empty list of urls in a project
    open_project.write(input(str("What is the URL of the page you'd like to watch? ")))
    open_project.close()

    url_to_watch = open(input(str("Which project would you like to verify?")), "r")
    print(url_to_watch.read())

def add_screenshot_to_url(url_to_watch):
    url_to_watch[].append

'''

if __name__ == '__main__':
    main()