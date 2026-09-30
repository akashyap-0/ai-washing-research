# NVIDIA Corporation — Q1 FY24 Earnings Call (transcript)

- **Company:** NVIDIA (NVDA); fiscal year ends late January
- **Period:** Q1 FY24 (call held May 24, 2023)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/05/24/nvidia-nvda-q1-2024-earnings-call-transcript/
- **Note:** NVIDIA does not host an official transcript for this call. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing.
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**144 AI sentences of 518 total**
(Borderline, listed at the end: 0 automation/robotics, 73 infrastructure, none containing an AI term.)

## Prepared remarks

### Colette Kress, Executive Vice President and Chief Financial Officer
1. Generative AI is driving exponential growth in compute requirements and a fast transition to NVIDIA accelerated computing, which is the most versatile, most energy-efficient, and the lowest TCO approach to train and deploy AI.
2. Generative AI drove significant upside in demand for our products, creating opportunities and broad-based global growth across our markets.
3. First, CSPs around the world are racing to deploy our flagship Hopper and Ampere architecture GPUs to meet the surge in interest from both enterprise and consumer, AI applications for training, and inference.
4. Multiple CSPs announced the availability of H100 on their platforms, including private previews at Microsoft Azure, Google Cloud, and Oracle Cloud Infrastructure, upcoming offerings at AWS and general availability at emerging GPU specialized cloud providers like CoreWeave and Lambda. ⚑ uncertain
5. In addition to enterprise AI adoption, these CSPs are serving strong demand for H100 from generative AI pioneers.
6. Second, consumer internet companies are also at the forefront of adopting generative AI and deep learning-based recommendation systems, driving strong growth.
7. For example, Meta has now deployed its H100-powered brand Teton AI supercomputer for its AI production and research teams.
8. Third, enterprise demand for AI and accelerated computing is strong.
9. We are seeing momentum in verticals such as automotive, financial services, healthcare, and telecom where AI and accelerated computing are quickly becoming integral to customers' innovation road maps and competitive positioning.
10. For example, Bloomberg announced it has a $50 billion parameter model, BloombergGPT, to help with financial natural language processing tasks such as sentiment analysis, named entity recognition, news classification, and question answering.
11. Auto insurance company, CCC Intelligence Solutions, is using AI for estimating repairs.
12. And AT&T is working with us on AI to improve fleet dispatches so their field technicians can better serve customers.
13. Among other enterprise customers using NVIDIA AI are Deloitte, for logistics and customer service, and Amgen, for drug discovery and protein engineering.
14. This quarter, we started shipping DGX H100, our Hopper generation AI system, which customers can deploy on-prem.
15. And with the launch of DGX Cloud through our partnership with Microsoft Azure, Google Cloud, and Oracle Cloud Infrastructure, we deliver the promise of NVIDIA DGX to customers from the cloud. ⚑ uncertain
16. Whether customer -- whether the customers deploy DGX on-prem or via DGX Cloud, they get access to NVIDIA AI software, including NVIDIA-based command, end-to-end AI frameworks, and pretrained models.
17. We provide them with the blueprint for building and operating AI, spanning our expertise across systems, algorithms, data processing, and training methods.
18. We also announced NVIDIA AI Foundations, which are model foundry services available on DGX Cloud that enable businesses to build, refine, and operate custom large language models and generative AI models trained with their own proprietary data, created for unique domain-specific tasks.
19. They include NVIDIA NeMo for large language models; NVIDIA Picasso for images, video, and 3D; and NVIDIA BioNeMo for life sciences. ⚑ context-dependent
20. Each service has six elements: pretrained models, frameworks for data processing and curation, proprietary knowledge-based vector databases, systems for fine-tuning, aligning and guardrailing, optimized inference engines, and support from NVIDIA experts to help enterprises fine-tune models for their custom use cases. ⚑ uncertain
21. ServiceNow, a leading enterprise services platform is an early adopter of DGX Cloud and NeMo.
22. They are developing custom large language models trained on data specifically for the ServiceNow platform. ⚑ context-dependent
23. Our collaboration will let ServiceNow create new enterprise-grade generative AI offerings with the thousands of enterprises worldwide running on the ServiceNow platform, including for IT departments, customer service teams, employees, and developers.
24. Generative AI is also driving a step function increase in inference workflows.
25. The latest MLPerf industry benchmark released in April showed NVIDIA's inference platforms deliver performance that is orders of magnitude ahead of the industry with unmatched versatility across diverse workloads. ⚑ uncertain
26. To help customers deploy generative AI applications at scale, at GTC, we announced four major new inference platforms that leverage the NVIDIA AI software stack.
27. These include L4 Tensor Core GPU for AI video; L40 for Omniverse and graphics rendering, H100 NBL for large language models; and the Grace Hopper Superchip for LLM and also recommendation systems and vector databases. ⚑ context-dependent
28. Google Cloud is the first CSP to adopt our L4 inference platform with the launch of its G2 virtual machines for generative AI inference and other workloads, such as Google Cloud Dataproc, Google [Inaudible], Google Alpha Fold and Google Cloud's Immersive Stream, which render 3D and AR experiences.
29. In addition, Google is integrating our Triton Inference Server with Google Kubernetes engine and its cloud-based Vertex AI platform.
30. In networking, we saw strong demand at both CSPs and enterprise customers for generative AI and accelerated computing, which require high-performance networking like NVIDIA's Mellanox networking platforms.
31. As generative AI applications grow in size and complexity, high-performance networks become essential for delivering accelerated computing at data center scale to meet the enormous demand of both training and inferencing.
32. Our 400-gig Quantum-2 InfiniBand platform is the gold standard for AI-dedicated infrastructure, with broad adoption across major cloud and consumer internet platforms, such as Microsoft Azure.
33. For multi-tenant cloud transitioning to support generative AI, our high-speed ethernet platform with BlueField-3 DPUs and Spectrum-4 ethernet switching offers the highest available ethernet network performance.
34. We look forward to sharing more about our 400-gig spectrum for accelerated AI networking platform next week at the COMPUTEX conference in Taiwan.
35. This adds to growing momentum for Grace with both CPU-only and CPU-GPU opportunities across AI and cloud and supercomputing applications. ⚑ context-dependent
36. The coming wave of BlueField-3, Grace, and Grace Hopper superchips will enable a new generation of super energy-efficient accelerated data centers. ⚑ uncertain
37. The GeForce RTX 40 Series GPU laptops are off to a great start, featuring four NVIDIA inventions, RTX path tracing, DLSS 3 AI rendering, Reflex Ultra-low latency rendering, and Max-Q energy-efficient technologies.
38. Unlike our desktop offerings, 40 Series laptops support the NVIDIA Studio platform for software technologies, including acceleration for creative data science and AI workflows, and Omniverse, giving content creators unmatched tools and capabilities.
39. Generative AI will be transformative to gaming and content creation from development to runtime.
40. At the Microsoft Build Developer Conference earlier this week, we showcased how Windows PCs and workstations with NVIDIA RTX GPUs will be AI-powered at their core.
41. NVIDIA and Microsoft have collaborated on end-to-end software engineering, spanning from the Windows operating system to the NVIDIA graphics drivers and NeMo LLM framework to help make Windows on NVIDIA RTX Tensor Core GPUs a supercharged platform for generative AI.
42. Generative AI is a major new workload for NVIDIA-powered workstation.
43. Our collaboration with Microsoft transforms Windows into the ideal platform for creators and designers harnessing generative AI to elevate their creativity and productivity.
44. At GTC, we announced NVIDIA Omniverse Cloud and NVIDIA Fully Managed Service, running in Microsoft Azure, that includes the full suite of Omniverse applications and NVIDIA OVX infrastructure. ⚑ uncertain
45. NVIDIA Omniverse Cloud will be available starting in the second half of this year. ⚑ uncertain
46. Microsoft NVIDIA will also connect Office365 applications with Omniverse. ⚑ uncertain
47. Omniverse Cloud is being used by companies to digitize the workflows from design and engineering to smart factories and 3D content generation for marketing. ⚑ uncertain
48. The automotive industry has been a leading early adopter of Omniverse, including companies such as BMW Group, Geely Lotus, General Motors and Jaguar Land Rover. ⚑ uncertain
49. We expect this sequential growth to largely be driven by data center, reflecting a steep increase in demand related to generative AI and large language models.
50. In addition, we will be attending the BofA Global Technology Conference in San Francisco on June 6th, and Rosenblatt Virtual Technology Summit on the Age of AI on June 7th, and the New Street Future of Transportation Virtual Conference on June 12th.

