from os import listdir, walk, chdir, curdir
import os
from os.path import isfile, join, curdir, basename
from pprint import pformat, pprint as pp
import requests, zipfile, io
import tempfile
import datetime
from constants import *
import json


def all_file_paths(path=curdir, extension=EXT_ANY_FILE):
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
    download_release(repo)
    # raise NotImplemented


def parse_release(release):
    raise NotImplemented


def download_release(zip_file_url, dir):
    r = requests.get(zip_file_url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path=dir)

    return join(dir, z.namelist()[0])


def parse_dir(dir=curdir, file_ext=[JAVASCRIPT]):
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

    return result


def setup_results_dir(repo):
    org, repo = repo.split("/")
    org_path = os.path.join(DIR_RESULTS, org)
    repo_path = os.path.join(org_path, repo)
    if (not os.path.exists(org_path)):
        os.mkdir(org_path)
    if (not os.path.exists(repo_path)):
        os.mkdir(repo_path)


if __name__ == '__main__':
    repo = "jitsi/jitsi-meet"
    setup_results_dir(repo)
    pagination = {'page': 0, 'per_page': 100}
    all_tags = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        for page in range(100):
            pagination['page'] = page
            r = requests.get("https://api.github.com/repos/{}/tags".format(repo), params=pagination)
            page_tags = r.json()
            if page_tags:
                all_tags.extend(page_tags)
            else:
                break
        print("For repo {} found {} tags".format(repo, len(all_tags)))
        for tag in all_tags:
            release_zip_url = tag["zipball_url"]
            location = download_release(release_zip_url, dir=tmp_dir)
            result = parse_dir(dir=location)
            with open(join(DIR_RESULTS, repo, "{}.json".format(tag['name'].replace(".", "_"))), 'w') as f:
                json.dump(result, f, indent=2)
