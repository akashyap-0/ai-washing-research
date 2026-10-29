# Advanced Micro Devices — 2024_Q4 Earnings Call (transcript)

- **Company:** Advanced Micro Devices (AMD); fiscal year ends December (SEC fiscalYearEnd 1226)
- **Ticker:** AMD
- **CIK:** 0000002488
- **Period:** 2024_Q4 (call held February 4, 2025; date from page date line)
- **Calendar quarter:** 2024 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2025/02/05/advanced-micro-devices-amd-q4-2024-earnings-call-t/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 2)
- **Source SHA-256:** ef0f5f214004f39b66601edebeff58ddd92b7e619fa75b69c059f454695e42ca
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**61 AI sentences of 502 total**
(Borderline, listed at the end: 0 automation/robotics, 79 infrastructure, none containing an AI term.)

## Prepared remarks

### Lisa T. Su, President and Chief Executive Officer
1. We successfully established our multibillion-dollar data center AI franchise.
2. AWS, Alibaba, Google, Microsoft, and Tencent launched more than 100 AMD general-purpose in AI instances in the fourth quarter alone.
3. Turning to our data center AI business.
4. 2024 was an outstanding year, as we accelerated our AI hardware road map to deliver an annual cadence of new Instinct accelerators, expanded our ROCm software suite with significant uplifts in inferencing and training performance, built strong customer relationships with key industry leaders, and delivered greater than $5 billion of data center AI revenue for the year.
5. Meta exclusively used MI300X to serve their Llama 405B frontier model on meta.ai and added instinct GPUs to its OCP-compliant Grand Teton platform, designed for deep learning recommendation models and large-scale AI inferencing workloads.
6. Microsoft is using MI300X to power multiple GPT 4-based Copilot services and launched flagship instances that scale up to thousands of GPUs for AI training and inference and HPC workloads.
7. IBM, Digital Ocean, Vultr, and several other AI-focused CSPs have begun deploying AMD Instinct accelerators for new instances.
8. IBM also announced plans to enable MI300X on their Watson X AI and data platform for training and deploying enterprise-ready generative AI applications.
9. To simplify and accelerate enterprise adoption of AMD Instinct platforms, Dell began offering MI300X as a part of their AI factory solution suite and is providing multiple ready-to-deploy containers via the Dell Enterprise Hub on Hugging Face.
10. Notably, the El Capitan system at Lawrence Livermore National Labs, debuted as the world's fastest supercomputer, using over 44,000 MI300 AI APUs to deliver more than 1.7 exaflops of compute performance.
11. Like El Capitan, Hunter will be used for both foundational scientific research and advanced AI projects, including training LOMs in 24 different European languages.
12. On the AI software front, we made significant progress across all layers of the ROCm stack in 2024.
13. Our strategy is to establish AMD ROCm as the industry's leading open software stack for AI, providing developers with greater choice and accelerating the pace of industry innovation.
14. More than 1 million models on Hugging Face now run out of the box on AMD. ⚑ uncertain
15. And our platforms are supported in the leading frameworks like PyTorch and JAX, serving solutions like VLLM and compilers like OpenAI Triton.
16. We ended the year with the release of ROCm 6.3 that included multiple performance optimizations, including support for the latest flash attention algorithm that runs up to three times faster than prior versions and SG Lang run time that enabled day-zero support for state-of-the-art models like DeepSeek V3.
17. As a result of these latest enhancements, MI300X inferencing performance has increased 2.7 times since launch. ⚑ uncertain
18. Looking forward, we're continuing to accelerate our software investments to improve the out-of-the-box experience for a growing number of customers adopting Instinct to power their diverse AI workloads.
19. For example, we recently closed several large wins with MI300 and MI325 at Lighthouse AI customers that are deploying instinct at scale across both their inferencing and training production environments for the first time.
20. CDNA 4 will deliver the biggest generational leap in AI performance in our history, with a 35 times increase in AI compute performance compared to CDNA 3.
21. We were running large-scale LLMs within 24 hours of receiving first silicon and validation work is progressing ahead of schedule.
22. We designed CDNA next to deliver leadership AI and HPC flops while expanding our memory capacity and bandwidth advantages and supporting an open ecosystem of scale-up and scale-out networking products.
23. We are seeing strong customer interest in the MI400 series for large-scale training and inference deployments and remain on track to launch in 2026. ⚑ uncertain
24. In mobile, we believe we had a record OEM PC sell-through share in the fourth quarter as Ryzen AI 300 Series notebooks ramp.
25. At CES, we expanded our Ryzen portfolio with the launch of 22 new mobile processors that deliver leadership compute, graphics, and AI capabilities.
26. For AI PCs, we are the only provider that offers a complete portfolio of CPUs, enabling Windows Copilot plus experiences on premium ultrathin, commercial, gaming, and mainstream notebooks.
27. RDNA 4 delivers significantly better rate tracing performance and add support for AI-powered upscaling technology that will bring high-quality 4K gaming to mainstream players when the first Radeon 9070 series GPUs go on sale in early March.Now turning to our Embedded segment.
28. We established our multibillion-dollar data center AI business and accelerated both our Instinct hardware and ROCm software road maps.
29. Looking further ahead, the recent announcements of significant AI infrastructure investments like Stargate, and latest model breakthroughs from DeepSeek and the Allen Institute highlight the incredibly rapid pace of AI innovation across every layer of the stack, from silicon to algorithms to models, systems, and applications.
30. These are exactly the types of advances we want to see as the industry invests in increased compute capacity while pushing the envelope on software innovation to make AI more accessible and enable breakthrough generative and agentic AI experiences that can run on virtually every digital device. ⚑ context-dependent
31. AMD is the only provider with the breadth of products and software expertise needed to power AI from end-to-end across data center, edge, and client devices.
32. And we believe this places AMD on a steep long-term growth trajectory, led by the rapid scaling of our data center AI franchise for more than $5 billion of revenue in 2024 to tens of billions of dollars of annual revenue over the coming years.

