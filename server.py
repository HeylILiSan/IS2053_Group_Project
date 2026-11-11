"""THE EMAIL SERVER"""

import asyncio # asynchronous script running
import signal # check for keyboard interrupt
from aiosmtpd.controller import Controller # server controller

class MailHandler: # handler object
    async def handle_DATA(self, server, session, envelope):
        """Triggers when 'DATA' command sent by SMTP client"""

        # report new message
        print("===================================")
        print(f"=== New Message ===\nSender: {envelope.mail_from}\nRecipient(s): {envelope.rcpt_tos}")

        # decode message contents
        contents = envelope.content.decode('utf-8', errors = 'replace')
        print(f"Message body:\n")
        print(contents)
        print("===================================")

        # email allow/block goes here

        # return status code 250 OK
        return "250 Message accepted for delivery"


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