import argparse
import ipaddress
import requests
import json
import datetime


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
    server = {
        'host': ipaddress.ip_address(args.host),
        'port': args.port
    }
except ValueError as e:
    print('The given host is not a valid IP address')
    exit(0)

if not(1024 < server["port"] < 65535):
    print('The given port number is not in the range between 1024 and 65535!')
    exit(0)

server["address"] = 'http://' + server["host"].compressed + ':' + str(server["port"])


route = server["address"]+"/tweet"
user = "Húrin"


def get_tweets():
    return requests.get(route).json()


def format_tweets():
    for i in get_tweets():
        print(i["poster"], "<" + str(datetime.datetime.utcfromtimestamp(int(i["timestamp"]))) + ">:", i["content"])
    print("")


def post_tweet(message):
    payload = {"content": str(message), "poster": user}
    requests.post(route, json=payload)


def main_menu():
    print("Available commands: \n\n refresh: Refresh the latest tweets \n exit: "
          "Exit the program \n post: Post a tweet\n")
    command = input("Type in command: ")
    return command


print("Tweetcool client starting...")
while True:
    try:
        command = main_menu()
        if command == "refresh":
            format_tweets()
        elif command == "exit":
            exit()
        elif command == "post":
            message = input("Type your message: ")
            post_tweet(message)
            format_tweets()
        else:
            print("Unknow command. Try again.\n")
    except EOFError:
        print("An error occured. ")
        exit()
    finally:
        print("\n")