## Q&A

### Colette Kress, Executive Vice President and Chief Financial Officer
1. So, when we talk about our sequential growth that were expected between Q1 and Q2, our generative AI, large language models are driving this surge in demand.
2. And it's broad-based across both our consumer Internet companies, our CSPs, our enterprises, and our AI start-ups.
3. It is also interest in both of our architectures, both of our Hopper latest architecture, as well as our Ampere architecture. ⚑ uncertain ⚑ context-dependent

### C.J. Muse, Evercore ISI, Analyst
4. Number one, where are we in terms of driving acceleration into servers to support AI?

### Jensen Huang, President and Chief Executive Officer
5. The -- remember, we were in full production of both Ampere and Hopper when the ChatGPT moment came.
6. And it helped everybody crystallize how to transition from the technology of large language models to a product and service based on a chatbot.
7. And what happened is when generative AI I came along, it triggered a killer app for this computing platform that's been in preparation for some time.
8. In the future, it's fairly clear now with this -- with generative AI becoming the primary workload of most of the world's data centers generating information, it is very clear now that -- and the fact that accelerated computing is so energy-efficient, that the budget of a data center will shift very dramatically toward accelerated computing, and you're seeing that now.
9. You'll have a pretty dramatic shift in the spend of a data center from traditional computing and to accelerate computing with SmartNICs, smart switches, of course, GPUs and the workload is going to be predominantly generative AI.

