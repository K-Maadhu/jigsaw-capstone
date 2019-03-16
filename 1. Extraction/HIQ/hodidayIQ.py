import scrapy


class HolidayIQSpider(scrapy.Spider):
    #identity
    name = "holidayiq"

    #Requestscrapy
    start_urls= [

        'https://www.holidayiq.com/India-Hill-destinations/p1.html',
        'https://www.holidayiq.com/India-Heritage-destinations/p1.html',
        'https://www.holidayiq.com/India-Beach-destinations/p1.html'  
    ]


    #Response
    def parse(self, response):
        for holiday in response.selector.xpath("//div [@class='media-body-box media-body']"):
            yield {
                'Type': holiday.xpath("//ul[@class='breadcrumb']//span[contains(text(), 'Holidays')]/text()").extract_first(),
                'Location': holiday.xpath(".//h2[@class='media-heading']/text()[1]").extract_first(),
                'url' :  'https://www.holidayiq.com' + holiday.xpath(".//a[contains(@class,'themeHeading')]/@href[1]").extract_first(),
                '# of Sight seeing': holiday.xpath(".//p/span/strong/text()[1]").extract_first() 
                 



                
            }

        next_page=response.selector.xpath("//a[@aria-label='Next']/@href").extract_first()

        if next_page is not None:
           next_page_link= response.urljoin(next_page)  
           yield scrapy.Request(url=next_page_link, callback=self.parse) 


