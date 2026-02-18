#!/usr/bin/env python3
from concurrent import futures
import grpc
import imageops_pb2
import imageops_pb2_grpc

from PIL import Image
import io

class ImageOpsServicer(imageops_pb2_grpc.ImageOpsServicer):
    def Add(self, request, context):
        return imageops_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.data))
            return imageops_pb2.ImageInfo(width=img.size[0], height=img.size[1])
        except Exception:
            return imageops_pb2.ImageInfo(width=0, height=0)

    # gRPC need no JSON+base64，just send bytes
    def JsonImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.data))
            return imageops_pb2.ImageInfo(width=img.size[0], height=img.size[1])
        except Exception:
            return imageops_pb2.ImageInfo(width=0, height=0)

    def DotProduct(self, request, context):
        if len(request.a) != len(request.b):
            return imageops_pb2.DotReply(dot=0.0)
        s = 0.0
        for x, y in zip(request.a, request.b):
            s += float(x) * float(y)
        return imageops_pb2.DotReply(dot=s)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    imageops_pb2_grpc.add_ImageOpsServicer_to_server(ImageOpsServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server listening on 0.0.0.0:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
