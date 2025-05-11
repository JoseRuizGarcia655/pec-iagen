import requests
import json
import os
import re
import random
from config.config import PATH

class Downloader_books():
  def __init__(self, path_books:str) -> None:
    """
        Downloader_books is a class that allows you to download books from the Gutendex API.
        It provides methods to download a random book, download multiple random books,
        and load a book from a file.
        :param path_books: The path where the downloaded books will be saved.
        :return: None
    """
    self.__api_url = "https://gutendex.com/books/"
    self.output_path = path_books
    self.__count = self.__count_books()
    self.__update_list_books()

  def __count_books(self) -> int:
    """
        This method retrieves the total number of books available in the Gutendex API.
        :return: The total number of books.
    """
    api_response = requests.get(self.__api_url)
    if api_response.status_code == 200:
      book_data = json.loads(api_response.text)
      return book_data["count"]

  def __update_list_books(self) -> None:
    """
        This method updates the list of downloaded books by checking the output path.
        It retrieves the names of all files in the output path and stores them in the books attribute.
        :return: None
    """
    try:
      filenames = [f for f in os.listdir(self.output_path) if os.path.isfile(os.path.join(self.output_path, f))]
      self.books = filenames
    except FileNotFoundError:
      self.books = []

  def download_book(self, book_url, output_file_name) -> bool:
    """
        This method downloads a book from the given URL and saves it to the specified output path.
        :param book_url: The URL of the book to be downloaded.
        :param output_file_name: The path where the downloaded book will be saved.
        :return: True if the download was successful, False otherwise.
    """
    try:
        response = requests.get(book_url, stream=True)
        response.raise_for_status()

        with open(output_file_name, "w", encoding="utf-8") as file:
          for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk.decode("utf-8"))

        self.__update_list_books()
        return True

    except Exception as e:
        print(f"Error downloading book: {output_file_name}")
        if os.path.exists(output_file_name[:-4]):
          if os.path.getsize(output_file_name[:-4]) == 0:
            os.remove(output_file_name[:-4])
            print(f"Corrupted or incomplete file {output_file_name} has been deleted.")
        print(e)
        return False
        

  def download_random_book(self) -> None:
    """
        This method downloads a random book from the Gutendex API.
        It generates a random book ID, retrieves the book data from the API,
        and downloads the book in plain text format.
        :return: None
    """
    book_id = random.randint(1, self.__count)
    api_response = requests.get(f"{self.__api_url}{book_id}")
    if api_response.status_code == 200:
      book_data = json.loads(api_response.text)
      book_name = book_data["title"]
      book_name = re.sub(" ", "_", book_name)
      book_name = re.sub(r"[^a-zA-Z0-9_]", "", book_name)

      if "formats" in book_data:
          if "text/plain; charset=us-ascii" in book_data["formats"]:
            book_url = book_data["formats"]["text/plain; charset=us-ascii"]
            output_file_name = f"{self.output_path}{book_name}.txt"
            os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
            if self.download_book(book_url, output_file_name):
              if os.path.exists(output_file_name[:-4]):
                if os.path.getsize(output_file_name[:-4]) == 0:
                  os.remove(output_file_name[:-4])
                  print(f"Corrupted or incomplete file {output_file_name} has been deleted.")
              else:
                print(f"Download completed successfully: {output_file_name}") 
          else:
            print("Plain text format not available for this book.")
      else:
          print("Formats data not available for this book in the API response.")
    else:
        print("Failed to retrieve the data. Check the book id or api endpoint.")

  def download_n_random_books(self, n_books:int) -> None:
    """
        This method downloads a specified number of random books from the Gutendex API.
        It calls the download_random_book method for each book to be downloaded.
        :param n_books: The number of random books to download.
        :return: None
    """
    if str(n_books).isnumeric():
      n_books = int(n_books)
      if n_books > 0:
        for _ in range(n_books):
          self.download_random_book()
  
  def get_metadata_random_book(self) -> dict:
    """
        This method retrieves metadata for a random book from the list of downloaded books.
        It selects a random book from the list and constructs its metadata.
        :return: A dictionary containing the title, path to the book, name of the article, and path to the article.
    """
    number_books = len(self.books)
    id = random.randint(0, number_books - 1)
    title = self.books[id][:-4]
    path_book = PATH.BOOKS.value + self.books[id]
    name_article = f"Cook_Article_{title}.md"
    path_article = PATH.ARTICLES.value + name_article

    return {
      "title": title,
      "path_book": path_book,
      "name_article": name_article,
      "path_article": path_article
    }

  def load_book(self, file_name:str) -> list:
    """
        This method loads a book from a file.
        :param file_name: The name of the file containing the book.
        :return: The content of the book as a string.
    """
    file_path = f"{self.output_path}{file_name}"
    with open(file_path, "r", encoding="utf-8") as file:
      book = file.read()
    return book
