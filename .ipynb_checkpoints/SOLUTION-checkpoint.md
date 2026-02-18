
|  Method 	        | Local  	| Same-Zone  	|  Different Region 	|
|---	            |---	    |---	        |---   	                |
|   REST add	    |   2.1364	    |   	4.0390        |  250.9598	    |
|   gRPC add	    |   0.5488	    |   	1.3205        |  131.8160  	|
|   REST rawimg	    |   	4.6684    |   	 22.91719       |   1615.8800	|
|   gRPC rawimg	    |      9.01323     |   	 10.6642      |   195.7728	|
|   REST dotproduct	|   	2.8567    |   	  4.6275      |  	272.4452    |
|   gRPC dotproduct	|   	0.6027    |   	   1.5837     |    119.4114	|
|   REST jsonimg	|   	22.7872    |   	  32.5930      |  1094.4907 	|
|   gRPC jsonimg	|       8.5921    |   	 14.07127       |   187.4887	|
|   PING            |      0.051     |       0.521        |    115.772   |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

Start code
-ssh into new vm
gcloud compute ssh <vm-name> --zone=us-central1-a

-install venv
sudo apt update
sudo apt install python3-venv -y

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt



Observations:
Based on the experimental results, gRPC generally performed faster than REST in most cases, especially in the localhost and same-zone tests. This is probably because gRPC keeps a persistent TCP connection and uses Protocol Buffers for binary serialization, which reduces overhead compared to REST, which uses JSON and may create more connection overhead. For smaller operations like add and dotproduct, the performance difference was quite clear and gRPC had noticeably lower latency.

In the different-region tests, both REST and gRPC showed much higher latency because of the physical network distance between regions. The ping latency was already around 115 ms, which suggests that network delay became the main factor affecting performance. Even though gRPC was still faster than REST, the difference between them was smaller compared to the overall network latency. This indicates that protocol efficiency matters more when latency is low, but when communicating across regions, network latency dominates the total response time.