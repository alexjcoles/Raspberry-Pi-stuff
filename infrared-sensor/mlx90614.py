"""
Simple Micropython MLX90614 Library
https://github.com/CAATZ/Simple-Micropython-MLX90614-Library

MIT License

Copyright (c) 2022 CAATZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ustruct
import time

class MLX90614:

    _REGISTER_RAW1 = 0x04
    _REGISTER_RAW2 = 0x05
    _REGISTER_TA = 0x06
    _REGISTER_TOBJ1 = 0x07
    _REGISTER_TOBJ2 = 0x08
    _REGISTER_TOMAX = 0x20
    _REGISTER_TOMIN = 0x21
    _REGISTER_PWMCTRL = 0x22
    _REGISTER_TARANGE = 0x23
    _REGISTER_EMISSIVITY = 0x24
    _REGISTER_CONFIG = 0x25
    _REGISTER_BUSADD = 0x2E
    
    _CONFIG = {"IIR": {"size":7, "location":0},
               "RST": {"size":1, "location":3},
               "PWM": {"size":3, "location":3},
               "DUZ": {"size":1, "location":6},
               "KSS": {"size":1, "location":7},
               "FIR": {"size":7, "location":8},
               "GAI": {"size":7, "location":11},
               "KTS": {"size":1, "location":14},
               "EST": {"size":1, "location":15},
               "ALL": {"size":65535, "location":0}}
    
    def __init__(self, i2c, address=0x5a):
        self.i2c = i2c
        self.address = address
        _config1 = i2c.readfrom_mem(address, self._REGISTER_CONFIG, 2)
        _dz = ustruct.unpack('<H', _config1)[0] & (1<<6)
        self.dual_zone = True if _dz else False
        
    def read16(self, register):
        _data = self.i2c.readfrom_mem(self.address, register, 2)
        return ustruct.unpack('<H', _data)[0]

    def read_temp(self, register):
        _temp = self.read16(register)
        _temp *= .02
        _temp -= 273.15
        return _temp
    
    def read_raw1(self):
        return self.read16(self._REGISTER_RAW1)
    
    def read_raw2(self):
        if self.dual_zone:
            return self.read16(self._REGISTER_RAW2)
        else:
            raise RuntimeError("Device only has one thermopile")

    def read_ambient_temp(self):
        return self.read_temp(self._REGISTER_TA)

    def read_object_temp(self):
        return self.read_temp(self._REGISTER_TOBJ1)

    def read_object2_temp(self):
        if self.dual_zone:
            return self.read_temp(self._REGISTER_TOBJ2)
        else:
            raise RuntimeError("Device only has one thermopile")
               
    def read_emissivity(self):  
        return self.read16(self._REGISTER_EMISSIVITY)
    
    def read_address(self):  
        return self.read16(self._REGISTER_BUSADD) & 0x00FF
    
    def read_config(self, val="ALL"):  
        _config = self.read16(self._REGISTER_CONFIG)
        _size = self._CONFIG[val]["size"]
        _location = self._CONFIG[val]["location"]
        _data = _config & (_size<<_location)
        return _data >> _location
    
    def write_eeprom(self, register, data):
        clear = 0x0000
        
        pec = 0
        pec = self._crc8(pec, self.address<<1)
        pec = self._crc8(pec, register)
        pec = self._crc8(pec, clear & 0xFF)
        pec = self._crc8(pec, clear >> 8)
        
        buffer = bytes([0x00, 0x00, pec])
        
        self.i2c.writeto_mem(self.address, register, buffer)
        
        time.sleep(0.1)

        pec = 0
        pec = self._crc8(pec, self.address<<1)
        pec = self._crc8(pec, register)
        pec = self._crc8(pec, data & 0xFF)
        pec = self._crc8(pec, data >> 8)
        
        buffer = bytes([data & 0xFF, data >> 8, pec])
        
        self.i2c.writeto_mem(self.address, register, buffer)
        
        time.sleep(0.1)
        
    def write_emissivity(self, emissivity):
        if (emissivity <= 65535) and (emissivity >= 0):
            self.write_eeprom(self._REGISTER_EMISSIVITY, emissivity)
            time.sleep(0.1)
            return self.read_emissivity()
        else:
            raise RuntimeError("Value out of range")

    def write_config(self, val):  
        _size = self._CONFIG[val]["size"]
        _location = self._CONFIG[val]["location"]
        
        if (val <= _size) and (val >= 0):            
            _config1 = self.read16(self._REGISTER_CONFIG)
            _clear = (_config1 & ~(_size<<_location))
            _data = (val<<8) | _clear        
            
            self.write_eeprom(self._REGISTER_CONFIG, _data)
            
        else:
            raise RuntimeError("Value out of range")
        
    def write_address(self, address):
        if (address <= 127) and (address >= 0):
            _oldadd = self.read16(self._REGISTER_BUSADD)
            _temp = _oldadd & 0xFF00
            _newadd = _temp | address
            self.write_eeprom(self._REGISTER_BUSADD, _newadd)
        else:
            raise RuntimeError("Value out of range")

    def _crc8(self, icrc, data):
        crc = icrc ^ data
        for _ in range(8):
            crc <<= 1
            if crc & 0x0100:
                crc ^= 0x07
            crc &= 0xFF
        return crc 
