from scrapy.utils.reqser import request_to_dict, request_from_dict


class Base(object):

    def __init__(self, server,resource, spider, QueueUrl, serializer=None):
        self.server = server
        self.resource = resource
        self.spider = spider
        self.key = QueueUrl
        self.serializer = serializer

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class LifoQueue(Base):
    """Per-spider LIFO queue."""

    def __len__(self):
        """Return the length of the stack"""
        return int(self.resource.Queue(self.key).attributes["ApproximateNumberOfMessages"])

    def push(self, request):
        """Push a request"""
        self.server.send_message(self.key, self._encode_request(request))

    def pop(self, timeout=0):
        data = receive_message(self.server,self.key)
        if data:
            return self._decode_request(data)


def receive_message(server,key):
    response = server.receive_message(
        QueueUrl=key,
        AttributeNames=["All"],
    )
    Messages = response.get("Messages", "")
    if Messages:
        # print(Messages)
        Message = Messages[0]
        server.delete_message(QueueUrl=key, ReceiptHandle=Message["ReceiptHandle"])
        print(Message["Body"])
        return Message["Body"]



# TODO: Deprecate the use of these names.
SpiderStack = LifoQueue
