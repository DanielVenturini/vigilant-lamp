import json
import unittest
import os.path as path
import subprocess as sp

class PythonTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # execute the lampy and resolve the package.json
        # sp.call(['python3', path.join('..', 'lamp.py'), 'package.json'])
        test_file = path.join('test', 'package.json')
        sp.call(['python3', 'lamp.py', test_file])

        self.file = open(test_file)
        self.package = json.load(self.file)
        self.msg = 'The resolved version of {0} should be {1}, but got {2} instead'

    @classmethod
    def tearDownClass(self):
        self.file.close()

    '''
    n, m and o represents a constants
    x represents a range
    '''

    # test for the range ^n.m.o
    def test_express(self):
        # Arrange
        version = self.package['dependencies']['express']
        # Act
        resolved = '4.13.0'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('express', resolved, version))

    # test for the range ~n.m.o
    def test_lodash(self):
        # Arrange
        version = self.package['dependencies']['lodash']
        # Act
        resolved = '3.9.3'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('lodash', resolved, version))

    # test for a specify range n.m.o
    def test_mocha(self):
        # Arrange
        version = self.package['devDependencies']['mocha']
        # Act
        resolved = '2.2.0'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('mocha', resolved, version))

    # test for a unexisted range in specify date
    def test_mongoose(self):
        # Arrange
        version = self.package['devDependencies']['mongoose']
        # Act
        resolved = '^4.5.9'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('mongoose', resolved, version))

    # test for the range ^n.x
    def test_socket_io(self):
        # Arange
        version = self.package['peerDependencies']['socket.io']
        # Act
        resolved = '1.3.5'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('socket.io', resolved, version))

    # test for the range n.x
    def test_jsdom(self):
        # Arange
        version = self.package['peerDependencies']['jsdom']
        # Act
        resolved = '4.5.2'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('jsdom', resolved, version))

    # test for the range *
    def test_react(self):
        # Arange
        version = self.package['dependencies']['react']
        # Act
        resolved = '0.13.3'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('react', resolved, version))

    # test for the range latest
    def test_validate_npm_pn(self):
        # Arange
        version = self.package['optionalDependencies']['validate-npm-package-name']
        # Act
        resolved = '2.2.1'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('validate-npm-package-name', resolved, version))

    # test for the range >= n.m
    def test_mongodb(self):
        # Arange
        version = self.package['optionalDependencies']['mongodb']
        # Act
        resolved = '2.0.35'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('mongodb', resolved, version))

    # test for the range ^n.x || ^n
    def test_jsdom_other(self):
        # Arange
        version = self.package['optionalDependencies']['jsdom']
        # Act
        resolved = '5.5.0'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('jsdom', resolved, version))

    # test for pre-releases resolving to release
    def test_grunt(self):
        # Arange
        version = self.package['peerDependencies']['grunt']
        # Act
        resolved = '0.4.5'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('grunt', resolved, version))

    # test for pre-releases resolving to release
    def test_react_pre(self):
        # Arange
        version = self.package['optionalDependencies']['react']
        # Act
        resolved = '0.13.3'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('react', resolved, version))

    # test for pre-releases resolving to pre-releases
    def test_react_pre(self):
        # Arange
        version = self.package['devDependencies']['karma']
        # Act
        resolved = '0.13.0-rc.6'
        # Assert
        self.assertEqual(version, resolved, self.msg.format('karma', resolved, version))


if __name__ == '__main__':
    unittest.main()