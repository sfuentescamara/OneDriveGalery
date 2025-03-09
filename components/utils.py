def nice_dates(fecha_str):
    "YYYY-MM-DD to YYYY-Mon"
    try:
        year, mes, day = map(int, fecha_str.split('-'))
        meses = {
            1: "ene", 2: "feb", 3: "mar", 4: "abr",
            5: "may", 6: "jun", 7: "jul", 8: "ago",
            9: "sep", 10: "oct", 11: "nov", 12: "dic"
        }
        return f"{year}-{meses[mes]}"
    except (ValueError, KeyError):
        return None