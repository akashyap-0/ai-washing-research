# Microsoft Corporation — FY26 Q4 Earnings Call (transcript)

- **Company:** Microsoft (MSFT); fiscal year ends June 30
- **Period:** FY26 Q4
- **Source:** official transcript on Microsoft Investor Relations — https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**138 AI sentences of 519 total**
(Borderline, listed at the end: 1 automation/robotics, 33 infrastructure, none containing an AI term.)

## Prepared remarks

### Satya Nadella, chairman and chief executive officer
1. First, ensuring AI empowers every person, amplifying their agency and ambition.
2. Now, let’s talk about how we are delivering this across our stack, starting with our AI platform and infrastructure.
3. For example, we increased the throughput for Copilot workloads 4X since the start of the year.
4. AI sovereignty is increasingly top of mind for our customers, and we are expanding our offerings to meet that need.
5. Just last week, we announced a partnership with Mistral to bring its models to Microsoft Sovereign Cloud, enabling customers to run them across public, customer-controlled, and fully disconnected environments.
6. Maia 200 continues to scale.
7. It delivers 30% better performance per dollar than the latest-generation hardware in our fleet and is now supporting both OpenAI and MAI models. ⚑ context-dependent
8. And we will be among the first cloud providers to deploy next-generation rack-scale AI infrastructure based on AMD Helios and NVIDIA Vera Rubin.
9. When it comes to running agents, CPUs are just as important as GPUs. ⚑ uncertain
10. Our Cobalt VMs are powering both our own first-party workloads, as well as workloads for customers including Adobe, Arm, Elastic, OpenAI, Sprinklr, and Tom Tom.
11. Now, let me turn to the end-to-end platform we are building on this infrastructure to run, govern, and distribute apps and agents. ⚑ uncertain
12. It starts with model choice. ⚑ uncertain ⚑ context-dependent
13. Every customer wants the right model for each task, based on quality, latency, cost, and compliance. ⚑ uncertain
14. We offer the broadest model catalog in the cloud, with over 11,000 models, including the latest from OpenAI, Anthropic, Mistral, xAI, as well as our own MAI family.
15. Since the start of the year, we have seen a 5X increase in the number of customers building with models from multiple providers. ⚑ uncertain
16. Levi Strauss & Co. for example is using models from OpenAI and Anthropic on Foundry, as it brings more than 1,000 domain-specific agents into a unified enterprise AI platform.
17. We are also accelerating our own model development. ⚑ uncertain
18. We announced more than a dozen new models across image, voice, transcription, coding, and security, including our first reasoning model MAI Thinking 1, all with cost efficient inference at their core for Enterprise use cases.
19. We are co-designing these models with our silicon, and are seeing 40% better performance per watt when running MAI models on Maia 200.
20. But more importantly, we are building a new model system, where the harness, context, memory, and action space are separate from any one model family, thereby moving the frontier on the cost-to-outcome curve. ⚑ uncertain
21. It also has the added benefit of business continuity and resilience because every model is substitutable. ⚑ uncertain ⚑ context-dependent
22. For example, millions of developers have used MAI-Code-1-Flash on GitHub Copilot, achieving higher code acceptance rates and 10% lower median token usage, while still having access to frontier capabilities from OpenAI and Anthropic.
23. In Excel, MAI-Code-1-Flash is delivering comparable quality to GPT-5.6 for the most common tasks, while operating at significantly lower cost.
24. In security, MAI-Cyber-1-Flash achieves better performance than the much larger Mythos model but at half the cost, when combined with our multi-agent security harness.
25. More broadly, across our model implementations we’re seeing significant efficiency gains, including 89% reduction of GPU costs in Dynamics 365 with MAI-Voice-2-Flash and up to 84% reduced GPU costs in PowerPoint with MAI-Image-2.5.
26. And this system is available to any company as part of Foundry. ⚑ uncertain
27. The data estate is evolving from primarily supporting apps used by people to supporting agents. ⚑ uncertain
28. Customers are rapidly adopting our AI-optimized databases like Cosmos DB and PostgreSQL, to give agents fast, secure access to real-time data and context they need for memory and retrieval.
29. Also, the number of PostgreSQL customers also using Foundry increased 80%, as customers increasingly choose it as their database for AI workloads.
30. And over 17,000 customers now use Foundry and Fabric, up 60% year-over-year, as enterprises connect agents to real-time operational, analytical, and unstructured data in Fabric. ⚑ uncertain
31. This quarter, we also introduced Rayfin, the agent-first SDK that delivers a backend as a service for building apps on Fabric. ⚑ uncertain
32. On top of this data estate, we are building an IQ layer that combines data with model capabilities to deliver the right context at the right time. ⚑ uncertain
33. Tens of thousands of customers – including nearly 90% of the Fortune 500 – are already grounding their agents in enterprise context with Foundry, Fabric, and Work IQ. ⚑ uncertain
34. And this quarter we introduced Web IQ, which gives agents access to real-world intelligence from across the web. ⚑ uncertain
35. It is already used by many of the most popular AI assistants, including ChatGPT. ⚑ context-dependent
36. Beyond model choice, data, and context, we are building Foundry as the complete app and agent stack. ⚑ uncertain
37. It gives agents access to the IQ layer and tools they use, along with durable state and memory, secure sandboxes, rubrics and evals, and even their own self-improvement loops. ⚑ uncertain ⚑ context-dependent
38. We now have 100,000 Foundry customers, and revenue more than doubled year-over-year. ⚑ uncertain
39. Telefónica for example adopted Foundry as the foundation of its corporate agentic platform, with its first wave of agents tackling mission-critical network ops.
40. All up, the number of Foundry customers at a one trillion token annualized run rate increased 4X year-over-year. ⚑ uncertain
41. And finally, with Agent 365 we offer a control plane that extends companies’ existing governance, identity, security, and management frameworks to agents they build. ⚑ uncertain
42. Just two months in, Agent 365 now has nearly 40 million agents registered across tens of thousands of companies. ⚑ uncertain
43. Now, let me turn to the apps and agents we are building on top of this platform for individuals and organizations. ⚑ uncertain
44. When it comes to knowledge work, we now have over 30 million paid Microsoft 365 Copilot seats, with net seat adds more than doubling quarter-over-quarter.
45. Copilot is evolving rapidly, from chat to Cowork to Autopilots.
46. This quarter, we also introduced Autopilots, autonomous, long-running agents with full enterprise compliance, including an always-on personal agent powered by OpenClaw. ⚑ uncertain
47. And this quarter we will bring these Copilot experiences together, including Code, in one “super app” spanning both consumer and commercial experiences.
48. More broadly, we have steadily been improving the quality and performance of Copilot, and have been delighted by the recent customer feedback.
49. And the number of enterprise customers deploying Copilot to the majority of their information workers grew nearly 75% quarter-over-quarter, a signal of how central Copilot has become to their operations.
50. NHS England, for example, is rolling out Copilot to 505,000 clinicians and staff — the largest healthcare deployment of its kind — after a trial showed it saved employees an average of 43 minutes per day.
51. And we have been encouraged by the response to our new E7 suite, as customers increasingly go “all in” on an integrated AI offering that brings together Copilot, E5, Entra, and Agent 365.
52. In biz apps, we have been reinventing Dynamics 365 for an agent-first world. ⚑ uncertain
53. We are exposing over 650,000 MCP actions across sales, finance, supply chain, HR, and customer service so that agents can now access business context and take action using the same data models, rules, permissions, security guardrails, and audit trails as any application user. ⚑ uncertain
54. When it comes to developers, GitHub Copilot now has 50 million users.
55. This quarter, we introduced usage-based billing, and have continued to see Business and Enterprise seat growth, and also significant consumption revenue after the new model went into effect. ⚑ uncertain
56. Copilot revenue accelerated over 60% quarter-over-quarter.
57. All up, GitHub now has 225 million users, as organizations across every industry – including over 90% of the Fortune 500 – choose GitHub for their AI-powered development.
58. The agentic era is being built on GitHub.
59. Every major coding agent runs on the platform and one in three pull requests on GitHub now involves an agent. ⚑ uncertain
60. In security, we are helping customers both secure their AI deployments and use AI to strengthen their security posture.
61. To date, Purview has audited over 50 billion Copilot interactions to meet compliance obligations, up nearly 360% year-over-year.
62. And earlier this week we introduced Project Perception, a complete multi-model agentic security system that brings together teams of agents to simulate attacks, investigate threats, and drive remediation.
63. Mass General Brigham rolled out Dragon Copilot to over 4,000 providers after a study found ambient AI reduced burnout by 21%.
64. And in science, Microsoft Discovery, now broadly available, provides a comprehensive platform for building and governing agentic workflows for science and engineering.
65. Across both our high value agentic experiences and the AI platform and infrastructure, we are focused on helping customers turn AI into measurable outcomes.
66. And therefore there is an enormous opportunity to turn customers' workflows, domain knowledge, and accumulated judgment into AI systems that learn and improve with every usage.
67. We will embed 6,000 industry and engineering experts with customers to co-design, co-innovate, and continuously improve AI systems at scale.
68. We have been testing this model over the past year, completing over 330 projects across 164 customers, including many of the world’s leading companies across industries. ⚑ uncertain
69. For example, our FDE teams worked with Novo Nordisk to build an agent that helps analyze clinical data while meeting its strict compliance requirements. ⚑ uncertain
70. And we partnered with LSEG to embed AI into LSEG Workspace, helping finance professionals ask complex questions and quickly find answers across structured and unstructured financial content.
71. In Windows, we are investing to ensure that it has the best quality and fundamentals, while also ensuring it is the best place to run secure edge AI.
72. Recruiters at over 20,000 companies are now using our AI-powered solutions to reduce time to hire and improve candidate matching.
73. I have never been more confident in Microsoft’s opportunity to drive durable, long-term growth and ensure the benefits of AI flow broadly.

