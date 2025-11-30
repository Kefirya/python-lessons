from smartphone import Smartphone
catalog = [
    Smartphone("Apple", "Iphone 16 pro max", "+1234567890"),
    Smartphone("Xiaomi", "Poko X3", "+79008887711"),
    Smartphone("Motorola", "Edge 50 Pro", "+78005553535"),
    Smartphone("OnePlus", "10r", "+77007777777"),
    Smartphone("Samsung", "Galaxy S66 Ultra Lite Max HP pro", "+79077099977")
]
for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")
