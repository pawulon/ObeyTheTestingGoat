from os import path
import subprocess
THIS_FOLDER = path.dirname(path.abspath(__file__))

KEY_PARAM = r'D:\Projekty\AWS\PR_AWS.pem'

def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            'fab',
            'create_session_on_server:email={}'.format(email),
            '--host=pawel@{}'.format(host),
            '--hide=everything,status',
            '-i',
            KEY_PARAM
        ],
        cwd=THIS_FOLDER
    ).decode().strip()
        
def reset_database(host):
    print('jestem tu: {}'.format(KEY_PARAM))
    subprocess.check_call(
        [
            'fab', 
            'reset_database',
            '--host=pawel@{}'.format(host),
            '-i',
            KEY_PARAM
        ],
        cwd=THIS_FOLDER
    )