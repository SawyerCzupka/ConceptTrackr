import os
import csv
import requests
from bs4 import BeautifulSoup
import dask
from dask import delayed, compute

PROJECTS_CSV_PATH = "projects.csv"
BASE_URL = "https://www.thegef.org/projects-operations/projects/"
OUTPUT_PATH = "dump"
INTERESTED_YEARS = [i for i in range(2012, 2024)]


def get_project_ids_from_csv(path):
    project_ids = []
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            try:
                year = int(row[9])  # Assuming the year is in the 10th column
                if year in INTERESTED_YEARS:
                    project_id = row[1]  # Assuming the ID is in the 2nd column
                    project_ids.append(project_id)
            except:
                continue
    return project_ids


@delayed
def download_pdf(link, project_id, pdf_counter):
    href = link.get("href")
    if href and ".pdf" in href:
        try:
            pdf_response = requests.get(href)
            pdf_file_path = os.path.join(
                OUTPUT_PATH, f"pdf{project_id}_{pdf_counter}.pdf"
            )
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(pdf_response.content)
            return f"Downloaded file {pdf_counter}"
        except Exception as e:
            return f"Failed to download PDF from: {href}", e


@delayed
def download_pdfs_from_project_page(project_id):
    url = BASE_URL + str(project_id)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Failed to access website: {url}"

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    results = []
    pdf_counter = 0
    for link in links:
        pdf_counter += 1
        result = download_pdf(link, project_id, pdf_counter)
        results.append(result)

    return results


def main():
    project_ids = get_project_ids_from_csv(PROJECTS_CSV_PATH)

    tasks = [download_pdfs_from_project_page(pid) for pid in project_ids]
    results = compute(*tasks)  # This will parallelly compute the tasks

    for result in results:
        for msg in result:
            print(msg)


if __name__ == "__main__":
    main()
