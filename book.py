# pip install requests bs4

import requests
from bs4 import BeautifulSoup
import os
import time

def download_pdf_books(book_name):
    print("Searching for the book...")

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
            )
        }
        
        # Folder to save the downloaded PDFs
        os.makedirs("books", exist_ok=True)

        # URL of the first page of Google search results
        search_url = f"https://www.google.com/search?q={book_name}+pdf"
        
        # Loop through multiple pages of search results
        page_number = 0
        pdf_links = []

        while True:
            # Add the page number to the search URL (start with page=0, increment it to get subsequent pages)
            url = f"{search_url}&start={page_number * 10}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Parse the search results
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all the links on the current page
            links = [a['href'] for a in soup.find_all("a", href=True)]

            # Filter links to find those that contain ".pdf"
            page_pdf_links = [link for link in links if ".pdf" in link]
            pdf_links.extend(page_pdf_links)

            # If no new links were found, stop the loop (i.e., last page)
            if not page_pdf_links:
                break

            # Print progress and move to the next page
            print(f"Found {len(pdf_links)} possible PDF links. Moving to next page...")
            page_number += 1

            # Adding a small delay to avoid too many requests in a short time
            time.sleep(2)

        if not pdf_links:
            print("No PDF links found for the book.")
            return

        print(f"Found {len(pdf_links)} possible PDF links.")

        # Download each PDF
        for index, pdf_url in enumerate(pdf_links):
            try:
                if not pdf_url.startswith("http"):
                    pdf_url = "https://" + pdf_url.lstrip(":/")

                print(f"Attempting to download: {pdf_url}")

                # Request the PDF
                pdf_response = requests.get(pdf_url, headers=headers)
                pdf_response.raise_for_status()

                # Save the PDF locally
                filename = f"books/{book_name.replace(' ', '_')}_{index+1}.pdf"
                with open(filename, "wb") as f:
                    f.write(pdf_response.content)
                print(f"Downloaded: {filename}")

            except Exception as e:
                print(f"Error downloading {pdf_url}: {e}")

    except Exception as e:
        print(f"Error searching for {book_name}: {e}")

# Example usage
book_name = input("Enter Book Name: ")
download_pdf_books(book_name)
