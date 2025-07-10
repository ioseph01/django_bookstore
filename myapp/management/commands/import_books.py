# Create this file: management/commands/import_books.py
# Directory structure: your_app/management/commands/import_books.py

import json
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Author, Publisher, Book, Subject  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Import books from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {json_file} not found'))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Invalid JSON: {e}'))
            return

        # Use transaction to ensure data integrity
        with transaction.atomic():
            for item in data:
                try:
                    # Create or get publisher
                    publisher, created = Publisher.objects.get_or_create(
                        name=item['publisher']
                    )
                    if created:
                        self.stdout.write(f'Created publisher: {publisher.name}')

                    # Create or get authors
                    authors = []
                    for author_data in item['authors']:
                        author, created = Author.objects.get_or_create(
                            first_name=author_data['first_name'],
                            last_name=author_data['last_name']
                        )
                        if created:
                            self.stdout.write(f'Created author: {author}')
                        authors.append(author)

                    # Create book
                    subjects = []
                    for subject_name in item['subjects']:
                        subject, created = Subject.objects.get_or_create(
                            name=subject_name['name']
                        )
                        if created:
                            self.stdout.write(f'Created subject: {subject}')
                        subjects.append(subject)


                    book, created = Book.objects.get_or_create(
                        title=item['title'],
                        defaults={
                            'page_count': item['page_count'],
                            'publisher': publisher,
                            'summary': item['summary'],
                            'downloads': item['downloads'],
                            'cost': item['cost'],
                            'cover_image': item['book_cover']
                        }
                    )
                    
                    if created:
                        # Add authors to the book (many-to-many relationship)
                        book.authors.set(authors)
                        book.subjects.set(subjects)

                        self.stdout.write(f'Created book: {book.title}')
                    else:
                        self.stdout.write(f'Book already exists: {book.title}')

                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Missing key in JSON: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing item: {e}'))

        self.stdout.write(self.style.SUCCESS('Data import completed successfully'))


# Example JSON structure (books.json):
"""
[
    {
        "title": "The Great Gatsby",
        "page_count": 180,
        "publisher": "Scribner",
        "authors": [
            {
                "first_name": "F. Scott",
                "last_name": "Fitzgerald"
            }
        ]
    },
    {
        "title": "Good Omens",
        "page_count": 416,
        "publisher": "Gollancz",
        "authors": [
            {
                "first_name": "Terry",
                "last_name": "Pratchett"
            },
            {
                "first_name": "Neil",
                "last_name": "Gaiman"
            }
        ]
    }
]
"""