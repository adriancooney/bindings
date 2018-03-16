# uWebSockets Python Bindings [#25](https://github.com/uNetworking/bindings/pull/25)

 * These bindings are on [PyPi](https://pypi.python.org/pypi/uWebSockets) for Python 2.7 and Python 3.6
 * `pip2 install uWebSockets` or `pip3 install uWebSockets`
 
## IMPORTANT ##
 * If you think you found a bug in a binary wheel package on PyPi, please first try to reproduce it after downloading the `tar.gz` version of the package.
This is essential because the `manylinux1` wheels are basically a giant hack and may behave differently.
 * While we are compatible with `manylinux1` in terms of the ABI versioning, we might not be compatible with ancient linux kernel versions that don't support `eventfd`


## Usage:

 * See [test_client.py](tests/test_client.py)
 * The API mimics `websocket-client` as closely as possible (except we always exit on exceptions).
   1. The object must be provided a URI at initialisation eg: `MyWebSocket("wss://echo.websocket.org")`
   2. `on_open()` called when opened (if defined)
   3. `on_message(message)` called on messages (if defined)
   4. `on_close()` called on clean exit (if defined)
   5. `send(message)` send message if possible
   6. `close()` close socket, idempotent
       **Warning** Once the socket is closed, it can't be re-opened - you have to make a new one.
       
 * This is not optimized at all but it's already better than `websocket-client` due to the upstream `uWebSockets` being so good.


## Compiling from Source

### Linux x86_64
 * Either use the provided vagrant/docker setup and `make all-vagrant` or:
   * Install `g++ gcc make git libssl-dev libuv1-dev python python-pip python3 python3-pip python3-all-dev python2.7-dev`
     * `make wheels`
 
### Windoze
 * Install the dependencies listed [here](./windoze.md)
   * Full guide from http://cowboyprogrammer.org/building-python-wheels-for-windows/
 * `cmd /c build-all-wheels.bat`
     
### OSX
 * Use [brew](https://brew.sh/) to install development libraries / gcc
 * `make wheels`

## Complaints/Support
 * This is a third party binding, which is seperate from the main uWebSockets project (and also the node binding)
   * See [#25](https://github.com/uNetworking/bindings/pull/25)
   * Tag issues with Python bindings to @szmoore
   * See the [section above](#Important) about `manylinux1` issues.

#### The eternal struggle
 * Python2 will never disappear, so you have to support it forever
 * Python3 will never be stable, so you have to support it forever

```
Thus farther still upon the outermost
  Head of that seventh circle all alone
  I went, where sat the melancholy folk.
```


