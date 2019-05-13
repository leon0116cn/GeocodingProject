import requests
import sys

class MerchantLocation(object):

    def __init__(self, mid, address):
        self._mid = mid
        self._address = address

    def __str__(self):
        return "Mid:{0} address:{1} formatted_address:{2} lat:{3} lng:{4}".format(self._mid, self._address, self._formatted_address, self._lat, self._lng)

    def geocoding(self, goomap_key):
        geocoding_urltemp = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'
        request_url = geocoding_urltemp.format(self.address, goomap_key)
        print("Google geocoding request is:{0}".format(request_url))
        respons = requests.get(request_url)
        if respons.status_code != 200:
            print("Google geocoding response is ERROR! Response status code is", respons.status_code)
            return
        respons_data = respons.json()
        if respons_data and respons_data['status'] == 'OK':
            results = respons_data['results'][0]
            if "formatted_address" in results:
                self.formatted_address = results['formatted_address']
            if "geometry" in results:
                self.lat = results['geometry']['location']['lat']
                self.lng = results['geometry']['location']['lng']
            print("Google geocoding response json is proccessed WELL!")
        else:
            print("Google geocoding response json is proccessed ERROR!")
            self.formatted_address = ""
            self.lat = ""
            self.lng = ""
        return self

    def get_mid(self):
        return self._mid

    def get_address(self):
        return self._address

    def get_formatted_address(self):
        return self._formatted_address

    def get_lat(self):
        return self._lat

    def get_lng(self):
        return self._lng


def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    google_key = sys.argv[3]
    with open(output_file_path, "w", encoding="utf-8") as output_data:
        with open(input_file_path, encoding="utf-8") as input_data:
            for input_line in input_data.readlines():
                input_list = input_line.strip().split("\t")
                merchantLocation = MerchantLocation(input_list[0], input_list[1])
                if merchantLocation.geocoding(google_key):
                    outputStr = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(merchantLocation.get_mid(), merchantLocation.get_address(), merchantLocation.get_formatted_address(), merchantLocation.get_lat(), merchantLocation.get_lng())
                    print(outputStr)
                    output_data.write(outputStr)


if(__name__ == '__main__'):
    main()





