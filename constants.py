# Regular expression for the finding IP addresses
IP_V4_REGEX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
IP_V6_REGEX = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
URL_REGEX = r"(https?:\/\/)?([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)"

# API endpoints
IP_DATA_ENDPOINT = "https://api.ipdata.co/%s"
CO2_SIGNAL_ENDPOINT = "https://api.co2signal.com/v1/latest"
IP_GEOLOCATION_ENDPOINT = "https://api.ipgeolocation.io/ipgeo"
WHO_IS_ENDPOINT = "http://rest.db.ripe.net/geolocatioN"
BID_DATA_CLOUD_ENDPOINT = "https://api.bigdatacloud.net/data/ip-geolocation"

# Graph labels
GRAPH_LABELS = {
    "x_label": "Destinations",
    "carbon": "Carbon Intensity (gCO2/KWh)",
    "hops": "Hops",
    "carbon_error": "# Carbon Error values",
    "lookup_error": "# Hops Error values",
}

# Export types
EXPORT_TYPE = {
    "carbon": "Carbon Emission",
    "hops": "Hops",
    "carbon_error": "Error Carbon Val",
    "lookup_error": "Error lookup",
    "unknown_routers": "Unknown Routers",
}
