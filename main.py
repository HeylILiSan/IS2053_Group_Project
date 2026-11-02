def email_security_checker():
    print("=== Trusted Email Setup ===")

    trusted_input = input("Enter trusted email addresses (separated by commas): ")

    trusted_emails = {email.strip().lower() for email in trusted_input.split(",") if email.strip()} 
    # if you want to take the emails in as a list, try setting the input up as a looping input in a separate function
    # that allows this function to run independent of the input process, allowing us to use it with preexisting inputs
    
    if not trusted_emails:
        print("No trusted emails provided. Exiting program.")
        return # good, maybe try returning none instead of just return

    print(f"\n[Info] Successfully registered {len(trusted_emails)} trusted email(s).")
    print("You can now check emails. Type 'exit' to quit.\n")

    while True:
        email_to_check = input("Enter an email address to check: ").strip() # more clearly state the exit prompt
        
        if email_to_check.lower() == 'exit':
            print("Exiting email checker. Goodbye!")
            break
            
        if not email_to_check:
            continue # good

        if email_to_check.lower() in trusted_emails:
            print(f" [SAFE] '{email_to_check}' is in your trusted list.\n")
        else:
            print(f" [WARNING] '{email_to_check}' is NOT a trusted email! Exercise caution.\n")

if __name__ == "__main__":
    email_security_checker()

#Let me know the changes I need to make

# I like the ideas, but break it down more. I know it can feel redundant but it's good practice.
# One function for handling inputting trusted emails, returning a list of them
# One function that takes in a list of trusted emails and an email to be checked and returns true or false for if it's trusted
# Separating the functionality allows us to better integrate it with the mail server stuff later without completely rewriting stuff
