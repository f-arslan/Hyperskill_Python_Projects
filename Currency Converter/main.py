import requests


class Bank(object):
    def __init__(self):
        self.rate = {}  # keep the rate of values after processing.
        self.cache = {}  # keep the default usd and eur cache values.
        Bank.usd_eur_cache(self)  # automatically generated.

    def run(self):
        main_cur = input()
        while True:
            temp_cur = input()
            if temp_cur == '':
                return 0
            amount = float(input())
            print("Checking the cache...")
            Bank.cache_checking(self, main_cur, temp_cur, amount)

    def cache_checking(self, main_cur, cur, amount):
        cur = cur.lower()
        main_cur = main_cur.lower()
        current = ['usd', 'eur']
        # check the main and temp currency in cache dict.
        check_current_cache = (main_cur in self.cache and cur in self.cache)
        # if rate is adding the rate dict than pass or temp currency in current values and main cur not in currency
        check_current = (
            cur in current and main_cur not in current) or cur in self.rate
        if check_current or check_current_cache:
            print("Oh! It is in the cache!")
            if cur in current and main_cur not in current:
                # if the temp in current, we will divide the amount the cur_rate in cache.
                given_cur_rate = float(self.cache[cur][main_cur]['rate'])
                print(
                    f"You received {round(amount / given_cur_rate, 2)} {cur}.")
            elif cur in current and main_cur in current:
                # if the both currency in current then, we will product
                given_cur_rate = float(self.cache[main_cur][cur]['rate'])
                self.rate[cur] = given_cur_rate
                print(
                    f"You received {round(given_cur_rate * amount, 2)} {cur.upper()}.")
            else:
                # if currency in rate dict.
                given_cur_rate = float(self.rate[cur])
                self.rate[cur] = given_cur_rate
                print(
                    f"You received {round(given_cur_rate * amount, 2)} {cur.upper()}.")

        elif cur not in self.rate:
            # if not in the rate dict.
            print("Sorry, but it is not in the cache!")
            address = "http://www.floatrates.com/daily/"
            req = requests.get(address + main_cur + ".json")
            json_file = req.json()
            given_cur_rate = float(json_file[cur]['rate'])
            print(
                f"You received {round(given_cur_rate * amount, 2)} {cur.upper()}.")
            self.rate[cur] = given_cur_rate

    # Adding the cache dict for default.
    def usd_eur_cache(self):
        address = "http://www.floatrates.com/daily/"
        for i in ['usd', 'eur']:
            req = requests.get(address + i + ".json")
            json_file = req.json()
            self.cache[i] = json_file


# run the program.
def main():
    bank = Bank()
    bank.run()


if __name__ == '__main__':
    main()
