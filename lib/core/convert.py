import os
import re
import sys
import base64
import codecs
import binascii
import string
import time
import random
import json

from lib.core.settings import IS_WIN
from lib.core.settings import UNICODE_ENCODING
import collections.abc as _collections


def single_time_warn_message(message):
    """
    Cross-linked function
    """
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.flush()


def stdout_encode(data):
    ret = None

    try:
        data = data or ""

        # Reference: http://bugs.python.org/issue1602
        if IS_WIN:
            output = data.encode(sys.stdout.encoding, "replace")

            if '?' in output and '?' not in data:
                warn_msg = "cannot properly display Unicode characters "
                warn_msg += "inside Windows OS command prompt "
                warn_msg += "(http://bugs.python.org/issue1602). All "
                warn_msg += "unhandled occurances will result in "
                warn_msg += "replacement with '?' character. Please, find "
                warn_msg += "proper character representation inside "
                warn_msg += "corresponding output files. "
                single_time_warn_message(warn_msg)

            ret = output
        else:
            ret = data.encode(sys.stdout.encoding)
    except Exception:
        ret = data.encode(UNICODE_ENCODING) if isinstance(data, str) else data

    return ret



def decodeBase64(value, binary=True, encoding=None):
    """
    Returns a decoded representation of provided Base64 value

    >>> decodeBase64("MTIz") == b"123"
    True
    >>> decodeBase64("MTIz", binary=False)
    '123'
    >>> decodeBase64("A-B_CDE") == decodeBase64("A+B/CDE")
    True
    >>> decodeBase64(b"MTIzNA") == b"1234"
    True
    >>> decodeBase64("MTIzNA") == b"1234"
    True
    >>> decodeBase64("MTIzNA==") == b"1234"
    True
    """

    if value is None:
        return None

    padding = b'=' if isinstance(value, bytes) else '='

    # Reference: https://stackoverflow.com/a/49459036
    if not value.endswith(padding):
        value += 3 * padding

    # Reference: https://en.wikipedia.org/wiki/Base64#URL_applications
    # Reference: https://perldoc.perl.org/MIME/Base64.html
    if isinstance(value, bytes):
        value = value.replace(b'-', b'+').replace(b'_', b'/')
    else:
        value = value.replace('-', '+').replace('_', '/')

    retVal = base64.b64decode(value)

    if not binary:
        retVal = getText(retVal, encoding)

    return retVal

def encodeBase64(value, binary=True, encoding=None, padding=True, safe=False):
    """
    返回提供值的Base64编码
    例：
    encodeBase64(b"123") == b"MTIz" >>>  True
    encodeBase64(u"1234", binary=False) >>> 'MTIzNA=='
    encodeBase64(u"1234", binary=False, padding=False) >>> 'MTIzNA'
    encodeBase64(decodeBase64("A-B_CDE"), binary=False, safe=True) >>> 'A-B_CDE'
    """

    if value is None:
        return None

    if isinstance(value, str):
        value = value.encode(encoding or UNICODE_ENCODING)
    retVal = base64.b64encode(value)
    if not binary:
        retVal = getText(retVal, encoding)

    if safe:
        padding = False

        if isinstance(retVal, bytes):
            retVal = retVal.replace(b'+', b'-').replace(b'/', b'_')
        else:
            retVal = retVal.replace('+', '-').replace('/', '_')

    if not padding:
        retVal = retVal.rstrip(b'=' if isinstance(retVal, bytes) else '=')

    return retVal


def getText(value, encoding=None):
    """
    返回给定值的文本值
    """

    retVal = value

    if isinstance(value, bytes):
        retVal = getUnicode(value, encoding)

    return retVal
def getOrds(value):
    """
    返回ORD（…）提供的字符串值的表示形式
    """
    return [_ if isinstance(_, int) else ord(_) for _ in value]

