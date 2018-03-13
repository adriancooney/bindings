# uWebSockets Python Bindings [#25](https://github.com/uNetworking/bindings/pull/25)

 * These bindings are on [PyPi](https://pypi.python.org/pypi/uWebSockets) for Python 2.7 and Python 3.6
 * `pip2 install uWebSockets` or `pip3 install uWebSockets`

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

#### The eternal struggle
 * Python2 will never disappear, so you have to support it forever
 * Python3 will never be stable, so you have to support it forever

```
Thus farther still upon the outermost
  Head of that seventh circle all alone
  I went, where sat the melancholy folk.
```


