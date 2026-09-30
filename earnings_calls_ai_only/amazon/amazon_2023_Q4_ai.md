# Amazon.com, Inc. — Q4 2023 Earnings Call (transcript)

- **Company:** Amazon (AMZN)
- **Period:** Q4 2023 (quarter ends calendar Q4 2023; call held the following month)
- **Audio source:** https://s2.q4cdn.com/299287126/files/doc_financials/2023/q4/Amazon-Earnings-Call-Q4-2023-Full-Call-v1.wav
- **Transcription:** machine transcript (faster-whisper small.en), no speaker labels; expect errors on names and numbers
- **Audio duration:** 55 min
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**50 AI sentences of 441 total**
(Borderline, listed at the end: 1 automation/robotics, 8 infrastructure, none containing an AI term.)

Source/parse flags: machine transcript (Whisper), no speaker labels.

## Prepared remarks

### Speaker not labeled
1. 2023 also was a very significant year of delivery and customer trial for generative AI or Gen
2. AI in AWS.
3. AI stack, each of which is gigantic and each of which were deeply invested.
4. At the bottom layer, where customers who are building their own models run training and inference on compute where the chip is the key component in that compute, we offer the most expansive collection of compute instances with NVIDIA chips. ⚑ uncertain
5. AI chips, just as we have with GraviTime for generalized CPU chips, which are 40% more price performance than other x86 alternatives.
6. And as a result, we've built custom AI training chips named Tranium and inference chips named Inferentia.
7. We already have several customers using our AI chips, including Anthropic, Airbnb,
8. In the middle layer, where companies seek to leverage an existing large language model, customize it with their own data, and leverage AWS's security and other features, all as a managed service, we've launched Bedrock, which is off to a very strong start with many thousands of customers using the service after just a few months.
9. The team continues to rapidly iterate on Bedrock, recently delivering capabilities including guardrails to safeguard what questions applications will answer, knowledge bases to expand models knowledge base with retrieval augmented generation or RAG and real-time queries, agents to complete multi-step tasks, and fine-tuning to keep teaching and refining models, all of which will help customers' applications be higher quality and have better customer experiences.
10. We also added new models from Anthropic, Cohere, Meta with Lama 2, Stability AI, and our own
11. Amazon Titan family of LLMs.
12. What customers have learned at this early stage of GenAI is that there's meaningful iteration required in building a production GenAI application with the requisite enterprise quality at the cost and latency needed.
13. Customers don't want only one model. ⚑ uncertain
14. They want different models for different types of applications and different size models for different applications. ⚑ uncertain ⚑ context-dependent
15. And this is what Bedrock does, which is why so many customers are excited about it.
16. One of the very best early GenAI applications is a coding companion.
17. It was designed with security and privacy in mind from the start, making it easier for organizations to use generative AI safely. ⚑ context-dependent
18. By the way, don't underestimate the point about Bedrock and Queue inheriting the same security and access control as customers get with AWS.
19. The data in these models is some of companies' most sensitive and critical assets. ⚑ uncertain
20. With AWS's advantage security capabilities and track record relative to other providers, we continue to see momentum around customers wanting to do their long-term Gen AI work with AWS.
21. We're building dozens of Gen AI apps across Amazon's businesses, several of which have launched and others of which are in development.
22. Gen AI is and will continue to be an area of pervasive focus and investment across Amazon, primarily because there are few initiatives, if any, that give us the chance to reinvent so many of our customer experiences and processes and we believe it will ultimately drive tens of billions of dollars of revenue for Amazon over the next several years.
23. The customer experience continued to improve as our talent, production, streaming quality, analytics, and unique AI features like prime vision and defensive alerts all took big leaps forward on top of their very good start last year.
24. The strength in advertising was primarily driven by sponsored products, as our teams work hard to increase the relevancy of the ads we show customers by leveraging machine learning.
25. Customers are also excited about our approach to generative AI.
26. It's still relatively early days, but the revenues are accelerating rapidly across all three layers, and our approach to democratizing AI is resonating well with our customers. ⚑ context-dependent
27. We have seen significant interest from our customers wanting to run generative AI applications and build large language models and foundation models, all with the privacy, reliability, and security they've grown accustomed to with AWS.
28. As we look forward to 2024, we anticipate CapEx to increase year over year, primarily driven by increased infrastructure CapEx, support growth of our AWS business, including additional investments in generative AI and large language models.

## Q&A

