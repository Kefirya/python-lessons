from address import Address
from mailing import Mailing

to_address = Address("123056", "Нью-Йорк", "Мейн-Стрит", "07", "77")
from_address = Address("120456", "Пхеньян", "Ленина", "77", "7")
mailing = Mailing(to_address, from_address, 500, "s123654789")

print(f"Отправление {mailing.track} из {mailing.from_address.index}, {mailing.from_address.city}, {mailing.from_address.street}, {mailing.from_address.house} - {mailing.from_address.apartment} в {mailing.to_address.index}, {mailing.to_address.city}, {mailing.to_address.street}, {mailing.to_address.house} - {mailing.to_address.apartment}. Стоимость {mailing.cost} долларов США.")
