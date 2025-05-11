#!/usr/bin/env python
# src/ai_recipes/main.py
from config.config import PATH
from manage_books import Downloader_books
from crew import CookingCrew

def run():
    # Download a random book and show the list of books
    db = Downloader_books(PATH.BOOKS.value)
    while len(db.books) < 10:
        db.download_random_book()
    
    # Get metadata for the random book
    metadata = db.get_metadata_random_book()

    inputs = {
    'title': metadata['title'],
    }
    crew = CookingCrew()
    crew.initializer(metadata)
    crew.crew().kickoff(inputs=inputs)

if __name__ == '__main__':
    run()
