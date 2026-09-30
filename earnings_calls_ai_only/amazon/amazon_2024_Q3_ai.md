# Amazon.com, Inc. — Q3 2024 Earnings Call (transcript)

- **Company:** Amazon (AMZN)
- **Period:** Q3 2024 (quarter ends calendar Q3 2024; call held the following month)
- **Audio source:** https://s2.q4cdn.com/299287126/files/doc_financials/2024/q3/Amazon-Quarterly-Earnings-Report-Q3-2024-Full-Call-v2.wav
- **Transcription:** machine transcript (faster-whisper small.en), no speaker labels; expect errors on names and numbers
- **Audio duration:** 50 min
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**58 AI sentences of 411 total**
(Borderline, listed at the end: 11 automation/robotics, 17 infrastructure, none containing an AI term.)

Source/parse flags: machine transcript (Whisper), no speaker labels.

## Prepared remarks

### Speaker not labeled
1. We're just entering our first broadcast season for Prime Video Advertising, following a very strong showing at up-fronts, and we're continuing to support brands of all sizes with our generative AI-powered creative tools across display, video, and audio, including our video generator that uses a single product image to curate custom AI-generated videos.
2. However, it also allows them to organize their data in the right architecture and environment to do generative AI at scale.
3. It's much harder to be successful and competitive in generative AI if your data is not in the cloud. ⚑ context-dependent
4. The AWS team continues to make rapid progress in delivering AI capabilities for customers and building a substantial AI business.
5. In the last 18 months, AWS has released nearly twice as many machine learning and Gen AI features as the other leading cloud providers combined.
6. AWS's AI business is a multi-billion dollar revenue run rate business that continues to grow at a triple digit year-over-year percentage and is growing more than three times faster at this stage of its evolution as AWS itself grew.
7. We talk about our AI offering as three macro layers of the stack, with each layer being a giant opportunity and each is progressing rapidly.
8. At the bottom layer, which is for model builders, we were the first major cloud provider to offer NVIDIA's H200 GPUs through our EC2 P5E instances. ⚑ uncertain
9. And while we have a deep partnership with NVIDIA, we've also heard from customers that they want better price performance on their AI workloads.
10. As customers approach higher scale in their implementations, they realize quickly that AI can get costly.
11. It's why we've invested in our own custom silicon in Tranium for training and Inferentia for inference. ⚑ context-dependent
12. We also continue to see increasingly more model builders standardized in Amazon SageMaker, our service that makes it much easier to manage your ⚑ uncertain
13. AI data, build models, experiment, and deploy to production.
14. This team continues to add features at a rapid clip punctuated by SageMaker's unique HyperPod capability, which automatically splits training workloads across more than a thousand AI accelerators, prevents interruptions by periodically saving checkpoints and automatically repairing faulty instances from their last save checkpoint, and saving training time up to 40%. ⚑ context-dependent
15. At the middle layer, where teams want to leverage an existing foundation model, customize with their data, and then have features to deploy high-quality generative AI applications, Amazon Bedrock has the broadest selection of leading foundation models and most compelling modules for key capabilities like model evaluation, guardrails, rag, and agents.
16. Recently, we've added Anthropics Cloud 3.5 Sonnet model, ⚑ uncertain
17. Metaslama 3.2 models, Mistral's large two models, and multiple stability AI models.
18. We also continue to see teams use multiple model types from different model providers and multiple model sizes in the same application. ⚑ uncertain
19. There's muck and orchestration required to make this happen, and part of what makes Bedrock so appealing to customers and why it has so much traction is that Bedrock makes this much easier.
20. Customers have many other requests, access to even more models, making prompt management easier, further optimizing inference costs, and our Bedrock team is hard at work making this happen.
21. At the application or top layer, we're continuing to see strong adoption of Amazon Queue, the most capable generative AI-powered assistant for software development and to leverage your own data.
22. Expect more practical AI game changers from Queue.
23. We're also using generative AI pervasively across Amazon's other businesses, with hundreds of apps and development are launched.
24. For consumers, we've expanded Rufus, our generative AI-powered expert shopping assistant to the UK, India, Germany, France, Italy, Spain, and Canada.
25. We've recently debuted AI
26. Shopping Guides for consumers, which simplifies product research by using generative AI to pair key factors to consider in a product category with Amazon's wide selection, making it easier for customers to find the right product for their needs.
27. Project Amelia, an AI assistant that offers tailored business insights to boost productivity and drive seller growth.
28. We continue to re-architect the brain of Alexa with a new set of foundational models that we'll share with customers in the near future, and we're increasingly adding more AI into all of our devices.
29. The note-taking experience is much more powerful with the new built-in AI-powered notebook, which enables you to quickly summarize pages of notes into concise bullets in a script font that can easily be shared.
30. The business continues to grow, and we see opportunity to expand our core cloud offering and our AI services.
31. Customers increasingly recognize that to get the true benefit of generative AI, they also need to move to the cloud.
32. This primarily relates to AWS as we invest to support demand for our AI services, while also including technology infrastructure to support our North America and international segments. ⚑ context-dependent

