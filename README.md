# flask_downloader_app

This is an app build using python flask for downloading a file and getting the status of the download.

# How this app work:

This is an API based backend code, for running the app on container follow the steps:

1. Clone the repo
2. docker build --tag downloader_app .
3. docker run --detach -ti -p 80:8000 downloader_app
4. HOSTNAME/download?url=url_of_the_file - in responce you will get the unique id 31
5. 

