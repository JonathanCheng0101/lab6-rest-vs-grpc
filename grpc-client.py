#!/usr/bin/env python3
import sys
import time
import random
import grpc
import imageops_pb2
import imageops_pb2_grpc

IMAGE_PATH = "Flatirons_Winter_Sunrise_edit_2.jpg"

def do_add(stub, debug=False):
    resp = stub.Add(imageops_pb2.AddRequest(a=5, b=10))
    if debug:
        print("sum =", resp.sum)

def do_rawimage(stub, img_bytes, debug=False):
    resp = stub.RawImage(imageops_pb2.ImageBytes(data=img_bytes))
    if debug:
        print("rawimage:", resp.width, resp.height)

def do_jsonimage(stub, img_bytes, debug=False):
    resp = stub.JsonImage(imageops_pb2.ImageBytes(data=img_bytes))
    if debug:
        print("jsonimage:", resp.width, resp.height)

def do_dotproduct(stub, debug=False):
    n = 128
    a = [random.random() for _ in range(n)]
    b = [random.random() for _ in range(n)]
    resp = stub.DotProduct(imageops_pb2.VectorPair(a=a, b=b))
    if debug:
        print("dot =", resp.dot)

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
        print("cmd in: add, rawImage, jsonImage, dotProduct")
        sys.exit(1)

    host = sys.argv[1]
    cmd = sys.argv[2]
    reps = int(sys.argv[3])

    addr = f"{host}:50051"
    print(f"Running {reps} reps against gRPC {addr}")

    # gRPC channel
    channel = grpc.insecure_channel(addr)
    stub = imageops_pb2_grpc.ImageOpsStub(channel)

    # image reads only once to avoif i/o affects benchmark
    img_bytes = None
    if cmd in ("rawImage", "jsonImage"):
        with open(IMAGE_PATH, "rb") as f:
            img_bytes = f.read()

    start = time.perf_counter()

    if cmd == "add":
        for _ in range(reps):
            do_add(stub)
    elif cmd == "rawImage":
        for _ in range(reps):
            do_rawimage(stub, img_bytes)
    elif cmd == "jsonImage":
        for _ in range(reps):
            do_jsonimage(stub, img_bytes)
    elif cmd == "dotProduct":
        for _ in range(reps):
            do_dotproduct(stub)
    else:
        print("Unknown option", cmd)
        sys.exit(1)

    delta_ms = ((time.perf_counter() - start) / reps) * 1000.0
    print("Took", delta_ms, "ms per operation")

if __name__ == "__main__":
    main()