## Q&A

### Speaker not labeled
1. And specifically, the increased bumps here are really driven by generative AI.
2. As I was mentioning in my own opening comments, our AI business is a multi-billion dollar business that's growing triple digit percentages year over year, and is growing three times faster at its stage of evolution than
3. And of course, in the hardware of AI, the accelerators of the chips are more expensive than the CPU hardware.
4. And we expect the same thing will happen here with generative AI.
5. You talk about how AI is about the same size, but growing way faster than early AWS.
6. And it seems like a lot of that is what's going on right now in AI with these new AI data centers where you've got competitive pricing and suboptimal utilization just in the whole industry.
7. So, as that revenue line grows from where it is today to tens of billions of dollars in coming years, how does that margin come on from the AI data centers versus your existing income at 30 plus percent margin at AWS?
8. Any thoughts on how quickly you can close the gap and how that looks on the new AI workloads versus maybe the mid 30s that the core business is running at?
9. And it's meant that we've had to develop very sophisticated models in anticipating how much capacity we need where in which SKUs and units. ⚑ uncertain
10. And so, I think that the AI space is for sure, an earlier stage and more fluid and dynamic than our non AI part of AWS.
11. AI where the offerings are new and people are very excited about it.
12. And I think as the market matures over time, they're going to be very healthy margins here in the generative AI space.
13. And the last piece I would add to that is, we really do believe that that AI is going to be a big piece of what we do in our robotics network.
14. We just hired a number of people from an incredibly strong robotics AI organization.
15. And then secondly, you made a lot of progress with the AI agents on AWS and for sellers and roof for buyers.
16. I wonder with all the underlying data that you have and leveraging those agent capabilities, if you could provide any perspective on what an next generation Alexa might look like and your opportunities there to perhaps drive incremental revenues. ⚑ uncertain
17. And on your second question, Colin, around Alexa, you know, I think we have a really broad number of Alexa devices all over people's homes and offices and automobiles and hospitality suites. ⚑ uncertain
18. And when we first were pursuing Alexa, we had this vision of it being the world's best personal assistant. ⚑ uncertain
19. And I think if you look at what's happened in generative AI over the last couple years, I think, you know, you're kind of missing the boat.
20. And so we have, you know, we have a really broad footprint where we believe if we re-architect the brains of Alexa with next generation foundational models, which we're in the process of doing, we have an opportunity to be the leader in that space.
21. I think if you look at a lot of the applications today that use generative AI, you know, there's a large number of them that are having success in cost avoidance and productivity.
22. And I think that the next generation of these assistants and the generative AI applications will be better at not just answering questions and summarizing, indexing and aggregating data, but also taking actions.
23. And you can imagine us being pretty good at that with Alexa. ⚑ uncertain
24. And so, you know, we're growing at a very rapid rate and have grown a pretty big business here in the AI space.
25. It's also true that for customers that start to scale out their implementations on the inference side, particularly, they realize pretty quickly that it can get costly. ⚑ uncertain ⚑ context-dependent
26. And it's really why we have pursued building Tranium and Inferentia, which is our custom silicon.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Speaker not labeled] And third, we continue to innovate in robotics to speed delivery, lower cost to serve, and further improve safety in our fulfillment network.
2. [Prepared remarks · Speaker not labeled] This is the first facility that incorporates our newest robotics inventions that simplify stowing, picking, packing, and shipping processes.
3. [Prepared remarks · Speaker not labeled] Though we believe we have more expansive automation in robotics than other retail peers, it's still early days in how much automation we expect in our fulfillment network.
4. [Prepared remarks · Speaker not labeled] This includes investments in same-day delivery facilities, in our inbound network, and as well in robotics and automation.
5. [Q&A · Speaker not labeled] And then the second one, I wanted to sort of ask you more about the robotics that you mentioned.
6. [Q&A · Speaker not labeled] I know you've been investing in robotics now for quite a few years.
7. [Q&A · Speaker not labeled] Where are you now in that journey and how do we think about the next largest areas of investment in robotics in the warehouse network?
8. [Q&A · Speaker not labeled] On the robotics piece, what I would say is even though we believe we have more expansive and advanced automation robotics capabilities in our fulfillment network than other peers, it's so early with respect to what we're going to do automation robotics wise in our fulfillment network.
9. [Q&A · Speaker not labeled] We're just at the stage right now where we're starting to roll out, we had about a five or six very significant new robotics capabilities in the areas of stowing, picking, packing and shipping that we are finally put into one facility to get the entire workflow.
10. [Q&A · Speaker not labeled] And of course, the reason why we're trying to have more robotics automation or a fulfillment network is it allows us to fast to ship more quickly, to ship more cost effectively and to make conditions even safer for our fulfillment teammates than what they already have today.
11. [Q&A · Speaker not labeled] And I think something that the team has done in a very disciplined way, and I talked about this a little bit in my annual letter, my shareholder letter is just they have been very thoughtful about defining what are the primitive foundational building blocks that you need, that you can then use in lots of different combinations to build additional automation robotics capabilities down the road so that we can move even more quickly with the next generation of robotics capabilities.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Speaker not labeled] You can look at our partnership with NVIDIA called Project Ceba, where NVIDIA has chosen AWS's infrastructure for its R&D supercomputer, due in part to AWS's leading operational performance and security.
2. [Prepared remarks · Speaker not labeled] And you can see how AWS continues to innovate in its infrastructure capabilities, with deliveries like Aurora Limited List Database, which extends AWS's very successful relational database to support millions of database rights per second and manage petabytes of data, while maintaining the simplicity of operating a single database, or with our custom Graviton4 CPU instances, which provide up to nearly 40 percent better price performance versus other leading x86 processors.
3. [Prepared remarks · Speaker not labeled] Companies are focused on new efforts spending energy on modernizing their infrastructure from on-premises to the cloud.
4. [Prepared remarks · Speaker not labeled] And as a result of our continued focus on cost control, including a measured pace of hiring, a focus on driving efficiencies on our infrastructure, and reducing costs across the business.
5. [Prepared remarks · Speaker not labeled] Additionally, we increased the estimated useful life of our servers starting in 2024, which contributed approximately 200 basis points to the AWS margin increase here over here in Q3.
6. [Prepared remarks · Speaker not labeled] As a reminder, we define these as a combination of cash CapEx plus equipment finance leases.
7. [Prepared remarks · Speaker not labeled] We expect to spend approximately $75 billion in CapEx in 2024.
8. [Prepared remarks · Speaker not labeled] The majority of the spend is to support the growing need for technology infrastructure.
9. [Q&A · Speaker not labeled] And then perhaps related the step up in CapEx that you saw in 3Q, you gave the full year number, which was helpful, any kind of early read or thoughts on how we should think about 2025.
10. [Q&A · Speaker not labeled] And of course, what you just mentioned, I believe the change in made the useful life for our servers this year.
11. [Q&A · Speaker not labeled] Let me remind you on that one, we made the change in 2024 to extend the useful life of our servers, this added about 200 basis points of margin year over year.
12. [Q&A · Speaker not labeled] So we're really working hard to maintain our efficiencies, not only in the Salesforce and other areas and production teams, but also in our infrastructure areas.
13. [Q&A · Speaker not labeled] Infrastructure is a big part of our cost structure in AWS.
14. [Q&A · Speaker not labeled] Yeah, I'll take the CapEx part of that.
15. [Q&A · Speaker not labeled] AWS business is the cash lifecycle is such that the faster we grow demand, the faster we have to invest capital in data centers, and networking gear, and hardware.
16. [Q&A · Speaker not labeled] But, you know, of course, a lot of these assets are many year useful life assets, data centers, for instance, are useful assets for 20 to 30 years.
17. [Q&A · Speaker not labeled] If you think about, we have 35 or so regions around the world, which is an area of the world where we have multiple data centers and then probably about 130 availability zones or data centers.