### Jean Hu, Executive Vice President, Chief Financial Officer
33. We expanded gross margin by 300 basis points and achieved earnings-per-share growth of 25% while investing aggressively in AI to fuel our future growth.
34. All while investing in AI and the innovation to fuel long-term growth.

## Q&A

### Lisa T. Su, President and Chief Executive Officer
1. I mean, I believe that the demand for AI compute is strong.
2. MI350 series is stronger and addresses a broader set of workloads including both inference as well as training. ⚑ uncertain

### Vivek Arya, Analyst
3. And for my follow-up, I would love your perspective on the news from DeepSeek recently, right?

### Lisa T. Su, President and Chief Executive Officer
4. I think the DeepSeek announcements, Allen Institute as well as some of the Stargate announcements, talk about just how much the rate and pace of innovation that's happening in the AI world.
5. So, specifically relative to DeepSeek, look, we think that innovation on the models and the algorithms is good for AI adoption.
6. The fact that there are new ways to bring about training and inference capabilities with less infrastructure actually is a good thing because it allows us to continue to deploy AI compute and broader application space and more adoption.
7. And from that standpoint, having open-source models, looking at the rate and pace of adoption there, I think is pretty amazing.
8. And similarly, on some of the infrastructure investments that were announced with open AI and Stargate and building out, let's call it, massive infrastructure for next-generation AI.
9. I think all of those say that AI is certainly on the very steep part of the curve.
10. And so, with AI, given the diversity of workloads, large models, media models, small models, training, inference when you are talking about broad foundational models or very specific models, you're going to need all types of compute.
11. But my belief is, given how much change there is still going on in AI algorithms that ASICs will still be the smaller part of that TAM because it is a more, call it, specific workload-optimized, whereas GPUs will enable significant programmability and adjustments to all of these algorithm changes.

### Lisa T. Su, President and Chief Executive Officer
12. And from a first-half, second-half statement, as I mentioned, we have some new important AI design wins that are going to be deployed with and MI300 and MI325 in the first half of the year.
13. I mean, it is a more powerful GPU, ASPs go up, and you would expect larger deployments that include training and inference in that time frame. ⚑ uncertain

### Joshua Buchalter, Analyst
14. Obviously, the growth number in the fourth quarter, I mean, it was certainly higher than our model. ⚑ uncertain

### Lisa T. Su, President and Chief Executive Officer
15. And on the notebook side, we also saw a number of our OEM partners launching new AI PCs with the slew of new bulk mobile part numbers that we announced at CES.
16. We have our strongest PC portfolio on the mobile side with top-to-bottom Copilot+ PC-compatible products, and those are playing very well into the market.