def getUnicode(value, encoding=None, noneToNull=False):
    """
    返回所提供值的unicode表示形式
    """

    if noneToNull and value is None:
        return ''

    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        candidates = filterNone((encoding, UNICODE_ENCODING, sys.getfilesystemencoding()))
        if all(_ in value for _ in (b'<', b'>')):
            pass
        elif any(_ in value for _ in (b":\\", b'/', b'.')) and b'\n' not in value:
            candidates = filterNone((encoding, sys.getfilesystemencoding(), UNICODE_ENCODING))
       
        for candidate in candidates:
            try:
                return str(value, candidate)
            except (UnicodeDecodeError, LookupError):
                pass

        try:
            return str(value, encoding or UNICODE_ENCODING)
        except UnicodeDecodeError:
            return str(value, UNICODE_ENCODING, errors="reversible")
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return str(value)
        except UnicodeDecodeError:
            return str(str(value), errors="ignore")  # 对非基字符串实例忽略编码


def filterNone(values):  
    return [_ for _ in values if _] if isinstance(values, _collections.Iterable) else values

def isListLike(value):  
    return isinstance(value, (list, tuple, set))

def decodeHex(value, binary=True):
    """
    返回提供的十六进制值的解码表示形式
    """
    retVal = value
    if isinstance(value, bytes):
        value = getText(value)

    if value.lower().startswith("0x"):
        value = value[2:]
    try:
        retVal = codecs.decode(value, "hex")
    except LookupError:
        retVal = binascii.unhexlify(value)

    if not binary:
        retVal = getText(retVal)
    return retVal


