import tkinter as tk
from tkinter import Toplevel, StringVar, IntVar, Checkbutton, Entry, Label, Button, Listbox, Scrollbar, Text
import json

def main():
    bookInformation = {}

    def addBook():
        # Create a new top-level window
        bookInfoWindow = Toplevel(root)
        bookInfoWindow.title("Add Book")
        bookInfoWindow.geometry("250x380")
        bookInfoWindow.grab_set()

        # Widgets for book name
        Label(bookInfoWindow, text="Book Name:").pack(padx=5, pady=5)
        bookNameEntry = Entry(bookInfoWindow)
        bookNameEntry.pack(padx=5, pady=5)

        # Widgets for book author
        Label(bookInfoWindow, text="Book Author:").pack(padx=5, pady=5)
        bookAuthorEntry = Entry(bookInfoWindow)
        bookAuthorEntry.pack(padx=5, pady=5)

        # Widgets for book completion status
        completedVar = IntVar()
        completedCheck = Checkbutton(bookInfoWindow, text="Completed", variable=completedVar)
        completedCheck.pack(padx=5, pady=5)

        # Widgets for book rating
        ratingVar = StringVar()
        ratingEntry = Entry(bookInfoWindow, textvariable=ratingVar)
        ratingEntry.pack(padx=5, pady=5)
        ratingEntry.configure(state='disabled')

        # Label for Notes
        Label(bookInfoWindow, text="Notes:").pack(padx=5, pady=5, anchor='w')

        # Text widget for Notes
        bookNoteText = Text(bookInfoWindow, height=6, width=30)
        bookNoteText.pack(padx=5, pady=5)

        def toggleRating(*args):
            if completedVar.get() == 1:
                ratingEntry.configure(state='normal')
            else:
                ratingEntry.configure(state='disabled')
                ratingVar.set("")


        completedVar.trace("w", toggleRating)

        def saveBook():
            # Gather the book information into a dictionary
            book_info = {
                'Name': bookNameEntry.get(),
                'Author': bookAuthorEntry.get(),
                'Completed': completedVar.get(),
                'Rating': ratingVar.get() if completedVar.get() else 'N/A',
                'Notes': bookNoteText.get("1.0", tk.END).strip()  # Using strip() to remove the last newline
            }

            # Update the in-memory book information dictionary
            bookInformation[bookNameEntry.get()] = book_info

            # Add the new book to the Listbox
            books_listbox.insert(tk.END, bookNameEntry.get())

            # Write the book information to a JSON file
            with open('books.json', 'w') as file:
                json.dump(bookInformation, file, indent=4)

            # Close the add book window
            bookInfoWindow.destroy()

        # Save Button with function to pass data
        saveButton = Button(bookInfoWindow, text="Save", command=saveBook)
        saveButton.pack(padx=5, pady=5)
    
    def loadBooks():
        try:
            with open('books.json', 'r') as file:
                bookInformation = json.load(file)  # Load book data from JSON file into the dictionary
        except FileNotFoundError:
            bookInformation = {}  # If no file exists, start with an empty dictionary
        except json.JSONDecodeError:
            print("Error: The JSON file is corrupt or empty. Starting with an empty data set.")
            bookInformation = {}
        return bookInformation


    def displayBookDetails(event):
        # Get selected book name
        selected_index = books_listbox.curselection()
        if selected_index:
            selected_book = books_listbox.get(selected_index)
            book_details = bookInformation[selected_book]
            # Clear current content
            for widget in bookDetail.winfo_children():
                widget.destroy()
            # Display book details
            Label(bookDetail, text=f"Name: {book_details['Name']}").pack()
            Label(bookDetail, text=f"Author: {book_details['Author']}").pack()
            Label(bookDetail, text=f"Completed: {'Yes' if book_details['Completed'] else 'No'}").pack()
            Label(bookDetail, text=f"Rating: {book_details['Rating']}").pack()

    def updateShownTitles(searchBarContent):
        books_listbox.delete(0, tk.END)
        if searchBarContent != "" and searchBarContent != "<Completed>" and searchBarContent != "<In Progress>":
            searchLength = len(searchBarContent)
            for book_name in sorted(bookInformation.keys()):
                if searchBarContent == book_name[:searchLength]:
                    books_listbox.insert(tk.END, book_name)
        elif searchBarContent == "<Completed>":
            for book_name in bookInformation.keys():
                if bookInformation[book_name]['Completed'] != 'N/A':
                    books_listbox.insert(tk.END, book_name)
        elif searchBarContent == "<In Progress>":
            for book_name in bookInformation.keys():
                if bookInformation[book_name]['Completed'] == 'N/A':
                    books_listbox.insert(tk.END, book_name)
        else:
            for book_name in bookInformation.keys():
                books_listbox.insert(tk.END, book_name)

    bookInformation = loadBooks()

    # Create Our Window
    root = tk.Tk()
    root.geometry("800x600")
    root.maxsize(800, 600)
    root.minsize(800, 600)

    # Create Content Frame
    contentFrame = tk.Frame(root, bg='grey')
    contentFrame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create Search Frame at the top
    searchFrame = tk.Frame(contentFrame, bg='lightgray')
    searchFrame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    # Search Entry and Button in the Search Frame
    searchEntry = tk.Entry(searchFrame, width=50)
    searchEntry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
    searchEntry.bind('<KeyRelease>', lambda event: updateShownTitles(searchEntry.get()))

    # Configure grid rows and columns within contentFrame
    contentFrame.rowconfigure(1, weight=1)
    contentFrame.columnconfigure(0, weight=2)
    contentFrame.columnconfigure(1, weight=3)

    # Create BookList Frame
    bookList = tk.Frame(contentFrame, bg="white")
    bookList.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    # Add Listbox with Scrollbar
    scrollbar = Scrollbar(bookList)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    books_listbox = Listbox(bookList, yscrollcommand=scrollbar.set)
    books_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    books_listbox.bind('<<ListboxSelect>>', displayBookDetails)
    scrollbar.config(command=books_listbox.yview)

    # Create BookDetail Frame
    bookDetail = tk.Frame(contentFrame, bg='white')
    bookDetail.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

    # Add Book Button in the Bottom Frame
    addBookButton = tk.Button(contentFrame, text="Add Book", command=addBook)
    addBookButton.grid(row=2, columnspan=2, sticky='w', padx=5, pady=5)

    # Run Everything
    updateShownTitles("")
    root.mainloop()

if __name__ == "__main__":
    main()