### Amy Hood, chief financial officer
74. This fiscal year, we delivered over $331 billion in revenue, with growth accelerating to 18%, driven by strong demand across both the Azure platform and our first-party AI applications and services. ⚑ context-dependent
75. Earnings per share was $4.74, an increase of 23%, when adjusted for the impact from our investment in OpenAI.
76. These include a $3.2 billion gain from our investment in Anthropic and lower-than-expected expenses related to the Voluntary Retirement Program, which were partially offset by severance expense and impairment charges in XBOX. ⚑ context-dependent
77. Company gross margin percentage was 67%, down year-over-year, driven by sales mix shift to Azure as well as continued investments in AI infrastructure and growing product usage, partially offset by ongoing efficiency gains, particularly in Azure and M365 Commercial cloud.
78. When adjusted for the impact of our investments in OpenAI, other income and expense was $2.8 billion driven by the gain on investment in Anthropic noted earlier.
79. Roughly two thirds of our capex was for short-lived assets, primarily CPUs and GPUs as customers increasingly build solutions that leverage both AI and non-AI infrastructure.
80. Commercial bookings grew 18% when excluding the impact from OpenAI driven by strong execution in our core annuity sales motions and reflecting broad customer demand across geographies and customer segments.
81. Bookings increased 10% and 11% in constant currency when including Azure commitments from OpenAI.
82. All sequential commercial RPO growth was driven by commitments from customers outside of frontier model companies.
83. And RPO increased 25% when excluding OpenAI.
84. RPO, including OpenAI, has a weighted average duration of 2.3 years.
85. Microsoft Cloud revenue was $59.3 billion and grew 27%, reflecting strong demand across Azure and our first-party AI applications and services.
86. And for the full year, our cloud revenue surpassed $214 billion, with nearly 90% from customers outside of frontier model companies.
87. Microsoft Cloud gross margin percentage was better than expected at 65%, and down year-over-year driven by sales mix shift to Azure, as well as continued investments in AI infrastructure and increased product usage, partially offset by ongoing efficiency gains noted earlier.
88. Building on our Copilot momentum from Q3, net paid seat adds more than doubled sequentially, with paid seats now over 30 million.
89. Premium offerings, including Copilot, E5, and early traction in E7, drove ARPU growth this quarter.
90. And gross margin percentage decreased slightly with increased M365 Copilot usage as we continue to invest in product quality and drive further efficiency gains.
91. Results also benefited from stronger-than-expected GitHub Copilot consumption following the June business model change to align pricing with usage and value.
92. Segment gross margin dollars increased 24% and gross margin percentage decreased year-over-year primarily driven by sales mix shift to Azure, as well as the continued scaling of our AI infrastructure ahead of growing demand, partially offset by ongoing efficiency gains in Azure.
93. Segment gross margins were also impacted by growing GitHub Copilot usage, though margins improved through the quarter with the June business model change to usage-based pricing.
94. In commercial bookings, when adjusted for the impact from OpenAI, we expect healthy growth on a growing expiry base driven by strong execution across our core annuity sales motions.
95. As a reminder, the significant OpenAI contracts signed in the prior year will result in some quarterly volatility in both the bookings and RPO growth rates.
96. Sequential growth from our momentum in Copilot, E5, and E7, is mitigated a bit by the lower ARPU new seat adds in frontline worker and small and medium business SKUs.
97. Excluding any impact from our investments in OpenAI, other income and expense is expected to be roughly negative $100 million as interest income will be more than offset by interest expense, which includes the interest payments related to datacenter finance leases.

