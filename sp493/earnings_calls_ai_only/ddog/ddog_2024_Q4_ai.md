# Datadog — 2024_Q4 Earnings Call (transcript)

- **Company:** Datadog (DDOG); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** DDOG
- **CIK:** 0001561550
- **Period:** 2024_Q4 (call held February 13, 2025; date from page date line)
- **Calendar quarter:** 2024 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2025/02/13/datadog-ddog-q4-2024-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** 2276765e90f2a7e1c406e9c1839d2129d8a91c031ae992ee6a72649719d1ed59
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**45 AI sentences of 522 total**
(Borderline, listed at the end: 1 automation/robotics, 15 infrastructure, none containing an AI term.)

## Prepared remarks

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
1. During 2024, we kept building and innovating as we scaled up our teams and went broader and deeper into the problems we solve for our customers from the cloud to AI.
2. We now have more than 850 integrations, making it easy for our customers to bring in every type of data they need, benefits from all the new AWS, Azure, GCP, and OCI capabilities, and engage with the latest technologies like the newly emerging AI stack.
3. And we took several big steps to expand on Datadog as the best observability platform for OpenTelemetry users, including making our infra monitoring and APM instrumentation fully interoperable with OTel components and improving the experience for OTel customers by embedding the OTel collector directly within the Datadog agent. ⚑ uncertain
4. In the next-gen AI and LLM space, we continue to add capabilities to Bits AI, launching Bits AI for incident management and previewing Bits AI for autonomous investigations.
5. We launched LLM Observability in general availability to help customers evaluate, safely deploy, and manage their models in production, and we continue to see increased interest in next-gen AI.
6. At the end of Q4, about 3,500 customers use one or more Datadog AI integrations to send us data about their machine learning, AI, and LLM usage.
7. We launched Event Management for general availability using AI Ops to intelligently aggregate, consolidate, and simplify alerts from any sources.
8. And we think moving to modern cloud-based technologies is more important than ever as more companies step up to adopt AI capabilities.

### David M. Obstler, Chief Financial Officer
9. Next, we continue to see robust contribution from AI-native customers who represented about 6% of Q4 ARR, roughly the same as the quarter -- as last quarter and up from about 3% of ARR in the year-ago quarter.
10. AI-native customers contributed about five percentage points of year-over-year revenue growth in Q4 versus four points in the last quarter and about three points in the year-ago quarter.
11. So, we saw strong growth from AI-native customers in Q4.
12. We believe that adoption of AI will continue to benefit Datadog in the long term.

## Q&A

### Mark Murphy, Analyst
1. I'm curious how you're feeling overall about the book of business for AI-native customers.
2. In other words, I'm trying to understand if the AI usage and commits are kind of on the same trajectory that they were on or whether you feel that there are some oscillations there.

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
3. When you look at the AI cohort, we definitely saw some renewals with higher commits, better terms, and optimization usage all at the same time, which is fairly typical, which typically happens with larger customers, in particular.
4. And when we talk about the AI cohort, what's interesting is not so much this relatively small set of AI-native companies, and we see them more as a sign of things to come in terms of a broader AI adoption.
5. So, what's interesting to us is how the rest of the world starts operating in AI workload and grows into that.

### Mark Murphy, Analyst
6. And they were talking about capacity constraints on the AI side.
7. But the non-AI side for some of them seem to slow just regular typical cloud migrations.
8. And I'm just wondering if you felt the timing of the holidays, excuse me, had any impact on December or whether their AI capacity constraints might be flowing through to Datadog as well.

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
9. It's hard to tell exactly what's going on with the AI capacity constraint and things like that. ⚑ context-dependent
10. If you back out the -- as you mentioned, the GPU-related, AI-related part of the growth for the top providers, they are slowing down, and we are meaningfully outgrowing them at that part of the business.

### Raimo Lenschow, Analyst
11. There's a lot of focus on the big AI guys at the moment, but how do you -- I mean, that's -- but that's only the starting point for the AI opportunity.
12. Can you see -- like what you see in first feedback on people looking at inference workloads and trying to have observability on them?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
13. So ,on the inference side, mostly, still what customers do is they use a third-party model, either through an API or through a third-party inference platform. ⚑ uncertain
14. And they -- and what they're interested in is measuring whether that model is doing the right thing. ⚑ uncertain
15. And that's what we serve right now with LLM Observability, for example.
16. That's where we see quite a bit of adoption that does not come largely from the AI-native companies. ⚑ context-dependent
17. In terms of operating the inference stack fully, we see relatively few customers do that yet. ⚑ uncertain
18. It looks like there's many, many different options that are going to be viable for running your AI inference. ⚑ context-dependent
19. There's models that you can install in the open source. ⚑ uncertain
20. There are models in the open source today that are rivaling in quality with the best closed API models. ⚑ uncertain
21. So, we think the ecosystem is developing into a rich, diverse ecosystem that will allow customers to have a diversity of modalities for using AI, which is exciting.