### Harlan Sur, Analyst
17. Networking is a very critical part of the AI infrastructure becoming even more important.
18. So, as you continue to drive customer adoption of your overall AI platforms, what's the feedback been like on your AI networking architectures?

### Lisa T. Su, President and Chief Executive Officer
19. Networking is an extremely important part of the AI solution, and it's an area that we have been investing and spending quite a bit of effort with our customers and our partners jointly.
20. Certainly, on inference, we've shown great performance and total cost of ownership.We now also have a number of training systems that we are putting on board. ⚑ uncertain
21. In addition to third-party networking solutions, we are also with our Pensando team developing our own in-house AI NIC that Forrest mentioned at our Q4 advancing AI event.

### Blayne Curtis, Analyst
22. I also want to just ping your brain on in terms of when you look at the ASIC storylines, there tends to be kind of a shift to focus on training versus inference. ⚑ uncertain
23. So, just your perspective, I know a lot of your workloads initially were inference. ⚑ uncertain
24. Are you seeing any shift in terms of the demand from your customers between training inference as well? ⚑ uncertain

### Lisa T. Su, President and Chief Executive Officer
25. People like the work that we've done in inference. ⚑ uncertain

### Lisa T. Su, President and Chief Executive Officer
26. I think for some of the models that are out there, you might be a little bit light in the Q3 data center GPU number. ⚑ uncertain

