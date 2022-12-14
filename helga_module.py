import json


def book_commend(category, subcategory):
    result = []
    subcateg = []
    subcategories = []
    with open('books.json') as f:
        books = json.load(f)
        categories = list(books.keys())

        for item in categories:
            subcateg.append(list(books[item].keys()))
        for e in subcateg:
            for el in e:
                subcategories.append(el)

        if category in categories and subcategory in subcategories:
            recommend = books[category][subcategory]
            for i in recommend:
                title, auther, url = i.split(',')[0], i.split(',')[1], i.split(',')[2]
                result.append(f'Title: {title}\n'
                              f'Author: {auther}\n'
                              f'Book summary & order: {url}\n')
            return '\n'.join(result)

        else:
            return 'No books are recommended\nCheck input parameters and try again'


if __name__ == '__main__':
    print(book_commend(category='non-fiction', subcategory='history'))
    # print('=' * 100)
    # print(book_commend(category='fiction', subcategory='action & adventure'))
