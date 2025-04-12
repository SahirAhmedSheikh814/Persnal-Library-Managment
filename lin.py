import json
import os
import streamlit as st

# File to store book data
LIBRARY_FILE = "library.json"

# Load library from file (if exists)
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Display book details
def print_book(book):
    st.markdown(f"**📖 Title:** {book['title']}")
    st.markdown(f"**✍ Author:** {book['author']}")
    st.markdown(f"**📅 Year:** {book['year']}")
    st.markdown(f"**📂 Genre:** {book['genre']}")
    st.markdown(f"**📖 Read:** {'✅ Yes' if book['read'] else '❌ No'}")

# App starts here
st.title("📚 Personal Library Manager")

# Load session state for library
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# Menu options
menu = st.sidebar.selectbox("Choose an option", [
    "Add a Book",
    "Remove a Book",
    "Search for a Book",
    "List All Books",
    "Mark Book as Read/Unread",
    "Show Statistics"
])

library = st.session_state.library

# Add Book
if menu == "Add a Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Enter the book title")
    author = st.text_input("Enter the author")
    year = st.text_input("Enter the publication year")
    genre = st.text_input("Enter the book genre")
    read = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        if title and author and year and genre:
            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            library.append(book)
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.error("⚠ Please fill all fields.")

# Remove Book
elif menu == "Remove a Book":
    st.header("❌ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        found = False
        for book in library:
            if book["title"].lower() == title.lower():
                library.remove(book)
                save_library(library)
                st.success(f"❌ '{title}' removed successfully!")
                found = True
                break
        if not found:
            st.warning("⚠ Book not found!")

# Search Book
elif menu == "Search for a Book":
    st.header("🔍 Search for a Book")
    title = st.text_input("Enter the title to search for")
    if st.button("Search"):
        found = False
        for book in library:
            if book["title"].lower() == title.lower():
                st.success("📖 Book Found:")
                print_book(book)
                found = True
                break
        if not found:
            st.warning("⚠ Book not found!")

# List All Books
elif menu == "List All Books":
    st.header("📚 Your Book Collection")
    if not library:
        st.info("Your library is empty.")
    else:
        for idx, book in enumerate(library, 1):
            st.markdown(f"**{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']}**")
            st.markdown(f"{'✅ Read' if book['read'] else '❌ Not Read'}")
            st.markdown("---")

# Update Read Status
elif menu == "Mark Book as Read/Unread":
    st.header("🔁 Update Read Status")
    title = st.text_input("Enter the title of the book to update")
    if st.button("Toggle Read Status"):
        found = False
        for book in library:
            if book["title"].lower() == title.lower():
                book["read"] = not book["read"]
                save_library(library)
                st.success(f"✅ '{title}' marked as {'Read' if book['read'] else 'Not Read'}")
                found = True
                break
        if not found:
            st.warning("⚠ Book not found!")

# Show Statistics
elif menu == "Show Statistics":
    st.header("📊 Library Statistics")
    total = len(library)
    read = sum(1 for b in library if b["read"])
    unread = total - read

    st.write(f"📚 Total Books: **{total}**")
    st.write(f"✅ Books Read: **{read}**")
    st.write(f"❌ Books Unread: **{unread}**")
