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

# FUNCTIONALITY CHANGES
# The code must now be a function that takes a string argument for an email address and a bool argument for the mode (True for whitelist, False for blacklist), ex: def checker(email_address, mode):
# The code will use pandas to find that email address in senders.csv
# if the user is not present, it will ask for additional identifiers like an alias, and if we trust the user, and it will add the user to the database accordingly
# if the user is present (or added), it will check what list the user is on and, depending on the mode, return True to allow or False to block it
# the main function in this code, whatever you may call it, will be imported into the communicator and called whenever an incoming email needs to be checked
