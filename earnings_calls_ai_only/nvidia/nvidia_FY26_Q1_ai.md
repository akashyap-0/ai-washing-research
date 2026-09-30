# NVIDIA Corporation — Q1 FY26 Earnings Call (transcript)

- **Company:** NVIDIA (NVDA); fiscal year ends late January
- **Period:** Q1 FY26 (call held May 28, 2025)
- **Source:** official transcript published on NVIDIA Investor Relations (q4cdn PDF)
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**203 AI sentences of 470 total**
(Borderline, listed at the end: 2 automation/robotics, 22 infrastructure, none containing an AI term.)

## Prepared remarks

### Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.
1. AR workloads have transitioned strongly to inference, and AI factory build outs are driving significant revenue.
2. On April 9, the US government issued new export controls on H20. ⚑ uncertain
3. We sold H20 with the approval of the previous administration. ⚑ uncertain
4. Although our H20 has been in the market for over a year and does not have a market outside of China, the new export controls on H20 did not provide a grace period to allow us to sell through our inventory. ⚑ uncertain
5. In Q1, we recognized $4.6 billion in H20 revenue, which occurred prior to April 9, but also recognized a $4.5 billion charge, as we wrote down inventory and purchase obligations tied to orders we had received prior to April 9. ⚑ uncertain
6. We were unable to ship $2.5 billion in H20 revenue in the first quarter due to the new export controls. ⚑ uncertain
7. Losing access to the China AI accelerator market, which we believe will grow to nearly $50 billion, would have a material adverse impact on our business going forward and benefit our foreign competitors in China and worldwide.
8. Our Blackwell ramp, the fastest in our company's history, drove a 73% year-on-year increase in Data Center revenue. ⚑ uncertain
9. Blackwell contributed nearly 70% of Data Center compute revenue in the quarter, with a transition from Hopper nearly complete. ⚑ uncertain
10. The introduction of GB200 NVL was a fundamental architectural change to enable Data Center scale workloads and to achieve the lowest cost per inference token.
11. GB200 NVL racks are now generally available for model builders, enterprises and sovereign customers to develop and deploy AI.
12. On average, major hyperscalers are each deploying nearly 1,000 NVL72 racks or 72,000 Blackwell GPUs per week and are on track to further ramp output this quarter. ⚑ uncertain
13. Microsoft, for example, has already deployed tens of thousands of Blackwell GPUs and is expected to ramp to hundreds of thousands of GB200s with OpenAI as one of its key customers.
14. Key learnings from the GB200 ramp will allow for a smooth transition to the next phase of our product roadmap, Blackwell Ultra. ⚑ uncertain
15. Sampling of GB300 systems began earlier this month at the major CSPs, and we expect production shipments to commerce later this quarter. ⚑ uncertain
16. GB300 will leverage the same architecture, same physical footprint and the same electrical and mechanical specifications as GB200. ⚑ uncertain
17. The GB300 drop-in design will allow CSPs to seamlessly transition their systems and manufacturing used for GB200, while maintaining high yields. ⚑ uncertain
18. B300 GPUs with 50% more HBM will deliver another 50% increase in dense FP4 inference compute performance compared to the B200.
19. We are witnessing a sharp jump in inference demand.
20. OpenAI, Microsoft and Google are seeing a step function leap in token generation.
21. Microsoft processed over 100 trillion tokens in Q1, a five-fold increase on a year-over-year basis. ⚑ uncertain
22. This exponential growth in Azure OpenAI is representative of strong demand for Azure AI Foundry as well as other AI services across Microsoft's platform. ⚑ context-dependent
23. Inference serving startups are now serving models using B200, tripling their token generation rate and corresponding revenues for high value reasoning models such as DeepSeek-R1 as reported by artificial analysis.
24. NVIDIA Dynamo on Blackwell NVL72 turbocharges AI inference throughput by 30x for the new reasoning models sweeping the industry.
25. Developer engagements increased with adoption ranging from LLM providers such as Perplexity to financial services institutions such as Capital One, who reduced agentic chatbot latency by 5x with Dynamo.
26. In the latest MLPerf inference results, we submitted our first results using GB200 NVL72, delivering up to 30x higher inference throughput compared to our eight GPU H200 submission on the challenging Llama 3.1 benchmark.
27. This feat was achieved through a combination of tripling the performance for GPU as well as 9x more GPUs, all connected on a single NVLink domain. ⚑ uncertain ⚑ context-dependent
28. And while Blackwell is still early in its lifecycle, software optimizations have already improved its performance by 1.5x in the last month alone. ⚑ uncertain
29. We expect to continue improving the performance of Blackwell through its operational life as we have done with Hopper and Ampere. ⚑ uncertain
30. For example, we increased the inference performance of Hopper by four times over two years. ⚑ uncertain
31. This is the benefit of NVIDIA's programmable CUDA architecture and rich ecosystem. ⚑ uncertain ⚑ context-dependent
32. The pace and scale of AI factory deployments are accelerating with nearly 100 NVIDIA-powered AI factories in flight this quarter, a two-fold increase year-over-year, with the average number of GPUs powering each factory also doubling in the same period.
33. And more AI factory projects are starting across industries and geographies.
34. NVIDIA's full stack architecture is underpinning AI factory deployments as industry leaders like AT&T, BYD, Capital One, Foxconn, MediaTek, and Telenor are strategically vital sovereign clouds like those recently announced in Saudi Arabia, Taiwan and the UAE.
35. We have a line of sight to projects requiring tens of gigawatts of NVIDIA AI infrastructure in the not-too-distant future.
36. The transition from generative to agentic AI, AI capable of perceiving, reasoning, planning and acting will transform every industry, every company and country.
37. We envision AI agents as a new digital workforce capable of handling tasks ranging from customer service to complex decision-making processes.
38. We introduced the Llama Nemotron family of open reasoning models designed to supercharge agentic AI platforms for enterprises.
39. Built on the Llama architecture, these models are available as NIMs or NVIDIA inference microservices with multiple sizes to meet diverse deployment needs.
40. Our post training enhancements have yielded a 20% accuracy boost and a 5x increase in inference speed, leading platform companies including Accenture, Cadence, Deloitte and Microsoft are transforming work with our reasoning models.
41. NVIDIA NeMo microservices are generally available across industries are being leveraged by leading enterprises to build, optimize and scale AI applications.
42. With NeMo, Cisco increased model accuracy by 40% and improved response time by 10x in its code assistant.
43. Nasdaq realized a 30% improvement in accuracy and response time in its AI platform's search capabilities.
44. And Shell's custom LLM achieved a 30% increase in accuracy when trained with NVIDIA NeMo.
45. NeMo's parallelism techniques accelerated model training time by 20% when compared to other frameworks.
46. Brands, the world's largest restaurant company to bring NVIDIA AI to 500 of its restaurants this year and expanding to 61,000 restaurants over time to streamline order-taking, optimize operations and enhance service across its restaurants.
47. For AI-powered cybersecurity leading companies like Check Point, CrowdStrike and Palo Alto Networks are using NVIDIA's AI security and software stack to build, optimize and secure agentic workflows, with CrowdStrike realizing 2x faster detection triage with 50% less compute cost.
48. Our customers continue to leverage our platform to efficiently scale up and scale out AI factory workloads.
49. We created the world's fastest switch, NVLink for scale up, our NVLink compute fabric in its fifth generation offers 14x the bandwidth of PCIe Gen5. ⚑ uncertain
50. NVLink 72 carries 130 terabytes per second of bandwidth in a single rack, equivalent to the entirety of the world's peak internet traffic. ⚑ uncertain
51. NVLink is a new growth vector and is off to a great start with Q1 shipments exceeding $1 billion. ⚑ uncertain
52. At COMPUTEX, we announced NVLink Fusion. ⚑ uncertain
53. Hyperscale customers can now build semi-custom CCUs and accelerators that connect directly to the NVIDIA platform with NVLink. ⚑ uncertain
54. For scale out, our enhanced Ethernet offerings delivered the highest throughput, lowest latency networking for AI.
55. Adoption is widespread across major CSPs and consumer internet companies, including CoreWeave, Microsoft Azure, Oracle Cloud and xAI.
56. These platforms will enable next-level AI factory scaling to millions of GPUs through the increasingly power efficiency by 3.5x and network resiliency by 10x, while accelerating customer time to market by 1.3x. ⚑ context-dependent
57. China as a percentage of our Data Center revenue was slightly below our expectations and down sequentially due to H20 export licensing controls. ⚑ uncertain
58. Note that over 99% of H100, H200, and Blackwell Data Center compute revenue billed to Singapore was for orders from US-based customers. ⚑ uncertain
59. Moving to gaming and AI PCs.
60. Strong adoption by gamers, creatives and AI enthusiasts have made Blackwell our fastest ramp ever, against a backdrop of robust demand, we greatly improved our supply and availability in Q1 and expect to continue these efforts in Q2.
61. AI is transforming PC and creator and gamers.
62. This quarter, we added to our AI PC laptop offerings, including models capable of running Microsoft's CoPilot+.
63. This past quarter, we brought Blackwell architecture to mainstream gaming with its launch of GeForce RTX 5060 and 5060 Ti, starting at just $299. ⚑ uncertain ⚑ context-dependent
64. In console gaming, the recently unveiled Nintendo Switch 2 leverages NVIDIA's neural rendering and AI technologies, including next-generation custom RTX GPUs with DLSS technology deliver a giant leap in gaming performance to millions of players worldwide.
65. Tariff related uncertainty temporarily impacted Q1 systems and demand for our AI workstations is strong, and we expect sequential revenue growth to resume in Q2.
66. NVIDIA DGX Spark and DGX Station revolutionize personal computing by putting the power of an AI supercomputer in a desktop form factor.
67. DGX Spark delivers up to 1 petaflop of AI compute while DGX Station offers an incredible 20 petaflops and is powered by the GB300 Superchip.
68. DGX Spark will be available in calendar Q3 and DGX Station later this year. ⚑ uncertain
69. We have deepened Omniverse's integration and adoption into some of the world's leading software platforms including Databricks, SAP and Schneider Electric. ⚑ uncertain
70. New Omniverse blueprints such as Mega for at-scale robotic fleet management are being leveraged in KION Group, Pegatron, Accenture and other leading companies to enhance industrial operations. ⚑ uncertain
71. At COMPUTEX, we showcased Omniverse's great traction with technology manufacturing leaders, including TSMC, Quanta, Foxconn, Pegatron. ⚑ uncertain
72. Using Omniverse, TSMC saves months in work by designing fabs virtually. ⚑ uncertain
73. Year-on-year growth was driven by the ramp of self-driving across a number of customers and robust and demand for NAVs. ⚑ uncertain
74. We are partnering with GM to build the next-gen vehicles, factories and robots using NVIDIA AI, simulation and accelerated computing.
75. And we are now in production with our full stack solution for Mercedes-Benz starting with the new CLA hitting roads in the next few months We announced Isaac GR00T N1, the world's first open fully customizable foundation model for humanoid robots enabling generalized reasoning and skill development.
76. We also launched new open NVIDIA Cosmo world foundation models.
77. Leading companies include 1X, Agility Robotics, Figure AI, Uber and Waabi.
78. We've begun integrating Cosmos into their operations for synthetic data generation, while Agility Robotics, Boston Dynamics, and XPENG Robotics are harnessing Isaac's simulation to advance their humanoid efforts. ⚑ uncertain
79. GE Healthcare is using the new NVIDIA Isaac platform for healthcare simulation built on NVIDIA Omniverse and using NVIDIA Cosmos. ⚑ uncertain
80. The era of robotics is here, billions of robots, hundreds of millions of autonomous vehicles and hundreds of thousands of robotic factories and warehouses will be developed. ⚑ uncertain
81. Our investments include expanding our infrastructure capabilities and AI solutions, and we plan to grow these investments throughout the fiscal year.
82. In Data Center, we anticipate the continued ramp of Blackwell to be partially offset by a decline in China revenue. ⚑ uncertain
83. Note, our outlook reflects a loss in H20 revenue of approximately $8 billion for the second quarter. ⚑ uncertain
84. We expect better Blackwell profitability to drive modest sequential improvement in gross margins. ⚑ uncertain
85. Further financial details are included in the CFO commentary and other information available on our IR website, including a new financially information AI agent.
86. We will be at the BofA Global Technology Conference in San Francisco on June 4, The Rosenblatt Virtual AI Summit and Nasdaq Investor Conference in London on June 10, and GTC Paris at VivaTech on June 11 in Paris.

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
87. On export control, China is one of the world's largest AI markets and a springboard to global success.
88. With half of the world's AI researchers based there, the platform that wins China is positioned to lead globally.
89. The H20 export ban ended our Hopper Data Center business in China. ⚑ uncertain
90. We cannot reduce Hopper further to comply. ⚑ uncertain
91. We are exploring limited ways to compete, but Hopper is no longer an option. ⚑ uncertain
92. China's AI moves on with or without US chips.
93. It has to compute to train and deploy advanced models. ⚑ context-dependent
94. The question is not whether China will have AI, it already does.
95. The question is whether one of the world's largest AI markets will run on American platforms.
96. The AI race is not just about chips.
97. The US has based its policy on the assumption that China cannot make AI chips.
98. In the end, the platform that wins the AI developers wins AI.
99. Export controls should strengthen US platforms, not drive half of the world's AI talent to rivals.
100. On DeepSeek, DeepSeek and Qwen from China are among the most – among the best open source AI models.
101. DeepSeek-R1, like ChatGPT, introduced reasoning AI that produces better answers, the longer it thinks.
102. Reasoning AI enables step-by-step problem solving, planning and tool use, turning models into intelligent agents.
103. Reasoning is compute-intensive, requires hundreds to thousands more – thousands of times more tokens per task than previous one-shot inference. ⚑ uncertain
104. Reasoning models are driving a step-function surge in inference demand.
105. AI scaling laws remain firmly intact, not only for training, but now inference too, requires massive scale compute.
106. DeepSeek also underscores the strategic value of open source AI.
107. When popular models are trained and optimized on US platforms, it drives usage, feedback and continuous improvement, reinforcing American leadership across the stack. ⚑ uncertain
108. US platforms must remain the preferred platform for open source AI.
109. America wins when models like DeepSeek and Qwen runs best on American infrastructure.
110. In Houston, we're partnering with Foxconn to construct a million square foot factory to build AI supercomputers.
111. To encourage and support these investments, we've made substantial long-term purchase commitments, a deep investment in America's AI manufacturing future.
112. Each GB200 NVLink72 racks contains 1.2 million components and weighs nearly 2 tons. ⚑ uncertain
113. On AI diffusion rule, President Trump rescinded the AI diffusion rule, calling it counterproductive, and proposed a new policy to promote US AI tech with trusted partners.
114. I was honored to join him in announcing a 500 megawatt AI infrastructure project in Saudi Arabia and a 5 gigawatt AI campus in the UAE.
115. Every nation now sees AI as core to the next industrial revolution, a new industry that produces intelligence and essential infrastructure for every economy.
116. Countries are racing to build national AI platforms to elevate their digital capabilities.
117. At COMPUTEX, we announced Taiwan's first AI factory in partnership with Foxconn and the Taiwan government.
118. Last week, I was in Sweden to launch its first national AI infrastructure.
119. Japan, Korea, India, Canada, France, the UK, Germany, Italy, Spain and more are now building national AI factories to empower startups, industries and societies.
120. Sovereign AI is a new growth engine for NVIDIA.

