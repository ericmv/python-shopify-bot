import requests
import json
# from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
#
# from fake_useragent import UserAgent
# ua = UserAgent()

import webbrowser
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

base_url = 'https://ericvu.myshopify.com'
products_url = base_url + 'products.json'
keywords = ['992']
size = "6"
# r = requests.get('https://www.jjjjound.com/pages/closed2')
# print(r)

recaptcha_token = "03AGdBq262AhsDOUHizCJgNaqlVHUHINC7qqH-So8QP5fHTADfi9dPF-nr75pDjXAsWu-P5GvHim_aMwND7JsZGra1Ck-v93k8FKTsZVgp7tE75gxYXwfRGyNsVK7GrsT2tWZfQUIVWvi893iA9AtBV-p3JyrgNpOlm23DaggKd-_p3okne4cezyXCmBxrh-_OwdSKJVhbjxSV8PgpanhbyTdqsdVuGlqqG4PvClQFuhnGa2OnjAAaZcxOUJVm2h0nle8HMNbwLZp5kWLhKSm4UrQoHxfXobVGUW_mtM2zBzmvBdS1ZWUo9zh-FPUQ5-gARkd98aV5wH6IIZ6IWH3Ho0ThPyBGZAR8Rqa7kCOmr2BvBILMboDRXMGezicEMl4c2iwUPcAoifN-umSi1nMhVMqg1IawL_FQk17gNRNsHjNwsjlnPjoOTkNcqLsC4rIPgQw0a1eb-9h9rHLwPUio4spi47ZA0hQpAkgrLmIXHF7zIpEw2f463m52iSXjBOp9Kab-XDtmyzgGPTq2ThbCiYa9sS8RTj3jDX1i3ZXdDMM-Z4fEw9VKDk4vSvs-CRVb0h5-gRNX22bumsV0Fp8SGoN-KiHMIJbNlFxirJa5Hp5X6bYkq-Jlaxc1bHhWxAAzxaRv1M0-7xswRMk7Vi43LOo02HiSmNHkZiZa9Uoyf2rvK2E1YdXuNcU5Pc6xQeVjgJ1c-tF4DaW8fKp_H3CItSGKD0nvXNpKH8y8CNUU8xpHpT22kEUjbCW4ESF86Ek2nPApOWAWyIRUBGgpO6xKpzveUFNIev-t0D4k5SilyaVSWc2olmolTArYkn8MCkb18FMzfWmVXqKPOgCL1iDghLXwMlO5ccpE9cMc5RSWJprW6v26RH193dw3CclzLOjqCmFuEKl7FA7tAYIyK1Fe-yIQ82BWJSMDxHDoPEu2qrWuU9-UIjtpTFv-DaY1sHJ_U1sf5Sgdvqo2gau9h9CGn0lJ2xJT3BB-QUdN9Nh9w3KY9OuUZEUEy3d-nH3w-GcYrxbe7-kpXpYOd8PkMxD1IlLm3Tnpvk0922G-duqGe5bpYYqHsjN_InbAG3fTfJnThEK6xWdygxR6lqxsXN97HAHu1Dnzoh0JUDhh7WycjbZsuZ7jGom-dTYFa3Mji4nx7m1i1X65HGU_8zGYSSAnDGyXgdPqKDhWIVwq_rPi-A_X0IsXUztWwzgHXhMcrGTYayyG-LvlnpGTBUSUhALpxqAnqYnoxOqr34nTEVJwbDmfRVYudt5jN77MJyj31ZdnYAteXUxH7LyJ_iXar8QPGLm8J_tSIJly7eKYnN8mOLJkdTucHEFsMNwCpAhqfCI_rjDLe0kCaPI_oeR2BQ7W0HpTfuNeabr5GFLk2tHvHHdYBkxveCyWCceMO9H9pJIirHRasUEZ8YZS92AY-kwXRlWi-6qMAkR0_PdgrzfmNXLlu9IvT4gkHfTGxB5aJAmc-4snD1o8mt0l77HZXJkaOkpDOAwdDpMN-qxnwple0z5WTJx0obTXZIitbnCjM4AjHTsMMhP-NE9s4SGwVJgpVcFp9z2RwQy7NBkjAD2t__0Xw-DAYSVy5oeNXhgKfVYnBeUCUmCxMLRPAQJdB6KYPl7GnTqXg_ogOaTa6svJCK6r1ZJ4nZe_jx8tOHU-9mk0iKO5xZCsQPc3Zjuh7RMUH9YLG4kHyxoA0Y_tyUseDZ2SJxpzz-gIkv08lDDEEh1AriCHc6Iqj75dH9vto3fVDAS_nTrhjQGszw"

