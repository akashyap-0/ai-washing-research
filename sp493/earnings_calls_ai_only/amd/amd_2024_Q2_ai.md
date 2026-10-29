# Advanced Micro Devices — 2024_Q2 Earnings Call (transcript)

- **Company:** Advanced Micro Devices (AMD); fiscal year ends December (SEC fiscalYearEnd 1226)
- **Ticker:** AMD
- **CIK:** 0000002488
- **Period:** 2024_Q2 (call held July 30, 2024; date from page date line)
- **Calendar quarter:** 2024 Q2 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/07/30/advanced-micro-devices-amd-q2-2024-earnings-call-t/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 2)
- **Source SHA-256:** 9281aeebf0a4741ff634037f54cf7f9f9eee4c521be01a32ba9eb14ef1f97ced
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**56 AI sentences of 492 total**
(Borderline, listed at the end: 0 automation/robotics, 51 infrastructure, none containing an AI term.)

## Prepared remarks

### Lisa T. Su, President and Chief Executive Officer
1. We continued accelerating our AI traction as leading cloud and enterprise providers expanded availability of Instinct MI300X solutions, and we also saw positive demand signals for general-purpose compute in both our client and server processor businesses.
2. Turning to our data center AI business.
3. Microsoft expanded their use of MI300X accelerators to power GPT-4 Turbo and multiple copilot services, including Microsoft 365 Chat, Word, and Teams.
4. The new Azure VMs leverage the industry-leading compute performance and memory capacity of MI300X in conjunction with the latest ROCm software to deliver leadership inferencing price performance when running the latest frontier models, including GPT-4.
5. Hugging Face was one of the first customers to adopt the new Azure instances, enabling enterprise and AI customers to deploy hundreds of thousands of models on MI300X GPUs with one click.
6. Our enterprise and cloud AI customer pipeline grew in the quarter, and we are working very closely with our system and cloud partners to ramp availability of MI300 solutions to address growing customer demand.
7. On the AI software front, we made significant progress enhancing support and features across our software stack, making it easier to deploy high-performance AI solutions on our platforms.
8. We also continued to work with the open-source community to enable customers to implement the latest AI algorithms.
9. As an example, AMD support for Flash Attention 2 algorithm was upstreamed, providing out-of-the-box support for AMD hardware in the popular library that can increase training and inference performance on large transformer models. ⚑ uncertain
10. Our work with the model community also continued accelerating, highlighted by the launches of new models and frameworks with Day 1 support for AMD hardware. ⚑ uncertain
11. At Computex, I was joined by the co-CEO of Stable Diffusion to announce that MI300 is the first GPU to support their latest SD 3.0 Image Generation LLM.
12. Last week, we were proud to note that multiple partners use ROCm and MI300X to announce support for the latest Llama 3.1 models, including their 405 billion parameter version that is the industry's first frontier-level open-source AI model.
13. Llama 3.1 runs seamlessly on MI300 accelerators.
14. And because of our leadership memory capacity, we're also able to run the FP16 version of the Llama 3.1 405B model in a single server, simplifying deployment and fine-tuning of the industry-leading model and providing significant TCO advantages.
15. Earlier this month, we announced our agreement to acquire Silo AI, Europe's largest private AI lab with extensive experience developing tailored AI solutions for multiple enterprise and embedded customers, including Allianz, Ericsson, Finnair, Karber, Nokia, Philips, T-Mobile, and Unilever.
16. The Silo team significantly expands our capability to service large enterprise customers looking to optimize their AI solutions for AMD hardware.
17. Silo also brings deep expertise in large language model development, which will help accelerate optimization of AMD inference and training solutions.
18. In addition to our acquisitions of Silo AI, Mipsology, and Nod.ai, we have invested over $125 million across a dozen AI companies in the last 12 months to expand the AMD AI ecosystem, support partners, and advance leadership AMD computing platforms.
19. Looking ahead, from a road map perspective, we are accelerating and expanding our Instinct road map to deliver an annual cadence of AI accelerators, starting with the launch of MI325X later this year.
20. MI325X leverages the same infrastructure as MI300 and extends our generative AI performance leadership by offering twice the memory capacity and 1.3 times more peak compute performance than competitive offerings.
21. Turning to our AI solutions work.
22. Broadcom, Cisco, HP Enterprise, Intel, Google, Meta, and Microsoft, all joined us to announce Ultra Accelerator Link, an industry-standard technology to connect hundreds of AI accelerators that is based on AMD's proven Infinity Fabric technology.
23. By combining UALink with the widely supported Ultra Ethernet consortium specification, the industry is coming together to establish a standardized approach for building the next generation of high-performance data center AI solutions at scale.
24. For notebooks, we announced our Ryzen AI 300 series that extends our industry-leading CPU and GPU performance and introduces the industry's fastest NPU with 50 tops of AI compute performance for Copilot+ PCs.
25. The first Ryzen AI 300 Series notebooks went on sale over the weekend to strong reviews, and more than 100 Ryzen AI 300 Series premium, gaming, and commercial platforms are on track to launch from Acer, ASUS, HP, Lenovo, and others over the coming quarters.
26. We announced our Alveo V80 accelerators that deliver leadership capabilities in memory-intensive workloads and entered early access on next-generation edge AI solutions with more than 30 key partners on our upcoming second-gen Versal Adaptive SoCs.
27. Victor has made significant contributions to Xilinx and AMD, including helping scale our embedded business and leading our cross-company AI strategy.
28. Looking ahead, the rapid advances in generative AI and development of more capable models are driving demand for more compute across all markets.
29. Under this backdrop, we see strong growth opportunities over the coming years and are significantly increasing hardware, software, and solutions investments with a laser focus on delivering an annual cadence of leadership data center GPU hardware, integrating industry-leading AI capabilities across our entire product portfolio, enabling full-stack software capabilities, amplifying our ROCm development with the scale and speed of the open source community, and providing customers with turnkey solutions that accelerate the time to market for AMD-based AI systems.

