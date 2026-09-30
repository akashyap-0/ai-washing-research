# Amazon.com, Inc. — Q2 2024 Earnings Call (transcript)

- **Company:** Amazon (AMZN)
- **Period:** Q2 2024 (quarter ends calendar Q2 2024; call held the following month)
- **Audio source:** https://s2.q4cdn.com/299287126/files/doc_financials/2024/q2/Amazon-Earnings-Call-Q2-2024-Full-Call-v1.wav
- **Transcription:** machine transcript (faster-whisper small.en), no speaker labels; expect errors on names and numbers
- **Audio duration:** 48 min
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**53 AI sentences of 408 total**
(Borderline, listed at the end: 2 automation/robotics, 10 infrastructure, none containing an AI term.)

Source/parse flags: machine transcript (Whisper), no speaker labels.

## Prepared remarks

### Speaker not labeled
1. And third, builders and companies of all sizes are excited about leveraging AI.
2. Our AI business continues to grow dramatically with a multi-billion dollar revenue run rate despite it being such early days, but we can see in our results and conversations with customers that our unique approach and offerings are resonating with customers.
3. The same is true in AI.
4. You saw this several years ago when some companies tried to argue that TensorFlow would be the only machine learning framework that mattered and then PyTorch and others overtook it.
5. The same one model or one chip approach dominated the earliest moments of the generative AI boom, but we have a lot of data that suggests this is not what customers want here either.
6. You can see this philosophy in the primitive building blocks we're building at all three layers of the Gen AI stack.
7. At the bottom layer, which is for those building generative AI models themselves, the cost to compute for training and inference is critical, especially as models get to scale.
8. It's why we've invested in our own custom silicon in Tranium for training and Inferentia for inference. ⚑ context-dependent
9. These model builders also desire services that make it much easier to manage the data, construct the models, experiment, deploy to production and achieve high quality performance, all while saving considerable time and money. ⚑ uncertain ⚑ context-dependent
10. That's what Amazon SageMaker does so well, including its most recently launched feature called HyperPods that changes the game and networking performance for large models. ⚑ uncertain ⚑ context-dependent
11. And we're increasingly seeing model builders standardized on SageMaker. ⚑ uncertain
12. While many teams will build their own models, lots of others will leverage somebody else's frontier model, customize it with their own data and seek a service that provides broad model selection and great generative AI capabilities.
13. This is what we think of as the middle layer, what Amazon Bedrock does and why Bedrock has tens of thousands of companies using it already. ⚑ context-dependent
14. Bedrock has the largest selection of models, the best generative AI capabilities in critical areas like model evaluation, guardrails, rag and agenting, and then makes it easy to switch between different model types and model sizes.
15. Bedrock has recently added Anthropics Cloud 3.5 models, which are the best performing models on the planet,
16. Metas new Llama 3.1 models and Mistral's new large two models.
17. And Llamas and Mistral's impressive performance benchmarks and open nature are quite compelling to our customers as well.
18. At the application or top layer, we're continuing to see strong adoption of Amazon Q, the most capable generative AI powered assistant for software development and to leverage your own data.
19. During the past 18 months, AWS has launched more than twice as many machine learning and generative AI features into general availability than all of the other major cloud providers combined.
20. We remain very bullish on the medium to long-term impact of AI in every business we know and can imagine.
21. Generative AI especially is quite iterative and companies have to build muscle around the best way to solve actual customer problems.
22. We see it in how our generative AI-powered shopping assistant, Rufus, is helping customers make better shopping decisions.
23. We see it in how our AI features allow customers to simulate trying apparel items or changing the buying experience.
24. We see it in how our generative AI listing tool is enabling sellers to create new selection with a line or two of text versus the many forms previously required.
25. We see it in our fulfillment centers across North America where we're rolling out Project Private Investigator, which uses a combination of generative AI and computer vision to uncover defects before products reach customers.
26. We see it in how our generative AI is helping our customers discover new music and video.
27. We see it in how it's making Alexa smart. ⚑ uncertain
28. And we see it in how our custom Silicon and services like SageMaker and Bedrock are helping both our internal teams and many thousands of external companies reinvent their customer experiences in businesses.
29. We are investing a lot across the board in AI and we'll keep doing so as we like what we're seeing and what we see ahead of us.
30. During the second quarter, we saw continued growth across both generative AI and non-generative AI workloads.
31. We saw companies turn their attention to newer initiatives, bring more workloads to the cloud, restart or accelerate existing migrations from on-premises to the cloud and tap into the power of generative AI.
32. We remain focused on driving efficiencies across the business, which enables us to invest to support the strong growth we're seeing in AWS, including generative AI.
33. The majority of this spend will be to support the growing need for AWS infrastructure as we continue to see strong demand in both generative AI and our non generative AI workloads.

## Q&A

