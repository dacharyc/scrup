class User_Input():

    def __init__(self):
        print("User Created")

    def new_project(self):
        # Prompt the user for inputs
        name = input("What would you like to name your project? ")
        base_url = input("What is the base URL for your project, as you've entered it in Diffy? ")
        base_url = strip_trailing_slashes(base_url)
        diffy_project_id = int(input("What is the project ID in Diffy? "))
        return name, base_url, diffy_project_id


sample_user = User_Input()

print(sample_user)


class Menu():

    def __init__(self):
        pass

    def main_menu(self):
        print("1. Manage Projects \n 2. Manage screenshot inventory \n 3. Check diffs for changes")


class Project(name, base_url, diffy_project_id):

    def __init__(self):
        pass

    def create_project(self):
        # Create an empty dictionary for the project
        project_dict = {}

    def update_project(self):
        # Overwrite the project metadata for the project dict
        project_dict = project_dict(name, base_url, diffy_project_id)

    def delete_project(self):
        # Remove the project
        pass
    

class Screenshot_Inventory(URL, screenshot):

    def __init__(self):
        pass

    def create_screenshot_inventory(self):
        # Create an empty placeholder dictionary for the screenshot inventory
        screenshot_inventory = {}

    def update_screenshot_inventory(self):
        # Add the screenshot inventory to the project dict
        project_dict = add_screenshot_inventory_to_dict(screenshot_inventory, project_dict)

    def add_new_url(self):
        pass

    def update_url(self):
        pass

    def delete_url(self):
        pass

    def list_url(self):
        pass

    def add_screenshot(self):
        pass

    def remove_screenshot(self):
        pass



class
