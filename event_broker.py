import simpy


class EventBroker(object):
    """An message broker that allows communication via channels.

    This construct is useful when message consumers are running at
    different rates than message generators and provides an event
    buffering to the consuming processes.
    
    Simpy includes a filtered pipe concept that requires a filter
    be provided to the pipe. This concept removes the need to 
    check the filter so many times, since the subscriptions are
    grouped together by channels, or topics. Whenever a topic is
    published to, anyone on it will receive the event message.

    The parameters are used to create a new
    :class:`~simpy.resources.store.Store` instance each time
    :meth:`get_output_conn()` is called.

    """

    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.topics = {}

    def publish(self, topic, msg):
        """Broadcast a *value* to all receivers."""
        if not self.topics:
            raise RuntimeError('There are no output pipes.')
        events = [sub.publish(msg) for sub in self.topics[topic]]
        return self.env.all_of(events)  # Condition event for all "events"

    def subscribe(self, topic='global'):
        """Get a new output connection for this broadcast pipe.

        The return value is a :class:`~sim_utils.Subscription`.

        """
        sub = Subscription(self.env, topic=topic, capacity=self.capacity)

        # add topic if it doesn't exist
        if topic not in self.topics.keys():
            self.topics[topic] = []

        topic_store = self.topics[topic]
        topic_store.append(sub)
        return sub

        
class Subscription(object):
  def __init__(self, env, topic='default', capacity=simpy.core.Infinity):
      self.topic = topic
      self.topic_buffer = simpy.Store(env, capacity=capacity)

  def publish(self, msg):
      """ Delivers the provided message to the subscription.

      :param msg: any data type
      :return: None
      """
      return self.topic_buffer.put(msg)

  def next(self):
      """ Get the next message from the subscription, when a message is available.

      :return: the message that was published
      """
      return self.topic_buffer.get()


class Consumer(object):
    def __init__(self, eb, env, topic):
        self.eb = eb
        self.sub = self.eb.subscribe(topic=topic)
        self.con_proc = env.process(self.proc_messages())

    def proc_messages(self):
        while True:
            msg = yield self.sub.next()
            print(msg)
            
if __name__ == '__main__':
    environ = simpy.Environment()
    eb = EventBroker(environ)

    con = Consumer(eb, environ, topic='STATUS')
    eb.publish(topic='STATUS', msg='Active')
    eb.publish(topic='STATUS', msg='Down')
    eb.publish(topic='STATUS', msg='Active')

    environ.run()
