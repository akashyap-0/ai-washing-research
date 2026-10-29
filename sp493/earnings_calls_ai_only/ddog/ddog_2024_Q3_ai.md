# Datadog — 2024_Q3 Earnings Call (transcript)

- **Company:** Datadog (DDOG); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** DDOG
- **CIK:** 0001561550
- **Period:** 2024_Q3 (call held November 7, 2024; date from page date line)
- **Calendar quarter:** 2024 Q3 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/11/07/datadog-ddog-q3-2024-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** bd98388ba4fa8279480288fdb1b9836bf2bcd7ce6f044f9322a6365ed8b7f1c8
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**42 AI sentences of 520 total**
(Borderline, listed at the end: 5 automation/robotics, 22 infrastructure, none containing an AI term.)

## Prepared remarks

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
1. We kept broadening our platform in observability and beyond, including in next-gen AI, where interest continues to rise, and we added new customers while expanding with existing ones as they grow into the cloud.
2. In the next-gen AI space, customers continue to experiment with new AI technologies.
3. And as they do, they want to get visibility into their AI use.
4. At the end of Q3, about 3,000 customers used one or more Datadog AI integrations to send us data about their AI, machine learning, and LLM usage.
5. As some of these experiments start turning into production AI applications, we are seeing initial signs of traction for our LLM observability products.
6. Today, hundreds of customers are using LLM observability with more exploring it every day, and some of our first paying customers have told us that they have cut the time spent investigating LLM latency, errors, and quality from days or hours to just minutes.
7. Our customers not only want to understand the performance and cost of their LLM applications, they also want to understand the LLM model performance within the context of their entire application.
8. So they are using APM, alongside LLM observability, to get fully integrated end-to-end visibility across all their applications and tech stacks.
9. Next, we signed a seven-figure annualized expansion with a division of a hyperscaler delivering next-gen AI models.
10. They will be launching new features for their large language models soon and need a platform that can scale flexibly while supporting proactive incident detection. ⚑ context-dependent
11. By expanding the use of Datadog, they expect to efficiently onboard new teams and environments and support the rapidly increasing adoption of the LLMs.
12. We are seeing continued experimentation with new advances such as next-gen AI, and we believe this is one of the many factors that will drive greater use of the cloud and other modern technologies, so we are helping our customers every day to observe, secure, and act on their business-critical applications and workloads.

### David M. Obstler, Chief Financial Officer
13. Now some of our growth is coming from AI native customers who this quarter represented more than 6% of our Q3 ARR, up from more than 4% in Q2 and about 2.5% of our ARR in the year-ago quarter.
14. AI-native customers contributed about 4 percentage points of year-over-year growth in Q3 versus about 2 percentage points in the year-ago quarter.
15. While we believe that adoption of AI will continue to benefit Datadog in the long term, we are mindful that some of the large customers in this cohort have ramped extremely rapidly and that these customers may optimize cloud and observability usage and increase their commitments to us over time with better terms.

## Q&A

### Mark Murphy, Analyst
1. Olivier, we noticed your AI contributions surged to about 6% this quarter.
2. We're watching all the advances in the foundation models, including the OpenAI's strawberry version.
3. We're watching the multistep reasoning, how they're becoming multimodal, the longer-duration inference and video models. ⚑ uncertain
4. Does it seem reasonable to you that we are on the cusp of a pretty interesting period in the next couple of years for the inferencing loads and that might drive some incremental traction for Datadog that is tied to AI?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
5. So as we reported, we are seeing some customers moving to production, and we are seeing our production-minded LLM observability products, for example, being used by real paying customers with real volumes and real applications in real production workloads.
6. In general, in terms of the workloads, you're right that we're starting to see more inference workloads, but they still tend to be more concentrated across a number of API-driven providers.
7. So there are a few others, both on LLMs and other kinds of models.
8. We expect that to diversify more over time as companies get further into production with their applications and they start to be customizing more on their models. ⚑ uncertain

### Sanjit Singh, Analyst
9. Or are you starting to see customers focus more -- less about the consolidation opportunity and more about innovation and bringing their innovation budgets to bear to invest in AI and cloud and bringing on Datadog along for the ride?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
10. And at the same time, we are excited to see what's happening with the AI innovation as it gets further down the pipe and away from testing and experimenting and more into production applications.
11. Again, we see that with our LLM observability product.
12. But I would say it's still very early days in terms of customers being in production with their next-gen AI applications.

### Raimo Lenschow, Analyst
13. And how much of that is like taking project resources away, not so much money, but also time for kind of AI, and it's obviously like, as you said, early in its life cycle.

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
14. All that is going into AI, and that's largely right now in experimentation and model training and that sort of thing.
15. It does create a bit of a decorrelation between our numbers as a whole and the numbers you might see reported from the hyperscalers, where a lot of their short-term growth rides more into -- on the capacity of GPUs they bring online for those experimentation and training workloads. ⚑ context-dependent

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
16. I would say we're -- so right now, we're working with a number of customers that have real-world large inference workloads on how we can help on the GPU profiling side for inference.
17. There is a world where maybe in a durable fashion, 60% of workloads are inference and 40% are training. ⚑ uncertain

