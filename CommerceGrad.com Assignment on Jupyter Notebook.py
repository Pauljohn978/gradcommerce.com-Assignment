#!/usr/bin/env python
# coding: utf-8

# In[23]:


import scrapy

class sampleSpider(scrapy.Spider):
   name = 'Webscraping'
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


       yield {
           'title': title,
           'author': author,
           'publication_date': publication_date,
           'reading_time': reading_time,
           'content': content,
           'comments': comments_content
       }


# In[25]:


from scrapy.crawler import CrawlerProcess
process = CrawlerProcess(settings = {'FEEDS' :{'Webscraping.csv' :{'format':'csv'}}})
process.crawl(sampleSpider)
process.start()


# title,author,publication_date,reading_time,content,comments
# Airbnb Brandometer: Powering Brand Perception Measurement on Social Media Data with AI,Tiantian Zhang,"Apr 26, 2024",9 min read,"The Airbnb Tech Blog Listen Share By  At Airbnb, we have developed Brandometer, a state-of-the-art natural language understanding (NLU) technique for understanding brand perception based on social media data. Brand perception refers to the general feelings and experiences of customers with a company. Quantitatively, measuring brand perception is an extremely challenging task. Traditionally, we rely on customer surveys to find out what customers think about a company. The downsides of such a qualitative study is the bias in sampling and the limitation in data scale. Social media data, on the other hand, is the largest consumer database where users share their experiences and is the ideal complementary consumer data to capture brand perceptions. Compared to traditional approaches to extract concurrency and count-based top relevant topics, Brandometer learns   and utilizes embedding distances to measure relatedness of brand perceptions (e.g., ‘belonging’, ‘connected’, ‘reliable’). Word embedding represents words in the form of real-valued vectors, and it performs well in reserving semantic meanings and relatedness of words. Word embeddings obtained from deep neural networks are arguably the most popular and evolutionary approaches in NLU. We explored a variety of word embedding models, from quintessential algorithms   and  , to the latest language model  , and compared them in terms of generating reliable brand perception scores. For concepts represented as words, we use similarity between its embedding and that of “Airbnb” to measure how important the concept is with respect to the Airbnb brand, which is named as Perception Score. Brand Perception is defined as   between Airbnb and the specific keyword: where In this blog post, we will introduce how we process and understand social media data, capture brand perceptions via deep learning and how to ‘convert’ the cosine similarities to calibrated Brandometer metrics. We will also share the insights derived from Brandometer metrics. In order to measure brand perception on social media, we assessedall Airbnb related mentions from 19 platforms (e.g., X — formerly known as Twitter, Facebook, Reddit, etc) and generated word embeddings with state-of-the-art models. In order to use Social media data to generate meaningful word embeddings for the purpose of measuring brand perception, we conquered two challenges: We developed multiple data cleaning processes to improve data quality. At the same time, we innovated the modeling techniques to mitigate the impact on word embedding quality due to data quantity and quality. In addition to data, we explored and compared multiple word embedding training techniques with the goal to generate reliable brand perception scores.  is by far the simplest and most widely used word embedding model since 2013. We started with building CBOW-based Word2Vec models using  . Word2Vec produced decent in-domain word embeddings, and more importantly, the concept of analogies. In our domain-specific word embeddings, we are able to capture analogies in the Airbnb domain, such as  ,  . FastText takes into account the internal structure of words, and is more robust to out-of-vocabulary words and smaller datasets. Moreover, as inspired by  , we associate words with sentiments (i.e., POSITIVE, NEGATIVE, NEUTRAL), which forms brand perception concepts on the sentiment levels. Recent progress in transformer-based language models (e.g.,  ) has significantly improved the performance of NLU tasks with the advantage of generating contextualized word embeddings. We developed   based word embeddings, which works better with smaller dataset and pays more attention to surrounding context via disentangled attention mechanisms. We trained everything from scratch (including tokenizer) using  , and the concatenated last attention layer embeddings resulted in the best word embeddings for our case. The variability of word embeddings has been widely studied ( ). The causes range from the underlying stochastic nature of deep learning models (e.g., random initialization of word embeddings, embedding training which leads to local optimum for global optimization criteria) to the quantity and quality changes of data corpus across time. With Brandometer, we need to reduce the variability in embedding distances to generate stable time series tracking. Stable embedding distances helped preserve the inherent patterns and structures present in the time series data, and hence it contributes to better predictability of the tracking process. Additionally, it made the tracking process more robust to noisy fluctuations. We studied the influential factors and took the following steps to reduce: S For each month’s data, we trained   models with the same hyper-parameters, and took the average of   perception scores as the final score for each concept. Meanwhile, we did upsampling to make sure that each model iterated on an equal number of data points across months. We defined variability as: where  refers to the cosine similarity based perception score defined in Eq. 1,   refers to the algorithm,   refers to the time window (i.e. month),   refers to the vocabulary and   is the vocabulary size, and   refers to the number of repetitively trained models. As   approaches 30, the score variability values converge and settle within a narrow interval. Hence, we picked   for all. Based on   work, we used the overlap between nearest neighbors to measure the stability of word embeddings, since the relative distances matter more than the absolute distance values in downstream tasks. Therefore, we also developed rank-based scores, which shows greater stability as compared to similarity-based scores. For each word, we first ranked them in descending order of cosine similarity via Eq. 1. The rank-based similarity score is then computed as   where  . More relevant concepts will have higher rank-based perception scores. The score variability is defined the same as   in Eq. 2 except that where   refers to the rank based perception score. With rank-based scores, when   approaches to  , the score variability values converge to a much narrower interval especially for DeBERTa. One challenge of this project was that we didn’t have a simple and ultimate way to conclude which score output was better since there is no objective ‘truth’ of brand perception. Instead, we defined a new metric to learn some characteristics of the score. We checked these statistics on the calibrated results as shown above. We can see that the ranked-based score is the winner as compared to similarity-based scores: Though we set out to solve the problem of brand measurement, we believe use cases can go above and beyond: With top perceptions such as “Stay” and “Home,” Airbnb provides a brand image of “ ”, echoing our mission statement and unique supply inventory, while other companies have “Rental,” “Room,” “Booking,” a description of functionality, not human sensation. The   Perceptions are generally stable month to month. The top standing perceptions include Meanwhile, we use Brandometer to monitor emerging perceptions that jump to the top list, which may reflect major events associated with the brand or user preference changes. Businesses create campaigns to promote products and expand the brand image. We were able to capture a perception change on one specific Brand Theme after a related campaign. These use cases are just the beginning. Essentially, this is an innovative way of gathering massive online input as we learn the needs and perception of the community. We will constantly reflect on how we leverage these insights to continually improve the Airbnb experience for our community. Airbnb’s innovative Brandometer has already demonstrated success in capturing brand perception from social media data. There are several directions for future improvement: If this kind of work sounds appealing to you, check out our   — we’re hiring! Thanks to Mia Zhao, Bo Zeng, Cassie Cao for contributing the best ideas on improving and landing Airbnb Brandometer. Thanks to Jon Young, Narin Leininger, Allison Frelinger for the support of social media data consolidation. Thanks to Linsha Chen, Sam Barrows, Hannah Jeton, and Irina Azu who provide feedback and suggestions. Thanks to Lianghao Li, Kelvin Xiong, Nathan Triplett, Joy Zhang, Andy Yasutake for reviewing and polishing the blog post content and all the great suggestions. Thank Joy Zhang, Tina Su, Andy Yasutake for leadership support! Special thanks to Joy Zhang, who initiated the idea, for all the inspiring conversations, continuous guidance and support!",

# In[ ]:





# In[ ]:




