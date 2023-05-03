class ConfigVariables:
    # ----Elastic search cong
    elasticsearch_url = "https://elastic-test.noc.vpgrp.io:443"
    index_name = 'foundation-qa-salescheck'

    # ---- Web conf
    vp_fr_url = "https://www.veepee.fr"
    vp_es_url = "https://www.veepee.es"
    vp_privalia_url_es = "https://es.privalia.com"
    vp_privalia_url_it = "https://it.privalia.com"
    vp_it_url = "https://www.veepee.it"
    vp_de_url = "https://www.veepee.de"
    vp_at_url = "https://www.veepee.at"
    vp_nl_url = "https://www.veepee.nl"
    vp_lu_url = "https://www.veepee.lu"
    vp_be_url = "https://www.veepee.be"
    vp_home_default = "/gr/home/default"
    vp_sites_root_url = ["https://www.veepee.fr"]
    vp_sites_map = {
        "FR": {
            "country": "France",
            "vp_site_root_url": "https://www.veepee.fr",
            "user": "automation.software.20@gmail.com",
            "pass": "VQRw7G9Zk6ZTas9!"
        },
        "ES": {
            "country": "Spain",
            "vp_site_root_url": "https://www.veepee.es",
            "user": "automation.vp.es@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "PRIVALIA-ES": {
            "country": "Spain",
            "vp_site_root_url": "https://es.privalia.com",
            "user": "automation.vp.es@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "PRIVALIA-IT": {
            "country": "italy",
            "vp_site_root_url": "https://it.privalia.com",
            "user": "automation.vp.it@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "IT": {
            "country": "Italy",
            "vp_site_root_url": "https://www.veepee.it",
            "user": "automation.vp.it@gmail.com",
            "pass": "@Ut0mati0n.es"
        },
        "DE": {
            "country": "Germany",
            "vp_site_root_url": "https://www.veepee.de",
            "user": "automation.vp.de@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "AT": {
            "country": "Austria",
            "vp_site_root_url": "https://www.veepee.at",
            "user": "automation.vp.at@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "NL": {
            "country": "Netherlands",
            "vp_site_root_url": "https://www.veepee.nl",
            "user": "automation.vp.nl@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "LU": {
            "country": "Luxembourg",
            "vp_site_root_url": "https://www.veepee.lu",
            "user": "automation.vp.lu@mail.com",
            "pass": "@Ut0mati0n.es"
        },
        "BE": {
            "country": "Belgium",
            "vp_site_root_url": "https://nl.veepee.be",
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
        "appvp://operation/"
    ]



    def __init__(self):
        self.data = []
