import xmlrpc.client

def getAllNotes():
    with xmlrpc.client.ServerProxy("http://localhost:8001/RPC2") as proxy:
        return proxy.getAllNotes()

def saveNewNote(topic, title, text):
    with xmlrpc.client.ServerProxy("http://localhost:8001/RPC2") as proxy:
        return proxy.saveNewNote(topic, title, text)
