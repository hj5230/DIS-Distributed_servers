import time
import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

PORT = 8001

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', PORT),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def getAllNotes():
        tree = ET.parse('./db.xml')
        root = tree.getroot()
        topics = []
        for topic in root.findall('topic'):
            topic_name = topic.get('name')
            notes = []
            for note in topic.findall('note'):
                note_name = note.get('name')
                text = note.find('text').text
                timestamp = note.find('timestamp').text
                notes.append({'name': note_name, 'text': text, 'timestamp': timestamp})
            topics.append({'name': topic_name, 'notes': notes})
        return topics

    def saveNewNote(topic, title, text):
        if not topic or not title or not text:
            return False
        tree = ET.parse('./db.xml')
        root = tree.getroot()
        new_note = ET.Element('note')
        new_note.attrib['name'] = title
        new_topic = root.find('topic[@name="{}"]'.format(topic))
        if new_topic is None:
            new_topic = ET.Element('topic')
            new_topic.attrib['name'] = topic
            root.append(new_topic)
        new_text = ET.Element('text')
        new_text.text = text
        new_note.append(new_text)
        new_timestamp = ET.Element('timestamp')
        current_time = time.strftime('%d/%m/%Y - %H:%M:%S', time.localtime())
        new_timestamp.text = current_time
        new_note.append(new_timestamp)
        new_topic.append(new_note)
        tree.write('./db.xml')
        return True

    server.register_function(getAllNotes)
    server.register_function(saveNewNote)

    print(f'XMLRPC server is running at port: {PORT}')

    server.serve_forever()
