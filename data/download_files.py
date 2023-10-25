import os
import requests
import openpyxl
from bs4 import BeautifulSoup

PROJECTS_SPREADSHEET_PATH = "projects.xlsx"
BASE_URL = "https://www.thegef.org/projects-operations/projects/"
OUTPUT_PATH = "NEW"
INTERESTED_YEARS = [i for i in range(2012, 2024)]


def get_project_ids_from_spreadsheet(path):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active

    project_ids = []

    for row in range(1, sheet.max_row + 1):
        year_cell = sheet.cell(row=row, column=10)
        if year_cell.value in INTERESTED_YEARS:
            id_cell = sheet.cell(row=row, column=2)
            project_ids.append(id_cell.value)

    return project_ids


def download_pdfs_from_project_page(project_id):
    url = BASE_URL + str(project_id)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to access website: {url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    pdf_counter = 0
    for link in links:
        href = link.get("href")
        if href and ".pdf" in href:
            pdf_counter += 1
            try:
                pdf_response = requests.get(href)
                pdf_file_path = os.path.join(
                    OUTPUT_PATH, f"pdf{project_id}_{pdf_counter}.pdf"
                )
                with open(pdf_file_path, "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"Downloaded file {pdf_counter}")
            except Exception as e:
                print(f"Failed to download PDF from: {href}")
                print(e)


def main():
    project_ids = get_project_ids_from_spreadsheet(PROJECTS_SPREADSHEET_PATH)
    for project_id in project_ids:
        download_pdfs_from_project_page(project_id)


if __name__ == "__main__":
    main()
