# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CampaignkitabisaItem(scrapy.Item):
    judul = Field()
    nama = Field()
    target = Field()
    terkumpul = Field()
    jumlahdonatur = Field()
    jumlahshares = Field()
    mulai = Field()
    link_video = Field()
    video_existence = Field()
    jumlah_foto = Field()
    #word = Field()
    word_count = Field()
    status_campaigner = Field()
    status_akun = Field()
    offline_donasi = Field()
    

    