## Q&A

### Joe Moore, Analyst, Morgan Stanley & Co. LLC
1. You guys have talked about this scaling up of inference around reasoning models for at least a year now.
2. Can you give us a sense for how much of that demand you're able to serve and give us a sense for maybe how big the inference business is for you guys? ⚑ uncertain
3. And do we need full on NVL72 rack scale solutions for reasoning inference going forward? ⚑ uncertain

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
4. Grace Blackwell NVLink72 is the ideal engine today, the ideal computer thinking machine, if you will, for reasoning AI.
5. The first reason is that the token generation amount, the number of tokens reasoning goes through is 1,000 times more than a one-shot chatbot.
6. And so what we would like to do, and the reason why Grace Blackwell was designed to give such a giant step-up in inference performance is so that you could do all this and still get a response as quickly as possible. ⚑ uncertain
7. Compared to Hopper, Grace Blackwell is some 40 times higher speed and throughput compared. ⚑ uncertain
8. That was the core driving reason for Grace Blackwell NVLink72. ⚑ uncertain ⚑ context-dependent

### Vivek Arya, Analyst, BofA Securities, Inc.
9. So is there still some left as a headwind for the remaining quarters just, Colette, how to model that? ⚑ uncertain
10. Back at GTC, you had outlined a path towards almost $1 trillion of AI spending over the next few years.
11. Just what are your customer discussions telling you about how to model growth for next year? ⚑ uncertain

### Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.
12. Thanks so much for the question regarding H20. ⚑ uncertain
13. Yes, we recognized $4.6 billion H20 in Q1. ⚑ uncertain
14. And we had highlighted in terms of the amount of orders that we had planned for H20 in Q2, and that was $8 billion. ⚑ uncertain

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
15. Vivek, the – probably the best way to think through it is that AI is several things.
16. Of course, we know that AI is this incredible technology that's going to transform every industry from, of course, the way we do software to healthcare and financial services to retail to, I guess, every industry, transportation, manufacturing, and we're at the beginning of that.
17. And we know because of that, we recognize that AI is also an infrastructure.
18. It's a way of developing a technology – delivering a technology that requires factories and these factories produce tokens. ⚑ uncertain ⚑ context-dependent
19. Now we've reached an extraordinary milestone with AIs that are reasoning or thinking, what people call inference time scaling.
20. Of course, it created a whole new – we've entered an era where inference is going to be a significant part of the compute workload. ⚑ uncertain
21. But beyond that, we're going to have to – we're going to see AI go into enterprise, which is on-prem because so much of the data is still on-prem.
22. And so we're going to move AI into the enterprise.
23. And you saw that we announced a couple of really exciting new products, our RTX PRO enterprise AI server that runs everything enterprise and AI, our DGX Spark and DGX Station, which is designed for developers who want to work on-prem.
24. And so enterprise AI is just taking off.
25. Today, a lot of the telco infrastructure will be in the future software defined and built on AI, and so 6G is going to be built on AI and that infrastructure needs to be built out.
26. And then, of course, every factory today that makes things will have an AI factory that sits with it.
27. And the AI factory is going to be – drive creating AI and operating AI for the factory itself, but also to power the products and the things that are made by the factory.
28. So it's very clear that every car company will have AI factories.
29. And very soon, there'll be robotics companies, robot companies and those companies will be also building AIs to drive the robots.