### Lisa T. Su, President and Chief Executive Officer
27. I think as we went into sort of the early part of '24, there was a little bit of, let's call it, less investments on the CPU side as people were optimizing investments for AI.

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Launched a broad set of leadership products and gained significant server and PC market share.
2. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Importantly, the data center segment contributed roughly 50% of annual revenue, as Instinct and EPYC processor adoption expanded significantly with cloud, enterprise, and supercomputing customers.
3. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Fourth quarter revenue increased 24% year over year to a record $7.7 billion, led by record quarterly data center and client segment revenue both of which grew by a significant double-digit percentage.
4. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] On a full-year basis, annual revenue grew 14% to $25.8 billion as data center revenue nearly doubled and client segment revenue grew 52%, more than offsetting declines in our Gaming and Embedded segments.
5. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Data center segment revenue increased 69% year over year to a record $3.9 billion.
6. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] 2024 marks another major inflection point for our server business, as share gains accelerated, driven by the ramp of fifth-gen EPYC Turin and strong double-digit percentage year-over-year growth in fourth-gen EPYC sales.
7. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Hyperscaler demand for EPYC CPUs was very strong, driven by expanded deployments powering both their internal compute infrastructure and online services.
8. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Exiting 2024, there are more than 450 EPYC platforms available from the leading server OEMs and ODMs, including more than 120 Turin platforms that went into production in the fourth quarter from Cisco, Dell, HPE, Lenovo, Supermicro, and others.
9. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Looking forward, Turin is clearly the best server processor in the world with more than 540 performance records across a broad range of industry-standard benchmarks.
10. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] As a result, we see clear growth opportunities in 2025 across both cloud and enterprise based on our full portfolio of EPYC processors, optimized for leadership performance across the entire range of data center workloads and system price points.
11. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] AMD now powers five of the 10 fastest and 15 of the 25 most energy-efficient systems in the world, on the latest top 500 supercomputer list.
12. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Earlier this month, the high-performance computer center at the University of Stuttgart launched the Hunter supercomputer that also uses MI300A.
13. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] The CDNA next architecture takes another major leap enabling powerful rackscale solutions that tightly integrate networking CPU and GPU capabilities at the silicon level to support Instinct solutions at data center scale.
14. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Cloud and OEM customer response to the acquisition has been very positive, as ZTE's systems expertise can accelerate time to market for future Instinct accelerator platforms.
15. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We expect to successfully divest ZTE's industry-leading U.S.-based data center infrastructure production capabilities, shortly after we closed the acquisition, which remains on track for the first half of the year.
16. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Our Ryzen processor portfolio has never been stronger with leadership compute performance across the stack.
17. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] In Gaming Graphics, revenue declined year over year, as we accelerated channel sellout in preparation for the launch of our next-gen Radeon 9000 series GPUs.
18. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We launched our Versal RF series with industry-leading compute performance for aerospace and defense markets, introduced our Versal premium series Gen 2, as the industry's first adaptive compute devices supporting CXL 3.1 and PCI Gen 6, and began shipping our next-gen Alveo card with leadership performance for ultra-low latency trading.
19. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] For 2025, we expect the demand environment to strengthen across all of our businesses, driving strong growth in our data center and client businesses and modest increases in our gaming and Embedded businesses.
20. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] All of these initiatives require massive amounts of new compute and create unprecedented growth opportunities for AMD across our businesses.
21. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] AMD executed very well in 2024, delivering record revenue of $25.8 billion, up 14%, driven by 94% growth in our data center segment and a 52% growth in our client segment, which more than offset headwinds in our gaming and embedded segments.
22. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] For the fourth quarter of 2024, Revenue was a record $7.7 billion, growing 24% year over year as strong revenue growth in the data center and client segment was partially offset by lower revenue in our gaming and embedded segments.
23. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Revenue was up 12% sequentially, primarily driven by the growth of client, data center, and the gaming segments.
24. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Gross margin was 54%, up 330 basis points year over year due to a favorable shift in revenue mix with higher data center and client revenues lower gaming revenue, partially offset by the impact of lower embedded revenue.
25. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Now, turning to our reportable segment, starting with the data center segment.
26. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Revenue was a record of $3.9 billion, up 69% year over year, driven by strong growth, both AMD Instinct GPU and the fourth and the fifth generation AMD EPYC CPU sales.
27. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Data Center segment operating income was $1.2 billion or 30% of revenue compared to $666 million or 29% a year ago.
28. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Therefore, reporting three segments: data center, client with gaming, and the embedded.
29. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] We'll continue to provide distinct revenue disclosures for our data center, client, gaming, and embedded businesses, consistent with our current reporting.
30. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] We expect revenue to be approximately $7.1 billion plus or minus $300 million, up 30% year over year, driven by strong growth in our data center and the client business.
31. [Q&A · Aaron Rakers, Analyst] I guess I'll just ask it right out of the gate is, as we think about the GPU business, and I appreciate you talked about delivering north of $5 billion of revenue, which is extremely impressive in 2024.
32. [Q&A · Aaron Rakers, Analyst] I'm curious if you -- how we should think about framing the GPU, the instinct business, as we think about 2025?
33. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, first of all, look we were very pleased with how we finished 2024 in terms of the data center GPU business.
34. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, as it relates to how data center -- so the overall data center business will grow strong double digits certainly, both the server product line as well as the data center GPU product line will grow strong double digits.
35. [Q&A · Lisa T. Su, President and Chief Executive Officer] And from the shape of the revenue you would expect that the second half would be stronger than the first half, just given MI350 will be a catalyst for the data center GPU business.
36. [Q&A · Lisa T. Su, President and Chief Executive Officer] But overall, I think we are very pleased with the trajectory of the data center business in both 2024 and then going into full year 2025.
37. [Q&A · Aaron Rakers, Analyst] Are you assuming that you are down sequentially in data center in total in 1Q?
38. [Q&A · Lisa T. Su, President and Chief Executive Officer] And the way that breaks out in each of the segments assume that data center would be down just about that average, so the corporate average.
39. [Q&A · Timothy Arcuri, Analyst] I wanted to ask about the server CPU business.
40. [Q&A · Timothy Arcuri, Analyst] So, wondering if you still think that the server CPU business can grow in line with that core kind of mid- to high teens.
41. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] First, we always assume server CPU is a very competitive market, but we currently have the best lineup portfolio from not only Turin generation, but Genoa and then even Milan, we provide the best TCO for our customers based on the product portfolio.
42. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] So, overall, we are actually quite confident about continuing to drive the server CPU businesses not only growing from a unit perspective, ASP perspective and continue to gain share.
43. [Q&A · Timothy Arcuri, Analyst] And then, Jean, can you just give us a sense of where data center GPU came in for December?
44. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] I think the way to look at our Q4 performance is our data center business overall did really well.
45. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] Of course, when we look at the server and the data center GPU, server did better than data center GPU.
46. [Q&A · Lisa T. Su, President and Chief Executive Officer] I think you should assume that the first half of 2025 data center segment will be consistent with the second half of '24.
47. [Q&A · Lisa T. Su, President and Chief Executive Officer] And that's true for both businesses on the server side as well as the data center GPU side.
48. [Q&A · Vivek Arya, Analyst] Lisa, a few questions on the data center GPU business.
49. [Q&A · Lisa T. Su, President and Chief Executive Officer] I think what we look at is certainly for the first year of the data center GPU business, we wanted to give some clear progression as it was going.
50. [Q&A · Lisa T. Su, President and Chief Executive Officer] And we've talked about a data center accelerator TAM upwards of $500 billion by the time we get out to 2028.
51. [Q&A · Vivek Arya, Analyst] And then within that, have your views about GPU versus ASIC how that share develops over the next few years?
52. [Q&A · Lisa T. Su, President and Chief Executive Officer] I've always been a believer in you need the right compute for the right workload.
53. [Q&A · Lisa T. Su, President and Chief Executive Officer] And that includes CPUs, GPUs, ASICs, and FPGAs.
54. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, CPUs, GPUs.
55. [Q&A · Lisa T. Su, President and Chief Executive Officer] And we are also involved in a number of ASIC conversations, as well as customers want to really have an overall compute partner.
56. [Q&A · Joshua Buchalter, Analyst] But I wanted to clarify, you said first half '25 data center GPU likely consistent with second half '24, and I was wondering if you could speak to whether or not the shape of the first half changed over the last few months and is potentially related to this pulled in timeline, it could be a potential air pocket ahead of that launch, or this was sort of consistent with how you saw things playing out as MI350 and MI325X ramps more fully?
57. [Q&A · Lisa T. Su, President and Chief Executive Officer] No, I would say from our standpoint, we've gotten incrementally more positive on the 2025 data center GPU ramp.
58. [Q&A · Harlan Sur, Analyst] For the fourth quarter, did your overall server CPU business grow double digits sequentially?
59. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, I think as Jean mentioned earlier, so in the fourth quarter, we did see a sequential double-digit growth in our server business.
60. [Q&A · Lisa T. Su, President and Chief Executive Officer] I think the server business has been performing extremely well.
61. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, I think, we see a strong 2025 for server CPUs.
62. [Q&A · Blayne Curtis, Analyst] Lisa, I just want to follow up the data center GPU business, obviously, very strongly year over year, but it seems for your commentary kind of the sequential growth kind of slows for the next kind of three quarters.
63. [Q&A · Lisa T. Su, President and Chief Executive Officer] Look, the way I would say it is, we saw tremendous growth as we build up the data center GPU business throughout 2024.
64. [Q&A · Lisa T. Su, President and Chief Executive Officer] And then this is about just getting into data centers and ramping up tens of thousands of GPUs.
65. [Q&A · Lisa T. Su, President and Chief Executive Officer] And that's what I think differentiates our capability is that we do have all of the building blocks of CPUs, GPUs, as well as all of the networking technologies that you would need to put the solutions together.
66. [Q&A · Stacy Rasgon, Analyst] So, you said your server business was up strong double digits sequentially in Q4.
67. [Q&A · Stacy Rasgon, Analyst] My math suggests that could have even meant that the GPU business was down sequentially.
68. [Q&A · Stacy Rasgon, Analyst] And given your guidance for I guess, flattish GPUs in the first half of '25 versus second half of '24.
69. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, that perhaps is the -- so data center segment was up 9% sequentially.
70. [Q&A · Lisa T. Su, President and Chief Executive Officer] Server was a bit more than that.
71. [Q&A · Lisa T. Su, President and Chief Executive Officer] Data center GPU was a little less than that.
72. [Q&A · Stacy Rasgon, Analyst] And I guess for my follow-up, maybe to follow on there, do you think your exit rate on GPUs in '25 is higher than your exit rate in '24?
73. [Q&A · Toshiya Hari, Analyst] Lisa, I had a question on the server CPU business.
74. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, let me say, as we look into 2025, I think we see a good server market between cloud and enterprise.
75. [Q&A · Lisa T. Su, President and Chief Executive Officer] And certainly, there are a number of cloud vendors that are now, let's call it, reupdating some of their data centers.
76. [Q&A · Lisa T. Su, President and Chief Executive Officer] And look, the server market is always a competitive market.
77. [Q&A · Toshiya Hari, Analyst] Given your data center commentary skewed more to the second half, I would expect margins to improve in the second half.
78. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] Our gross margin is primarily driven by our revenue mix, I think when you look at looking to 2025, Q1 guide, not only data center continued to grow significantly year over year.
79. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] But going into second half, we do believe the data center is our fastest growth driver for the company and that will drive the gross margin to step up in second half.
