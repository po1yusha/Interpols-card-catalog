from dataclasses import dataclass
import sqlite3


@dataclass
class UserEntity:
    login: str
    password: str
    name: str


def execute_sql(query):
    connection = sqlite3.connect('database.sqlite')
    data = connection.execute(query)
    result = []
    for row in data:
        if row is None:
            break
        result.append(UserEntity(login=row[0], password=row[1], name=row[2]))
    connection.commit()
    connection.close()
    return result


class InmemoryUserRepository:
    def find_user_by_login(self, login) -> UserEntity:
        select = execute_sql("select * from user where LOGIN = '" + login + "'")
        if len(select) == 0:
            return None
        return select[0]

    def create_user(self, user: UserEntity):
        execute_sql(
            "INSERT INTO user (LOGIN, PASSWORD, NAME) VALUES ('" + user.login + "', '"
            + user.password + "', '"
            + user.name + "')")

    def find_all(self) -> [UserEntity]:
        return execute_sql("select * from user")

    def delete_by_login(self, login):
        execute_sql("delete from user where LOGIN = '" + login + "'")

    def count(self):
        return len(self.find_all())
