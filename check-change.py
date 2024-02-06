import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime
import git
import os

def fetch_and_convert(url):
    try:
        response = requests.get(url, timeout=60)  # Increased timeout
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        content = soup.find(id='content-area')
        return md(str(content))
    except requests.exceptions.Timeout:
        print(f"Request timed out. URL: {url}")
        return None

def has_content_changed(new_content, repo_path, slug):
    current_version_file = f'{slug}_current.md'
    with open(os.path.join(repo_path, 'versions', current_version_file), 'r', encoding='utf-8') as file:
        current_content = file.read()
    return current_content != new_content

def save_new_version(new_content, repo_path, slug):
    date_suffix = datetime.now().strftime("%Y%m%d")
    version_filename = f'version_{slug}_{date_suffix}.md'
    current_version_file = f'{slug}_current.md'

    with open(os.path.join(repo_path, 'versions', version_filename), 'w', encoding='utf-8') as file:
        file.write(new_content)
    with open(os.path.join(repo_path, 'versions', current_version_file), 'w', encoding='utf-8') as file:
        file.write(new_content)

def commit_and_push_changes(repo_path):
    repo = git.Repo(repo_path)
    repo.git.add(A=True)
    repo.git.commit('-m', 'Lepingumuudatused')
    repo.git.push()

def main():
    urls = {
        'lepingutekst-klubiga-liitujatele': 'https://casadebaile.ee/lepingutekst-klubiga-liitujatele/',
        'klubiliige': 'https://www.casadebaile.ee/klubiliige/',
        'vip-klubiliige': 'https://www.casadebaile.ee/vip-klubiliige/',
        'e-poe-muugitingimused': 'https://www.casadebaile.ee/e-poe-muugitingimused/',
        'privaatsustingimused':'https://www.casadebaile.ee/privaatsustingimused/'
        
    }
    repo_path = os.getcwd()  # e.g. /home/user/my-repo

    for slug, url in urls.items():
        new_content = fetch_and_convert(url)
        if new_content and has_content_changed(new_content, repo_path, slug):
            save_new_version(new_content, repo_path, slug)

    commit_and_push_changes(repo_path)

if __name__ == "__main__":
    main()
