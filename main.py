import fastapi
from fastapi import FastAPI, HTTPException
from netcalc import Network, Subnet

app = FastAPI()


def isNetmaskValid(net: Network):
    if net.netmask not in range(0, 33):
        raise HTTPException(status_code=400, detail="Invalid netmask")


def isCountOfSubnetsValid(sub: Subnet):
    if sub.netmask + sub.necessaryBits > 32:
        raise HTTPException(status_code=400, detail="Invalid count of subnets")


@app.get('/network/{ip}')
async def getNetwork(ip: str, mask: int):
    net = Network([int(bit) for bit in ip.split('.')], mask)
    isNetmaskValid(net)
    return net.getNetworkDetails()


@app.get('/subnets/{ip}')
async def getSubnets(ip: str, mask: int, subnets: int):
    sub = Subnet([int(bit) for bit in ip.split('.')], mask, subnets)
    isCountOfSubnetsValid(sub)
    return sub.calculateSubnets()