## Q&A

### Operator
1. Maybe I’ll start away from the numbers and ask if you could spend a minute and elaborate on your opening comments about model choice and the protection of corporate IP. ⚑ uncertain
2. First, how material do you think traction could be for open and custom models over the next year or two, knowing that many enterprises might be initially reticent to use open models? ⚑ uncertain

### Satya Nadella, chairman and chief executive officer
3. The way we are coming at this is at the end of the day, the goal is to have the firm be in control of their own destiny, in terms of what I describe as building their human capital and their token capital. ⚑ uncertain
4. And the models are an input, not some extraction of the knowledge of the enterprise. ⚑ uncertain
5. Given that direction of travel, we are very, very clear about the architectural design of the platform, which is you’ve got to keep your harness separate from the model, when the harness will ensure that your memory, your context all of that is external. ⚑ uncertain
6. That means any given model at any given time is swappable. ⚑ uncertain ⚑ context-dependent
7. You should and you can use frontier models.
8. If you look at some of the stats I gave, it’s a great example of how to use the frontier models for what they deliver, how to use low-cost models for what they deliver, and in fact, train your own model when you don’t want to use any external model itself, because after all, you have all the outputs, you have all the traces, you have all the context.
9. Copilot is built that way.
10. GitHub Copilot is built that way.
11. Our Security Copilot is built that way.
12. And by the way, one of the things that’s least talked about is remember, if you look even at the Hugging Face incident, the biggest thing that you should take away from that is you can’t depend on any one model. ⚑ uncertain
13. You will maybe need multiple models to even remediate some challenges that get caused by one model. ⚑ uncertain
14. That’s the way to think about it, which is you can’t be subject to the refusals of one model. ⚑ uncertain ⚑ context-dependent

