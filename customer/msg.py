from customer.errors import VERIFATION_CODE_NOT_SEND


class Message:
    PHONE_EXISTS = "This phone number is registered"
    USER_REGISTER_SUCCESSFULLY = "User registered successfully"
    USER_DOES_NOT_EXISTS = "User does not exists"
    INVALID_DATA = "Invalid data"
    VERIFATION_CODE_SEND = "A verification code has been sent to the user's phone"
    INVALID_VERIFATION_CODE = "Invalid verification code"
    USER_ACTIVATED = "User activated"