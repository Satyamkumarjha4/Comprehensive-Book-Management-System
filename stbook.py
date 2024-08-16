import streamlit as st
import sqlite3

# Function to connect to the database and fetch book names
def fetch_book_names():
    book_names = ["---Select Book---"]
    try:
        Books_file = sqlite3.connect('C:/Users/satya/OneDrive/Desktop/GUI/books.db')
        cursor_books = Books_file.cursor()
        cursor_books.execute('SELECT Books_Name FROM Books;')
        record = cursor_books.fetchone()
        while record:
            book_names.append(record[0])
            record = cursor_books.fetchone()
        Books_file.close()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
    return book_names

# Function to fetch the price of the selected book
def fetch_book_price(book_title):
    if book_title == "---Select Book---":
        return 0.0
    try:
        Books_file = sqlite3.connect('C:/Users/satya/OneDrive/Desktop/GUI/books.db')
        cursor_books = Books_file.cursor()
        cursor_books.execute('SELECT Books_Price FROM Books WHERE Books_Name = ?', (book_title,))
        record = cursor_books.fetchone()
        Books_file.close()
        if record:
            return record[0]
        else:
            return 0.0
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return 0.0
    except Exception as e:
        st.error(f"Error: {e}")
        return 0.0

# Function to calculate the total cost
def calculate_total_cost(book_price, quantity):
    try:
        quantity = int(quantity)
        total_cost = quantity * book_price
        return total_cost
    except ValueError:
        st.error("Invalid Quantity")
        return None

# Streamlit UI setup
st.title("Book Price & Cost Calculator")

# Dropdown to select book name
book_title = st.selectbox("Select Book Title", fetch_book_names())

# Button to get the price of the selected book
if st.button("Get Price"):
    book_price = fetch_book_price(book_title)
    st.write(f"Book Price: {book_price}")

# Input field for quantity
quantity = st.number_input("Enter Quantity")

# Button to calculate the total cost
if st.button("Get Total Cost"):
    book_price = fetch_book_price(book_title)
    total_cost = calculate_total_cost(book_price, quantity)
    if total_cost is not None:
        st.write(f"Total Cost: {total_cost}")
