class Empleado:

    def __get_email(self, name: str, last_name: str):
        return f"{name}.{last_name}@mycompany.com"

    def __init__(self, name: str, last_name: str):
        self.name = name
        self.last_name = last_name
        self.email = self.__get_email(self.name, self.last_name)

    def serialize(self):
        return self.__dict__


if __name__ == '__main__':

    try:
        body = {
            "name": "Jairo",
            "last_name": "Castañeda"
        }
        em = Empleado(**body)
        print("Python Object")
        print(em)
        print("Json object")
        print(em.serialize())

    except TypeError as error:
        print("The body is invalid")