### Karl Keirstead, Analyst
18. I've got a couple of questions about the comment, David, around some of your larger AI native customers, maybe revenues from them being a little bit more volatile going forward.
19. Is this just a natural phenomenon of a few of those AI native customers now becoming quite large?
20. And then maybe secondly, when you set your 4Q guide, did you embed the assumption of some of these AI start-up pricing and observability trends that you called out?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
21. I think the -- look, what we see there is we -- so we have that group of AI, like smaller -- relatively small number of AI companies or AI native companies.
22. Many of them are model providers or infrastructure providers for AI that serve the rest of the industry and they are really a proxy for the future growth of the rest of the industry in AI.That group has been growing very fast.
23. The first one is that the AI cohort is growing faster, and there are larger individual ACVs for these customers.

### Mike Cikos, Analyst
24. Just wanted to get a better understanding, is there anything you can speak to as it relates to those AI native customers, the intensity of those workloads, and then how your products feed into it or maybe even the broader portfolio and the product expansion you've seen?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
25. We see large growth -- very large growth on the AI native side.
26. We think that the one big catalyst for future acceleration will be those AI native applications or those AI applications, I should say, going into production for non-AI native companies for a much broader set of customers than the customers that are deploying these kind of applications to their -- in production.

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
27. Firstly, for the product management team for building great products last quarter, the customers that actually spent all this time with us on getting those products to work right, especially for the new products, and I'm talking about LLM observability, for example, or OnCall, and so I know we spent a lot of time with customers to get those right.

## Borderline: automation/robotics without an AI term

1. [Q&A · Sanjit Singh, Analyst] And any sort of early indications on the uptake of some of the service management products and more of the automation features within the Datadog platform?
2. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] So we feel good about handling the full loop for them, starting with when we detect something in observability, all the way to full incident resolution and automation as a big part of it.
3. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] And they're all growing quite nicely, I would say, from a small basis today, but we're very excited in the way they all come together to form an integrated platform where we can fully automate resolution for our customers.
4. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] And really as a step stone toward full automation of incident resolution and full ownership from end-to-end.
5. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] The part that strategically is the most interesting to us is the automation of the resolution, not physically aging customers.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We continue to execute on growth across the three pillars of observability, and we are pleased to report that infrastructure monitoring, our APM suite, and log management together represent more than $2.5 billion in ARR.
2. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] In September, we launched Datadog monitoring for Oracle cloud infrastructure for general availability.
3. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] With this launch, our customers gain visibility into their OCI stack and they can manage in real time the performance of OCI cloud services, servers, VMs, databases, containers, and apps in Datadog.
4. [Prepared remarks · David M. Obstler, Chief Financial Officer] And after taking into consideration capital expenditures and capitalized software, free cash flow was $204 million for a free cash flow margin of 30%.
5. [Prepared remarks · David M. Obstler, Chief Financial Officer] Finally, we expect capital expenditures and capitalized software together to be in the 3% to 4% of revenue range for fiscal 2024.
6. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We see that also with some of the workloads we monitor from our customers on the infrastructure side.
7. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] So you're right that when we look at the numbers from the hyperscalers and when we try to factor out what's GPU driven, the growth looks stable-ish.
8. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] Now on the edge of that, you're right that the -- where the workloads could have grown maybe instead of growing 20%, they could grow 25%, maybe some of those 5% instead are being invested both in terms of infrastructure budget or innovation -- time innovation budget.
9. [Q&A · Kash Rangan, Analyst] As you look at GPU workloads, what about the company's existing portfolio geared toward CPU applies in a GPU world?
10. [Q&A · Kash Rangan, Analyst] And how do you monetize an instance of GPU versus a CPU if that were to make sense?
11. [Q&A · David M. Obstler, Chief Financial Officer] For GPU --
12. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] I can go GPU, yeah.
13. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] There is -- how do you -- what can you do for GPU that's different from a CPU?
14. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] And there's quite a bit that's new and differentiated around profiling in general and understanding how you maximize the usage of the GPU bandwidth, which is usually what it's about.
15. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We're doing less on the training side, mostly because the training jobs tend to be more bespoke and temporary, and there's less of an application that's attached to those that these are just very large clusters of GPUs.
16. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] Today -- as of today, we really don't monetize GPU instances all that well compared to the other CPU instances.
17. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] So GPU instance is many times the cost of a CPU instance, and we charge the same amount for it.
18. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] If we do things that are particularly interesting and it's going to have a real impact on -- and deliver value and how customers use and make the best of their GPUs and in the end, save money.
19. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] And as they do, they will also look less like just large cluster of GPUs and more like traditional applications because the GPU needs a database.
20. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] It needs layers to secure it and authorize it and all the other things, so it's going to look a lot more like a normal application with some additional more concentrated compute and GPUs.
21. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] Unlike many others, we don't expect at this point to have outsized investments in compute.
22. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We're not building absolutely large GPU clusters, but we are building engineering capacity, and we are building sales capacity.
