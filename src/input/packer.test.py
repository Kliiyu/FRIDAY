import unittest
from packer import Packet

class TestPacket(unittest.TestCase):
    def test_verify_with_text(self):
        packet = Packet(text="Hello, world!")
        self.assertTrue(packet.verify())

    def test_verify_without_text(self):
        packet = Packet(text="")
        self.assertFalse(packet.verify())

if __name__ == '__main__':
    unittest.main()