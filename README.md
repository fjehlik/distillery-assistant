
# Distillation App for Spirits

## Overview

This application is a FastAPI-based web application designed to assist in the distillation process for making spirits. It allows users to input mash details such as water volume and grain types and quantities. The app calculates specific gravity, alcohol by volume (ABV), and provides gelatinization temperatures for the selected grains.

## Project Structure

```
distillation_app/
├── main.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

### Files and Directories

- **main.py**: The main application file that sets up the FastAPI app and handles requests.
- **templates/**: Contains the HTML template files.
- **static/**: Contains static files such as CSS.

## Installation and Setup

### Prerequisites

Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).

### Dependencies

Install the required dependencies using pip:

```bash
pip install fastapi uvicorn jinja2
```

### Running the Application

1. **Navigate to the project directory**:
   
   ```bash
   cd path/to/distillation_app
   ```

2. **Start the FastAPI application**:
   
   ```bash
   uvicorn main:app --reload
   ```

3. **Open your web browser** and go to [http://localhost:8000](http://localhost:8000).

## Usage

1. **Home Page**: The main form for entering mash details will be displayed.
2. **Enter Mash Details**:
   - **Water Gallons**: Input the total volume of water used (in gallons).
   - **Grain Types**: Select the types of grains used.
   - **Pounds**: Input the quantity of each grain in pounds.
   - **Ounces**: Input the quantity of each grain in ounces.
   - **Final Fermented Gravity**: Input the final specific gravity after fermentation (default is 1.000).

3. **Submit the Form**: Click the submit button to perform calculations.
4. **Results**: The app will display the calculated values:
   - Maximum and typical specific gravity
   - Maximum and typical ABV
   - Gelatinization temperatures for the selected grains

## Code Explanation

### main.py

- **Imports**:
  - FastAPI: Web framework for building APIs.
  - Jinja2Templates: Template engine for rendering HTML.
  - uvicorn: ASGI server for serving the FastAPI app.

- **App Initialization**:
  ```python
  app = FastAPI()
  ```

- **Static Files and Templates**:
  ```python
  app.mount("/static", StaticFiles(directory="static"), name="static")
  templates = Jinja2Templates(directory="templates")
  ```

- **Routes**:
  - **GET /**: Displays the form for entering mash details.
  - **POST /submit**: Handles form submission and performs calculations.
  - **GET /favicon.ico**: Serves the favicon.

### HTML Template (index.html)

- The template should contain a form for users to input mash details and a section to display the results.

### CSS (style.css)

- Contains styles for the application.

## Contribution

Feel free to contribute by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
