from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Dictionary mapping grain types to their Max PPG and Typical PPG values
grain_ppg = {
    "2 Row Barley": {"Max PPG": 37, "Typical PPG": 31},
    "6 Row Barley": {"Max PPG": 35, "Typical PPG": 30},
    "Biscuit/Victory Malt": {"Max PPG": 35, "Typical PPG": 30},
    "Vienna Malt": {"Max PPG": 35, "Typical PPG": 30},
    "Munich Malt": {"Max PPG": 35, "Typical PPG": 30},
    "Brown Malt": {"Max PPG": 32, "Typical PPG": 28},
    "Dextrin Malt": {"Max PPG": 32, "Typical PPG": 28},
    "Light Crystal (10 - 15L)": {"Max PPG": 35, "Typical PPG": 30},
    "Pale Crystal (25 - 40L)": {"Max PPG": 34, "Typical PPG": 29},
    "Medium Crystal (60 - 75L)": {"Max PPG": 34, "Typical PPG": 29},
    "Dark Crystal (120L)": {"Max PPG": 33, "Typical PPG": 28},
    "Special B": {"Max PPG": 31, "Typical PPG": 27},
    "Chocolate Malt": {"Max PPG": 28, "Typical PPG": 24},
    "Roast Barley": {"Max PPG": 25, "Typical PPG": 22},
    "Black Patent Malt": {"Max PPG": 25, "Typical PPG": 22},
    "Wheat Malt": {"Max PPG": 37, "Typical PPG": 31},
    "Rye Malt": {"Max PPG": 29, "Typical PPG": 25},
    "Cracked Corn": {"Max PPG": 30, "Typical PPG": None},
    "Oatmeal (Flaked)": {"Max PPG": 32, "Typical PPG": 28},
    "Corn (Flaked)": {"Max PPG": 39, "Typical PPG": 33},
    "Barley (Flaked)": {"Max PPG": 32, "Typical PPG": 28},
    "Wheat (Flaked)": {"Max PPG": 36, "Typical PPG": 30},
    "Rice (Flaked)": {"Max PPG": 38, "Typical PPG": 32},
    "Malto-Dextrin Powder": {"Max PPG": 40, "Typical PPG": 40},
    "Sugar (Corn, Cane)": {"Max PPG": 46, "Typical PPG": 46}
}

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
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
    grain_quantities = {
        grain_types[i]: pounds[i] + (ounces[i] / 16.0) for i in range(len(grain_types))
    }

    max_specific_gravity = sum(
        (grain_ppg[grain]["Max PPG"] * qty) / water_gallons for grain, qty in grain_quantities.items() if grain_ppg[grain]["Max PPG"]
    ) / 1000 + 1

    typical_specific_gravity = sum(
        (grain_ppg[grain]["Typical PPG"] * qty) / water_gallons for grain, qty in grain_quantities.items() if grain_ppg[grain]["Typical PPG"]
    ) / 1000 + 1

    # Calculate fermented ABV values
    max_fermented_abv = (max_specific_gravity - final_fermented_gravity) * 131.25
    typical_fermented_abv = (typical_specific_gravity - final_fermented_gravity) * 131.25

    # Format specific gravity and ABV values to 3 significant digits
    max_specific_gravity = f"{max_specific_gravity:.3f}"
    typical_specific_gravity = f"{typical_specific_gravity:.3f}"
    max_fermented_abv = f"{max_fermented_abv:.2f}"
    typical_fermented_abv = f"{typical_fermented_abv:.2f}"

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
            "grain_ppg": grain_ppg
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)