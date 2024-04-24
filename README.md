# Care Companion
Webová aplikace nápomocná v domově důchodců  
Ročníkový projekt 2023/2024 - Sabina Javůrková, Oliver Hurt, David Mikolášek  
## Instalace a spuštění
1. Clone repozitáře
    ```
    git clone https://github.com/gyarab/2023-3e-CareCompanion.git
    ```
2. Přesun do složky projektu
    ```
    cd 2023-3e-CareCompanion
    ```
3. Vytvoření virtualního prostředí (venv)
    ```
    python -m venv venv
    ```
4. Aktivace venv
    ```
   source ./venv/Scripts/activate
    ```
5. Instalace potřebných balíčků
    ```
   pip install -r requirements.txt
    ```
6. Zapnutí serveru
    ```
    python manage.py runserver
    ```
Server s naší webovou aplikací běží na [ZDE](http://127.0.0.1:8000/)  

## Jak si vyzkoušet náš web?  

**Vzhledem k povaze aplikace není možné si jako nepřihlášený vytvořit uživatelský účet**  
Pro přístup se přihlaste pod uživatelským jménem 'admin' a heslem 'unipasswrd'.  
Nyní jste přihlášený jako administrátor a máte možnost si zobrazit všechny účty uložené v databázi.  
Pro vyzkoušení klientské a opatrovnické části webu se přihlašte na jeden z již-existujících účtů s heslem 'unipasswrd' nebo si nový vytvořte.  
Univerzální a veřejné heslo u všech účtů je pouze nyní a to pro ukázku funkčnosti projektu.