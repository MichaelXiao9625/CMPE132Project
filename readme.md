# Spartan Library
> The online platform where users can create an account, and explore the books that are available in the library.

## Table of Contents
* [Introduction](#introduction)
* [Technologies and Libraries Used](#technologies-and-libraries-used)
* [Features](#features)
* [Functional Requirements](#functional-requirements)
* [Nonfunctional Requirements](#nonfunctional-requirements)
* [Setup](#setup)
* [Usage](#usage)
* [Author](#author)


## Introduction
- This application is a library platform for SJSU students to explore and find their favorite books.
- We wrote this application in hopes to make SJSU more connected through this app exclusively for students.


## Technologies and Libraries Used
- IDE such as Ubuntu(WSL) or VSCode
- Python (3.10 or above)
- Flask
- SQLAlchemy
- flask-wtf
- flask-login
- flask-sqlalchemy

## Features
- Custom account creation
- Easy to reach other pages
- Search for your favorite books
- Check out and return books with ease
- Purchase from the shop's inventory

## Functionality
- Login 
- Logout 
- Create new account 
- Delete account 
- User home page 
- Search for books
- Explore shops
- View announcements
- User profiles 
- Manage users, books, shops, and databse (Admin and Librarian only)
- Help page

## Setup
Start by cloning `myProject`:

```bash
git clone https://github.com/MichaelXiao9625/CMPE132Project.git
```

After cloning the project and ensuring that all the required libraries are installed, run the following command to start the server:

```bash
python run.py
```

## Usage

🚧 under construction 🚧

The first step to using our platform is to create an account, without an account the user cannot login to access anything beyond the base page. The password and e-mail must satisify certain guidelines in order for the account creation to be successful. After creating an account, the user's data will be stored into the database. The user then goes to login page to enter their login information, if it’s within the database the website will reroute them to the home page. From the home page user will be able to access all sorts of information such as announcements, book inventory, and the library shop. 

The user can choose to update their bio and other user account information on the profile page, where the bio must adhere to certain guidelines. The user can choose to delete their account on their profile page by clicking the Delete Account option, followed by entering their password to ensure their removal from the database. Finally, if the user decides to logout, the button will be on the left column of the website, which would direct them back to the base page of our website.

## Author
- Michael Xiao (@MichaelXiao9625)