### Jensen Huang, President and Chief Executive Officer
10. You have to engineer all of the software and all the libraries and all the algorithms, integrate them into and optimize the frameworks and optimize it for the architecture of not just one chip but the architecture of an entire data center all the way into the frameworks, all the way into the models. ⚑ uncertain
11. The second part is that generative AI is a large-scale problem and it's a data center scale problem.

### Aaron Rakers, Wells Fargo Securities, Analyst
12. I'm curious of what -- where do you think we're at in terms of that approach, in terms of the AI enterprise software suite and other drivers of software-only revenue going forward?

### Colette Kress, Executive Vice President and Chief Financial Officer
13. Not only do we have a substantial amount of software that we are including in our newest architecture and essentially all products that we have, we're now with many different models to help customers start their work in generative AI and accelerated computing.
14. So, anything that we have here from DGX Cloud on providing those services, helping them build models, or, as you've discussed, the importance of NVIDIA AI Enterprise, essentially, that operating system for AI, so all things should continue to grow as we go forward, both the architecture and the infrastructure, as well as the -- both availability of the software and our ability to monetize that with it as well.

### Jensen Huang, President and Chief Executive Officer
15. We can see in real time the growth of generative AI in CSPs, both for training the models, refining the models, as well as deploying the models.
16. As Colette said earlier, inference is now a major driver of accelerated computing because generative AI is used so capably in so many applications already.
17. Enterprise requires a new stack of software because many enterprises need to have all the capabilities that we've talked about, whether it's large language models, the ability to adapt them for your proprietary use case, and your proprietary data and alignment to your own principles and your own operating domains.
18. You want to have the ability to be able to do that in a high-performance computing sandbox, and we call that DGX Cloud and -- to create that model. ⚑ uncertain
19. Then, you want to deploy your chatbot or your AI in any cloud because you have services and you have agreements with multiple cloud vendors and depending on the applications, you might deploy it on various clouds.
20. And for the enterprise, we have NVIDIA AI Foundations for helping you create custom models, and we have NVIDIA AI Enterprise.
21. NVIDIA AI Enterprise is the only accelerated stack -- GPU accelerated stack in the world that is enterprise safe and enterprise supported.
22. There are 4,000 different packages that build up NVIDIA AI Enterprise and represents the operating engine -- end-to-end operating engine of the entire AI workflow.
23. Obviously, in order to train an AI model, you have a lot of data you have to process and package up and curate and align.
24. And then, the second aspect of it is training the model, refining the model.
25. And the third is deploying model for inferencing.NVIDIA AI Enterprise supports and patches and security patches continuously all of those 4,000 packages of software.
26. And so, NVIDIA AI Enterprise is the second part.
27. The third is Omniverse. ⚑ uncertain
28. Just as people are starting to realize that you need to align an AI to ethics, the same for robotics.
29. You need to align the AI for physics, and aligning an AI for ethics includes a technology called reinforcement learning human feedback.
30. In the case of industrial applications and robotics, it's reinforcement learning Omniverse feedback. ⚑ uncertain
31. And Omniverse is a vital engine for software-defined and robotic applications and industries. ⚑ uncertain
32. And so, Omniverse also needs to be a cloud service platform. ⚑ uncertain
33. And so, our software stack, the three software stacks, AI Foundations, AI Enterprise, and Omniverse, runs in all of the world's clouds that we have partnerships, DGX Cloud partnerships with.
34. Azure, we have partnerships on both AI, as well as Omniverse.
35. With GCP and Oracle, we have great partnerships in DGX Cloud for AI, and AI Enterprise is integrated into all three of them.
36. And so, I think the -- in order for us to extend the reach of AI beyond the cloud and into the world's enterprise and into the world's industries, you need two new types of -- you need new software stacks in order to make that happen.

