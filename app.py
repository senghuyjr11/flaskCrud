from flask import Flask, render_template, request, redirect, url_for
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database and tables

@app.route('/')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        description = request.form['description']

        new_book = Book(title=title, author=author, year=year, description=description)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('book_list'))

    return render_template('book_form.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        # Update book details with form data
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = request.form['year']
        book.description = request.form['description']

        # Save changes to the database
        db.session.commit()
        return redirect(url_for('book_list'))

    # Render the form with the current book details
    return render_template('book_form.html', book=book)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book_list'))
