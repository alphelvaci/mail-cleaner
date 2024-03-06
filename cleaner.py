from imapclient import IMAPClient


def display(lst):
    print()
    for item in lst:
        print(item)
    print()


client = IMAPClient(host='127.0.0.1', port='1143', ssl=False)
client.login(username='$$$$', password='$$$$')

print("Welcome to mail cleaner v0", end="\n\n")

print("Your mailboxes:")
display([x[2] for x in client.list_folders()])

mailbox = input("Type a mailbox name: ")
print()

client.select_folder(folder=mailbox)

ids = client.search(criteria="ALL")
mail = client.fetch(messages=ids, data=['ENVELOPE'])

senders = {}
for key, value in mail.items():
    has_single_from = len(value[b'ENVELOPE'].from_) == 1
    if has_single_from:
        _from = value[b'ENVELOPE'].from_
        address = f"{_from[0].mailbox.decode()}@{_from[0].host.decode()}"
        if address in senders:
            senders[address] += 1
        else:
            senders[address] = 1

print("Top senders:")
display([f"{senders[x]}, {x}" for x in sorted(senders, key=senders.get, reverse=True)[:10]])
