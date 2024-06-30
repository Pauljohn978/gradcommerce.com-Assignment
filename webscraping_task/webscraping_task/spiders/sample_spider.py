import scrapy

class Webscrapingtask(scrapy.Spider):
   name = 'Sample_spider'
   allowed_domains = ['medium.com']
   start_urls = [
       'https://medium.com/airbnb-engineering/airbnb-brandometer-powering-brand-perception-measurement-on-social-media-data-with-ai-c83019408051'
   ]

   def parse(self, response):
       # Extract the title of the article
       title = response.css('strong.al::text').get()
       print(f"Title: {title}")

       # Extract the author of the article
       author = response.css('div.ab * div.ab * div.ab * a::text').get()
       print(f"Author: {author}")

       # Extract the publication date
       publication_date = response.css('span[data-testid="storyPublishDate"]::text').get()
       print(f"Publication Date: {publication_date}")

       # Extract the reading time
       reading_time = response.css('span[data-testid="storyReadTime"]::text').get()
       print(f"Reading Time: {reading_time}")

       # Extract the content of the article
       paragraphs = response.css('article p::text').getall()
       content = ' '.join(paragraphs)
       print(f"Content: {content[:200]}...")  # Print only the first 200 characters for brevity

       # Extract comments (Assuming comments are in a div with class 'comments')
       comments = response.css('div.comments p::text').getall()
       comments_content = ' '.join(comments)
       print(f"Comments: {comments_content[:200]}...")  # Print only the first 200 characters for brevity
       
        #Extracting all images
       raw_images_urls = response.css('img::attr(src)').getall()
       clean_images_urls = []
       clean_images_urls = [response.urljoin(img_url) for img_url in raw_images_urls]
       
       yield {
           'title': title,
           'author': author,
           'publication_date': publication_date,
           'reading_time': reading_time,
           'content': content,
           'comments': comments_content,
           'images_urls': clean_images_urls
       }


