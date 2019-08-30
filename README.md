# flask_downloader_app

This is an app build using python flask for downloading a file and getting the status of the download.

# How this app work:

This is an API based backend code, for running the app on container follow the steps:

1. Clone the repo
2. Build the image from the dockerfile in the current directory by running the command "docker build --tag downloader_app ."
3. Launch a container from the build image by running the command "docker run --detach -ti -p 80:8000 downloader_app"
4. HOSTNAME/download?url=url_of_the_file e.g. https://readthedocs.org/projects/django/downloads/pdf/latest/
   - In response will get the unique id.
5. HOSTNAME/status?id=unique_id
   - In responce will get the status of the download
   - e.g. {
            "Total file size": "1651264 Bytes"
            "Downloaded file size": "1612.56KB",
            "Remaining file size": "0.0KB",
            "Estimated time": "0.0 seconds",
            "Status": "Completed",
            "File name": "give-and-take.pdf"
          }

