import random
import urllib.request
import urllib.parse
import urllib.error

__version__ = '0.1.3a1'
__url__ = 'http://pypi.python.org/pypi/randomdotorg'
__all__ = ['RandomDotOrg']
__author__ = "Clovis Fabricio <nosklo at gmail dot com>"
__license__ = "GPL-3"


def _fetch_randomorg(service, **kwargs):
    """Internal function to make a fetch in a random.org service.
    >>> _fetch_randomorg('numbers', num=3, min=10, max=20)
    ['15', '11', '18']
    """
    url = "https://www.random.org/%s/?%s"
    options = dict(format='plain', num=1, col=1,
                   min=0, base=10)  # default options
    options.update(kwargs)
    url = url % (service, urllib.parse.urlencode(options))
    headers = {
        'User-Agent': 'RandomDotOrg.py/%s + %s' % (__version__, __url__)}
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req).read().splitlines()


class RandomDotOrg(random.Random):
    def get_quota(self):
        """
        Returns used bit quota
        """
        return int(_fetch_randomorg('quota')[0])

    def randrange(self, start, stop=None, step=1, ammount=None):
        if stop is None:
            start, stop = 0, start
        xr = range(start, stop, step)
        n = len(xr)
        if n == 0:
            raise ValueError("range is empty")
        if ammount is None:
            nints = 1
        else:
            nints = ammount
        positions = _fetch_randomorg('integers', num=nints, max=n - 1)
        result = [xr[int(pos)] for pos in positions]
        if ammount is None:
            return result[0]
        else:
            return result


results = [0] * 6

for i in range(6):
    results[i] = random.randint(1, 60)

results_randomdotorg = [0] * 6
r = RandomDotOrg('Dice')

for i in range(6):
    results_randomdotorg[i] = r.randrange(1, 60, 1)

print("Mersenne Twister:")
print(results)

print("Random.org:")
print(results_randomdotorg)
