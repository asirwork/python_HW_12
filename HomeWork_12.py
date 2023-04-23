from collections import UserDict
from datetime import datetime
import re
import pickle


class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class Name(Field):
    ...


class Phone(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        pattern = r'^\(\d{3}\)\s\d{3}-\d{4}$'
        if value is not None and not re.match(pattern, value):
            raise ValueError(f"Invalid phone number format: {value}")
        self.__value = value


class Birthday(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if value is not None and not re.match(pattern, value):
            raise ValueError(f"Invalid birthday format: {value}")
        self.__value = value


class Record:

    def __init__(self,
                 name: Name,
                 phone: Phone = None,
                 birthday: Birthday = None):
        self.name = name
        self.birthday = birthday
        self.phones = [phone] if phone else []

    def __str__(self):
        return f"{self.name}: {(self.phones)} Day of birth: {self.birthday}"

    def __repr__(self):
        phones = ', '.join(str(phone.value) for phone in self.phones)
        return f"{self.name.value}: {phones} Day of birth: {self.birthday}"

    def add(self, phone: Phone):
        self.phones.append(phone)

    def edit(self, new_phone: Phone) -> str:
        old_phone = self.phone.value
        new_phone_value = new_phone.value
        self.phone = new_phone
        return f"Change {old_phone} to {new_phone_value}"

    def remove(self, phone: Phone):
        if phone in self.phones:
            self.phones.remove(phone)
            if phone == self.phone:
                self.phone = None
        else:
            raise ValueError("Phone not found in record.")

    def days_to_birthday(self):
        try:
            today = datetime.today()
            birthday = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)
            days_left = (birthday_this_year - today).days
            return f"{self.name} - Days to next birthday: {days_left}"
        except ValueError:
            return f"{self.name} - Not have date of birth"


class AddressBook(UserDict):

    def __init__(self):
        super().__init__()

    try:
        with open('data.bin', 'rb') as f:
            while True:
                try:
                    records = pickle.load(f)
                except EOFError:
                    break
    except FileNotFoundError:
        pass

    def add_record(self, record: Record):
        with open("data.bin", "wb") as f:
            pickle.dump(record, f)
        self.data[record.name.value] = record

    def __str__(self):
        output = []
        for name, record in self.data.items():
            phones = [
                phone.value for phone in record.phones
                if phone.value is not None
            ]
            phone_str = ", ".join(
                phones) if phones else "Not have a phone number"
            output.append(f"{name}: {phone_str}, {record.birthday}")

        return "\n".join(output)

    def iterator(self, page=2):
        keys_iterator = iter(self.data.keys())
        while True:
            result_keys = []
            for i in range(page):
                try:
                    result_keys.append(next(keys_iterator))
                except StopIteration:
                    break
            if not result_keys:
                break
            result = [self.data[key] for key in result_keys]
            yield result

    def search(self, param):
        if len(param) < 3:
            return "Parameter must be > 3 symbols"
        result = []
        for recoord in self.items():
            if param in str(recoord):
                result.append(str(recoord))
        return '\n'.join(result)


if __name__ == "__main__":

    first = AddressBook()
    name = Name("Bill")
    phone = Phone("(097) 007-0007")
    phone_2 = Phone("(099) 852-0010")
    bd = Birthday("10.12.2022")
    record_1 = Record(name, phone, bd)
    record_1.add(phone_2)
    first.add_record(record_1)

    name_22 = Name("Tom")
    phone_22 = Phone("(093) 123-3344")
    record_22 = Record(name_22, phone_22)
    first.add_record(record_22)

    name_33 = Name("Garry")
    phone_33 = Phone("(092) 123-4567")
    record_33 = Record(name_33, phone_33)
    first.add_record(record_33)

    name_44 = Name("Pol")
    phone_44 = Phone("(099) 123-9874")
    bd_44 = Birthday("15.05.2000")
    record_44 = Record(name_44, phone_44, bd_44)
    first.add_record(record_44)

    print(first)

    print("*" * 50)

    days_to_birthday = record_1.days_to_birthday()
    print(days_to_birthday)

    print("*" * 50)

    daysbd = record_33.days_to_birthday()
    print(daysbd)

    gen_ob = first.iterator(1)

    for i in gen_ob:
        print("*" * 50)
        print(i)

    print("*" * 50)
    print("*" * 50)
    print(first.search("ill"))