profile = {
    "email": "ericvooo@gmail.com",
    "first": "Eric",
    "last": "Vu",
    "address": "518 Pierpont Dr.",
    "city": "Costa Mesa",
    "state": "California",
    "zip": "92626",
    "phone": "7142712256"
}


def preload_payment(session):
        # link = "https://elb.deposit.shopifycs.com/sessions"
        link = "https://deposit.us.shopifycs.com/sessions"
        payload = {
            "credit_card": {
                "number": "1",
                "name": "Bogus Gateway",
                "month": 1,
                "year": 2022,
                "verification_value": "123"
            }
        }
        r = session.post(link, json=payload, verify=False)
        print(r.text)
        return json.loads(r.text)["id"]

def availability_check(base_url, keywords):
    '''Gets the products for the specified store and looks for keyword match on products
        title. If match is found, return the product's variant list. If not, return None'''
    # header = {'user-agent': ua.chrome}
    proxies = {
      'http': '162.243.171.1',
      'https': '162.243.171.1'
    }
    try:
        r = requests.get(base_url + '/products.json', verify=False);
        products = json.loads(r.text)["products"]
        for p in products:
            product_name = p["title"].lower()
            if all(x in product_name for x in keywords):
                handle = p["handle"]
                productUrl = base_url + '/products/' + handle
                # webbrowser.get(chrome_path).open(productUrl)
                return p["variants"]
        return None
    except:
        print("Error getting products")
        return None

def find_size(variants, size):
    # variants is a list of dicts
    '''For a given list of variants, find a size match and return the id of the variant.
        If there is no match, return None'''
    for v in variants:
        if size in v["title"]:
            print('Found size!')
            return str(v["id"])
    return None


def add_to_cart(session, site, product_id):
    '''Given a product variant id, add that product to the cart via shopify http request'''
    add_to_cart_url = site + "/cart/add.js?id=" + product_id
    added_to_cart = False
    while not added_to_cart:
        r = session.get(add_to_cart_url)
        data = json.loads(r.text)
        try:
            quantity = data["quantity"]
            if quantity >= 1:
                added_to_cart = True
                print("Added to cart")
        except:
            print('Error adding to cart. Retrying...')
            time.sleep(1)

def fill_customer_info(session, checkout_url, profile, recaptcha_token=None):
    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "contact_information",
        "step": "shipping_method",
        "checkout[email_or_phone]": profile["email"],
        "checkout[buyer_accepts_marketing]": "0",
        "checkout[shipping_address][first_name]": profile["first"],
        "checkout[shipping_address][last_name]": profile["last"],
        "checkout[shipping_address][company]": "",
        "checkout[shipping_address][address1]": profile["address"],
        "checkout[shipping_address][address2]": "",
        "checkout[shipping_address][city]": profile["city"],
        "checkout[shipping_address][country]": "United States",
        "checkout[shipping_address][province]": profile["state"],
        "checkout[shipping_address][zip]": profile["zip"],
        "checkout[shipping_address][phone]": profile["phone"],
        "checkout[remember_me]": "0",
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][browser_tz]": "420",
        "checkout[client_details][color_depth]": "30",
        "checkout[client_details][javascript_enabled]": "1",
        "button": ""
    }
    if recaptcha_token:
        payload["g-recaptcha-response"] = recaptcha_token
    return session.post(checkout_url, data=payload, allow_redirects=True)

