# Amazon.com, Inc. — Q1 2024 Earnings Call (transcript)

- **Company:** Amazon (AMZN)
- **Period:** Q1 2024 (quarter ends calendar Q1 2024; call held the following month)
- **Audio source:** https://s2.q4cdn.com/299287126/files/doc_financials/2024/q1/Amazon-Earnings-Call-Q1-2024-Full-Call-v1.wav
- **Transcription:** machine transcript (faster-whisper small.en), no speaker labels; expect errors on names and numbers
- **Audio duration:** 50 min
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**56 AI sentences of 456 total**
(Borderline, listed at the end: 4 automation/robotics, 18 infrastructure, none containing an AI term.)

Source/parse flags: machine transcript (Whisper), no speaker labels.

## Prepared remarks

### Speaker not labeled
1. We've recently launched a new generative AI tool that enables sellers to simply provide a URL to their own website, and we automatically create high-quality product detail pages on Amazon.
2. Already, over 100,000 of our selling partners have used one or more of our Gen AI tools.
3. Our AWS customers are also quite excited about leveraging Gen AI to change their customer experiences and businesses.
4. We see considerable momentum on the AI front, where we've accumulated a multi-billion dollar revenue run rate already.
5. You've heard me talk about our approach before, and we continue to add capabilities in all three layers of the Gen AI stack.
6. At the bottom layer, which is for developers and companies building models themselves, we see excitement about our offerings. ⚑ uncertain
7. We have the broadest selection of NVIDIA compute instances around, but demand for our custom silicon, training and inferences quite high given its favorable price performance benefits relative to available alternatives. ⚑ uncertain
8. Our managed end-to-end service has been a game changer for developers in preparing their data for AI, managing experiments, training models faster, lowering inference latency, and improving developer productivity.
9. Perplexity AI trains models 40% faster in SageMaker.
10. Workday reduces inference latency by 80% with ⚑ uncertain
11. SageMaker, and NatWest reduces its time to value for AI from 12 to 18 months to under 7 months using SageMaker.
12. This change is how challenging it is to build your own models, and we see an increasing number of model builders standardizing on SageMaker. ⚑ uncertain ⚑ context-dependent
13. The middle layer of this stack is for developers and companies who prefer not to build models from scratch, but rather seek to leverage an existing large language model or LLM, customize it with their own data, and have the easiest and best features available to deploy secure, high-quality, low-latency, cost-effective production Gen AI apps.
14. This is why we built Amazon Bedrock, which not only has the broadest selection of LLMs available to customers, but also unusually compelling model evaluation, retrieval augmented generation or RAG to expand models knowledge base, guardrails to safeguard what questions applications will answer, agents to complete multi-step tasks, and fine-tuning to keep teaching and refining models. ⚑ context-dependent
15. Bedrock already has tens of thousands of customers, including Adidas, New York Stock Exchange, Pfizer, Ryanair, and Toyota.
16. In the last few months, Bedrock's added Anthropic's Clov3 models, the best performing models on the planet right now, Metaslama3 models, Mistral's various models,
17. Kohira's newest models, and new first-party Amazon Titan models. ⚑ uncertain
18. Bedrock launched a series of other features, but perhaps most importantly, custom model import.
19. Custom model import is a sneaky big launch, as it satisfies a customer request we've heard frequently and that nobody has yet met. ⚑ uncertain
20. As increasingly more customers are using SageMaker to build their models, they're wanting to take advantage of all the Bedrock features I mentioned earlier that make it so much easier to build high-quality production-grade Gen AI apps.
21. Bedrock custom model import makes it simple to import models from SageMaker or elsewhere into Bedrock before deploying their application.
22. Customers are excited about this, and as more companies find they're employing a mix of custom-built models along with leveraging existing LLMs, the prospect of these two linchpin services in SageMaker and Bedrock working well together is quite appealing.
23. The top of the stack are the Gen AI applications being built, and today we announced the general availability of Amazon Queue, the most capable, generative AI-powered assistant for software development and leveraging companies' internal data.
24. Queue also has a unique capability called Agents, which can autonomously perform a range of tasks, everything from implementing features, documenting, and refactoring code to performing software upgrades. ⚑ uncertain
25. Developers can simply ask Amazon Queue to implement an application feature, such as asking it to create an Add to Favorites feature in a social sharing app, and the agent will analyze their existing application code and generate a step-by-step implementation plan, including code changes across multiple files and suggested new functions. ⚑ uncertain
26. Developers can collaborate with the agent to review and iterate on the plan, and then the agent implements it, connecting multiple steps together and applying updates across multiple files, code blocks, and test suites. ⚑ uncertain
27. Queue is not only the most functionally capable AI-powered assistant for software development and data, but also setting the standard for performance.
28. I'd also caution folks not to overlook the security and operational performance elements of these Gen AI services.
29. AI applications and the reliability of their training and production apps.
30. AWS is a meaningful edge which is adding to the number of companies moving their AI focus to AWS.
31. We expect the combination of AWS's re-accelerating growth and high demand for Gen AI to meaningfully increase year-over-year capital expenditures in 2024, which given the way the AWS business model works is a positive sign of the future growth.
32. And this is before you even calculate Gen AI, most of which will be created over the next 10 to 20 years from scratch and on the cloud.
33. During the first quarter, we saw growth in both generative AI and non-generative AI workloads across a diverse group of customers and across industries, as companies are shifting their focus towards driving innovation and bringing new workloads to the cloud.
34. We remain focused on driving efficiencies across the business, which enables us to invest to support the strong growth we're seeing in AWS, including generative AI, which brings us to capital investments.
35. As I mentioned, we're seeing strong AWS demand in both generative AI and our non-generative AI workloads, with customers signing up for longer deals and making bigger commitments.
36. It's still relatively early days in generative AI and more broadly the cloud space, and we see sizable opportunity for growth. ⚑ context-dependent
37. We anticipate our overall capital expenditures to meaningfully increase year over year in 2024, primarily driven by higher infrastructure CapEx support growth in AWS, including generative AI.