### Tim Arcuri, UBS, Analyst
37. I know you need the low latency of InfiniBand for AI.

### Jensen Huang, President and Chief Executive Officer
38. InfiniBand is designed for an AI factory, if you will.
39. There's a new segment in the middle where the cloud is becoming a generative AI cloud.
40. It's not an AI factory per se, but it's still a multi-tenant cloud, but it wants to run generative AI workloads. ⚑ context-dependent
41. At COMPUTEX, we're going to announce a major product line for this segment, which is for ethernet-focused generative AI application type of clouds.

### Stacy Rasgon, Bernstein Research, Analyst
42. I had a question on inference versus training for generative AI.
43. So, you're talking about inference as being a very large opportunity. ⚑ uncertain
44. Is that because inference basically scales with like the usage versus like training is more of a one and done? ⚑ uncertain
45. And can you give us some sort of -- even if it's just like qualitatively, like do you think inference is bigger than training or vice versa? ⚑ uncertain
46. Is there anything you can give us on those two workloads within generative AI, would be helpful?

### Jensen Huang, President and Chief Executive Officer
47. You're never done producing and processing a vector database that augments the large language model.
48. And so, whether you're building a recommender system, a large language model, a vector database, these are probably the three major applications of -- the three core engines, if you will, of the future of computing, as well as a bunch of other stuff.
49. The inference part of it are APIs that are either open APIs that can be connected to all kinds of applications, APIs that are integrated into workflows but APIs of all kinds. ⚑ uncertain
50. Some of them, part that -- many of them could come from companies like ServiceNow and Adobe that we're partnering with in AI Foundations.
51. And they'll create a whole bunch of generative AI APIs that companies can then connect into their workflows or use as an application.
52. And so, I think you're seeing for the very first time, simultaneously, a very significant growth in the segment of AI factories, as well as a market that -- a segment that really didn't exist before but now it's growing exponentially, practically by the week, for AI inference with APIs.
53. It's called generative AI. ⚑ context-dependent
54. Every quarter's capital, capex budget would lean very heavily into generative AI, into accelerated computing infrastructure, everywhere from the number of GPUs that would be used in the capex budget to the accelerated switches and accelerated networking chips that connect them all.
55. The easiest way to think about that is, over the next four, five, 10 years, most of that $1 trillion and then compensating, adjusting for all the growth in data center still, it will be largely generative AI.
56. And so, that's probably the easiest way to think about that, and that's training as well as inference. ⚑ uncertain

