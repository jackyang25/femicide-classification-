import scrapy
import pandas as pd 


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['google.com']
    #start_urls = ['http://google.com/']
    dta = pd.read_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtr.csv')
    #dta = pd.read_csv('/Users/fernandasobrino/Dropbox/Twitter Responsiveness/Data/Turkey_Femicide/femtr.csv')
    start = 1
    extraWords = ['cinayet', 'katil', 'öldürülen', 'öldüren', 'öldürdü', 'öldürüldü', 'cansız bedeni']
    domains = ['milliyet.com.tr', 'hurriyet.com.tr', 'aa.com.tr', 'dha.com.tr', 'iha.com.tr', 'haber7.com', 'haberler.com', 'sondakika.com']
    max_count = 50000
        
    def start_requests(self):
       for index,row in self.dta.iterrows():
           for word in self.extraWords:
               for domain in self.domains:
                    # News! 
                    #url = 'https://www.google.com.tr/search?q={}&hl=tr&source=tr&tbs=cdr%3A1%2Ccd_min%3A{}%&tbm=nws&={}%27'
                    # Google Search: 
                    url = 'https://www.google.com.tr/search?q={}&hl=tr&source=tr&tbs=cdr%3A1%2Ccd_min%3A{}%2Ccd_max%3A{}' 
                    if len(row['Name'].split()[-1]) != 1:
                        q = '"' + row['Name'] + '" ' + word + " site:" + domain
                    else: 
                        try:
                            q = '"' + row['Name'] + '" ' + row['Province'] + ' ' + word + " site:" + domain
                        except:
                            pass
                    year_min = row['Date']  
                    q = q.strip()
                    url2 = url.format(q.replace(' ','+'),str(year_min),self.start)
                    identifier = row['Unnamed: 0']
                    count = 0 
                    yield scrapy.Request(url2,cb_kwargs = {'Identifier': identifier,'count': count})
    
           
    
    
    def parse(self, response, Identifier, count):
        warning = response.xpath('//*[@id="topstuff"]//text()').extract_first()
        if warning is not None:
            yield{'links': 'No links',
                  #'Date': 'Meh',
                  'Identifier': Identifier}
        else:
            # For google news: 
            #links = response.xpath('//*[@class="dbsr"]/a/@href').extract() 
            # For google search:
            links = response.xpath('//*[@class="yuRUbf"]/a/@href').extract()
            dates = response.xpath('//*[@class="f"]/text()').extract()
            #Turkish googl is weird so I don't know which is the path for dates 
            #dates = response.xpath('//*[@class="f"]/text()').extract() 
            n = len(links)
            for i in range(n):
                yield{'links': links[i], 
                      'Date': dates[i],
                      'Identifier':Identifier}
            
            flag = response.xpath('//a[starts-with(descendant::text(),"Next")]/@href').extract()
            #flag = response.xpath('//*[@class="G0iuSb"]/span/text()').extract()
        
        
            if len(flag)==0:
                pass
            else:
                next_page_url = flag[0]
                absolute_next_page_url = response.urljoin(next_page_url)
                while int(count) <= self.max_count:
                    count += 1
                    yield scrapy.Request(absolute_next_page_url,cb_kwargs={'Identifier': Identifier,'count': count})