def choose_shipping_method(session, site, checkout_url):
    link = site + "//cart/shipping_rates.json?shipping_address[zip]={}&shipping_address[country]={}&shipping_address[province]={}".format("92626","United States","California")
    r = session.get(link, verify=False)
    shipping_options = json.loads(r.text)
    ship_opt = shipping_options["shipping_rates"][0]["name"].replace(' ', "%20")
    ship_prc = shipping_options["shipping_rates"][0]["price"]
    shipping_option = "shopify-{}-{}".format(ship_opt,ship_prc)
    return shipping_option

def submit_shipping(session, checkout_url, shipping_option):
    payload = {
        "utf8": u'\u2713',
        "_method": "patch",
        "previous_step": "shipping_method",
        "step": "payment_method",
        "checkout[shipping_rate][id]": shipping_option,
        "g-recaptcha-repsonse": "",
        "button": ""
    }
    return session.post(checkout_url, data=payload, allow_redirects=True)

def submit_payment(session, checkout_url, payment_token, payment_gateway, authenticity_token, isRetry):
    payload = {
        "utf8": u'\u2713',
        "_method": "patch",
        "previous_step": "payment_method",
        "step": "",
        "s": payment_token,
        "authenticity_token": authenticity_token,
        "checkout[payment_gateway]": payment_gateway,
        "checkout[different_billing_address]": "false",
        'checkout[credit_card][vault]': 'false',
        "complete": "1",
        "checkout[client_details][browser_width]": '979',
        "checkout[client_details][browser_height]": '631',
        "checkout[client_details][javascript_enabled]": "1",
        "g-recaptcha-repsonse": "",
        "button": ""
    }
    # if not isRetry:
    #     payload["s"] = payment_token
    r = session.post(checkout_url, data=payload, verify=False, allow_redirects=True)
    return r

def check_for_stock(session, url, response):
    while "stock_problems" in response.url:
        print('item is out of stock now. Refreshing...')
        time.sleep(1)
        response = session.get(url, verify=False, allow_redirects=True)
    print('Item in stock! Continuing...')
    return response

def run():
    s = requests.session()
    variants = None
    while variants is None:
        variants = availability_check(base_url, keywords)
        if variants is None:
            print('product not loaded yet...')
            time.sleep(5)
        else:
            print('product is LOADED!')

    variant_id = find_size(variants, size)
    if (variant_id is None):
        print("Could not find specified size")
        return
    else:
        print("Found correct size! ID is: " + variant_id)

    add_to_cart(s, base_url, variant_id)

    # product is in cart at this point
    site_checkout = base_url + "/checkout"
    r = s.get(site_checkout, verify=False)

    while "stock_problems" in r.url:
        print('Item is out of stock. Retrying...')
        time.sleep(1)
        r = s.get(site_checkout, verify=False)

    print("item still in stock!")
    checkout_url = r.url
    print("checkout landing url %s", r.url)

    # input('submit info?')
    info_response = fill_customer_info(s, checkout_url, profile, recaptcha_token)
    print('info_response', info_response.url)
    return
    check_for_stock(s, checkout_url, info_response)

    # input('submit shipping?')
    shipping_method = choose_shipping_method(s, base_url, checkout_url)
    shipping_response = submit_shipping(s, checkout_url, shipping_method)
    check_for_stock(s, checkout_url, shipping_response)

    # bs = soup(shipping_response.text, "html.parser")
    # radio_input = bs.find('input', {"name": "checkout[payment_gateway]"})
    # payment_gateway = radio_input["value"]

    # print(shipping_response.url)

    # prepaid payment already
    e = input("Continue to submit payment?")

    payment_success = False
    isRetry = False
    while payment_success == False:
        payment_token = preload_payment(s)

        bs = soup(shipping_response.text, "html.parser")
        authenticity_token = bs.find('input', {"name":"authenticity_token"})['value']
        radio_input = bs.find('input', {"name": "checkout[payment_gateway]"})
        payment_gateway = radio_input["value"]

        payment_response = submit_payment(s, checkout_url, payment_token, payment_gateway, authenticity_token, isRetry)
        # print(payment_response.text)
        print(payment_response.url)
        if "stock_problems" in payment_response.url:
            shipping_response = check_for_stock(s, checkout_url, payment_response)
        else:
            payment_success = True

    print("Order finished!")
    # print(payment_response.status_code)
    # print(payment_response.history)


run()
