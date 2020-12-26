'''
A tempory file for me to check stuffs.
'''
import base64
import ipfshttpclient


client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def b642str(b64):
    return base64.b64decode(b64).decode('utf-8')

def create_listener():
    print("creating listener")
    with client.pubsub.subscribe('DIYHydrus-IPFS-Pubsub-Introduction') as sub:
        try:
            for message in sub:
                print(message["from"], b642str(message["data"]), message["seqno"], message["topicIDs"])

        except Exception as e:
            print(e)
            create_listener()
            
create_listener()
