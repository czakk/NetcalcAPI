import unittest
import netcalc


class NumeralSystemConvertTest(unittest.TestCase):
    def test_binaryToDecimal(self):
        self.assertEqual(netcalc.binaryToDecimal('1010'), 10)

    def test_decimalToBinaryIn8bits(self):
        self.assertEqual(netcalc.decimalToBinaryIn8bits(10), '00001010')


class NetworkTest(unittest.TestCase):
    def test_network_init(self):
        net = netcalc.Network([192, 168, 16, 16], 24)

        self.assertEqual(net.address, [192, 168, 16, 16])
        self.assertEqual(net.netmask, 24)

        self.assertEqual(net.broadcast, [192, 168, 16, 16])
        self.assertEqual(net.hosts, 254)

    def test_calculateNetworkAddress(self):
        net = netcalc.Network([192, 168, 16, 16], 24)
        self.assertEqual(net.calculateNetworkAddress(), [192, 168, 16, 0])

    def test_calculateBroadcastAddress(self):
        net = netcalc.Network([192, 168, 16, 16], 24)
        self.assertEqual(net.calculateBroadcastAddress(), [192, 168, 16, 255])

    def test_calculateNetmask(self):
        net = netcalc.Network([192, 168, 16, 16], 24)
        self.assertEqual(net.calculateNetmask(), [255, 255, 255, 0])

    def test_getNetworkDetails(self):
        net = netcalc.Network([192, 168, 15, 100], 26)
        self.assertEqual(net.getNetworkDetails(),
                         {'address': '192.168.15.64',
                          'netmask': '255.255.255.192',
                          'broadcast': '192.168.15.127',
                          'hosts': 62})


class SubnetTest(unittest.TestCase):
    def test_getDecBitsList(self):
        sub = netcalc.Subnet([192, 168, 15, 100], 23, 4)
        self.assertEqual(sub.convertBitsListToDec(), [
            [0, 0, 0, 0],
            [0, 0, 0, 128],
            [0, 0, 1, 0],
            [0, 0, 1, 128],
        ])

    def test_calculateSubnet(self):
        sub = netcalc.Subnet([192, 168, 15, 100], 23, 4)
        self.assertEqual(sub.calculateSubnets(), {'address': '192.168.14.0',
                                                  'broadcast': '192.168.15.255',
                                                  'hosts': 510,
                                                  'netmask': '255.255.254.0',
                                                  'subnets': [{'address': '192.168.14.0',
                                                               'broadcast': '192.168.14.127',
                                                               'hosts': 126,
                                                               'netmask': '255.255.255.128'},
                                                              {'address': '192.168.14.128',
                                                               'broadcast': '192.168.14.255',
                                                               'hosts': 126,
                                                               'netmask': '255.255.255.128'},
                                                              {'address': '192.168.15.0',
                                                               'broadcast': '192.168.15.127',
                                                               'hosts': 126,
                                                               'netmask': '255.255.255.128'},
                                                              {'address': '192.168.15.128',
                                                               'broadcast': '192.168.15.255',
                                                               'hosts': 126,
                                                               'netmask': '255.255.255.128'}]})


if __name__ == '__main__':
    unittest.main()
