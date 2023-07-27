class ConfigVariables:
    # ----Elastic search cong
    elasticsearch_url = "https://elastic.noc.vpgrp.io:443"
    # elasticsearch_url = ""
    index_name = 'foundation-qa-salescheck'

    # ---- Tools
    retry = 3
    number_elements_to_test = 10

    # ---- Web conf
    vp_fr_url = "https://www.veepee.fr"
    vp_es_url = "https://www.veepee.es"
    vp_privalia_url_es = "https://es.privalia.com"
    vp_privalia_url_it = "https://it.privalia.com"
    vp_it_url = "https://www.veepee.it"

    vp_home_default = "/gr/home/default"
    vp_sites_root_url = ["https://www.veepee.fr"]
    vp_sites_map = {
        "DEBUG": {
            "country": "France",
            "front_preprod_url": "https://core-groot-nav-preprod.front.vpgrp.io",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.es@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "FR": {
            "country": "France",
            "vp_site_preprod_url": "https://preprod.veepee.fr",
            "vp_site_root_url": "https://www.veepee.fr",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.software.20@gmail.com",
            "pass": "VQRw7G9Zk6ZTas9!"
        },
        "ES": {
            "country": "Spain",
            "vp_site_preprod_url": "https://preprod.veepee.es",
            "vp_site_root_url": "https://www.veepee.es",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.es@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "PRIVALIA-ES": {
            "country": "PRIVALIA-Spain",
            "vp_site_preprod_url": "https://preprod-es.privalia.com",
            "vp_site_root_url": "https://es.privalia.com",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.es@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "PRIVALIA-IT": {
            "country": "PRIVALIA-italy",
            "vp_site_preprod_url": "https://preprod.veepee.es",
            "vp_site_root_url": "https://it.privalia.com",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.it@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "IT": {
            "country": "Italy",
            "vp_site_root_url": "https://www.veepee.it",
            "vp_site_preprod_url": "https://preprod.veepee.it",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.it@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "DE": {
            "country": "Germany",
            "vp_site_preprod_url": "https://preprod.veepee.de",
            "vp_site_root_url": "https://www.veepee.de",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.de@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "AT": {
            "country": "Austria",
            "vp_site_preprod_url": "https://preprod.veepee.at",
            "vp_site_root_url": "https://www.veepee.at",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.at@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "NL": {
            "country": "Netherlands",
            "vp_site_preprod_url": "https://preprod.veepee.nl",
            "vp_site_root_url": "https://www.veepee.nl",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.nl@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "LU": {
            "country": "Luxembourg",
            "vp_site_preprod_url": "https://preprod.veepee.lu",
            "vp_site_root_url": "https://www.veepee.lu",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.lu@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "BE": {
            "country": "Belgium",
            "vp_site_preprod_fr_url": "https://preprod-fr.veepee.be",
            "vp_site_preprod_nl_url": "https://preprod-nl.veepee.be",
            "vp_site_root_url": "https://nl.veepee.be",
            "vp_site_travel_top_menu": "/gr/home/travel",
            "user": "automation.vp.be@mail.com",
            "pass": "@Ut0mati0n.es"
        }
    }
    url_exceptions = [
        "/web/catalog/v1/sale/",
        "bit.ly",
        "club.veepee.fr",
        "ad.doubleclick.net",
        "clarins.commander",
        "experiences",
        "appvp://operation/",
        "coccinelle.com",
        "tinyurl.com",
        "clarins.commander",
        "ad.doubleclick",
        "greenchef",
        "go.nordvpn",
        "it.soshape.com",
        "peugeot",
        ".ly/"
    ]
    url_home_exceptions = [
        '/gr/home/catalog',
        '/gr/home/fashion',
        '/gr/home/sport',
        '/gr/home/kids',
        '/gr/home/life',
        '/gr/home/gas',
        '/gr/home/eve',
        '/gr/home/shoes',
        '/gr/home/home',
        'travel',
        'redirect',
        'media'
    ]

    def __init__(self):
        self.data = []