### Jean Hu, Executive Vice President, Chief Financial Officer
30. Operating expenses were $1.8 billion, an increase of 15% year over year as we continue to invest in R&D to address the significant AI growth opportunities ahead of us and enhanced go-to-market activities.
31. Also during the third quarter, we expect to close the acquisition of Silo AI for approximately $665 million in cash.
32. We expanded gross margin significantly and drove earnings growth while increasing investment in AI.

## Q&A

### Lisa T. Su, President and Chief Executive Officer
1. We're on track to launch MI325 later this year, and then next year, our MI350 Series, which will be very competitive with Blackwell solutions. ⚑ uncertain
2. So, I think, overall, we remain quite bullish on the overall AI market.

### Ross Seymore, Analyst
3. Lisa, can you talk about the AI PC side of things, how you believe AMD is positioned?

### Lisa T. Su, President and Chief Executive Officer
4. Our view of this is the AI PC is an important add to the overall PC category.
5. And then into 2025, you're going to see AI PCs across sort of a larger set of price points, which will also open up more opportunities.

### Vivek Arya, Analyst
6. Lisa, there seems to be this ongoing industry debate about AI monetization and whether your customers are getting the right ROI on their capex.

### Lisa T. Su, President and Chief Executive Officer
7. I think the overall view on AI investment is we have to invest.
8. The potential of AI is so large to impact the way enterprises operate and all that stuff.
9. And for large language models, GPUs are still the architecture of choice.
10. And I think our piece of that is really strong technology with strong partnerships with the key AI market makers.

### Joe Moore, Analyst
11. I wonder if you could talk about training versus inference. ⚑ uncertain
12. Do you have a sense -- I know that a lot of the initial focus was inference, but do you have traction on the training side? ⚑ uncertain

### Lisa T. Su, President and Chief Executive Officer
13. From that standpoint, the early deployments have largely been inference in most cases, and we've seen fantastic performance from an inference standpoint. ⚑ uncertain
14. As we go forward, I think you'll see -- the belief is that inference will be larger than training from a market standpoint. ⚑ uncertain
15. But from an AMD standpoint, I would expect both inference and training to be growth opportunities for us. ⚑ uncertain

### Lisa T. Su, President and Chief Executive Officer
16. So, Harsh, overall, maybe if I take a step back and just talk about how the systems are evolving, there's no question that the systems are getting more complex, especially as you go into large training clusters, and our customers need help to put those together.

