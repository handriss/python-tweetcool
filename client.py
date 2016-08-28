import argparse
import ipaddress
import requests
import json
import datetime


class Client():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-H", "--host",
                            help="IP address of the Tweetcool server",
                            default='127.0.0.1')  # Equals 'localhost'
        parser.add_argument("-P", "--port",
                            help="Post used by the Tweetcool server",
                            type=int,
                            default=9876)
        args = parser.parse_args()

        try:
            self.server = {
                'host': ipaddress.ip_address(args.host),
                'port': args.port
            }
        except ValueError as e:
            print('The given host is not a valid IP address')
            exit(0)

        if not(1024 < self.server["port"] < 65535):
            print('The given port number is not in the range between 1024 and 65535!')
            exit(0)

        self.server["address"] = 'http://' + self.server["host"].compressed + ':' + str(self.server["port"])
        self.route = self.server["address"]+"/tweet"
        self.user = input("Give in username: ")

        self.menu()

    def post_tweet(self, message):
        payload = {"content": str(message), "poster": self.user}
        requests.post(self.route, json=payload)

    def refresh(self):
        for i in requests.get(self.route).json():
            print(i["poster"], "<" + str(datetime.datetime.utcfromtimestamp(int(i["timestamp"]))) + ">:", i["content"])

    def menu(self):
        while True:
            try:
                command = input('''
---------------- TWITTERCOOL ------------------
-----------------------------------------------
Enter:
   post -- to post your thoughts;
   refresh -- to refresh the timeline;
   exit or CTRL+D -- to quit the application.
-----------------------------------------------

Command: ''')
                if command == "refresh":
                    self.refresh()
                elif command == "post":
                    self.post_tweet(input("\nEnter your message: "))
                elif command == "exit":
                    exit()
                else:
                    print("Unkown command. Try again.")
            except EOFError:
                exit()
            except KeyboardInterrupt:
                exit()


client = Client()