### Amy Hood, chief financial officer
15. And I think maybe, Karl, just to add a little bit to the end of your question, which is that it’s why it’s important that the platform is built, and I think Satya mentioned this in his comments, to be able to deliver the right model for the right job on the architecture called Azure. ⚑ uncertain
16. And so, given that we continue to see growing demand no matter what model is chosen or what model family or whether it’s run a model of your own, the Azure platform is quite efficient at delivering that. ⚑ uncertain

### Operator
17. Satya, Amy, sentiment around AI remains incredibly volatile with concerns about oversupply coming, as well as concerns about component pricing increasing impacting margins.

### Satya Nadella, chairman and chief executive officer
18. Amy talked about how what we’re doing, whether it’s in Copilot or the Super App, bringing all the form factors or all the way to Azure, and the agent-first primitives in Azure.

### Operator
19. I wanted to maybe just ask about M365 Copilot.

### Satya Nadella, chairman and chief executive officer
20. We now have chat, Cowork, autopilot, code all coming to essentially, what is going to become this flagship Super App that various roles can use it. ⚑ uncertain
21. It’s wired into the governance pieces with Agent 365 so that you have your IT Ops, SecOps, FinOps all wired in, as well as it’s all the business processes. ⚑ uncertain ⚑ context-dependent
22. In fact, if I think about historically, Office compared to what Copilot is, is much more narrower.

### Amy Hood, chief financial officer
23. Yeah, Adam, and I think I talked a little bit about it in my prepared remarks, but I do think what we’ve been seeing is over the course of this year, some of the growth in ARPU was from E5 plus the Copilot license that Satya is talking about.
24. We’ll see a little bit more from E7 really has a lot of interesting value in the Agent 365 component, in particular, where Satya is talking about, I mean, having SecOps and FinOps, think about in general, everyone is going to need both observability of token spend and the manageability of token spend for all business processes. ⚑ uncertain

