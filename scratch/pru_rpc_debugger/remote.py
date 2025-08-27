import zerorpc


def connect_to_node(host: str) -> zerorpc.Client | None:
    # TODO: could also use fabric/connection to start rpc server on node
    rpc_client = zerorpc.Client(timeout=60, heartbeat=20)
    rpc_client.connect(f"tcp://{host}:4242")

    # This replaces
    # shepherd_io = ShepherdDebug()
    # shepherd_io.__enter__()
    if check_connection(rpc_client):
        return rpc_client
    return None


def check_connection(rpc_client: zerorpc.Client | None = None) -> bool:
    if rpc_client is None:
        return False
    try:
        rpc_client.is_alive()
    except zerorpc.exceptions.RemoteError:
        return False
    return True


client = connect_to_node("10.0.0.52")

print("connected")
