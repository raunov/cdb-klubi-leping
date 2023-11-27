import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime
import git

def fetch_and_convert(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    content = soup.find(id='content-area')
    
    return md(str(content))

def has_content_changed(new_content, repo_path, current_version_file):
    with open(f"{repo_path}/{current_version_file}", 'r',encoding='utf-8') as file:
        current_content = file.read()
    return current_content != new_content

def main():
    url = 'https://www.casadebaile.ee/lepingutekst-klubiga-liitujatele/' 
    repo_path = 'versions' # e.g. /home/user/my-repo
    current_version_file = 'current.md'
    new_content = fetch_and_convert(url)

    if has_content_changed(new_content, repo_path, current_version_file):
        date_suffix = datetime.now().strftime("%Y%m%d")
        with open(f"{repo_path}/version_{date_suffix}.md", 'w',encoding='utf-8') as file:
            file.write(new_content)
        with open(f"{repo_path}/{current_version_file}", 'w',encoding='utf-8') as file:
            file.write(new_content)
        repo = git.Repo(repo_path)
        repo.git.add(A=True)
        repo.git.commit('-m', 'Updated content version')
        repo.git.push()

if __name__ == "__main__":
    main()
