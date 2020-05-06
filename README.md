# Scheduler
This is an event-driven scheduler designed to evaluate Sentinel. 

# Design

This system is built on two parts:

## Trace Generation

First a schedule configuration is created by the user. This configuration file contains the user-defined conditions, probabilities, and value ranges of the desired event.

The scheduler format is still being designed. 

The configuration is then fed to a trace generator, that will generate a random event trace based on it. The trace is then stored in a file.

The format of the trace file is one event per line, each event having three key-value pairs:
* Timestamp at which to fire
* Value that should be sent
* Target that should receive the value
The events in the trace are always ordered by increasing timestamp value (i.e. first to last to fire).

## Event Execution

Once the trace has been generated, it is fed to the event executer, that will start a timer until the first event of the trace. When the timer expires, the runner fires the event to the correct target, and setups a new timer for the following event. 

# Schedule file format

## Element types
* `one_shot`: an event that fires only once. The trigger time is picked randomly between `time_start` and `time_end`
* `mutli_state`: an event that switches between states at random. At the end of each cycle, a new state is picked among all available, and its duration is picked at random between `min_duration` and `max_duration`
* `periodic_change`: a series of events that represent a value varying linearly between multiple states. Each state's value is picked at random between `min_value` and `max_value`