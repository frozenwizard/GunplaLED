# Developer Setup

The recommended IDE is [Pycharm Community](https://www.jetbrains.com/pycharm). You will need to install the
[micropython plugin](https://plugins.jetbrains.com/plugin/9777-micropython)

## Tooling Installation

The tools needed to build and deploy are the same as the normal installation.  Follow [this](/docs/installation.md#tooling-setup)
for that setup.

## Debugging

Right now, there is no IDE support for debugging remotely and pdb has not been tested.  So all debugging needs to be
done with a Pico board attached and primarily through log or print statements.

The easiest way is to connect the Pico to the computer and run the following commands:

Build and deploy the latest code

```shell
  make build deploy && rshell
```

Navigate to the Pico board file system

```shell
  cd /pyboard
```

Activate the interactive Python interpreter

```shell
repl
```

Import and run the webserver

```python
import main
main.main()
```

The server logs start to appear in the console.
