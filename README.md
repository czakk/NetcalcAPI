
# NetcalcAPI

"Netcalc" is calculator of network address, netmask, broadcast address, number of hosts and subnets.
 


## Running server

`uvicorn main:app --reload` - Run server with tracking changes in code

`http://localhost:8000/docs` - API documentation


## Usage/Examples

## First Example

### Provide

`http://localhost:8000/network/164.247.101.142?mask=24`

### Recive
```
{
  "address": "164.247.101.0",
  "netmask": "255.255.255.0",
  "broadcast": "164.247.101.255",
  "hosts": 254
}
```

## Second Example
### Provide
`http://localhost:8000/subnets/192.168.0.68?mask=24&subnets=4`
### Recive
```
{
  "address": "192.168.0.0",
  "netmask": "255.255.255.0",
  "broadcast": "192.168.0.255",
  "hosts": 254,
  "subnets": [
      {
      "address": "192.168.0.0",
      "netmask": "255.255.255.192",
      "broadcast": "192.168.0.63",
      "hosts": 62
      },
      {
      "address": "192.168.0.64",
      "netmask": "255.255.255.192",
      "broadcast": "192.168.0.127",
      "hosts": 62
      },
      {
      "address": "192.168.0.128",
      "netmask": "255.255.255.192",
      "broadcast": "192.168.0.191",
      "hosts": 62
      },
      {
      "address": "192.168.0.192",
      "netmask": "255.255.255.192",
      "broadcast": "192.168.0.255",
      "hosts": 62
      }
  ]
}