class WichmannHill(random.Random):

    VERSION = 1     # used by getstate/setstate
    def seed(self, a=None):
        if a is None:
            try:
                a = int(binascii.hexlify(os.urandom(16)), 16)
            except NotImplementedError:
                a = int(time.time() * 256)  # use fractional seconds
        if not isinstance(a, int):
            a = hash(a)

        a, x = divmod(a, 30268)
        a, y = divmod(a, 30306)
        a, z = divmod(a, 30322)
        self._seed = int(x) + 1, int(y) + 1, int(z) + 1

        self.gauss_next = None

    def random(self):
        """获取[0.0,1.0]范围内的下一个随机数"""

        # This part is thread-unsafe:
        # BEGIN CRITICAL SECTION
        x, y, z = self._seed
        x = (171 * x) % 30269
        y = (172 * y) % 30307
        z = (170 * z) % 30323
        self._seed = x, y, z
        # END CRITICAL SECTION

        # Note:  on a platform using IEEE-754 double arithmetic, this can
        # never return 0.0 (asserted by Tim; proof too long for a comment).
        return (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0

    def getstate(self):
        return self.VERSION, self._seed, self.gauss_next

    def setstate(self, state):
        version = state[0]
        if version == 1:
            version, self._seed, self.gauss_next = state
        else:
            pass

    def jumpahead(self, n):
        """
        功能等价调用n次 random() 
        """
        if n < 0:
            raise ValueError("n must be >= 0")
        x, y, z = self._seed
        x = int(x * pow(171, n, 30269)) % 30269
        y = int(y * pow(172, n, 30307)) % 30307
        z = int(z * pow(170, n, 30323)) % 30323
        self._seed = x, y, z

    def __whseed(self, x=0, y=0, z=0):
        """
        从（x，y，z）设置Wichmann Hill种子。这些必须是[0，256]范围内的整数。
        """
        if not type(x) == type(y) == type(z) == int:
            raise TypeError('seeds must be integers')
        if not (0 <= x < 256 and 0 <= y < 256 and 0 <= z < 256):
            raise ValueError('seeds must be in range(0, 256)')
        if 0 == x == y == z:
            # Initialize from current time
            t = int(time.time() * 256)
            t = int((t & 0xffffff) ^ (t >> 24))
            t, x = divmod(t, 256)
            t, y = divmod(t, 256)
            t, z = divmod(t, 256)
        # Zero is a poor seed, so substitute 1
        self._seed = (x or 1, y or 1, z or 1)

        self.gauss_next = None

    def whseed(self, a=None):
        if a is None:
            self.__whseed()
            return
        a = hash(a)
        a, x = divmod(a, 256)
        a, y = divmod(a, 256)
        a, z = divmod(a, 256)
        x = (x + a) % 256 or 1
        y = (y + a) % 256 or 1
        z = (z + a) % 256 or 1
        self.__whseed(x, y, z)


def randomInt(length=4, seed=None):
    """
    返回带有给定位数的随机整数值 
    """
    if seed is not None:
        _ = WichmannHill()
        _.seed(seed)
        choice = _.choice
    else:
        choice = random.choice
    return int("".join(choice(string.digits if _ != 0 else string.digits.replace('0', '')) for _ in range(0, length)))

def randomRange(start=0, stop=1000, seed=None):
    """
    返回给定范围内的随机整数值
    """
    if seed is not None:
        _ = WichmannHill()
        _.seed(seed)
        randint = _.randint
    else:
        randint = random.randint
    return int(randint(start, stop))


def randomStr(length=4, lowercase=False, alphabet=None, seed=None):
    """
    返回带有给定位数的随机字符串
    """

    if seed is not None:
        _random = WichmannHill()
        _random.seed(seed)
        choice = _random.choice
    else:
        choice = random.choice

    if alphabet:
        retVal = "".join(choice(alphabet) for _ in range(0, length))
    elif lowercase:
        retVal = "".join(choice(string.ascii_lowercase) for _ in range(0, length))
    else:
        retVal = "".join(choice(string.ascii_letters) for _ in range(0, length))
    return retVal


def zeroDepthSearch(expression, value):
    retVal = []
    depth = 0
    for index in range(len(expression)):
        if expression[index] == '(':
            depth += 1
        elif expression[index] == ')':
            depth -= 1
        elif depth == 0:
            if value.startswith('[') and value.endswith(']'):
                if re.search(value, expression[index:index + 1]):
                    retVal.append(index)
            elif expression[index:index + len(value)] == value:
                retVal.append(index)
    return retVal

def str2hex_ascii_str(strVal, prefix = "\\x", suffix=""):
    retVal = ""
    if strVal:
        for i in range(len(strVal)):
            strHex = '%02x' % ord(strVal[i])
            retVal += "%s%s%s" % (prefix, strHex, suffix)
            # retVal += "%s%s%s" % (prefix, str(hex(ord(strVal[i])))[2:], suffix)
    return retVal

def str2dec_ascii_str(strVal, prefix = "\\", suffix=""):
    retVal = ""
    if strVal:
        for i in range(len(strVal)):
            retVal += "%s%s%s" % (prefix, str(ord(strVal[i])), suffix)
    return retVal

def str2oct_ascii_str(strVal, prefix = "\\", suffix=""):
    retVal = ""
    if strVal:
        for i in range(len(strVal)):
            retVal += "%s%s%s" % (prefix, str(oct(ord(strVal[i])))[2:], suffix)
    return retVal

def str2hex_unicode_str(strVal, prefix = "\\u", suffix=""):
    retVal = ""
    if strVal:
        for i in range(len(strVal)):
            strHex = '%02x' % ord(strVal[i])
            retVal += "%s%s%s" % (prefix, strHex, suffix)
            # retVal += "%s00%s%s" % (prefix, str(hex(ord(strVal[i])))[2:], suffix)
    return retVal


def str2byte(strVal):
    return str2dec_ascii_str(strVal=strVal, prefix="", suffix=", ").strip().strip(",")

def url_encode(strVal):
    return str2hex_ascii_str(strVal=strVal, prefix="%")


def jsonize(data):
    """
    Returns JSON serialized data
    >>> jsonize({'foo':'bar'})
    '{\\n    "foo": "bar"\\n}'
    """
    return json.dumps(data, sort_keys=False, indent=4)

def dejsonize(data):
    """
    Returns JSON deserialized data
    >>> dejsonize('{\\n    "foo": "bar"\\n}') == {u'foo': u'bar'}
    True
    """
    return json.loads(data)
