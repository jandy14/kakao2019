import requests

url = 'http://localhost:8000'

def start(user, problem, count):
    uri = url + '/start' + '/' + user + '/' + str(problem) + '/' + str(count)
    return requests.post(uri).json()

def oncalls(token):
    uri = url + '/oncalls'
    return requests.get(uri, headers={'X-Auth-Token': token}).json()

def action(token, cmds):
    uri = url + '/action'
    return requests.post(uri, headers={'X-Auth-Token': token}, json={'commands': cmds}).json()

def init(user, problem, count):
    ret = start(user, problem, count)
    return ret['token']
def posibleElevator(elevators, passenger):
    for e in elevators:
        pass
    return None
def potentialPassenger(elevator, passengers):
    passenger = []
    for p in passengers:
        pass
    return None
def p0_simulator():
    user = 'jandy'
    problem = 0
    count = 4
    token = init(user, problem, count)
    elevators = []
    progressing = []
    waiting = []
    is_end = False
    while not is_end:
        cmd = []
        respond = oncalls(token)
        # something algorithm
        call = respond['calls']
        elev = respond['elevators']
        waiting += [i for i in call if i not in progressing and i not in waiting]
        for e in elev:
            # check to get elevators
            index = posibleElevator(elev, w)
            # if w can get elevator, w get elevator and w move to progressing

        # action
        is_end = action(token, cmd)['is_end']
    print("Done!")
    print
if __name__ == '__main__':
    p0_simulator()
