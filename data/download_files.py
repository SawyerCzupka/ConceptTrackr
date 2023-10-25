import os
import csv
import requests
import logging
from bs4 import BeautifulSoup
import dask
from dask import delayed

PROJECTS_CSV_PATH = "projects.csv"
BASE_URL = "https://www.thegef.org/projects-operations/projects/"
OUTPUT_PATH = "dump"
INTERESTED_YEARS = [i for i in range(2012, 2024)]

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_project_ids_from_csv(path):
    project_ids = []
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            try:
                year = int(row[9])
                if year in INTERESTED_YEARS:
                    project_id = row[1]
                    project_ids.append(project_id)
            except ValueError:
                continue
    return project_ids


def download_pdfs_from_project_page(project_id):
    url = BASE_URL + str(project_id)
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Failed to access website: {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    pdf_links = [
        link.get("href")
        for link in links
        if link.get("href") and ".pdf" in link.get("href")
    ]

    downloaded_files = []
    for idx, href in enumerate(pdf_links):
        try:
            pdf_response = requests.get(href)
            pdf_file_path = os.path.join(OUTPUT_PATH, f"pdf{project_id}_{idx}.pdf")
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(pdf_response.content)
            logging.info(f"Downloaded file: {pdf_file_path}")
            downloaded_files.append(pdf_file_path)
        except Exception as e:
            logging.error(f"Failed to download PDF from: {href}. Error: {e}")

    return downloaded_files


def main():
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    project_ids = get_project_ids_from_csv(PROJECTS_CSV_PATH)
    tasks = [delayed(download_pdfs_from_project_page)(pid) for pid in project_ids]
    _ = dask.compute(*tasks)


if __name__ == "__main__":
    main()
