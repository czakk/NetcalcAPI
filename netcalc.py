from random import randint
import pprint


class Network:
    BITS = [128, 64, 32, 16, 8, 4, 2, 1]

    def __init__(self, address: list, netmask: int):
        self.address = address
        if netmask in range(0, 33):
            self.netmask = netmask
        else:
            raise ValueError('Netmask must be between 0 and 32')
        self.hosts = (2 ** (32 - netmask) - 2)
        self.broadcast = self.address[:]

    def __str__(self):
        return f'Address IP: {self.address}\nNetmask: {self.netmask}\nHosts: {self.hosts}'

    def calculateNetworkAddress(self):
        for netOctet, maskOctet, octet in zip(self.address, self.calculateNetmask(), range(len(self.address))):
            newOctet = 0
            for netBit, maskBit, bit in zip(decimalToBinaryIn8bits(netOctet), decimalToBinaryIn8bits(maskOctet),
                                            range(8)):
                if netBit == '1' and maskBit == '1':
                    newOctet += self.BITS[bit]
            self.address[octet] = newOctet
        return self.address

    def calculateBroadcastAddress(self):
        self.broadcast = self.calculateNetworkAddress()[:]

        maskToBinary = [decimalToBinaryIn8bits(x) for x in self.calculateNetmask()]
        replaceZeroWithOne = [('1' * x.count('0')).zfill(8 - x.count('0')) for x in maskToBinary]
        convertMaskToDec = [binaryToDecimal(x) for x in replaceZeroWithOne]

        return [bord + mask for bord, mask in zip(self.broadcast, convertMaskToDec)]

    def calculateNetmask(self, addonbits=0):
        netmaskBin = ('1' * (self.netmask + addonbits)) + ('0' * (32 - (self.netmask + addonbits)))
        netmaskDec = ''
        for k, v in enumerate(netmaskBin):
            netmaskDec += v
            if (k + 1) % 8 == 0:
                netmaskDec += '.'
        return [binaryToDecimal(x) for x in netmaskDec[:-1].split('.')]

    def getNetworkDetails(self):
        return {
            'address': '.'.join([
                str(x) for x in self.calculateNetworkAddress()]),
            'netmask': '.'.join([
                str(x) for x in self.calculateNetmask()]),
            'broadcast': '.'.join([
                str(x) for x in self.calculateBroadcastAddress()]),
            'hosts': self.hosts
        }


class Subnet(Network):
    def __init__(self, address: list, netmask: int, subnets: int):
        self.necessaryBits = 1
        while 2 ** self.necessaryBits < subnets:
            self.necessaryBits += 1
        super().__init__(address, netmask)
        self.subnets = subnets

    def getBitsList(self):
        addonBitsList = []
        while len(addonBitsList) != 2 ** self.necessaryBits:
            bits = ''.join([str(randint(0, 1)) for _ in range(self.necessaryBits)])
            if bits in addonBitsList:
                continue
            addonBitsList.append(bits)
        return sorted(addonBitsList)

    def convertBitsListToDec(self):
        bitsList = self.getBitsList()

        subnetMaskToBinary = ''.join([decimalToBinaryIn8bits(x)
                                      for x in self.calculateNetmask(addonbits=self.necessaryBits)])

        masksList = []
        for subnet in range(self.subnets):
            for index, bit in enumerate(list(subnetMaskToBinary)):
                if bit == '0':
                    masksList.append([
                        subnetMaskToBinary.replace(subnetMaskToBinary[index - self.necessaryBits:index + 1],
                                                   bitsList[subnet]) + '0'
                    ])
                    break

        def convertAddressToList(address):
            for i, k in enumerate(address):
                newOctet = ''
                for index, bit in enumerate(k[0]):
                    newOctet += bit
                    if (index + 1) % 8 == 0:
                        newOctet += '.'
                address[i] = newOctet[:-1].split('.')
            return address

        return [[add - net for add, net in zip(x, self.calculateNetmask())]
                for x in [[binaryToDecimal(i) for i in x] for x in convertAddressToList(masksList)]]

    def calculateSubnets(self):
        network = self.getNetworkDetails()
        network['subnets'] = [Network([self.calculateNetworkAddress()[index] + bit
                                       for index, bit in enumerate(self.convertBitsListToDec()[i])],
                                      self.netmask + self.necessaryBits).getNetworkDetails() for i in
                              range(self.subnets)][:self.subnets + 1]
        return network


def binaryToDecimal(binary):
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i]) * 2 ** (len(binary) - i - 1)
    return decimal


def decimalToBinaryIn8bits(decimal):
    return bin(decimal)[2:].zfill(8)

