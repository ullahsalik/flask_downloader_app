from flask import Flask, request, jsonify
import requests, uuid, os, time, re
from multiprocessing import Process, Manager

application = Flask(__name__)

# Global dictionary for key as Process_ID or download_id and value is a dictionary of attribute of that download_id eg. {'Total_file_size':, 'Downloaded':}
process_dict = Manager().dict()

# Function to start downloading a file and writing in chunks
def file_download(url, file_name, id):
    start = time.process_time()
    response = requests.get(url, stream = True, allow_redirects=True)
    with open(file_name,"wb") as file:
        dl = 0
        for chunk in response.iter_content(chunk_size=1024):
            dl += len(chunk)
            process_dict['speed'] = (dl//(time.process_time() - start)/8) # get the current download speed
            if chunk:
                file.write(chunk)


# IP/download?url=enter_url
@application.route('/download', methods=['GET'])
def main():
    r = requests.get(request.args.get('url'), allow_redirects=True)  # to get content after redirection
    url = r.url # 'https://media.readthedocs.org/pdf/django/latest/dj
    id = str(uuid.uuid4().hex[:5])
    header = requests.head(url, allow_redirects=True).headers
    try:
        filename = url.split('/')[-1]
    except Exception as e:
        filename = re.findall("filename=(.+)", header['content-disposition'])[0].replace('"', '') # get the filename from the header
    process_dict[id]={
        'Total file size': int(header.get('content-length', 0)),
        'File name': filename,
    }
    process = Process(name=str(id), target=file_download, args=(url, filename, id))
    process.daemon = True
    process.start()
    context = {
    'download_id' : id,
    }
    return(jsonify(context))


# Get the details of the download_process(download_id)
@application.route('/status', methods=['GET'])
def get_download_details():
    download_id = request.args.get('id')
    try:
        download_data = process_dict[download_id]
        d_file_size=os.path.getsize(download_data['File name'])
        r_file_size = download_data['Total file size'] - d_file_size
        eta = r_file_size/process_dict['speed']
        if r_file_size !=0:
            status = "Downloading"
        else:
            status = "Completed"
        download_data["Downloaded file size"] = "{}KB".format(round(((d_file_size)/1024),2))
        download_data["Remaining file size"] = "{}KB".format(round(((r_file_size)/1024),2))
        download_data["Status"] = status
        download_data["Estimated time"] = "{} seconds".format(round(eta, 2))
        download_data['Total file size'] = "{} Bytes".format(download_data['Total file size'])
        process_dict[download_id] = download_data
        return(process_dict[download_id])

    except Exception as e:
        raise e
        return(jsonify({'error': 'Unable to find the download with particular id'}))

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8000)


# I am not using any db for now for storing the details of the download
