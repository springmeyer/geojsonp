PROTOBUF_CXXFLAGS=$(shell pkg-config protobuf --cflags)
PROTOBUF_LDFLAGS=$(shell pkg-config protobuf --libs-only-L) -lprotobuf-lite

all: geojson_pb2.py geojson2_pb2.py

geojson_pb2.py: geojson.proto
	protoc -I./ --python_out=. ./geojson.proto

geojson2_pb2.py: geojson2.proto
	protoc -I./ --python_out=. ./geojson2.proto

#decode: decode.cpp
#	clang++ -o decode decode.cpp $(PROTOBUF_CXXFLAGS) $(PROTOBUF_LDFLAGS)

clean:
	@rm -f ./geojson_pb2.py
	@rm -f ./geojson2_pb2.py
	@rm -f ./decode

test:
	for i in $$(ls test/data/*); do ./encode.py $$i; ./decode.py; done

.PHONY: test
