from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import uvicorn
from grain_ppg import grain_ppg
from grain_gelatinization_table import grain_gelatinization_dict

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "grain_ppg": grain_ppg, "final_fermented_gravity": "1.000"})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    water_gallons: float = Form(...),
    grain_types: List[str] = Form(...),
    pounds: List[float] = Form(...),
    ounces: List[float] = Form(...),
    final_fermented_gravity: float = Form(...),
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

    max_fermented_abv = (max_specific_gravity - final_fermented_gravity) * 131.25
    typical_fermented_abv = (typical_specific_gravity - final_fermented_gravity) * 131.25

    max_specific_gravity = f"{max_specific_gravity:.3f}"
    typical_specific_gravity = f"{typical_specific_gravity:.3f}"
    max_fermented_abv = f"{max_fermented_abv:.2f}"
    typical_fermented_abv = f"{typical_fermented_abv:.2f}"
    final_fermented_gravity = f"{final_fermented_gravity:.3f}"

    grain_gelatinization_temps = {
        grain: grain_gelatinization_dict.get(grain, {"Fahrenheit": "N/A"})["Fahrenheit"]
        for grain in grain_types
    }

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
            "grain_gelatinization_temps": grain_gelatinization_temps,
            "submitted": True,
            "grain_types": grain_types,
            "pounds": pounds,
            "ounces": ounces,
            "final_fermented_gravity": final_fermented_gravity
        }
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
