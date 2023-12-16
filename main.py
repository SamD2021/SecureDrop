from typing import Dict, Any

import userReg
import userLogin
from contact import Contact
from securedrop import SecureDrop


def main():
    # Check if needs to register or login
    my_secure_drop = SecureDrop()
    my_secure_drop.main_loop()


if __name__ == '__main__':
    main()
