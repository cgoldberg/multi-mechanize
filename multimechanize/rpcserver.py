#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize


import SimpleXMLRPCServer
import socket
import thread
    
    
    
def launch_rpc_server(port, project_name, run_callback):  
    host = socket.gethostbyaddr(socket.gethostname())[0]
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((host, port), logRequests=False)
    server.register_instance(RemoteControl(project_name, run_callback))
    server.register_introspection_functions()
    print '\nMulti-Mechanize: %s listening on port %i' % (host, port)
    print 'waiting for xml-rpc commands...\n'
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
        


class RemoteControl(object):
    def __init__(self, project_name, run_callback):
        self.project_name = project_name
        self.run_callback = run_callback
        self.test_running = False
        self.output_dir = None
    
    def run_test(self):
        if self.test_running:
            return 'Test Already Running'
        else:
            thread.start_new_thread(self.run_callback, (self,))
            return 'Test Started'    
    
    def check_test_running(self):
        return self.test_running
    
    def update_config(self, config):
        with open('projects/%s/config.cfg' % self.project_name, 'w') as f:
            f.write(config)
            return True
 
    def get_config(self):
        with open('projects/%s/config.cfg' % self.project_name, 'r') as f:
            return f.read()
            
    def get_project_name(self):
        return self.project_name

    def get_results(self):
        if self.output_dir is None:
            return 'Results Not Available'
        else:
            with open(self.output_dir + 'results.csv', 'r') as f:
                return f.read()
