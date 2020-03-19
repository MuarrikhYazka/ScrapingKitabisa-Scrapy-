# -*- coding: utf-8 -*-
import scrapy
import wordcounter
from scrapy import Field, Item, Request
from scrapy.spiders import CrawlSpider, Spider
import lxml.html
from lxml.cssselect import CSSSelector


class CampaignkitabisaItem(Item):
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





class MasjidSpider(scrapy.Spider):
    name = 'masjid'
    allowed_domains = ['kitabisa.com']
    start_urls = ['https://www.kitabisa.com/search?keyword=wakaf']

    
        

    

    def start_requests(self):
        urls = ['https://www.kitabisa.com/search?keyword=wakaf']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in range(71,72):   #159
            urls= response.css('.m-card a ::attr("href")').extract()   
            for url in urls:
                yield response.follow(url=url, callback=self.parse2)      
            next_page_url = 'https://www.kitabisa.com/search?keyword=wakaf&page='
                            
            next_page_url=response.urljoin(next_page_url+str(i))
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse2(self, response):
        item=CampaignkitabisaItem()
        item['judul'] = response.xpath(".//div[contains(@class, 'project-header')]/h1[contains(@class, 'page-title')]/text()").extract()[0].strip()
        item['nama'] = response.xpath(".//div[contains(@class, 'campaigner-body')]/span[contains(@class, 'text-14')]/span[contains(@class, 'text-14')]/text()").extract()[0].strip()
        item['target'] = response.xpath(".//div[contains(@class, 'project-collected')]/text()").extract()[1].strip()
        item['terkumpul'] = response.xpath(".//div[contains(@class, 'project-collected')]/h1[contains(@class, 'project-collected__amount')]/text()").extract()[0].strip()
        item['jumlahdonatur'] = response.xpath(".//h3[contains(@class, 'fundraiser__title')]/span[contains(@class, 'fundraiser__count')]/text()").extract()[0].strip()
        item['jumlahshares'] = response.xpath(".//span[contains(@class, 'counter__number')]/text()").extract()
        item['mulai'] = response.xpath(".//div[contains(@class, 'project-report')]/span[contains(@class, 'text-14')]/span[contains(@class, 'text--bold')]/text()").extract()[0].strip()
        video = response.xpath(".//div[contains(@class, 'pwa-story__content')]/iframe/@src").extract()
        item['link_video'] = video

        if "www" in video:
            item['video_existence'] = "Ada"
        else:
            item['video_existence'] = "Tidak Ada"

        item['jumlah_foto'] = len(response.xpath(".//div[contains(@class, 'pwa-story__content')]//img/@src").extract())
        teks = response.xpath(".//div[contains(@class, 'pwa-story__content')]//text()").extract()
        teks = ' '.join(teks)
        teks = teks.strip()
        #item['word'] = teks

        for char in '-.,\n':
            teks = teks.replace(char,' ')
            teks = teks.lower()

        word_list = teks.split()
        count = len(word_list)
        item['word_count'] = count

        linkorg = response.xpath(".//div[contains(@class, 'd-ib')]/img/@src").extract()

        if "https://assets.kitabisa.com/images/icon__verified-org.svg" in linkorg:
            item['status_campaigner']='Organisasi'
        else:
            item['status_campaigner']='Individu'

        item['status_akun'] = response.xpath(".//div[contains(@class, 'campaigner-body')]/small[contains(@class, 'text-12')]/text()").extract()

        indikator = response.xpath("//*[contains(@id, 'project-donatur__dana')]/ul/li[1]/div[2]/div/div/time/text()").extract_first().strip()

        if "Offline Donation" in indikator:
            item['offline_donasi'] = response.xpath("//*[contains(@id, 'project-donatur__dana')]/ul/li[1]/div[2]/div/div/div/b/span/text()").extract_first()
        else:
            item['offline_donasi'] ='0'

        yield item
        
        
    