### Joe Moore, Morgan Stanley, Analyst
57. I wanted to follow up on that in terms of the focus on inference. ⚑ uncertain
58. It's pretty clear that this is a really big opportunity around large language models. ⚑ context-dependent
59. Is that where some of the specialty inference products that you launched at GTC come in? ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
60. Whether you're -- whether -- you start by building a large language model, and you use that large language model, very large version, and you could distill them into medium, small, and tiny size.
61. But obviously, the zero shot or the generalizability of the large language model, the biggest one is much more versatile, and it can do a lot more amazing things.
62. And the large one would teach the smaller ones how to be good AIs, and so you use the large one to generate prompts to align the smaller ones and so on and so forth.
63. That's exactly the reason why we have so many different sizes of our inference. ⚑ uncertain ⚑ context-dependent
64. You saw that I announced L4, L40, H100 NVL, which also has H100. ⚑ uncertain
65. And then, it has -- and then, we have H100 HGX, and then we have H100 multinode with NVLink. ⚑ uncertain
66. And so, there's a -- you could have model sizes of any kind that you like. ⚑ uncertain
67. The other thing that's important is these are models, but they're connected ultimately to applications. ⚑ uncertain
68. And it's because the length -- the model itself is only, call it, 25% of the data -- of the overall processing of inference. ⚑ uncertain
69. And so, I think the -- we -- the multi-modality aspect of inference, the multidiversity of inference that it's going to be done in the cloud on-prem, it's going to be done in multi-cloud. ⚑ uncertain
70. That's the reason why we have AI Enterprise in all the clouds. ⚑ context-dependent
71. That's the reason why we have a great partnership with ServiceNow and Adobe because they're going to be creating a whole bunch of generative AI capabilities. ⚑ context-dependent
72. And so, there's a -- the diversity and the reach of generative AI is so broad, you need to have some very fundamental capabilities like what I just described in order to really address the whole space of it.

### Jensen Huang, President and Chief Executive Officer
73. Nearly everybody who thinks about AI, they think about that chip, that accelerator chip.
74. You also see that our network expands starting from NVLink, which is a computing fabric with really super low latency, and it communicates using memory references, not network packaged. ⚑ uncertain
75. And then, we take NVLink. ⚑ uncertain
76. And then, beyond that, if you want to connect the smart AI factory -- this AI factory into your computing fabric, we have a brand-new type of ethernet that we'll be announcing at COMPUTEX.