### Operator
30. And then also we heard from Oracle and xAI, just to name a few.
31. And perhaps more importantly, how are these orders impacting your lead times for Blackwell and your current visibility sitting here today almost halfway through 2025? ⚑ uncertain

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
32. And it's – just about every country needs to build out AI infrastructure and their umpteenth AI factories being planned.
33. I think in the remarks, Colette mentioned there's some 100 AI factories being built.
34. We were talking about earlier that we had a huge breakthrough in the last couple of years with reasoning AI.
35. And now there are agents that reason and there are super-agents that use a whole bunch of tools and then there's clusters of super agents where agents are working with agents, solving problems. ⚑ uncertain
36. And so you could just imagine, compared to one-shot chatbots and the agents that are now using AI built on these large language models, how much more compute-intensive they really need to be and are.

### Ben Reitzes, Analyst, Melius Research LLC
37. The $8 billion for H20 just seems like it's roughly $3 billion more than most people thought with regard to what you'd be foregoing in the second quarter. ⚑ uncertain
38. And then this second part of my question, Jensen, I know you guide one quarter at a time, but with regard to the AI diffusion rule being lifted and this momentum with sovereign, there's been times in your history where you guys have said on calls like this, where you have more conviction in sequential growth throughout the year, et cetera.
39. And given the unleashing of demand with AI diffusion being revoked and the supply chain increasing, does the environment give you more conviction in sequential growth as we go throughout the year?

### Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.
40. When we look at our Q2 guidance and our commentary that we provided that had the export controls not occurred, we would have had orders of about $8 billion for H20, that's correct. ⚑ uncertain
41. So what we also have talked about here is the growth that we've seen in Blackwell, Blackwell across many of our customers, as well as the growth that we continue to have in terms supply that we need for our customers. ⚑ uncertain

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
42. The first positive surprise is the step function demand increase of reasoning AI.
43. I think it is fairly clear now that AI is going through an exponential growth, and reasoning AI really busted through.
44. Concerns about hallucination or its ability to really solve problems, and I think a lot of people are crossing that barrier and realizing how incredibly effective agentic AI is and reasoning AI is.
45. So number one is inference reasoning and the exponential growth there, demand growth. ⚑ uncertain
46. The second one, you mentioned AI diffusion.
47. It's really terrific to see that the AI diffusion rule was rescinded. ⚑ context-dependent
48. And so AI diffusion happened, the rescinding of it happened at almost precisely the time that countries around the world are awakening the importance of AI as an infrastructure, not just as a technology of great curiosity and great importance, but infrastructure for their industries and start-ups and society.
49. Just as they had to build out infrastructure for electricity and internet, you got to build out an infrastructure for AI.
50. The third is enterprise AI.
51. Agents work and agents are doing – these agents are really quite successful, much more than generative AI.
52. Agentic AI is game-changing.
53. Agents can understand ambiguous and rather implicit instructions and able to problem solve and use tools and have memory and so on. ⚑ uncertain
54. And so I think this is a – enterprise AI is ready to take off.
55. And it's taken us a few years to build a computing system that is able to integrate and run enterprise AI stacks, run enterprise IT stacks, but add AI to it.
56. And then lastly, industrial AI.
57. In addition to AI factories, of course, there are new electronics manufacturing, chip manufacturing being built around the world.
58. And all of these new plants and these new factories are creating exactly the right time when Omniverse and AI and all the work that we're doing with robotics is emerging.
59. Every factory will have an AI factory associated with it.
60. And in order to create these physical AI systems, you really have to train a vast amount of data.
61. So back to more data, more training, more AIs to be created, more computers.

