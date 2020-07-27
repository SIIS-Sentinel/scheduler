# Scheduler

Scheduler is an event generator and scheduler designed for evaluating Sentinel.

Note: while the event generator can be used to automate the generation of realistic traces, it is possible to manually create a trace, if more control is needed.

# Design

This system is made of two components:

## Trace Generation

This component uses a configuration file and to generate a random event trace.

This configuration file contains the user-defined conditions, probabilities, and value ranges of the desired event.

The configuration is then fed to a trace generator, that generates a random event trace based on it. The trace is then stored in a file.

The format of the trace file is one event per line, formatted as JSON, each event having three key-value pairs:
* `ts`: Timestamp at which to send the message
* `value`: Value that should be sent to the MQTT broker
* `target`: MQTT topic to which the value should be send

The events in the generated trace are always ordered by increasing timestamp value. However, this is not a strict requirement, as the event scheduler automatically sorts them when the trace is loaded.

Comments can be added to the trace, by writing a line that is not valid JSON. It is recommented to preface each comment line with a `//`, in order to help readability.

## Event Execution

Once the trace has been generated, it is fed to the event executer, that will start a timer until the first event of the trace. When the timer expires, the runner fires the event to the correct target, and setups a new timer for the following event. 

# Installation

* Create a new virtual environment: `virtualenv venv`
* Activate it: `source venv/bin/activate`
* Install Scheduler : `pip install -e .`

# Usage

## Trace Generation

* Create a schedule configuration file.
* Start a Python shell
* Import the trace generator: `import trace_maker`
* Create a TraceMaker object: `tm = TraceMaker($PATH_TO_CONFIG, $PATH_TO_TRACE, $START_DAY, $DURATION)`, where `$START_DAY` is an integer between 0 and 6, and `$DURATION` is the number of days the trace should last.
* Generate the trace: `tm.generate_trace()`

**Note:** this should ideally be placed in a Python file to make it easier to run and configure

## Scheduler

* Create a trace file
* Create a scheduler configuration file (see `files/scheduler_config.json` for more an example)
* Start a Python shell
* Import the scheduler: `from scheduler.main_scheduler import Scheduler`
* Create a Scheduler: `scheduler = Scheduler($PATH_TO_TRACE, $PATH_TO_CONFIG)`
* Start the scheduler: `scheduler.start()`

**Note:** Some Python scripts made for some specific experiments have already been created and are available in the `experiments/` folder


# Schedule file format

An example of a scheduler can be found in the `files/schedule.json` file.

## Element types
* `one_shot`: an event that fires only once. The trigger time is picked randomly between `time_start` and `time_end`
* `mutli_state`: an event that switches between states at random. At the end of each cycle, a new state is picked among all available, and its duration is picked at random between `min_duration` and `max_duration`
* `periodic_change`: a series of events that represent a value varying linearly between multiple states. Each state's value is picked at random between `min_value` and `max_value`

## Debug option
To run tests on the scheduler, the `debug:bool` argument can be passed at creation time. This will prevent any MQTT action from happening. The MQTT client will be created but will not connect to the broker, nor will any message be sent when an event occurs.

