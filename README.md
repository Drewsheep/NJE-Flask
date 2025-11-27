# 📖 Vendégkönyv - Flask dinamikus weboldal
Ennek a projektnek az a célja, hogy a felhasználók véleményt tudjanak írni egy adott cégről/vállalatról. Jelen esetben példaként az NJE-ről lehet írni. Jó ötletnek találtam, hogy a stílus is picit NJE-s legyen :)

## 🧩 Előkészítés
 - Létrehozni egy virtuális környezetet -> `python -m venv .venv`
 - Ezt a környezetet aktiváli kell (PowerShell-be) -> `.\.venv\Scripts\activate`
 - Majd telepíteni a Flasket -> `pip install flask`
 - Végül elindítani az alkalmazást -> `python app.py`

## 💡 Tulajdonságok
 - 👤 Login panel [Adminok részére] törlési, szerkesztési funkciókkal
 - 📊 Statisztika a moderált és az összes beküldött üzenetről + látogatásról
 - 🌟 1-5 csillagig való értékelés
 - 🕰️ Timestamp és egy egyedi hash megjelenítése a felhasználók neve mellett
 - 🛡️ "Admin által moderálva" jelző megjelenítése a név mellett
 - ↪️ Pagináció

## 👤 Hogyan tudok bejelentkezni?
Az alapértelmezett felhasználónév `admin`, az ehhez tartozó jelszó `admin123`.
 
 ### ℹ️ 2025/2026 - Haladó programozás
 - © 2025 Baranyai András | AEN3WU