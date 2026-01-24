# UI Playground Website – Python Flask

This repository contains a **UI Testing Playground web application** built with **Python and Flask**, designed specifically to support **manual and automated UI testing practice**.

The application is inspired by *the-internet.herokuapp.com* and provides a collection of interactive pages that simulate **real-world UI behaviors** commonly tested with tools like **Selenium WebDriver**.

**Live Application:** https://practice-login-page-for-test-automation.onrender.com/

**Purpose of the Project**
The goal of this project is to serve as a controlled testing environment for QA engineers and testers to practice:

- UI automation with Selenium
- Manual test case design
- Validation of edge cases and negative scenarios
- Handling dynamic and asynchronous UI elements

Each page focuses on a specific automation challenge and is intentionally built to be **test-friendly**, using stable selectors and predictable behaviors.

---

## Tech Stack

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

---

## Available Test Pages

The application currently includes **10 interactive pages**, each targeting a common UI testing scenario:

### Login Page 🔐
- Valid and invalid login attempts
- Required field validation
- Case sensitivity and whitespace handling
- Redirect protection

### Form Validation 📝
- Required fields
- Email and phone format validation
- Password rules and confirmation checks
- Boundary and edge cases

### Dynamic Loading ⏳
- Asynchronous content loading
- Loading indicators
- Delayed UI updates

### Alerts & Modals 🚨
- JavaScript alerts, confirms, and prompts
- Accept and dismiss actions
- Custom HTML modal behavior
- Clicking outside modals

### Checkboxes & Radio Buttons ☑️
- Single and multiple checkbox selection
- Radio button exclusivity
- Preview and validation messages

### Dropdowns 🔽
- Default selections
- Option changes
- Dependent dropdown behavior

### Iframe Interaction 🧩
- Switching into iframes
- Text input inside iframe elements
- Returning to main document context

### Hover & Mouse Actions 🖱
- Hover-triggered content
- Mouse interaction validation

### Sortable & Searchable Tables 📊
- Column sorting (Name, Email, Role, Age)
- Search and filtering functionality
- Dynamic result updates

### File Upload 📁
- Valid and invalid file type handling
- File name display
- Submission without file validation

---

## Test-Friendly Design

This application was intentionally built with automation in mind:

- Stable `data-test` attributes for reliable element selection
- Clear success and error messages
- Predictable UI behavior for consistent test results

It is actively used as the target application for a **separate Selenium + Pytest automation project**.

---

## Application Cold Start Behavior ⏱

The app is hosted on **Render** and may enter a sleep state after periods of inactivity.  
When this happens, the first request can take **30–40 seconds** while the server wakes up.

This is expected hosting behavior and **not a performance issue**.

---

## Running the Application Locally

```bash
pip install -r requirements.txt
python app.py

**Ruben Jimenez**
QA Automation Engineer
Python • Flask • HTML & CSS
