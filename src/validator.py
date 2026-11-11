class Validator:
    @staticmethod #can be used without creating an instance of the class (ex. validator.is_valid(name))
    def is_valid(name):
        return (
            isinstance(name, str) and len(name) > 0 and name.isascii()
            and name.isalnum()
            and name[0].isalpha()
        )
    @staticmethod
    def filename(user_a, user_b):
        for name in (user_a, user_b):
            if not Validator.is_valid(name):
                raise ValueError(f"Invalid username: {name!r}")
            if user_a.lower() == user_b.lower():
                raise ValueError("Usernames must be different.")
            first, second = sorted([user_a, user_b], key=str.lower)
            return f"{first}-{second}.txt"