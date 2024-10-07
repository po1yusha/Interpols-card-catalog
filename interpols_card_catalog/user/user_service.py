from user.user_repository import InmemoryUserRepository, UserEntity


class LastUserException(Exception):
    pass


class ExistUserException(Exception):
    pass


class UserService:
    def __init__(self, user_repository: InmemoryUserRepository):
        self.user_repository = user_repository

    def is_valid_user(self, login: str, password: str) -> bool:
        user = self.user_repository.find_user_by_login(login)
        if user is None:
            return False

        if password != user.password:
            return False

        return True

    def get_all_users(self) -> [UserEntity]:
        return self.user_repository.find_all()

    def delete_user(self, login: str):
        if self.user_repository.count() <= 1:
            raise LastUserException("Cannot remove last user")
        self.user_repository.delete_by_login(login)

    def add_user(self, login: str, user: UserEntity):
        if self.user_repository.find_user_by_login(login) is not None:
            raise ExistUserException("Entered login already exists")
        self.user_repository.create_user(user)

    def get_user_by_login(self, login) -> UserEntity:
        return self.user_repository.find_user_by_login(login)