### Speaker not labeled
1. If we take a step back, can you talk a little bit about the contribution from backlog conversion, AI workloads, and some elements that allowed you to reaccelerate revenue at AWS in Q4 and that we should think about those components from an exit velocity standpoint into 2024?
2. And then against your broader comments on CAPEX, any color on how we should be thinking about AI driven CAPEX within the AWS initiatives against the broader CAPEX commentary?
3. We're excited about the resumption, I guess, of migrations that companies may have put on hold during 2023 in some cases and the interest in our generative AI and products like Bedrock and Q as Andy was describing that.
4. I'm not giving a number today, but we're still working through plans for the year, but we do expect CAPEX to rise as we add capacity in AWS for region expansions, but primarily the work we're doing, the generative AI projects.
5. And then on the Gen AI side, if you look at the Gen AI revenue we have, in absolute numbers, it's a pretty big number, but in the scheme of a $100 billion annual revenue run rate business, it's still relatively small, much smaller than what it will be in the future, where we really believe we're going to drive tens of billions of dollars of revenue over the next several years.
6. You outlined the generative AI stack, which I think is, which is very clear.
7. And then maybe expand, if you could, Andy, a little bit on the strategy for Gen AI on the consumer facing side of the business.
8. So Colin, I would say a few things on, first on generative AI.
9. You know, it's, when we talk to customers, particularly at enterprises, as they're thinking about generative AI, many are still thinking through at which layers of those three layers of the stack I laid out that they want to operate in.
10. They will build their own models, they will leverage existing models from us, and then they're going to build apps. ⚑ uncertain ⚑ context-dependent
11. And I know one of the other interesting things that we see early on right now in generative AI is that it's a very iterative process and real work to go from plugging a question into a chatbot and getting an answer, to turning that into a production quality application at the quality you need for your customer experience and your reputation.
12. They don't want just one model to rule the world, they want different models for different applications. ⚑ uncertain ⚑ context-dependent
13. And they want to experiment with all different sized models because they yield different cost structures and different latency characteristics. ⚑ uncertain
14. And they have something that manages all those different transitions and changes so they can figure out what works best for them, especially in the first couple of years where they're learning how to build successful generative AI applications is incredibly important to them.
15. The question about how we're thinking about Gen AI and our consumer businesses, we're building dozens of generative AI applications across the company.
16. Every business that we have has multiple generative AI applications that they're building.
17. So if you just look in some of our consumer businesses, on the retail side, we built a generative AI application that allowed customers to look at summary of customer reviews so that they didn't have to read hundreds and sometimes thousands of reviews to get a sense for what people like or dislike about a product.
18. We launched a generative AI application that allows customers to quickly be able to predict what kind of fit they'd have for different apparel items.
19. We've built a generative application that in our fulfillment centers that forecasts how much inventory we need in each particular fulfillment center.
20. And so the start of the rollout of ROOF is today is really just another step, but we think one that's pretty meaningful in being a generative AI powered shopping assistant.
21. And you can kind of think about Alexa where we're building a very large expansive, large language model that's gonna make Alexa even more productive and helpful for customer.
22. Every one of our consumer businesses has a significant number of generative AI applications that they either have built and delivered or they're in the process of building.

## Borderline: automation/robotics without an AI term

1. [Q&A · Speaker not labeled] In the fulfillment center and logistics area, I would say it's more incremental capacity at this point based on additional demand, although we are seeing some additional investments for same day delivery sites and automation robotics.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Speaker not labeled] We define our capital investments as a combination of CapEx plus equipment finance leases.
2. [Prepared remarks · Speaker not labeled] In 2023, full year CapEx was $48.4 billion, which was down $10.2 billion year over year, primarily driven by lower spend on fulfillment and transportation.
3. [Prepared remarks · Speaker not labeled] One thing I'd like to highlight in our first quarter guidance is that we recently completed a useful life study for our servers, and we are increasing the useful life from five years to six years beginning in January 2024.
4. [Q&A · Speaker not labeled] On the CAPEX side, let me talk in total for the company.
5. [Q&A · Speaker not labeled] A lot of the mix of investment in 2023 was tied to infrastructure, mostly supporting AWS, but also supporting our core Amazon businesses.
6. [Q&A · Speaker not labeled] CAPEX will go up in 2024.
7. [Q&A · Speaker not labeled] But the trend for that most of the large percentage of the spend will be in infrastructure is going to continue into 2024.
8. [Q&A · Speaker not labeled] I would assume that most of the factors like rising capacity utilization, given your CAPEX commentary about retail, the regional center efficiencies, and then overall, you know, moderation in shipping and logistics costs, labor costs.
