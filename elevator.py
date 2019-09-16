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
def makeCommand(elevator):
    pass
def allocatePassenger(elevator,calls):
    pass
def p0_simulator():
    user = 'jandy'
    problem = 0
    count = 4
    token = init(user, problem, count)
    elevators = [ [i,[],"DOWN"] for i in oncalls(token)['calls'] ]
    is_end = False
    while not is_end:
        cmd = []
        respond = oncalls(token)
        # something algorithm
        call = respond['calls']
        elevators = [ [n] + o[1:] for o,n in zip(elevators,respond['elevators']) ]
        # allocate elevator
        for e in elevators:
            allocatePassenger(e,call)
        # make command based on condition of elevator
        for e in elevators:
            cmd.append(makeCommand(e))
        # action
        is_end = action(token, cmd)['is_end']
        # do something to do after action
        for i,c in enumerate(cmd):
            if c['command'] in ['ENTER','EXIT']:
                elevators[i][1] = [ p for p in elevators[i] if p['id'] not in c['call_ids'] ]
    print("Done!")
    print
if __name__ == '__main__':
    p0_simulator()
