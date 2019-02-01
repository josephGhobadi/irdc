from StreamServer import StreamServer


class ShareThisDesktop:
    def __init__(self):
        self.isConnected = False
        self.shareCode = 'NaN!'

        ''' Run Command Server '''

        ''' Run Stream Server'''
        stream_server_object = StreamServer()
        stream_server_object.lunch_server()
        ''' Run ssh port forwarding '''
        self.isConnected = True
