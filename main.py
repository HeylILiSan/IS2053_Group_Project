def email_security_checker():
    print("=== Trusted Email Setup ===")

    trusted_input = input("Enter trusted email addresses (separated by commas): ")

    trusted_emails = {email.strip().lower() for email in trusted_input.split(",") if email.strip()}
    
    if not trusted_emails:
        print("No trusted emails provided. Exiting program.")
        return

    print(f"\n[Info] Successfully registered {len(trusted_emails)} trusted email(s).")
    print("You can now check emails. Type 'exit' to quit.\n")

    while True:
        email_to_check = input("Enter an email address to check: ").strip()
        
        if email_to_check.lower() == 'exit':
            print("Exiting email checker. Goodbye!")
            break
            
        if not email_to_check:
            continue

        if email_to_check.lower() in trusted_emails:
            print(f" [SAFE] '{email_to_check}' is in your trusted list.\n")
        else:
            print(f" [WARNING] '{email_to_check}' is NOT a trusted email! Exercise caution.\n")

if __name__ == "__main__":
    email_security_checker()

#Let me know the changes I need to make
