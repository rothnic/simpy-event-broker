# simpy-event-broker
Implements a simple event broker for simpy, utilizing named channels for separating traffic.

## Purpose
Simpy includes a filtered pipe concept that requires a filter be provided to the pipe. This concept removes the need to check the filter so many times, since the subscriptions are grouped together by channels, or topics. Whenever a topic is published to, anyone on it will receive the event message.

This was based off of the [Broadcast Pipe](http://simpy.readthedocs.org/en/latest/examples/process_communication.html) example from the simpy docs.

## How To
If you run the broker file directly, there is a simple example included. This example includes a `Consumer` that represents your modeled component that will subscribe to the topic. Run the example with:
```
python event_broker.py
```
This should result in the output of:
```
Active
Down
Active
```

