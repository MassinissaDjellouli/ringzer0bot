from firebase_admin import initialize_app
from firebase_admin.firestore import client,firestore
from firebase_admin.credentials import Certificate
from requests import get
from time import time_ns,sleep
from logging import info,basicConfig,INFO
RINGZERO_URL = "https://ringzer0ctf.com/api/"
HOUR_SECONDS = 3600
DAY_NS = 86400000000000
cred = Certificate('admin_key.json')
firebase = initialize_app(credential=cred)
db = client(firebase)
basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def get_group(group_id: str):
    res = db.collection('groups').document(str(group_id)).get().to_dict()
    if not res:
        return {'success':False,'error': 'Group not found'}
    users = res["users"]
    rzero_users = []
    for user in users:
        user = get_from_rzero(f"user/info/{user}")
        if user is None:
            return {'success':False,'error': f'User {user} in group {group_id} does not exist'}
        rzero_users.append(user)
    return {'success':True,'users':rzero_users}

def create_group():
    doc = db.collection('creation_request').document()
    doc.set({'timestamp': time_ns(), 'status': 'pending'})
    return {'success':True,'group_id': doc.id}

def confirm_group(group_id: str):
    doc = db.collection('creation_request').document(group_id)
    if not doc:
        return {'success':False,'error': 'Group not found'}
    if doc.get().to_dict()['status'] == 'confirmed':
        return {'success':False,'error': 'Group already confirmed'}
    doc2 = db.collection('groups').document(group_id)
    doc2.set({'users': []})
    doc.update({'status': 'confirmed'})
    return {'success': True}


def add_user(group_id: str, user: str):
    rzero_user = get_from_rzero(f"user/info/{user}")
    if rzero_user is None:
        return {'success':False,'error': f'User {user} does not exist on ringzer0'}
    doc = db.collection('groups').document(group_id)
    res = doc.get().to_dict()
    if not res:
        return {'success':False,'error': 'Group not found'}
    users = res["users"]
    users.append(user)
    doc.update({'users': users})
    return {'success': True}
def remove_user(group_id: str, user: str):
    doc = db.collection('groups').document(group_id)
    res = doc.get().to_dict()
    if not res:
        return {'success':False,'error': 'Group not found'}
    users = res["users"]
    if user not in users:
        return {'success':False,'error': f'User {user} not in group'}
    users.remove(user)
    doc.update({'users': users})
    return {'success': True}

def get_from_rzero(endpoint:str):
    res = get(RINGZERO_URL + endpoint).json()
    if res['success'] == 1:
        return res['data']['users'][0]['user']
    return None

def clean_db():
    while True:
        sleep(HOUR_SECONDS)
        to_delete = []
        docs = db.collection('creation_request').stream()
        for doc in docs:
            if doc.to_dict()['status'] != 'confirmed' and time_ns() - doc.to_dict()['timestamp'] > DAY_NS:
                to_delete.append(doc.reference)
        info(f'Deleting {len(to_delete)} documents')
        delete(db.transaction(),to_delete)

def setup_server(server_id,server_name):
    doc = db.collection('servers').document(server_id)
    if doc.get().exists:
        return {'success':False,'error': 'Server already setup'}
    res = create_group()
    if not res['success']:
        return res
    confirm_group(res['group_id'])
    if not res['success']:
        return res
    doc.set({'group_id': res['group_id'],'name': server_name})
    return {'success':True}
def get_group_from_server(server_id):
    doc = db.collection('servers').document(server_id).get().to_dict()
    if not doc:
        return {'success':False,'error': 'Server not setup'}
    return {'success':True,'group_id':doc['group_id']}
@firestore.transactional
def delete(transaction,docs):
    for doc in docs:
        transaction.delete(doc)