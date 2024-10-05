def location_label(s):
    label = s.lower() + ("s" if s[-1]!='s' else '')
    label = (label
        .replace("sdg ", "SDG ")
        .replace("country/areas","countries/areas")
        .replace("special others","special other regions")
    )
    return label
