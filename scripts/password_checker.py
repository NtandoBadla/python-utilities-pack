def check_password_strength(password):
    """
    Check the strength of a password
    and return the result and missing requirements.
    """

    has_uppercase = False
    has_lowercase = False
    has_number = False
    has_special = False

    special_characters = "!@#$%^&*()-_=+[]{};:,.<>?/"

    for character in password:
        if character.isupper():
            has_uppercase = True
        elif character.islower():
            has_lowercase = True
        elif character.isdigit():
            has_number = True
        elif character in special_characters:
            has_special = True

    missing_requirements = []

    if len(password) < 8:
        missing_requirements.append(
            "Password must contain at least 8 characters."
        )

    if not has_uppercase:
        missing_requirements.append(
            "Add at least one uppercase letter."
        )

    if not has_lowercase:
        missing_requirements.append(
            "Add at least one lowercase letter."
        )

    if not has_number:
        missing_requirements.append(
            "Add at least one number."
        )

    if not has_special:
        missing_requirements.append(
            "Add at least one special character."
        )

    if len(missing_requirements) == 0:
        strength = "STRONG"
    elif len(missing_requirements) <= 2:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    return strength, missing_requirements


def display_result(strength, missing_requirements):
    """Display the password strength result."""

    print("\n" + "=" * 45)
    print("          PASSWORD STRENGTH CHECKER")
    print("=" * 45)

    print(f"\nPassword Strength: {strength}")

    if strength == "STRONG":
        print("\n✓ Password meets all requirements.")
    else:
        print("\nMissing requirements:")

        for requirement in missing_requirements:
            print(f"  - {requirement}")

    print("\n" + "=" * 45)


def main():
    print("=" * 45)
    print("          PASSWORD STRENGTH CHECKER")
    print("=" * 45)

    password = input("\nEnter password: ")

    strength, missing_requirements = check_password_strength(password)

    display_result(strength, missing_requirements)


if __name__ == "__main__":
    main()