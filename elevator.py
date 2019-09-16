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
def getDirection(elevator):
    direction = 'STOP'
    if elevator[0]['floor'] > elevator[0]['passengers'][0]['end']:
        direction = 'DOWN'
    else:
        direction = 'UP'
    return direction
def makeCommand(elevator):
    elev = elevator[0]
    if elev['status'] in ['OPENED', 'STOPPED']:
        if elev['floor'] in [ i['end'] for i in elev['passengers']]:
            if elev['status'] == 'OPENED':
                return {'elevator_id': elev['id'], 'command': 'EXIT', 'call_ids':[ i['id'] for i in elev['passengers'] if i['end'] == elev['floor']]}
            if elev['status'] == 'STOPPED':
                return {'elevator_id': elev['id'], 'command': 'OPEN'}
        elif elev['floor'] in [ i['start'] for i in elevator[1]]:
            if elev['status'] == 'OPENED':
                return {'elevator_id': elev['id'], 'command': 'ENTER', 'call_ids':[ i['id'] for i in elevator[1] if i['start'] == elev['floor']]}
            if elev['status'] == 'STOPPED':
                return {'elevator_id': elev['id'], 'command': 'OPEN'}
        else:
            if elev['status'] == 'OPENED':
                return {'elevator_id': elev['id'], 'command': 'CLOSE'}
            if elev['status'] == 'STOPPED':
                return {'elevator_id': elev['id'], 'command': getDirection(elevator)}
    else:
        if elev['floor'] in [ i['end'] for i in elev['passengers']]:
            return {'elevator_id': elev['id'], 'command': 'STOP'}
        elif elev['floor'] in [ i['start'] for i in elevator[1]]:
            return {'elevator_id': elev['id'], 'command': 'STOP'}
        else:
            return {'elevator_id': elev['id'], 'command': getDirection(elevator)}
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
                elevators[i][1] = [ p for p in elevators[i][1] if p['id'] not in c['call_ids'] ]
            if c['command'] in ['DOWN','UP']:
                elevators[i][2] = c['command']
    print("Done!")
if __name__ == '__main__':
    p0_simulator()
