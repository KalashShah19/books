import requests
from bs4 import BeautifulSoup
import os

def download_pdf_books(book_name):
    print("Searching for the book...")

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
            )
        }
        url = f"https://www.google.com/search?q={book_name}+pdf"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        pdf_links = [
            a['href'] for a in soup.find_all("a", href=True) 
            if ".pdf" in a['href']
        ]

        if not pdf_links:
            print("No PDF links found for the book.")
            return

        print(f"Found {len(pdf_links)} possible PDF links.")

        for index, pdf_url in enumerate(pdf_links):
            try:
                if not pdf_url.startswith("http"):
                    pdf_url = "https://" + pdf_url.lstrip(":/")

                print(f"Attempting to download: {pdf_url}")

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
book_name = input("Enter Book Name : ")
download_pdf_books(book_name)