### Matthew Hedberg, Analyst
22. And then maybe to put a finer point on the AI-native question earlier, does your guidance assume that we see a pretty stable contribution there throughout the year?

### David M. Obstler, Chief Financial Officer
23. In terms of the AI contribution, I think we try to embed that in the level of the discount.
24. I think we essentially don't assume that there's going to be some non-pro rata acceleration of AI.

### Eric Heath, Analyst
25. And Oli, I'd love to just get some of your thoughts on agentic AI and AI generally.
26. Just curious, when we think about agents, which parts of the core observability platform that you think are most relevant or going to be most beneficial to your business as you start to monitor those? ⚑ uncertain

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
27. What we do see, though, is that when we built -- we started building our LLM Observability product.
28. Most of the use cases we saw there from customers were chatbot in nature or rag in nature, trying to access information and return the information.
29. Now, we see more and more customers building agents on top of that and sending us the data from their agents. ⚑ uncertain
30. And the LLM Observability product is a good level of abstraction, at least for the current iteration of these agents to look at them.
31. In our internal development, obviously, we use our own products heavily for that, and we see a lot of different opportunities to automate work with agents on top of our platform. ⚑ uncertain
32. I will say, though, that we also do see new modalities, different modalities for developing those agents. ⚑ uncertain

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
33. Well, it's everywhere, like the -- what's fascinating about the current evolution of AI, in particular, is that it touches a lot of the different areas of the business.

## Borderline: automation/robotics without an AI term

1. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] Part of that is [Inaudible] or new products for automating incident resolution and that sort of thing.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] And we have achieved this milestone largely by growing our first product, Infrastructure Monitoring, and expanding into the other pillars of observability: APM and Log Management.
2. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] Today, Infrastructure Monitoring contributes over $1.25 billion in ARR.
3. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We launched Datadog Monitoring for Oracle Cloud Infrastructure, so customers can now monitor their OCI stack and unify their monitoring across all clouds and on-prem environments.
4. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We shipped Datadog Infrastructure-as-Code Security, so our customers can identify and fix misconfigurations in their Terraform and CloudFormation code.
5. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] This customer is moving thousands of hosts from on-prem to the cloud and will replace two legacy infrastructure network monitoring tools.
6. [Prepared remarks · David M. Obstler, Chief Financial Officer] After taking into account capital expenditures and capitalized software, free cash flow was $241 million for a free cash flow margin of 33%.
7. [Prepared remarks · David M. Obstler, Chief Financial Officer] Finally, we expect capital expenditures and capitalized software together to be in the 4% to 5% of revenues range in 2025.
8. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] If you look at the top five, 10 companies in the world by infrastructure size today, some don't run any third-party software and build everything themselves.
9. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] If I would just compare and contrast what we do with our growth with the cloud providers, overall, we're growing a bit faster than the cloud providers, including the very big bump they're getting from selling GPUS, which is not something we monetize very well on our end, in part because those GPUs are largely attached to trading workloads that we don't play a big role in, but also in part because these are sort of new pieces of infrastructure that will have different needs as they become more broadly used by a larger number of companies.
10. [Q&A · Koji Ikeda, Analyst] I appreciate all the disclosure on ARR coming from the three core pillars here on Infrastructure Monitoring, APM, and logs.
11. [Q&A · Koji Ikeda, Analyst] And so, as we move into 2025 and beyond, how do you think about the potential for Infrastructure Monitoring specifically the growth there to accelerate from current levels?
12. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] I think there's -- first, there's a number of new DCs that are emerging that are related to infrastructure that we might want to cover.
13. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] I'm talking in particular about infrastructure concerns around GPU management, GPU optimization, I guess quite a lot going on there that we can potentially do.
14. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] But we -- for that, we need to see broad usage of the raw GPUs by a large number of customers as opposed to usage by a smaller number of native customers, which is mostly what we still see to that.
15. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] So, there's a number already has where we can progress on the on the infrastructure side.