### Satya Nadella, chairman and chief executive officer
25. I took that document to Copilot, which is a PDF, and I said, “Build me a new Power BI dashboard, essentially.” But here is the thing.
26. It built a rich semantic model that went into my Fabric with OneLake that brought all the data in from the external sources. ⚑ uncertain ⚑ context-dependent
27. And then on top of that, the repo itself is in GitHub, but the artifact is sitting in my Copilot as a site.
28. And by the way, it’s all registered with Agent 365. ⚑ uncertain

### Operator
29. Satya, appreciating cybersecurity is so core to everything Microsoft does, the playing field shifted recently with the latest frontier model releases, and this week you introduced Project Perception.

### Satya Nadella, chairman and chief executive officer
30. What we are focused on is first, again, take the same approach we’ve taken for knowledge work or coding, which is you’ve got to start with an intelligence-first, model-forward approach. ⚑ uncertain
31. And so, what we launched with Perception is essentially saying, let’s really make sure that you have the Red Team agents that know how to find – constantly are red teaming and finding the vulnerabilities. ⚑ uncertain
32. Then you have the Blue Team agent that is constantly going and making sure that you’re triaging, and the Green Team that fixes. ⚑ uncertain
33. You create your own agentic system that’s continuously operating to create the cyber defense you need.
34. The other thing we’ve also said is especially in cyber, it becomes critical to have that multi-model approach, to the first question that was asked, not just for cost. ⚑ uncertain
35. In fact, we proved with the MDASH data in CyberGym that essentially, you can have Mythos-level performance with 50% less cost because of this MAI-Cyber-1-Flash.
36. And the reason is because 90% of the tasks are done by the Cyber-1-Flash model, and 10% of the tasks, you still go to the frontier. ⚑ uncertain
37. This is that mixing of the right model for the right task in what is essentially a pipeline job is a super important characteristic. ⚑ uncertain ⚑ context-dependent
38. For whatever reason, if a given model goes away, then you can’t be left high and dry. ⚑ uncertain

