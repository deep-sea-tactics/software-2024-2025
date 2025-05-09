"""
This file is intended to run on an RPI-3, raspbian linux. If this file throws errors on your system,
it's likely because you're *not* on raspbian linux
"""

try:
        import pigpio # type: ignore
except ModuleNotFoundError:
        print("error(client): pigpio not found- are you executing on the client")
        exit()

import time
import threading

class SN:
        """
        Sequence node class
        """

        def __init__(self, duration: float, value: int):
                self.duration: float = duration
                self.value: int = value

class ServoSequence:
        """
        Submits tickets at specified intervals
        """

        def __init__(self, nodes: list[SN]):
                self.nodes: list[SN] = nodes

        def exec_seq(self, app, pin: int):
                """
                Eexcutes the sequence
                """

                for node in self.nodes:
                        print("Seq: val {}, dur {}".format(node.value, node.duration))

                        app.submit_ticket(pin, node.value)
                        time.sleep(node.duration)

                app.submit_ticket(pin, 0)

class Ticket:
        """
        Requests a servo value
        """
        def __init__(self, pin: int, value: int):
                self.value: int = value
                self.pin: int = pin

class Application:
        def __init__(self):
                self.tickets: list[Ticket] = []

                self.pi = None

        def init_pi(self):
                """
                Sets the 'pi' property to the local pi, using pigpio
                """
                self.pi = pigpio.pi()

        def submit_ticket(self, pin: int, value: int):
                self.tickets.append(Ticket(pin, value))

        def process_ticket(self, ticket: Ticket):
                """
                NOTE: THIS FUNCTION IS UNSAFE.
                DO NOT CALL IT DIRECTLY, PLEASE.

                This assumes the pi is initialized!
                """

                self.pi.set_servo_pulsewidth(ticket.pin, ticket.value)

        def handle_tickets(self):
                if self.pi == None:
                        return

                if len(self.tickets) == 0:
                        return

                index: int = 0
                for ticket in self.tickets:
                        self.tickets.pop(index)
                        self.process_ticket(ticket)

                        index += 1

                print("Proc: {} tickets".format(index))

class SEQUENCES:
        INIT = ServoSequence([
                SN(1.5, 1500),
        ])

        END = ServoSequence([
                SN(1.0, 0)
        ])

        THRUSTER_TEST = ServoSequence([
                SN(1.5, 1500),
                SN(1.5, 1550),
                SN(1.0, 0)
        ])

TESTING_PIN = 4

# NOTE:
# THIS IS IMPORTANT. Don't skim over it...
#
# IF YOU CREATE A SEQUENCE. Make sure it ends with
# a zero signal (SN(1.0, 0)) so the thrusters do
# not get confused. (They will continue to run even
# after the sequence ends unless told otherwise)

def thruster_seq(application: Application, seq: ServoSequence, pin: int):
        thread = threading.Thread(target=seq.exec_seq, args=(application, pin,))
        thread.start()
        return thread

def ticketing_heartbeat(application: Application):
        while True:
                application.handle_tickets()

def main():
        application = Application()
        application.init_pi()
        ticketing_thread = threading.Thread(target=ticketing_heartbeat, args=(application,))
        ticketing_thread.start()

        thruster_seq(application, SEQUENCES.THRUSTER_TEST)

        ticketing_thread.join()

if __name__ == "__main__":
        main()