## Q&A

### Speaker not labeled
1. We do see though on the CapEx side that we will be meaningfully stepping up our CapEx and the majority of that will be in our support AWS infrastructure and specifically generative AI efforts.
2. As Andy said earlier, we are seeing strong demand signals from our customers and longer deals and larger commitments, many with generative AI components.
3. And that's before the generative AI opportunity, which I don't know if any of us have seen a possibility like this and technology in a really long time, you know, for sure, since the cloud, perhaps since since the internet.
4. But it's work, all of this generative AI set of workloads, which will transform every experience are going to be built from scratch on the cloud, largely.
5. So I think the CEO of enthropic has said that I think the next generation of models cost in the neighborhood of 1 billion to train, this would be like Claude for I guess, high end.
6. And I think people have moved to newer initiatives that I would in a macro level describe as modernizing their infrastructure and then trying to drive value at a generative AI.
7. And at the same time, we're seeing very significant momentum and people trying to figure out how to run their generative AI on top of AWS.
8. You know, I mentioned we have a multi billion dollar revenue run rate that we see in AI already, and it's still relatively early days.
9. I think first of all, there are so many companies that are still building their models, and these range from the largest foundational model builders like Anthropic, you mentioned, to every 12 to 18 months are building new models.
10. And those models consume an incredible amount of data with a lot of tokens, and they're significant to actually go train. ⚑ uncertain
11. And I expect the increasing amount of those to be built on AWS over time, because our operational performance and security, and as well as our chips, both what we offer from NVIDIA, but you know, if you take Anthropic as an example, they're training their future models on our custom silicon on training them.
12. And so I think we'll have a real opportunity for a lot of those models to run on top of AWS. ⚑ uncertain
13. I think the thing that people sometimes don't realize is that while we're in the stage that so many companies are spending money training models, once you get those models into production, which not that many companies have, but when you think about how many generative AI applications will be out there over time, most will end up being in production when you see the significant run rates, you spend much more in inference than you do in training, because you train only periodically, but you're spitting out predictions and inferences all the time.
14. And so we also see quite a few companies that are building their generative applications to do inference on top of AWS.
15. And, you know, the primary example we see there is how many companies, tens of thousands of companies already are building on top of Amazon bedrock, which has the largest selection of large language models around and a set of features that make it so much easier to build a high quality, cost-effective, low latency, production grade generative AI application.
16. And so we see both training and inference being really big drivers on top of AWS. ⚑ uncertain
17. And then you layer on top of that, the fact that so many companies, their models and these generative AI applications are going to have the most sensitive assets and data, and it's going to matter a lot to them what kind of security they get around those applications.
18. And we have a meaningful edge on the AWS side so that as companies are now getting into the phase of seriously experimenting and then actually deploying these applications to production, people want to run their generative AI on top of AWS.
19. And generally, we still have many opportunities, but that capital use that would generate meaningful returns, especially as you've heard in generative AI.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Speaker not labeled] Queue has the highest known score and acceptance rate for code suggestions, outperforms all other publicly benchmarkable competitors on catching security vulnerabilities, and leads all software development assistance on connecting multiple steps together and applying automatic actions.
2. [Prepared remarks · Speaker not labeled] Within our fulfillment network, we are focused on investing in our inbound network, streamlining and standardizing process paths, and adding robotics and automation.
3. [Q&A · Speaker not labeled] And then you'd like to have a way to be able to know when your your more scarce supply in the fulfillment centers needs replenishment and be able to do it automatically from those upstream storage facilities.
4. [Q&A · Speaker not labeled] We allow them to store items in our upstream, go-cost warehouses that they can either automatically replenish into our fulfillment centers where we ship or they can move to other facilities that they have.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Speaker not labeled] And given our much larger infrastructure cloud computing base, at this growth rate, we see more absolute dollar growth again, quarter over quarter in AWS than we can see elsewhere.
2. [Prepared remarks · Speaker not labeled] Before the pandemic, companies were marching to modernize their infrastructure, moving from on-premises infrastructure to the cloud to save money, innovating a more rapid rate and to drive more developer productivity.
3. [Prepared remarks · Speaker not labeled] Companies are pursuing this relatively low-hanging fruit of modernizing their infrastructure.
4. [Prepared remarks · Speaker not labeled] The more demand AWS has, the more we have to procure new data centers, power, and hardware.
5. [Prepared remarks · Speaker not labeled] As a reminder, these results include the impact from the change in the estimated useful life of our servers, which primarily benefits the AWS segment.
6. [Prepared remarks · Speaker not labeled] We've made progress in managing our infrastructure and fixed costs, while still growing at a healthy rate, which has resulted in improved leverage.
7. [Prepared remarks · Speaker not labeled] As a reminder, we define these as the combination of CapEx plus equipment finance leases.
8. [Q&A · Speaker not labeled] CapEx right now in Q1 we had $14 billion of CapEx.
9. [Q&A · Speaker not labeled] So a little bit of long winded answer to your question, but yes, the main issue that we'll see in the near term is additional CapEx.
10. [Q&A · Speaker not labeled] And we continue to see, you know, strong CapEx performance in our stores business.
11. [Q&A · Speaker not labeled] And, you know, unlike in the cloud, where so much, there's a lot of work to be done to move from on premises to the cloud, people do it and they get value out of it, which is why they modernize their infrastructure.
12. [Q&A · Speaker not labeled] Hey, guys, some more related question on CapEx intensity in AWS.
13. [Q&A · Speaker not labeled] I'll call it macro trends in that I think are contributing to AWS performance, at least in the last quarter, I think, you know, first of all, I think the lion's share of cost optimization is behind us, I think companies will be smart and have learned a lot over the last number of months, and how they run their infrastructure in the cloud.
14. [Q&A · Speaker not labeled] I think it should lead to significant incremental cashflow even with more capex.
15. [Q&A · Speaker not labeled] We are again, still anticipating a higher CapEx this year.
16. [Q&A · Speaker not labeled] So that's our first priority as well as 2024 capital expenditures, but otherwise nothing to share on that front.
17. [Q&A · Speaker not labeled] And does that require a step function increasing in CapEx?
18. [Q&A · Speaker not labeled] And that is not the case if you build the infrastructure with the right building blocks the way we have over the last couple years.
