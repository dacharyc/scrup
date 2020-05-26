Scrup, which stands for SCReenshot UPdate, is a program designed 
to let you know when you need to update screenshots in technical 
documentation.

To use Scrup:
___
Create a project in Diffy (https://diffy.website/)
- Diffy is the visual diffing tool where Scrup will check for changes to the website or web app you're documenting
- You'll need the Project ID when you create the project in Scrup - this will enable Scrup to make API calls to and from Diffy
- If you want to check a specific diff in Diffy for changes, you can get the diff ID and enter it; otherwise, Scrup will just check the latest diff for changes
- Diffy can automatically generate a list of URLs to track in your website or webapp, and if you choose to do that, you can import that list into Scrup versus generating it manually

Create a screenshot inventory in Scrup:
- Create a project using the project ID from Diffy
- Pull in URLs from Diffy, if you'd like, otherwise manually input the URLs for a website or web app that you want to change;
- Input screenshots associated with that URL.

Check a diff for changes to URLs
- After you're all set up in Diffy and Scrup, go into Scrup and choose "Check a diff for changes to URLs." Scrup makes an API call to Diffy to get changes, and then gives you a list of all the URLs that have changed, as well as the screenshots associated with those URLs that you'll need to review.

ScrUp is written in Python 3.
