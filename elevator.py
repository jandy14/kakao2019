import requests
MAXPASSENGER = 8
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
    dest = [ i['end'] for i in elevator[0]['passengers']] + [ i['start'] for i in elevator[1] ]
    if not dest:
        return direction
    if all(i >= elevator[0]['floor'] for i in dest):
        direction = 'UP'
    if all(i <= elevator[0]['floor'] for i in dest):
        direction = 'DOWN'
    if direction == 'STOP':
        raise
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
def allocatePassenger(elevators,calls):
    for elevator in elevators:
        calls = [ p for p in calls if p not in elevator[1]]
    for elevator in elevators:
        passengers = elevator[0]['passengers']
        progressing = elevator[1]
        if len(passengers) + len(progressing) > MAXPASSENGER:
            raise
        elif len(passengers) + len(progressing) == MAXPASSENGER:
            continue
        else:
            p0_allocate(elevator,calls)
def choosePassenger(elevator, candidate):
    test = [ (i['start']==elevator[0]['floor'],
    i['start'] in [p['end'] for p in elevator[0]['passengers']] or i['start'] in [p['start'] for p in elevator[1]],
    i['end'] in [p['end'] for p in elevator[0]['passengers']] or i['end'] in [p['start'] for p in elevator[1]],
    -abs(i['start'] - elevator[0]['floor']), i) for i in candidate ]
    test.sort(reversed=True)
    return [i[-1]['id'] for i in test[:MAXPASSENGER - len(elevator[0]['passengers']) + len(elevator[1])]
def p0_allocate(elevator, calls):
    if elevator[0]['passengers'] + elevator[1]:
        if not elevator[0]['passengers']:
            if getDirection(elevator) == 'UP':
                if [i for i in elevator[1] if i['start'] > i['end']]:
                    return
            else:
                if [i for i in elevator[1] if i['start'] < i['end']]:
                    return
        candidate = []
        if getDirection(elevator) == 'UP':
            candidate = [ i for i in calls if i['start'] >= elevator[0]['floor']]
        if getDirection(elevator) == 'DOWN':
            candidate = [ i for i in calls if i['start'] <= elevator[0]['floor']]
        if getDirection(elevator) == 'STOP':
            raise
        final = choosePassenger(elevator,candidate)
        [ elevator[1].append(i), calls.remove(i) for i in candidate if i['id'] in final ]
    else:
        d_candidate = sorted([i for i in calls if i['start'] > i['end']], key=lambda x: x['start'], reversed=True)
        u_candidate = sorted([i for i in calls if i['start'] < i['end']], key=lambda x: x['start'])
        candidate = None
        if elevator[2] == 'UP':
            if d_candidate:
                candidate = d_candidate
            elif u_candidate:
                candidate = u_candidate
            else:
                pass
        else:
            if u_candidate:
                candidate = u_candidate
            elif d_candidate:
                candidate = d_candidate
            else:
                pass
        if candidate:
            [ elevator[1].append(i), calls.remove(i) for i in candidate if i['start'] == candidate[0]['start'] ]
def simulator():
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
        allocatePassenger(elevators,call)
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
    simulator()
