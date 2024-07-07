from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import uvicorn
from grain_ppg import grain_ppg
from grain_gelatinization_table import grain_gelatinization_dict

# Initialize the FastAPI app
app = FastAPI()

# Mount the static files directory for serving static content
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """
    Display the form for entering mash details.

    Args:
        request (Request): The request object containing the details of the HTTP request.

    Returns:
        HTMLResponse: The rendered HTML form for the user to input mash details.
    """
    return templates.TemplateResponse("index.html", {"request": request, "grain_ppg": grain_ppg})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    water_gallons: float = Form(...),
    grain_types: List[str] = Form(...),
    pounds: List[float] = Form(...),
    ounces: List[float] = Form(...),
    final_fermented_gravity: float = Form(default=1.000)
):
    """
    Handle form submission, perform specific gravity and ABV calculations, and display the results.

    Args:
        request (Request): The request object containing the details of the HTTP request.
        water_gallons (float): The total volume of water used in gallons.
        grain_types (List[str]): List of selected grain types.
        pounds (List[float]): List of quantities of grains in pounds.
        ounces (List[float]): List of quantities of grains in ounces.
        final_fermented_gravity (float): The final specific gravity after fermentation.

    Returns:
        HTMLResponse: The rendered HTML response displaying the calculation results.
    """
    # Convert grain quantities to pounds
    grain_quantities = {
        grain_types[i]: pounds[i] + (ounces[i] / 16.0) for i in range(len(grain_types))
    }

    # Calculate maximum specific gravity
    max_specific_gravity = sum(
        (grain_ppg[grain]["Max PPG"] * qty) / water_gallons for grain, qty in grain_quantities.items() if grain_ppg[grain]["Max PPG"]
    ) / 1000 + 1

    # Calculate typical specific gravity
    typical_specific_gravity = sum(
        (grain_ppg[grain]["Typical PPG"] * qty) / water_gallons for grain, qty in grain_quantities.items() if grain_ppg[grain]["Typical PPG"]
    ) / 1000 + 1

    # Calculate maximum fermented alcohol by volume (ABV)
    max_fermented_abv = (max_specific_gravity - final_fermented_gravity) * 131.25

    # Calculate typical fermented alcohol by volume (ABV)
    typical_fermented_abv = (typical_specific_gravity - final_fermented_gravity) * 131.25

    # Format the results to three decimal places for specific gravity and two decimal places for ABV
    max_specific_gravity = f"{max_specific_gravity:.3f}"
    typical_specific_gravity = f"{typical_specific_gravity:.3f}"
    max_fermented_abv = f"{max_fermented_abv:.2f}"
    typical_fermented_abv = f"{typical_fermented_abv:.2f}"

    # Get gelatinization temperatures for the selected grains
    grain_gelatinization_temps = {
        grain: grain_gelatinization_dict.get(grain, {"Fahrenheit": "N/A"})["Fahrenheit"]
        for grain in grain_types
    }

    # Render the response template with the calculated results
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "water_gallons": water_gallons,
            "grain_quantities": grain_quantities,
            "max_specific_gravity": max_specific_gravity,
            "typical_specific_gravity": typical_specific_gravity,
            "max_fermented_abv": max_fermented_abv,
            "typical_fermented_abv": typical_fermented_abv,
            "grain_ppg": grain_ppg,
            "grain_gelatinization_temps": grain_gelatinization_temps
        }
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Serve the favicon for the application.

    Returns:
        FileResponse: The response object for serving the favicon.
    """
    return FileResponse("static/favicon.ico")

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
