import requests
import sys


class MerchantLocation:

    def __init__(self, mid, address):
        self._mid = mid
        self._address = address
        self._formatted_address = None
        self._lat = None
        self._lng = None

    def __str__(self):
        return "Mid:{0} address:{1} formatted_address:{2} lat:{3} lng:{4}".format(self._mid, self._address, self._formatted_address, self._lat, self._lng)

    def __repr__(self):
        return self.__str__()

    def geocoding(self, key):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        payload = {'address': self._address, 'key': key}
        resp = requests.get(url, params=payload)
        if resp.status_code != requests.codes.ok:
            print("ERROR! Response status code: {0} and mid: {1}".format(resp.status_code, self.mid))
            return self
        data = resp.json()
        if data and data['status'] == 'OK':
            results = data['results'][0]
            if "formatted_address" in results:
                self._formatted_address = results['formatted_address']
            if "geometry" in results:
                self._lat = results['geometry']['location']['lat']
                self._lng = results['geometry']['location']['lng']
        else:
            print("ERROR! Google response status: %s and mid: %s" % (data['status'], self.mid))
        return self

    @property
    def mid(self):
        return self._mid

    @property
    def address(self):
        return self._address

    @property
    def formatted_address(self):
        return self._formatted_address

    @property
    def lat(self):
        return self._lat

    @property
    def lng(self):
        return self._lng


def load_input_file(file_path='data/input.txt'):
    try:
        with open(file_path, encoding='utf-8') as lines:
            for line in lines:
                yield str(line).strip().split('\t')
    except IOError as ex:
        print('Load input file error!')
        print(ex)


def main():
    with open(sys.argv[2], "w", encoding="utf-8") as output_data:
        for mid, address in load_input_file(sys.argv[1]):
            ml = MerchantLocation(mid, address)
            if ml.geocoding(sys.argv[3]):
                output_line = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(ml.mid, ml.address, ml.formatted_address, ml.lat, ml.lat)
                print(output_line)
                output_data.write(output_line)


if(__name__ == '__main__'):
    main()
