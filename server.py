"""THE EMAIL SERVER"""

import asyncio # asynchronous script running
import signal # check for keyboard interrupt
# pyrefly: ignore[missing-import]
from aiosmtpd.controller import Controller # server controller

class MailHandler: # handler object

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        """Triggers when message is being received, allow/block should go here"""

        sender = envelope.mail_from # string of sender's email address

        # Here would be the code to decide if the email is allowed through or not.
        # It will take the sender and run it through the authenticator, then set accepted to True or False.
        accepted = True

        if accepted:
            envelope.rcpt_tos.append(address)
            # if accepted, return positive status code 250
            return "250 ACCEPTED"

        else:
            # if rejected, return negative status code 550
            return "550 REJECTED"

    async def handle_DATA(self, server, session, envelope):
        """Triggers if message accepted by RCPT"""

        # Extracted info
        Sender = envelope.mail_from # string containing the email address of the sender
        Receivers = envelope.rcpt_tos # list of strings containing the email addresses of the receivers
        Contents = envelope.content.decode('utf-8', errors = 'replace') # big string containing a the content type, content transfer encoding, mime version, subject, from, to, and body

        print("DEBUG: Message Received")

        # here would be the printout of the message

        return "250 OK"



async def main():
    handler = MailHandler() # set up handler

    controller = Controller(handler, hostname='127.0.0.1', port=8025)
    # first argument is mail handler object
    # "hostname" keyword argument takes a string for the ip address of the host machine (127.0.0.1 is local host)
    # "port" keyword argument takes an integer as the port used for communications, default for smtp protocol is TCP 8025

    controller.start() # start loop
    print(f"SMTP server running @ {controller.hostname}:{controller.port}")
    print(f"Ctrl + C to stop")

    stop_event = asyncio.Event()

    def stop_server():
        print("\nStopping server...")
        stop_event.set()

    loop = asyncio.get_running_loop() # registers OS signals

    try:
        loop.add_signal_handler(signal.SIGINT, stop_server)
        loop.add_signal_handler(signal.SIGTERM, stop_server)
    except NotImplementedError:
        # fallback for windows which does not support add_signal_handler
        pass

    try:
        # pause execution without blocking hooks
        if hasattr(signal, 'SIGINT') and stop_event.is_set() is False:
            while not stop_event.is_set():
                try:
                    # interrupt handling for windows
                    await asyncio.sleep(0.5)
                except asyncio.CancelledError:
                    break
        else:
            await stop_event.wait()
    finally:
        controller.stop() # stops server


if __name__ == '__main__':
    # run loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt: # end if keyboard interrupt)
        pass