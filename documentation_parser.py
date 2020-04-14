from os import listdir, walk, chdir, curdir
from os.path import isfile, join, curdir, basename
from pprint import pformat, pprint as pp
import requests, zipfile, io
import tempfile

from constants import *
import json


ANY_FILE = ""

def all_file_paths(path=curdir, extension=ANY_FILE):
    """
    Retreive all the paths
    :param path:
    :return:
    """
    file_paths = []
    for root, dirs, files in walk(path):
        for file in files:
            if file.endswith(extension):
                file_paths.append(join(root, file))
    return file_paths

def format_result(result):
    raise NotImplemented

def save_result(result):
    raise NotImplemented

def parse_repo(repo):
    download_repo(repo)
    # raise NotImplemented

def parse_release(release):
    raise NotImplemented

def download_repo(zip_file_url, dir):

    r = requests.get(zip_file_url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path=dir)

    return join(dir, z.namelist()[0])


def parse_dir(dir=curdir):
    paths = all_file_paths(path=dir, extension='.' + JAVASCRIPT)
    histogram = {}
    result = {'files': [], "histogram": histogram}
    for file_path in paths:
        file_result = {
            'path': basename(file_path),
            'documentations': 0
        }
        with open(file_path, 'r') as f:
            try:
                t = f.read()
                docs = DOCUMENTATION_REGEX[JAVASCRIPT][ALL].findall(t)
                for doc in docs:
                    for word in doc.split(" "):
                        word = word.replace("\n", "")
                        if "*" in word:
                            continue
                        if word not in histogram:
                            histogram[word] = 0
                        histogram[word] += 1
                file_result["documentations"] += len(docs)
            except UnicodeDecodeError as e:
                print("bad file: " + file_path)
            except Exception as e:
                print("Unknown Error: " + file_path)
                print(e)
            finally:
                result["files"].append(file_result)


    # pp(sorted([(k, v) for k, v in histogram.items()], key=lambda kv: kv[1]))
    # pp(result)

    # print(len(paths))
    return result
    # raise NotImplemented

if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as d:
        r = requests.get("https://api.github.com/repos/twbs/bootstrap/tags")
        tags = r.json()
        for tag in tags:
            release_zip_url = tag["zipball_url"]
            # release = "https://api.github.com/repos/twbs/bootstrap/zipball/v4.4.0"
            path = download_repo(release_zip_url, dir=d)
            # print(path)
            result = parse_dir(dir=path)
            with open(tag['name'].replace(".", "_") + ".json", 'w') as f:
                json.dump(result, f, indent=2)
