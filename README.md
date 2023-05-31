# AutoFashion - Automated Fashion Detection and Recommendation

This is Hyunjae Chung and Michael Sun's senior research lab project for Computer Systems Lab 2022-2023 under Dr. Yilmaz Period 4. This app utilizes YOLOv5m convolutional neural network models in the backend and is combined with a user-friendly Flask frontend. The code files available in the main folder are a part of the full project, and files under the "Preliminary Code" folder are snippets/examples of code we wrote prior to/during the process of creating AutoFashion, but are not a part of the final product itself.

## Prerequisites

Prior to beginning the program, make sure that these are installed:

- Python 3.x
- pip (Python Package Installer)
- venv (Python3-venv)

## Getting Started

### 1. Clone the Repository

Firstly, clone the repository to your local machine using the following command:

```bash
git clone <repository_url>
```

### 2. Create and Activate a Virtual Environment
Navigate into the project directory and create a virtual environment using the venv module:

```bash
cd <project_directory>
python3 -m venv venv
```

and then activate the virtual environment (Windows):

```bash
venv\Scripts\activate
```

### 3. Install Dependencies
Install the necessary dependencies for the project using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application:
Now you're ready to run the Flask application. Set the FLASK_APP environment variable and run the application:

```bash
set FLASK_APP=app
flask run
```

### 5. Open the Application on Browser

The website will be hosted on '**http://127.0.0.1:5000/**' or '**localhost**'. Open either of the links on browser, and it should be there.