### Speaker not labeled
1. There's been a theme during the last couple of weeks of earnings of the potential to over-invest as opposed to under-invest in AI as a broad theme.
2. I think on the question about investment in AWS and on the AI side, I think where I'd start is I think one of the least understood parts about AWS over the last 18 years has been what a massive logistics challenge it is to run that business.
3. And we have built models over a long period of time that are algorithmic and sophisticated that land the right amount of capacity. ⚑ uncertain
4. And we've done the same thing on the AI side.
5. Now AI is newer and it's true that people take down clumps of capacity in AI that are different sometimes.
6. I mean, but it's also true that it's not like a company shows up to do a training cluster asking for a few hundred thousand chips the same day.
7. So while the models are more fluid, it's also true that we've built, I think, a lot of muscle and skill over time and building these capacity signals and models. ⚑ uncertain
8. You know, I think that it's, you know, the reality right now is that while we're investing a significant amount in the AI space and in infrastructure, we would like to have more capacity than we already have today.
9. And so we built custom Silicon in the generalized CPU space with Graviton, which we're on our fourth model right now. ⚑ uncertain
10. And so that's why we went about building Tranium, which is our trading chip and Inferentia, which is our inference chip, which we're on the second versions of both of those.
11. And I think the generative AI component is in its very early days.
12. As I said, we kind of sometimes look at it and say, that's interesting that we have a multi-billion dollar revenue run rate already in AI and it's so early.
13. But I also think that generative AI itself and AI as a whole, it's gonna be really large.
14. And unlike the non-AI space where you're basically taking all this infrastructure that's been built on premises over a long period of time and working with customers to help them migrate it to the cloud, which is a lot of work, by the way, in the generative AI space, it's gonna get big fast and it's largely all gonna be built from the get-go in the cloud, which allows the opportunity for those businesses to continue to grow.
15. I know AI today is early, but when you see most of these companies are having to move to public cloud, are you seeing a step up and a return to workloads moving to get ready for this day to stay, even if they're not ready to adopt AI?
16. On the second part of your question, Brent, what I would say is that it's true in analytics, but it's even maybe more so true in AI, which is that it's quite difficult to be able to do AI effectively if your data is not organized in such a way that you can access that data and run the models on top of them and then build the application.
17. So when we work with customers, and this is true both when we work directly with customers as well as when we work with systems integrator partners, everyone's in a hurry to get going on doing generative AI.
18. And there's very often work associated with getting your data in the right shape and in the right spot to be able to do generative AI.
19. Fortunately, because so many companies have done the work to move to the cloud, there's a number of companies who are ready to take advantage of AI, and that's where we've seen a lot of the growth.
20. There are a lot of companies who have yet to move to the cloud who will, and the ability to use AI more effectively is gonna be one of the many drivers in doing so for them.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Speaker not labeled] It tests code, outperforms all other publicly benchmarkable competitors on catching security vulnerabilities and leads all software development assistants on connecting multiple steps together and applying automatic action.
2. [Prepared remarks · Speaker not labeled] We have a number of opportunities to further reduce costs, including expanding our use of automation and robotics, further building out our same day facility network and regionalizing our inbound network.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Speaker not labeled] Second, companies are spending their energy again on modernizing their infrastructure and moving from on-premises infrastructure to the cloud.
2. [Prepared remarks · Speaker not labeled] Additionally, AWS operating margin includes an approximately 200 basis point favorable impact from the change in the estimated useful life of our servers that we instituted in cube one.
3. [Prepared remarks · Speaker not labeled] As a reminder, we define these as a combination of CapEx plus equipment finance leases.
4. [Prepared remarks · Speaker not labeled] For the first half of the year, CapEx was $30.5 billion.
5. [Q&A · Speaker not labeled] If you think about the fact that we have about 35 regions and think of a region as a cluster of multiple data centers and then about 110 availability zones, which is roughly equivalent to a data center, sometimes it includes multiple.
6. [Q&A · Speaker not labeled] And we saw this same trend happening about five years ago in the accelerator space, in the GPU space, where the products are good, but there was really primarily one provider and supply was more scarce than what people wanted.
7. [Q&A · Speaker not labeled] And in a world where it's hard to get GPUs today, the supply is scarce and all the schedules continue to move over time, customers are quite excited and demanding at a high clip, our custom Silicon, and we're producing it as fast as we can.
8. [Q&A · Speaker not labeled] And I also do believe that, you know, pre pandemic, we were on this March where most companies were trying to figure out to modernize their infrastructure, which really means moving from on-premises to the cloud because they can save money and invent more quickly and get better developer productivity.
9. [Q&A · Speaker not labeled] I mean, it makes, I don't wanna run my own data centers.
10. [Q&A · Speaker not labeled] There's also an adjustment that we made to the useful life of servers that happened in Q1.