### Matt Ramsay, Cowen and Company, Analyst
77. One of the things I wanted to dig into a little bit is the DGX Cloud offering. ⚑ uncertain
78. And as we look forward over the next number of quarters, as Colette discussed, the high visibility in the data center business, maybe you could talk a little bit about the mix you're seeing of hyperscale customers buying for their own first-party internal workloads versus their own sort of third party, their own customers versus what of that big upside in data center going forward is systems that you're selling in with potential to support your DGX Cloud offerings and what you've learned since you've launched it about the potential of that business. ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
79. It's -- without being too specific about numbers, but the ideal scenario, the ideal mix is something like 10% NVIDIA DGX Cloud and 90% the CSPs' clouds. ⚑ uncertain ⚑ context-dependent
80. And the reason -- and our DGX Cloud is the NVIDIA stack. ⚑ uncertain
81. Like for example, we're partnering with Azure to bring Omniverse Cloud to the world's industries. ⚑ uncertain
82. And the world has never had a system like that, the computing stack with all the generative AI stuff and all the 3D stuff and the physics stuff, incredibly large database and really high-speed networks and low-latency networks.
83. And so, we partnered with Microsoft to create Omniverse Cloud inside Azure Cloud. ⚑ uncertain
84. But number two, the amount of data and services and security services and all of the amazing things that Azure and GCP and OCI have, they can instantly have access to that through Omniverse Cloud. ⚑ uncertain
85. And if they would like to take their software and run it on the CSP's cloud themselves and manage it themselves, we're delighted by that because NVIDIA AI Enterprise, NVIDIA AI Foundations, and long term, this is going to take a little longer, but NVIDIA Omniverse will run in the CSP's clouds.
86. Our partnership with the three CSPs and that we currently have DGX Cloud in and their sales force and marketing teams, their leadership teams is really quite spectacular. ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
87. The computer industry is going through two simultaneous transitions, accelerated computing and generative AI.
88. CPU scaling has slowed, yet computing demand is strong, and now, with generative AI, supercharged.
89. Companies are now racing to deploy accelerated computing for the generative AI era.
90. Large language models can learn information encoded in many forms.
91. Guided by large language models, generative AI models can generate amazing content with models to fine-tune, guardrail, align to guiding principles.
92. And ground -- ground to facts, generative AI is emerging from labs and is on its way to industrial applications.
93. Whether within one of our CSP partners or on-prem with Dell Helix, whether on a leading enterprise platform like ServiceNow and Adobe or bespoke with NVIDIA AI Foundations, we can help enterprises leverage their domain expertise and data to harness generative AI securely and safely.
94. We are ramping a wave of products in the coming quarters, including H100, our Grace and Grace Hopper Superchips and our BlueField-3 and Spectrum-4 networking platform. ⚑ uncertain

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Strong sequential growth was driven by record data center revenue with our gaming and professional visualization platforms emerging from channel inventory corrections.
2. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Starting with data center.
3. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Record revenue of 4.28 billion was up 18% sequentially and up 14% year on year on strong growth of our accelerated computing platform worldwide.
4. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Demand relating to general purpose CPU infrastructure remains soft.
5. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] With the combination of in-network computing technology and the industry's only end-to-end data center scale optimized software stack, customers routinely enjoy a 20% increase in throughput for their sizable infrastructure investment.
6. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Lastly, our Grace data center CPU is sampling with customers.
7. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] At this week's International Supercomputing Conference in Germany, the University of Bristol announced a new supercomputer based on the NVIDIA Grace CPU superchip, which is 6x more energy efficient than the previous supercomputer.
8. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Strong sequential growth was driven by sales of the 40 Series GeForce RTX GPUs for both notebooks and desktops.
9. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] In desktop, we ramped the RTX 4070, which joined the previously launched RTX 4090, 4080, and the 4070 TI GPUs.
10. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] These GPUs, for the first time, provide 2x the performance of the latest gaming console at mainstream price points.
11. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] The ramp of our Ada Lovelace GPU architecture in workstations kicks off a major product cycle.
12. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] At GTC, we announced six new RTX GPUs for laptops and desktop workstations, with further rollouts planned in the coming quarters.
13. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] This demand has extended our data center visibility out a few quarters, and we have procured substantially higher supply for the second half of the year.
14. [Prepared remarks · Colette Kress, Executive Vice President and Chief Financial Officer] Capital expenditures are expected to be approximately 300 million to 350 million.
15. [Q&A · Toshi Hari, Goldman Sachs, Analyst] Just one question on data center.
16. [Q&A · Toshi Hari, Goldman Sachs, Analyst] Colette, you mentioned the vast majority of the sequential increase in revenue this quarter will come from data center.
17. [Q&A · Colette Kress, Executive Vice President and Chief Financial Officer] So, we have visibility right now for our data center demand that has probably extended out a few quarters.
18. [Q&A · C.J. Muse, Evercore ISI, Analyst] You know, I guess with data center essentially doubling quarter on quarter, two natural kind of questions that relate to one another come to mind.
19. [Q&A · Jensen Huang, President and Chief Executive Officer] And we build supercomputers in volume, and these are giant systems, and we build them in volume.
20. [Q&A · Jensen Huang, President and Chief Executive Officer] It includes, of course, the GPUs.
21. [Q&A · Jensen Huang, President and Chief Executive Officer] But on our GPUs, the system boards have 35,000 other components.
22. [Q&A · Jensen Huang, President and Chief Executive Officer] And the networking and the fiber optics and the incredible transceivers and the NICs, the SmartNICs, the switches, all of that has to come together in order for us to stand up a data center.
23. [Q&A · Jensen Huang, President and Chief Executive Officer] Now, let me talk about the bigger picture and why the entire world's data centers are moving toward accelerated computing.
24. [Q&A · Jensen Huang, President and Chief Executive Officer] It's been known for some time, and you've heard me talk about it, that accelerated computing is a full stack problem but -- is full stack challenged.
25. [Q&A · Jensen Huang, President and Chief Executive Officer] But if you could successfully do it in a large number of application domain that's taken us 15 years, it's sufficiently that almost the entire data centers' major applications could be accelerated, you could reduce the amount of energy consumed and the amount of cost for our data center substantially by an order of magnitude.
26. [Q&A · Jensen Huang, President and Chief Executive Officer] And so, now, we see ourselves in two simultaneous transitions: the world's $1 trillion data center is nearly populated entirely by CPUs today.
27. [Q&A · Jensen Huang, President and Chief Executive Officer] But over the last four years, call it $1 trillion worth of infrastructure installed, and it's all completely based on CPUs and dumb NICs.
28. [Q&A · Jensen Huang, President and Chief Executive Officer] We're going through that moment right now as we speak while the world's data center capex budget is limited.
29. [Q&A · Jensen Huang, President and Chief Executive Officer] But at the same time, we're seeing incredible orders to retool the world's data centers.
30. [Q&A · Jensen Huang, President and Chief Executive Officer] And so, I think you're starting -- you're seeing the beginning of, call it, a 10-year transition to basically recycle or reclaim the world's data centers and build it out as accelerated computing.
31. [Q&A · Vivek Arya, Bank of America Merrill Lynch, Analyst] I just wanted to clarify, does visibility mean data center sales can continue to grow sequentially in Q3 and Q4, or do they sustain at Q2 level?
32. [Q&A · Vivek Arya, Bank of America Merrill Lynch, Analyst] Does it invite more competition in terms of other GPU solutions or other kinds of solutions?
33. [Q&A · Jensen Huang, President and Chief Executive Officer] And the reason for that is because accelerated computing is two things that I talked about often, which is it's a full stack problem.
34. [Q&A · Jensen Huang, President and Chief Executive Officer] It's another way of thinking that the computer is the data center or the data center is the computer.
35. [Q&A · Jensen Huang, President and Chief Executive Officer] It's not the chip, it's the data center.
36. [Q&A · Jensen Huang, President and Chief Executive Officer] And so, in order to get the best performance, you have to understand full stack and understand data center scale.
37. [Q&A · Jensen Huang, President and Chief Executive Officer] And that's what accelerated computing is.
38. [Q&A · Jensen Huang, President and Chief Executive Officer] If you can do one thing and do one thing only incredibly fast, then your data center is largely underutilized, and it's hard to scale that out.
39. [Q&A · Jensen Huang, President and Chief Executive Officer] NVIDIA's universal GPU, the fact that we accelerate so many of these stacks, makes our utilization incredibly high.
40. [Q&A · Jensen Huang, President and Chief Executive Officer] And so, number one is steer put, and that's software-intensive problems and data center architecture problem.
41. [Q&A · Jensen Huang, President and Chief Executive Officer] And the third, it's just data center expertise.
42. [Q&A · Jensen Huang, President and Chief Executive Officer] We've built five data centers of our own, and we've helped companies all over the world build data centers.
43. [Q&A · Jensen Huang, President and Chief Executive Officer] From the moment of delivery of the product to the standing up and the deployment, the time to operations of a data center is measured not -- it can -- if you're not good at it and not proficient at it, it could take months.
44. [Q&A · Jensen Huang, President and Chief Executive Officer] Standing up a supercomputer -- let's see.
45. [Q&A · Jensen Huang, President and Chief Executive Officer] Some of the largest supercomputers in the world were installed about 1.5 years ago, and now they're coming online.
46. [Q&A · Jensen Huang, President and Chief Executive Officer] And that's -- we've taken data centers and supercomputers, and we've turned it into products.
47. [Q&A · Jensen Huang, President and Chief Executive Officer] All of this technology translates into infrastructure, the highest throughput and the lowest possible cost.
48. [Q&A · Aaron Rakers, Wells Fargo Securities, Analyst] As we kind of think about unpacking the various different growth drivers of the data center business going forward, I'm curious, Colette, of just how we should think about the monetization effect of software considering that the expansion of your cloud service agreements continues to grow.
49. [Q&A · Tim Arcuri, UBS, Analyst] But can you sort of talk about the attach rate of your InfiniBand solutions to what you're shipping on the core compute side and maybe whether that's similarly crowding out ethernet like you are with -- on the compute side?
50. [Q&A · Jensen Huang, President and Chief Executive Officer] InfiniBand and ethernet are -- target different applications in a data center.
51. [Q&A · Jensen Huang, President and Chief Executive Officer] If that data center is running a few applications for a few people for a specific use case and is doing it continuously, and that infrastructure costs you, pick a number, $500 million.
52. [Q&A · Jensen Huang, President and Chief Executive Officer] And if you spent $500 million on an infrastructure and the difference is 10% to 20%, and it's $100 million, InfiniBand's basically free.
53. [Q&A · Jensen Huang, President and Chief Executive Officer] The difference in data center throughput is just -- it's too great to ignore.
54. [Q&A · Jensen Huang, President and Chief Executive Officer] And so -- however, if your data center is a cloud data center and it's multi-tenant, it's a bunch of little jobs, a bunch of little jobs and is shared by millions of people, then ethernet is really the right answer.
55. [Q&A · Jensen Huang, President and Chief Executive Officer] The simple way to think about it in the end is that the world has a $1 trillion of data center installed, and it used to be 100% CPUs.
56. [Q&A · Jensen Huang, President and Chief Executive Officer] We've seen it in a lot of places now that you can't reasonably scale out data centers with general purpose computing and that accelerated computing is the path forward.
57. [Q&A · Jensen Huang, President and Chief Executive Officer] And so, the easiest way to think about that is your $1 trillion infrastructure.
58. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] I mean, it's really an integral part to sort of maximize the full performance of your compute platforms.
59. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] I think your data center networking business is driving about $1 billion of revenues per quarter, plus or minus.
60. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] But given the very high attach of your InfiniBand ethernet solutions, your accelerated compute platforms, is the networking run rate stepping up in line with your compute shipments?
61. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] And then, what is the team doing to further unlock more networking bandwidth going forward just to keep pace with the significant increase in compute complexity, data sets, requirements for lower latency, better traffic predictability and so on?
62. [Q&A · Jensen Huang, President and Chief Executive Officer] And I've mentioned before that accelerated computing is about the stack, about the software.
63. [Q&A · Jensen Huang, President and Chief Executive Officer] Nobody ever talks about it because it's hard to understand, but it makes it possible for us to connect tens of thousands of GPUs.
64. [Q&A · Jensen Huang, President and Chief Executive Officer] How do you connect tens of thousands of GPUs if the operating system of the data center, which is the infrastructure, is not insanely great?
65. [Q&A · Jensen Huang, President and Chief Executive Officer] We connect it inside multiple GPUs, and I've described going beyond the GPU.
66. [Q&A · Jensen Huang, President and Chief Executive Officer] And so the -- this whole area of the computing fabric extending -- connecting all of these GPUs and computing units together all the way through the networking, through the switches, the software stack is insanely complicated.
67. [Q&A · Jensen Huang, President and Chief Executive Officer] We sell it to all of the world's data centers as components so that they can integrate it into whatever style or architecture that they would like and we can still run our software stack.
68. [Q&A · Jensen Huang, President and Chief Executive Officer] It's way more complicated the way that we do it, but it makes it possible for NVIDIA's computing architecture to be integrated into anybody's data center in the world from cloud of all different kinds to on-prem of all different kinds, all the way out to the edge to 5G.
69. [Q&A · Jensen Huang, President and Chief Executive Officer] It gives us the ability to partner very deeply with the CSPs to create the highest-performing infrastructure, number one.
70. [Q&A · Jensen Huang, President and Chief Executive Officer] Accelerated computing, a full stack and data center scale approach that NVIDIA pioneered is the best path forward.
71. [Q&A · Jensen Huang, President and Chief Executive Officer] There's $1 trillion installed in the global data center infrastructure based on the general purpose computing method of the last era.
72. [Q&A · Jensen Huang, President and Chief Executive Officer] Over the next decade, most of the world's data centers will be accelerated.
73. [Q&A · Jensen Huang, President and Chief Executive Officer] They will help deliver data center scale computing that is also energy-efficient and sustainable computing.
