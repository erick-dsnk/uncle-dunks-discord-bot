import json

def log_incident(incident, reason, time, server):
    i_dict = {
        "incident":incident,
        "reason":reason,
        "time":time,
        "server":server
    }

    with open('incidents.json', 'r') as f:
        data = json.load(f)

        data['incidents'].append(i_dict)

    with open('incidents.json', 'w') as f:
        json_obj = json.dumps(data, indent=4)

        f.write(json_obj)


def retrieve_incidents(server_id):
    with open('incidents.json', 'r') as f:
        incidents = json.load(f)

        incidents_in_server = []

        if incidents:
            for i in incidents:
                if i['server'] == server_id:
                    incidents_in_server.append(i)

                else:
                    pass
            
            return incidents_in_server
        
        else:
            return None