### Lisa T. Su, President and Chief Executive Officer
17. So, if you think about our Q2 revenue, think about it as almost all AI.
18. So, it's MI300X, it's for large AI, hyperscalers as well as OEM customers going to enterprise and Tier 2 data centers.
19. We are going to continue to invest in software, and that was one of the reasons that we did the Silo AI acquisition.
20. And that's -- so we view this as the opportunity to expand the customer base with talent like Silo AI, like Nod.ai which brought a lot of compiler talent.
21. So, I think Jean said earlier that we see leverage in the model, but we're going to continue to invest because this opportunity is huge, and we have all of the pieces. ⚑ uncertain

### Tom O'Malley, Barclays, Analyst
22. You're obviously launching a new notebook, desktop product, but you're also talking about AI PC.
23. Is it a unit assumption that's coming with AI PC?

### Lisa T. Su, President and Chief Executive Officer
24. The AI PC element is certainly one element of that, but there is just the overall refresh.

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] As a result, second-quarter revenue increased 9% year over year to $5.8 billion as significantly higher sales of our data center and client processors more than offset declines in gaming and embedded product sales.
2. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We also expanded gross margin by more than three percentage points and grew EPS 19% as data center product sales accounted for nearly 50% of overall sales in the quarter.
3. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Data center segment revenue increased 115% year over year to a record $2.8 billion, driven by the steep ramp of Instinct MI300 GPU shipments and a strong double-digit percentage increase in EPYC CPU sales.
4. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We are seeing hyperscalers select EPYC processors to power a larger portion of their applications and workloads, displacing incumbent offerings across their infrastructure with AMD solutions that offer clear performance and efficiency advantages.
5. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Importantly, more than one-third of our enterprise server wins in the first half of the year were with businesses deploying EPYC in their data centers for the first time, highlighting our success attracting new customers while also continuing to expand our footprint with existing customers.
6. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We publicly previewed Turin for the first time in June, demonstrating our significant performance advantages in multiple compute-intensive workloads.
7. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We delivered our third straight quarter of record data center GPU revenue with MI300 quarterly revenue exceeding $1 billion for the first time.
8. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] As a result, we now expect data center GPU revenue to exceed $4.5 billion in 2024, up from the $4 billion we guided in April.
9. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] In gaming graphics, revenue increased year over year, driven by improved sales of our Radeon 6000 and 7000 Series GPUs in the channel.
10. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Design wins in the first half of the year increased by more than 40% from the prior year to greater than $7 billion, including multiple triple-digit million-dollar wins, combining our Adaptive and x86 compute products.
11. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] In summary, we delivered strong second-quarter results and are well-positioned to grow revenue significantly in the second half of the year, driven by our data center and client segments.
12. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] Our data center GPU business is on a steep growth trajectory as shipments ramp across an expanding set of customers.
13. [Prepared remarks · Lisa T. Su, President and Chief Executive Officer] We're also seeing strong demand for our next-generation Zen 5, EPYC, and Ryzen processors that deliver leadership performance and efficiency in both data center and client workloads.
14. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] On a year-over-year basis, data center segment revenue more than doubled, client segment revenue grew significantly, and we expanded the gross margin by 340 basis points.
15. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] For the second quarter of 2024, revenue was $5.8 billion, up 9% year over year as revenue growth in the data center and the client segments was partially offset by lower revenue in our gaming and embedded segment.
16. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Revenue increased 7% sequentially, primarily driven by growth in the data center and client segments revenue.
17. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Gross margin was 53%, up 340 basis points year over year, primarily driven by higher data center revenue.
18. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Starting with data center, data center delivered record quarterly segment revenue of $2.8 billion, up 115%, a $1.5 billion increase year over year.
19. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] The data center segment accounted for nearly 50% of total revenue, led primarily by the steep ramp of AMD Instinct GPUs and a strong double-digit percentage EPYC server revenue growth.
20. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] On a sequential basis, revenue increased 21%, driven primarily by strong momentum in AMD Instinct GPUs.
21. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Data center segment operating income was $743 million or 26% of revenue compared to $147 million or 11% a year ago.
22. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Inventory increased sequentially by $339 million to $5 billion, primarily to support the continued ramp of data center GPU products.
23. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Sequentially, we expect revenue to grow approximately 15%, primarily driven by strong growth in the data center and client segment.
24. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer] Year over year, we expect revenue to grow approximately 16%, driven by the steep ramp of our AMD Instinct processors and strong server and client revenue growth to more than offset the declines in the gaming and the embedded segment.
25. [Q&A · Lisa T. Su, President and Chief Executive Officer] When we started the year, I think the key point for us was to get our products into our customers' data centers, to have them qualify their workloads, to really ramp in production, and then see what the production capabilities are, especially performance and all of those things.
26. [Q&A · Lisa T. Su, President and Chief Executive Officer] I think the market continues to need more compute.
27. [Q&A · Aaron Rakers, Analyst] I guess sticking on the data center side, as we look forward and you think about the full year, I'm curious of how you're currently thinking about the EPYC server CPU growth expectations as we go forward.
28. [Q&A · Aaron Rakers, Analyst] And any kind of updated thoughts on your ability to kind of continue to gain share in the server market?
29. [Q&A · Aaron Rakers, Analyst] Just kind of just update us on how you see the server market playing out over the next couple of quarters.
30. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, overall, I think the server market and our ability to continue to grow share in the server market is one of the things that we see in the second half of the year.
31. [Q&A · Timothy Arcuri, Analyst] Lisa, I wanted to ask about the data center GPU road map.
32. [Q&A · Lisa T. Su, President and Chief Executive Officer] But we also have many customers who want to use their current infrastructure.
33. [Q&A · Lisa T. Su, President and Chief Executive Officer] I think the beauty of the MI350 series is it actually fits into the same infrastructure as the MI300 series.
34. [Q&A · Ross Seymore, Analyst] Well, data center is obviously very important.
35. [Q&A · Vivek Arya, Analyst] They can buy GPUs from your largest competitor with all the software bells and whistles and incumbency, or they can do custom chips, or they can buy from AMD.
36. [Q&A · Vivek Arya, Analyst] Do you think your customers, given all this concern around monetization, does it make them consolidate their capex around just the other two suppliers?
37. [Q&A · Lisa T. Su, President and Chief Executive Officer] And then relative to the various choices for the size of the market, I firmly believe that there will be multiple solutions, whether you're talking about GPUs or you're talking about custom chips or ASICs, there will be multiple solutions.
38. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] If you look at our data center platform, especially both the server and the data center GPU side, we are ramping the revenue.
39. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] The business model can leverage very significantly even from GPU side.
40. [Q&A · Stacy Rasgon, Analyst] So, with gaming down double digits, it probably means you've got close to $1 billion of growth revenue across data center, client, and embedded.
41. [Q&A · Stacy Rasgon, Analyst] Like if I had 70% of it going to data center and 20% going to client and 10% going to embedded, like would that be like way off?
42. [Q&A · Lisa T. Su, President and Chief Executive Officer] Think of it as the data center is the largest piece of it, client, next.
43. [Q&A · Stacy Rasgon, Analyst] So, I mean, within that data center piece then, how does that split out?
44. [Q&A · Stacy Rasgon, Analyst] Or like again, how does it -- again, if you got, I don't know, $400 million to $600 million of sequential data center growth or something like that, how does it split up?
45. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, again, without being that granular, we will see both -- certainly, the Instinct GPUs will grow, and we'll see also very nice growth on the server side.
46. [Q&A · Lisa T. Su, President and Chief Executive Officer] So, this is part of how we help customers get to market faster is by investing in all of the components, so the CPUs, the GPUs, the networking capability as well as system-level solutions.
47. [Q&A · Lisa T. Su, President and Chief Executive Officer] First, on your question about, I think you're basically asking about the supercomputing piece.
48. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] The primary driver is really the faster data center business growth.
49. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] If you look at the data center business as a percentage of revenue from 37% in Q4 last year to now close to 50%.
50. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] When you look at the second half, we'll continue to see data center to be the major driver of our top-line revenue growth, will help with the margin expansion.
51. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer] We feel pretty good about the overall data center business to continue to be absolutely the driver of gross margin expansion.
