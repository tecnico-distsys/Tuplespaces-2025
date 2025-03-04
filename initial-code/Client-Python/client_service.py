import sys
import grpc

sys.path.insert(1, '../Contract/target/generated-sources/protobuf/python')

import TupleSpaces_pb2_grpc
import TupleSpaces_pb2

class ClientService:
    def __init__(self, host_port: str, client_id: int):
        self.client_id = client_id
        try:
            channel = grpc.insecure_channel(host_port)
            self.stub = TupleSpaces_pb2_grpc.TupleSpacesStub(channel)
            print("Connected to server")
        except grpc.RpcError as e:
            print(f"Failed to connect to server: {e.details()}")
            sys.exit(1)
            # TODO: Create channel/stub for each server

    def operation_put(self,tuple_data):
        try:
            request = TupleSpaces_pb2.PutRequest(newTuple=tuple_data)
            response = self.stub.put(request,timeout=5)
            print(f"Response: {response.message}")
        except grpc.RpcError as e:
            print(e.details())
    
    def operation_read(self,tuple_data):
        try:
            request = TupleSpaces_pb2.ReadRequest(searchPattern=tuple_data)
            response = self.stub.read(request,timeout=5)
            print(f"Response: {response.message}")
        except grpc.RpcError as e:
            print(e.details())

    def operation_take(self,tuple_data):
        try:
            request = TupleSpaces_pb2.TakeRequest(searchPattern=tuple_data)
            response = self.stub.take(request,timeout=5)
            print(f"Response: {response.message}")
        except grpc.RpcError as e:
            print(e.details())

    def operation_get_tuple_spaces_state(self):
        try:
            request = TupleSpaces_pb2.getTupleSpacesStateRequest()
            response = self.stub.getTupleSpacesState(request,timeout=5)
            print(f"Response: {response.message}")
        except grpc.RpcError as e:
            print(e.details())

    # TODO: Implement individual methods for each remote operation of the TupleSpaces service