### Amy Hood, chief financial officer
39. The work, frankly, on model diversification also is a margin improvement opportunity. ⚑ uncertain
40. Being able to serve the best possible outcome with a more efficient, or both efficient in terms of token usage and efficient in terms of cost structure are also margin levers. ⚑ uncertain
41. As we think about the mix of the portfolio being able to have a pretty broad pool across knowledge work, coding, security, then basically the agent layer, I’ll call that Agent 365 as kind of a cheat, but all of that also is an opportunity, and then of course what we talked about on the Azure side between model efficiency, silicon, and component efficiency, including our investments in 1P solutions there, and just the overall efficiency of running it at a hyperscale. ⚑ uncertain

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Satya Nadella, chairman and chief executive officer] In healthcare, we are on pace to automate over 100 million patient encounters this calendar year, including 28 million this quarter, up 2X year-over-year.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Satya Nadella, chairman and chief executive officer] We added 31 new datacenters across 5 continents this quarter, bringing the total to 88 this year, as we expand our footprint in response to accelerating demand.
2. [Prepared remarks · Satya Nadella, chairman and chief executive officer] Over the last fiscal year, we have reduced dock-to-live times for new GPUs in our largest regions by nearly 50%.
3. [Prepared remarks · Satya Nadella, chairman and chief executive officer] We are also getting more from the infrastructure we already have by optimizing across silicon, systems, and software.
4. [Prepared remarks · Satya Nadella, chairman and chief executive officer] And by the end of this month, we expect to have our Cobalt 200 racks in over 25 datacenters around the world as we rapidly expand capacity.
5. [Prepared remarks · Satya Nadella, chairman and chief executive officer] We see significant opportunity for Windows to become the offload for unmetered intelligence, combining powerful on device compute with enterprise-grade security.
6. [Prepared remarks · Amy Hood, chief financial officer] Operating expenses increased 10% driven by continued investment in R&D compute capacity, talent, and data to support product development across the portfolio.
7. [Prepared remarks · Amy Hood, chief financial officer] Capital expenditures were $41 billion including the impact from higher component pricing as noted in our guide.
8. [Prepared remarks · Amy Hood, chief financial officer] This quarter, total finance leases were $5.6 billion and were primarily for large datacenter sites.
9. [Prepared remarks · Amy Hood, chief financial officer] And free cash flow was $19.6 billion reflecting higher capital expenditures.
10. [Prepared remarks · Amy Hood, chief financial officer] Revenue growth was ahead of expectations driven by efficiency gains across our CPU and GPU fleet as well as process improvements to enable earlier delivery of new capacity.
11. [Prepared remarks · Amy Hood, chief financial officer] In our on-premises server business, revenue was relatively unchanged year-over-year and was down 1% in constant currency.
12. [Prepared remarks · Amy Hood, chief financial officer] Now, before I move to outlook, effective at the start of FY27, we are extending the estimated useful lives of our datacenters and office buildings, from 15 to 25 years, reflecting our operating history and expected use of these assets.
13. [Prepared remarks · Amy Hood, chief financial officer] The greater impact is on capital expenditures as more of our future datacenter leases will shift from finance leases to operating leases as a result of this update.
14. [Prepared remarks · Amy Hood, chief financial officer] Finance leases are included in capital expenditures while operating leases are not.
15. [Prepared remarks · Amy Hood, chief financial officer] Outside of this useful life impact, our calendar year 2026 CapEx investment expectations remain unchanged.
16. [Prepared remarks · Amy Hood, chief financial officer] In both the M365 Commercial products and Server products KPIs, we are lapping higher transactional purchasing from the timing of product launches and expect revenue from both to decline in the mid-single digits for the full fiscal year.
17. [Prepared remarks · Amy Hood, chief financial officer] Operating expenses should grow in the mid to high-single digits, reflecting continued investment in R&D compute capacity, talent, and data.
18. [Prepared remarks · Amy Hood, chief financial officer] And we expect FY27 capital expenditures will grow year-over-year given demand signals across our portfolio.
19. [Prepared remarks · Amy Hood, chief financial officer] In our on-premises server business, we expect revenue to decline in the low to mid-single digits, with ongoing customer shift to cloud offerings and the prior-year comparable noted earlier.
20. [Prepared remarks · Amy Hood, chief financial officer] And operating expense of $16.8 to $16.9 billion or growth of 7% to 8% driven by continued investment in R&D compute capacity and talent.
21. [Prepared remarks · Amy Hood, chief financial officer] Next, capital expenditures.
22. [Prepared remarks · Amy Hood, chief financial officer] We expect CapEx spend will be over $50 billion including the lease reclassification impact from the useful life update.
23. [Q&A · Amy Hood, chief financial officer] Think about that infrastructure as being pretty fungible.
24. [Q&A · Amy Hood, chief financial officer] It’s going to be efficiency gains in the GPU fleet.
25. [Q&A · Amy Hood, chief financial officer] I would also say some of the process improvements we’ve made to make sure both CPUs and GPUs, just the lead time from how quickly we can get things to simplify it tremendously plugged in, was also improved over the past 90 days.
26. [Q&A · Operator] Amy, two related questions: How does Microsoft protect itself if there really is overcapacity and overbuilding of data centers or overbuilding of chips, etcetera?
27. [Q&A · Amy Hood, chief financial officer] Currently, the situation is obviously that demand exceeds available supply in a relatively extreme moment, but when you start to think about over the duration, I try to remind people, a lot of the expense, especially you see it in CapEx, you’ve seen our CapEx really pivot toward what I would call and do call short-lived assets, which really, that’s CPUs and GPUs that have relatively shorter lead times.
28. [Q&A · Amy Hood, chief financial officer] The investment into land and data center builds is actually quite flexible.
29. [Q&A · Amy Hood, chief financial officer] It’s a smaller percentage of the overall cost structure, and timing can be changed on much of that, especially on the builds, or you can stagger the timing of the build out of, as I was saying, some of the GPUs and CPUs that you plan to put in.
30. [Q&A · Amy Hood, chief financial officer] We’re reminding people that frankly, the cloud offers tremendous benefits versus having to make these purchases as servers on-prem yourself, or the price increases are even more hard for customers.
31. [Q&A · Operator] You’ve given us color on the CapEx side of the equation.
32. [Q&A · Operator] When you look at and track ROI on the CapEx decisions you’re making today, how does that compare to a year ago, and what are some of the levers that you can still pull, perhaps from the internal silicon side, for example, as a driver of incremental monetization going forward?
33. [Q&A · Amy Hood, chief financial officer] I would say the way to think about it for me is more the confidence in the TAM expansion, the margin levers that we have in terms of both product improvements than the infrastructure improvements.
