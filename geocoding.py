import requests


GOOGLE_KEY = 'AIzaSyC_fPG4fhLPLR5p9SdZK51xSez1M0DtEIs'
GOOGLE_GEOCODING_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'


class MerchantLocation:

    def __init__(self, mid, address):
        self.mid = mid
        self.address = address

    def __str__(self):
        return "Mid:{0} address:{1} formatted_address:{2} lat:{3} lng:{4}".format(self.mid, self.address, self.formatted_address, self.lat, self.lng)

    def geocoding(self):
        request_url = GOOGLE_GEOCODING_URL.format(self.address, GOOGLE_KEY)
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
        return self.mid

    def get_address(self):
        return self.address

    def get_formatted_address(self):
        return self.formatted_address

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng


def main():
    with open("output.dat", "w", encoding="utf-8") as output_data:
        with open("input.dat", encoding="utf-8") as input_data:
            for input_line in input_data.readlines():
                input_list = input_line.strip().split("\t")
                merchantLocation = MerchantLocation(input_list[0], input_list[1])
                if merchantLocation.geocoding():
                    outputStr = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(merchantLocation.get_mid(), merchantLocation.get_address(), merchantLocation.get_formatted_address(), merchantLocation.get_lat(), merchantLocation.get_lng())
                    print(outputStr)
                    output_data.write(outputStr)


if(__name__ == '__main__'):
    main()