### Timothy Arcuri, Analyst, UBS Securities LLC
62. It sounds like the July guidance assumes there's no SKU replacement for the H20. ⚑ uncertain ⚑ context-dependent
63. I think we're all trying to figure out how much to add back to our models and when. ⚑ uncertain

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
64. And the new set of limits pretty much make it impossible for us to reduce Hopper any further for any productive use. ⚑ uncertain
65. And so the new limits, it's kind of the end the road for Hopper. ⚑ uncertain

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
66. And that platform is called NVLink. ⚑ uncertain
67. And NVLink is – comes with it chips and switches and NVLink spines and it's really complicated. ⚑ uncertain
68. But in the case of AI, you have a lot of computers working together.
69. And the traffic of AI is insanely bursty.
70. Latency matters a lot, because the AI is thinking and it wants to get work done as quickly as possible, and you got a whole bunch of nodes working together.

### Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.
71. Grace Blackwell is in full production. ⚑ uncertain
72. Inference, once the lighter workload is surging with revenue generating AI services.
73. AI is growing faster and will be larger than any platform shifts before, including the internet, mobile and cloud.
74. Blackwell is built to power the full AI lifecycle from training frontier models to running complex inference and reasoning agents at scale.
75. Training demand continues to rise with breakthroughs in post training and like reinforcement learning and synthetic data generation.
76. But inference is exploding. ⚑ uncertain
77. Reasoning AI agents require orders of magnitude more compute.
78. Sovereign AI, nations are investing in AI infrastructure like they once did for electricity and internet.
79. Enterprise AI, AI must be deployable on-prem and integrated with existing IT.
80. Our RTX PRO, DGX Spark and DGX Station enterprise AI systems are ready to modernize the $500 billion IT infrastructure on-prem or in the cloud.
81. Industrial AI from training to digital twin simulation to deployment, NVIDIA Omniverse and Isaac GR00T are powering next-generation factories and humanoid robotic systems worldwide.
82. The age of AI is here from AI infrastructures, inference at scale, sovereign AI, enterprise AI, and industrial AI, NVIDIA is ready.
83. Join us at GTC Paris, our keynote at VivaTech on June 11, talking about quantum GPU computing, robotic factories and robots and celebrate our partnerships building AI factories across the region.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] The platform speeds development of robotic imaging and surgery systems.
2. [Prepared remarks · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] Future plants will be highly computerized in robotics.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] Data Center revenue of $39 billion grew 73% year-on-year.
2. [Prepared remarks · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] Our data center GPU designed specifically for the China market.
3. [Prepared remarks · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] We are still evaluating our limited options to supply Data Center compute products compliant with the US government's revised export control rules.
4. [Prepared remarks · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] For Q2, we expect a meaningful decrease in China Data Center revenue.
5. [Prepared remarks · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] These GeForce RTX 5060 and 5060 Ti desktop, GPUs and laptops are now available.
6. [Prepared remarks · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] As that stack grows to include 6G and quantum, US global infrastructure leadership is at stake.
7. [Prepared remarks · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] Our goal from chip to supercomputer built in America within a year.
8. [Prepared remarks · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] No one has produced supercomputers on this scale.
9. [Prepared remarks · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] The deals he announced are wins for America, creating jobs, advancing infrastructure, generating tax revenue and reducing the US trade deficit.
10. [Prepared remarks · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] The US will always be NVIDIA's largest market and home to the largest installed base of our infrastructure.
11. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] Of course, in order to do that, we had to reinvent, literally redesign, the entire way that these supercomputers are built.
12. [Q&A · Colette M. Kress, Chief Financial Officer & Executive Vice President, NVIDIA Corp.] When we look at our Q2, our Q2 is going to be meaningfully down in terms of China Data Center revenue.
13. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] But anyhow, it's going to be a new infrastructure, and we're building it out in the cloud.
14. [Q&A · Operator] There have been many large GPU cluster investment announcements in the last month, and you alluded to a few of them with Saudi Arabia, the UAE.
15. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] And I think the important concept here which makes it easier to understand is that like other technologies that impact literally every single industry, of course, electricity was one and it became infrastructure.
16. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] Of course, the information infrastructure, which we now know as the internet affects every single industry, every country, every society.
17. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] It's essential infrastructure.
18. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] And so I think we're clearly in the beginning of the build-out of this infrastructure.
19. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] And what's unique about this infrastructure is that it needs factories.
20. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] It's a little bit like the energy infrastructure, electricity.
21. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] And this is the RTX PRO enterprise server that we announced at COMPUTEX just last week.
22. [Q&A · Jensen Huang, Co-Founder, President, Chief Executive Officer & Director, NVIDIA Corp.] But remember, enterprise IT is really three pillars, it's compute, storage and networking.
