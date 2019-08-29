For running the app on container follow the steps:

1. Clone the repo
2. docker build --tag downloader_app .
3. docker run --detach -ti -p 80:8000 downloader_app
