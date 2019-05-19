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


def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    google_key = sys.argv[3]
    with open(output_file_path, "w", encoding="utf-8") as output_data:
        with open(input_file_path, encoding="utf-8") as input_data:
            for input_line in input_data.readlines():
                input_list = input_line.strip().split("\t")
                merc_loca = MerchantLocation(input_list[0], input_list[1])
                if merc_loca.geocoding(google_key):
                    outputStr = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(merc_loca.mid, merc_loca.address, merc_loca.formatted_address, merc_loca.lat, merc_loca.lat)
                    print(outputStr)
                    output_data.write(outputStr)


if(__name__ == '__main__'):
    main()
