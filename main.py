from customtkinter import *
import os

from translations import translations
from conversions import DISTANCE_FACTORS, to_l_per_100km
from utils import resize_icon

def set_language(lang):
    current_lang.set(lang)
    app.title(translations[lang]["title"])
    appNameLabel.configure(text=translations[lang]["title"])
    saveBtn.configure(text=translations[lang]["save"])
    distanceLabel.configure(text=translations[lang]["distance"])
    consumptionLabel.configure(text=translations[lang]["consumption"])
    currencyLabel.configure(text=translations[lang]["price"])
    calcResult()

def calcResult(event=None):
    try:
        distance = float(distanceEntry.get())
        consumption = float(consumptionEntry.get())
        literPrice = float(resultEntry.get())

        distance_km = distance * DISTANCE_FACTORS[currentDistanceUnit.get()]
        consumption_l100km = to_l_per_100km(consumption, currentConsumptionMetric.get())

        result = (distance_km / 100) * consumption_l100km * literPrice

        resultLabel.configure(text=f"{result:.2f}{currentCurrency.get()}")
        return result
    except ValueError:
        resultLabel.configure(text="---")
        return None

def saveResult():
    result = calcResult()
    if result is None:
        log_label.configure(text=translations[current_lang.get()]["saveNothing"])
        return

    log_entry = (
        f"{translations[current_lang.get()]['distance']}: {distanceEntry.get()} {currentDistanceUnit.get()}, "
        f"{translations[current_lang.get()]['consumption']}: {consumptionEntry.get()} {currentConsumptionMetric.get()}, "
        f"{translations[current_lang.get()]['price']}: {resultEntry.get()} {currentCurrency.get()}, "
        f"{translations[current_lang.get()]['result']}: {result:.2f}{currentCurrency.get()}\n"
    )
    file_path = "MySavedConsumptions.txt"
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        log_label.configure(text=translations[current_lang.get()]["saveError"] + f"{e}")
    else:
        log_label.configure(text=translations[current_lang.get()]["saveSuccess"] + f"{file_path}")

app = CTk()
app.resizable(False, False)

current_lang = StringVar(value="pt")
currentDistanceUnit = StringVar(value="km")
currentConsumptionMetric = StringVar(value="L/100km")
currentCurrency = StringVar(value="€")

app.title(translations[current_lang.get()]["title"])

frame = CTkFrame(master=app)
frame.pack(fill="both", expand=True)

distanceLabel = CTkLabel(frame, text=translations[current_lang.get()]["distance"], font=("Segoe UI", 18, "bold"))
distanceLabel.pack(pady=(10, 0))
distanceLabelMenu = CTkOptionMenu(
    frame, height=20, values=["km", "mi"], variable=currentDistanceUnit, fg_color="#333333",
    command=lambda _: calcResult(),
)
distanceLabelMenu.pack(pady=(5, 0))
distanceEntry = CTkEntry(master=frame)
distanceEntry.pack(pady=(3, 10), padx=20)
distanceEntry.bind("<KeyRelease>", calcResult)

consumptionLabel = CTkLabel(frame, text=translations[current_lang.get()]["consumption"], font=("Segoe UI", 18, "bold"))
consumptionLabel.pack(pady=(10, 0))
consumption_label_menu = CTkOptionMenu(
    frame, height=20, values=["L/100km", "km/L", "mpg"], variable=currentConsumptionMetric, fg_color="#333333",
    command=lambda _: calcResult(),
)
consumption_label_menu.pack(pady=(5, 0))
consumptionEntry = CTkEntry(master=frame)
consumptionEntry.pack(pady=(3, 10), padx=20)
consumptionEntry.bind("<KeyRelease>", calcResult)

currencyLabel = CTkLabel(frame, text=translations[current_lang.get()]["price"], font=("Segoe UI", 18, "bold"))
currencyLabel.pack(pady=(10, 0))
currency_label_menu = CTkOptionMenu(frame, height=20, values=["€", "$", "£"], variable=currentCurrency, fg_color="#333333",)
currency_label_menu.pack(pady=(5, 0))
resultEntry = CTkEntry(master=frame)
resultEntry.pack(pady=(3, 10), padx=20)
resultEntry.bind("<KeyRelease>", calcResult)

resultLabel = CTkLabel(master=frame, text="---", font=("Arial", 20))
resultLabel.pack(pady=5)

log_label = CTkLabel(master=frame, text="", font=("Arial", 11), justify="center")
log_label.pack(fill="both", padx=10, pady=5)

saveBtn = CTkButton(master=frame, text=translations[current_lang.get()]["save"], command=saveResult)
saveBtn.pack(pady=5)

footer = CTkFrame(master=app, fg_color="#202020")
footer.pack(side="bottom", fill="x")

appNameLabel = CTkLabel(master=footer, text=translations[current_lang.get()]["title"], text_color="#999999", font=("Arial", 12))
appNameLabel.pack(side="left", pady=2, padx=(10, 0))

footer_label = CTkLabel(master=footer, text="pjgoliveira21", text_color="#999999", font=("Arial", 12), cursor="hand2")
footer_label.pack(side="left", pady=2, padx=10)
footer_label.bind("<Button-1>")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
flag_pt_path = os.path.join(BASE_DIR, "assets", "pt.png")
flag_en_path = os.path.join(BASE_DIR, "assets", "en.png")
flag_pt_img = resize_icon(flag_pt_path, (24, 16))
flag_en_img = resize_icon(flag_en_path, (24, 16))

lang_btn_pt = CTkButton(master=footer, image=flag_pt_img, text="", width=30, fg_color="transparent",hover_color="#333333", command=lambda: set_language("pt"))
lang_btn_pt.pack(side="right", padx=5, pady=2)
lang_btn_en = CTkButton(master=footer, image=flag_en_img, text="", width=30, fg_color="transparent",hover_color="#333333", command=lambda: set_language("en"))
lang_btn_en.pack(side="right", padx=5, pady=2)

lang_btn_pt.image = flag_pt_img
lang_btn_en.image = flag_en_img

app.update()
app.minsize(app.winfo_width(), app.winfo_height())
set_language(current_lang.get())

app.mainloop()
