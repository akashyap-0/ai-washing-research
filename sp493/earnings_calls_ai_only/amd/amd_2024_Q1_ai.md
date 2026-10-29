# Advanced Micro Devices — 2024_Q1 Earnings Call (transcript)

- **Company:** Advanced Micro Devices (AMD); fiscal year ends December (SEC fiscalYearEnd 1226)
- **Ticker:** AMD
- **CIK:** 0000002488
- **Period:** 2024_Q1 (call held April 30, 2024; date from page date line)
- **Calendar quarter:** 2024 Q1 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/04/30/advanced-micro-devices-amd-q1-2024-earnings-call-t/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 2)
- **Source SHA-256:** cda78edb17fa73640fd382a23078922241854209d271b99bd21763d552fc84e2
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**50 AI sentences of 571 total**
(Borderline, listed at the end: 0 automation/robotics, 68 infrastructure, none containing an AI term.)

## Prepared remarks

### Lisa Su, President and Chief Executive Officer
1. This is an incredibly exciting time for the industry as the widespread deployment of AI is driving demand for significantly more compute across a broad range of markets. ⚑ context-dependent
2. Under this backdrop, we are executing very well as we ramp our data center business and enable AI capabilities across our product portfolio.
3. In the enterprise, we have seen signs of improving demand as CIOs need to add more general purpose and AI compute capacity while maintaining the physical footprint and power needs of their current infrastructure.
4. In cloud, MI300X production deployments expanded at Microsoft, Meta, and Oracle to power generative AI training and inferencing for both internal workloads and a broad set of public offerings.
5. In addition, we have more than 100 enterprise and AI customers actively developing or deploying MI300X.
6. On the AI software front, we made excellent progress adding upstream support for AMD hardware in the OpenAI Triton compiler, making it even easier to develop highly performant AI software for AMD platforms.
7. We also released a major update to our ROCm software stack that expands support for open-source libraries including VLLM and frameworks including JAX, adds new features like video decode and significantly increases generative AI performance by integrating advanced attention algorithms support for sparsity and FP8.
8. Our partners are seeing very strong performance in their AI workloads.
9. As we jointly optimize for their models, MI300X GPUs are delivering leadership, inferencing performance and substantial TCO advantages compared to H100. ⚑ uncertain
10. For instance, several of our partners are seeing significant increases in tokens per second when running their flagship LLMs on MI300X compared to H100.
11. We're also continuing to enable the broad ecosystem required to power the next generation of AI systems, including as a founding member of the Ultra Ethernet Consortium working to optimize the widely adopted Ethernet protocol to run AI workloads at data center scale.
12. Longer term, we are increasingly working closer with our cloud and enterprise customers as we expand and accelerate our AI hardware and software roadmaps and grow our data center GPU footprint.
13. Ryzen Pro 8040 mobile CPUs deliver industry-leading performance and battery life for commercial notebooks, and our Ryzen Pro 8000 series desktop CPUs are the first processor to offer dedicated on-chip AI accelerators in commercial desktop PCs.
14. Looking forward, we believe the market is on track to return to annual growth in 2024, driven by the start of an enterprise refresh cycle in AI PC adoption.
15. We see AI as the biggest inflection point in PCs since the internet with the ability to deliver unprecedented productivity and usability gains.
16. We're working very closely with Microsoft and a broad ecosystem of partners to enable the next generation of AI experiences powered by Ryzen processors with more than 150 ISVs on track to be developing for AMD AI PCs by the end of the year.
17. We will also take the next major step in our AI PC roadmap later this year with the launch of our next-generation Ryzen mobile processors codenamed Strix.
18. Design win momentum for premium notebooks is outpacing prior generations as Strix enables next-generation AI experiences in laptops that are thinner, lighter, and faster than ever before.
19. Longer term, we see AI at the edge as a large growth opportunity that will drive increased demand for compute across a wide range of devices.
20. To address this demand, we announced our second generation of versal adaptive SoCs that deliver a 3 times increase in AI tops per watt and a 10 times greater scalar compute performance compared to our prior generation of industry leading adaptive SoCs.
21. Versal gen two adaptive SoCs are the only solution that combined multiple compute engines to handle AI, pre-processing, inferencing, and post-processing on a single chip, enabling customers to rapidly add highly performant and efficient AI capabilities to a broad range of products.
22. We were pleased to be joined at our launch by Subaru, who announced they adopted versal AI Edge Series Gen two devices, to power the next generation of their EyeSight ADAS system.
23. Looking further ahead, AI represents an unprecedented opportunity for AMD.
24. While there has been significant growth in AI infrastructure build-outs, we are still in the very early stages of what we believe is going to be a period of sustained growth driven by an insatiable demand for both high-performance AI and general purpose compute.
25. We have expanded our investments across the company to capture this large growth opportunity, from rapidly expanding our AI software stack to accelerating our AI hardware roadmaps, increasing our go-to-market activities, and partnering closely with the largest AI companies to co-optimize solutions for their most important workloads.

### Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer
26. Operating expenses were $1.7 billion, an increase of 10% year over year as we continue to invest aggressively in R&D and marketing activities to address the significant AI growth opportunities ahead of us.
27. Looking ahead, we believe the investment we are making will position us very well to address the large AI opportunities ahead.

## Q&A

### Lisa Su, President and Chief Executive Officer
1. I think what is true is we're getting much closer to our top AI customers.
2. Right now, I think MI300X is in a sweet spot for inference, very, very strong inference performance. ⚑ uncertain

### Ross Seymore, Deutsche Bank, Analyst
3. The non AI side of the data center business, it sounds like the enterprise side has some good traction even though the sequential drop happened seasonally, Lisa.

### Ross Seymore, Deutsche Bank, Analyst
4. And perhaps more importantly, when you talk about the whole AI PC side of things, do you believe that's more of a unit driver for you, an ASP driver?

### Lisa Su, President and Chief Executive Officer
5. Yeah, so I think, again I think we're pretty excited about the AI PC, both opportunity in, let's call it, the near term and even more so in the medium term.
6. The AI PC products, when we look at the Strix products, it's -- they're really well suited for the premium segments of the market.
7. And I think that's where you're going to see some of the AI PC content strongest in the beginning.

### Matt Ramsay, TD Cowen, Analyst
8. And we continue to hear more and more from other folks about internal ASIC programs at some of your primary customers, whether they be for inference, or training, or both. ⚑ uncertain

### Lisa Su, President and Chief Executive Officer
9. So look, I think one of the things that we see and we've said is that the TAM for AI compute is growing extremely quickly, and we see that continuing to be the case in all conversations.
10. But the overall AI compute needs, as we talk to customers, is very, very strong.
11. First of all, we have great relationships with all of sort of the top AI companies.
12. When you look at these large language models and everything that you need for training and inferencing there, although there will be many solutions, I don't think there's just one solution that will fit all.
13. The GPU is still the preferred architecture, especially as the algorithms and the models are continuing to evolve over time, and that favors our architecture and also our ability to really optimize CPU with GPU. ⚑ uncertain

### Lisa Su, President and Chief Executive Officer
14. We also see AI head nodes, as another place where we see growth in, let's call it, the more traditional market.

### Lisa Su, President and Chief Executive Officer
15. I think overall, AI demand has exceeded anyone's expectations in 2024.
16. And as we pass those milestones, we put that into the um, the overall full-year guidance for AI.

### Lisa Su, President and Chief Executive Officer
17. And then we're working across the networking ecosystem with key partners like Broadcom, and Cisco, and Arista who are with us at our AI data center event in December.

### Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer
18. Actually, the major reason is that we actually increase the investment quite significantly to -- as Lisa mentioned, to expand and accelerating our roadmap in the AI side.

### Harlan Sur, JPMorgan Chase and Company, Analyst
19. And how much of it is just a more aggressive build-out plan by customers versus their prior expectations given what appears to be pretty strong urgency for them to move forward with their important AI initiatives?

### Lisa Su, President and Chief Executive Officer
20. And the work that we're doing is hand in hand with our customers to optimize their key models. ⚑ uncertain
21. And then I think the other thing is, as you said, there's a huge demand for more AI compute and so our ability to participate in that, and help customers get that up and running is great.

### Lisa Su, President and Chief Executive Officer
22. I think as we look at sort of how AI shapes up over the next few years, there are customers who would be looking at very large training environments.

### Harsh Kumar, Piper Sandler, Analyst
23. So Jean, I put everything into the model that you talked about for June. ⚑ uncertain

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Lisa Su, President and Chief Executive Officer] We expanded gross margin by more than two percentage points and increased profitability as data center and client segment sales each grew by more than 80% year over year.
2. [Prepared remarks · Lisa Su, President and Chief Executive Officer] Data center segment revenue grew 80% year over year and 2% sequentially to a record $2.3 billion.
3. [Prepared remarks · Lisa Su, President and Chief Executive Officer] The substantial year-over-year growth was driven by the strong ramp of AMD Instinct MI300X GPU shipments and a double-digit percentage increase in server CPU sales.
4. [Prepared remarks · Lisa Su, President and Chief Executive Officer] We believe we gained server CPU revenue share in the seasonally down first quarter led by growth in enterprise adoption and expanded cloud deployments.
5. [Prepared remarks · Lisa Su, President and Chief Executive Officer] Given our high core count and energy efficiency, we can deliver the same amount of compute with 45% fewer servers compared to the competition, cutting initial capex by up to half and lowering annual opex by more than 40%.
6. [Prepared remarks · Lisa Su, President and Chief Executive Officer] In addition, there are 30% more Turin platforms in development from our server partners compared to fourth-gen EPYC platforms, increasing our enterprise SAM with new solutions optimized for additional workloads.
7. [Prepared remarks · Lisa Su, President and Chief Executive Officer] Turning to our broader data center portfolio, we delivered our second straight quarter of record data center GPU revenue as MI300 became the fastest-ramping product in AMD history, passing $1 billion in total sales in less than two quarters.
8. [Prepared remarks · Lisa Su, President and Chief Executive Officer] And based on our expanding customer engagements, we now expect data center GPU revenue to exceed $4 billion in 2024, up from the $3.5 billion we guided in January.
9. [Prepared remarks · Lisa Su, President and Chief Executive Officer] Embedded design win momentum remains very strong as customers adopt our full portfolio of FPGAs, CPUs, GPUs, and adaptive SoCs to address a larger portion of their compute needs.
10. [Prepared remarks · Lisa Su, President and Chief Executive Officer] Our priorities for 2024 are very clear: accelerate our data center growth by ramping Instinct GPU production and gaining share with our EPYC processors, launch our next-generation Zen five PC and server processors that extend our leadership performance, and expand our adaptive computing portfolio with differentiated solutions.
11. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] We delivered a strong year-over-year revenue growth in our data center and client segments in the first quarter and drew 230 basis points of gross margin expansion.
12. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] For the first quarter of 2024, revenue was $5.5 billion, up 2% year over year, as revenue growth in the data center and client segment was partially offset by lower revenue in our gaming and embedded segments.
13. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Revenue declined 11% sequentially as higher data center revenue resulting from the ramp of our AMD Instinct GPUs was offset by lower gaming and embedded segment revenues.
14. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Gross margin was 52%, up 230 basis points year over year, driven by higher revenue contribution from the data center and the client segment, partially offset by lower embedded and gaming segment revenue contribution.
15. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Now turning to our reportable segments, starting with the data center.
16. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Data center delivered record quarterly segment revenue of $2.3 billion, up 80%, a $1 billion increase year over year.
17. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Data center accounted for more than 40% of total revenue, primarily led by the ramp of AMD Instinct GPUs from both cloud and enterprise customers and a strong double-digit percentage growth in our server processing revenue as a result of growth across our Zen 4 products.
18. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Our sequential basis revenue increased 2% driven by the ramp-up of our AMD Instinct GPUs, partially offset by seasonal decline in server CPU sales.
19. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Data center segment operating income was $541 million or 23% of revenue, compared to $148 million or 11% a year ago.
20. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Gaming segment revenue was $922 million, down 48% year over year and down 33% sequentially due to a decrease in [semi] customer and Radeon GPU sales.
21. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Inventory increases sequentially by $301 million to $4.7 billion, primarily to support the continued ramp of data center and client products in advanced process nodes.
22. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Sequentially, we expect our data center segment revenue to increase by double-digit percentage, primarily driven by the data center GPU ramp; client segment revenue to increase; embedded segment revenue to be flat; and in the gaming segment based on current demand signals, revenue to decline by significant double-digit percentage.
23. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] Year over year, we expect our data center and client segment revenue to be up significantly driven by the strength of our product portfolio, the embedded and gaming segment revenue to decline by a significant double-digit percentage.
24. [Prepared remarks · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] We made significant progress on our strategic priorities, delivered year-over-year revenue growth in our data center and client segment, and expanded the gross margin.
25. [Q&A · Lisa Su, President and Chief Executive Officer] If we look at just what's happened over the last 90 days, we've been working very closely with our customers to qualify MI300 in their production data centers, both from a hardware standpoint, software standpoint.
26. [Q&A · Toshiya Hari, Goldman Sachs, Analyst] And then as my follow-up, I was hoping you could speak to your data center GPU roadmap beyond the MI300.
27. [Q&A · Toshiya Hari, Goldman Sachs, Analyst] But beyond the MI300, how should we think about your roadmap and your ability to compete in data center?
28. [Q&A · Ross Seymore, Deutsche Bank, Analyst] But I was just wondering, what's implied in your second-quarter guidance for the data center CPU side of things?
29. [Q&A · Ross Seymore, Deutsche Bank, Analyst] And generally speaking, how are you seeing that whole kind of GPU versus CPU crowding out dynamic playing out for the rest of 2024?
30. [Q&A · Lisa Su, President and Chief Executive Officer] In the second quarter, we expect overall data center to be up strong double digits.
31. [Q&A · Lisa Su, President and Chief Executive Officer] And then within that, we expect server to be up as well.
32. [Q&A · Lisa Su, President and Chief Executive Officer] We do expect some improvement in the overall market conditions for the server business, but we also have our Turin launch in the second half of the year.
33. [Q&A · Lisa Su, President and Chief Executive Officer] That will also, we believe, extend our leadership position within the server market.
34. [Q&A · Aaron Rakers, Wells Fargo Securities, Analyst] And then as a quick follow-up, going back to the earlier question on server demand, more traditional server.
35. [Q&A · Aaron Rakers, Wells Fargo Securities, Analyst] As you see the ramp of maybe share opportunities in more traditional enterprise, I'm curious to how you would characterize the growth that you expect to see in more traditional server CPU market as we move through '24 or even longer term, how you characterize that growth trend.
36. [Q&A · Lisa Su, President and Chief Executive Officer] So I think overall, we see it as a continued good progression for us with the server business going through 2024 and beyond.
37. [Q&A · Vivek Arya, Bank of America Merrill Lynch, Analyst] Or alternatively, if you could give us some sense of what the exit rate of your GPU sales could be.
38. [Q&A · Vivek Arya, Bank of America Merrill Lynch, Analyst] Can we continue to expect, I don't know, 100 basis points a quarter in terms of gross margin expansion because of the data center mix?
39. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] And going back to your gross margin question is when you look at our gross margin expansion in both Q1 and guided Q2, the primary driver is the strong performance on the data center side.
40. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] The data center will continue to ramp in second half.
41. [Q&A · Timothy Arcuri, UBS, Analyst] I also wanted to ask about your data center GPU roadmap.
42. [Q&A · Timothy Arcuri, UBS, Analyst] The customers that we talk to say that they're engaged, not just because of MI300 but really because of what's coming, and it seems like there's a big demand shift to rack scale systems that try to optimize performance per square foot given some of the data center and power constraints.
43. [Q&A · Lisa Su, President and Chief Executive Officer] So our work right now in future generations is not just specifying a GPU.
44. [Q&A · Timothy Arcuri, UBS, Analyst] And then just as a quick follow up, I know you know this year looks like it's going to be pretty back half loaded in your server CPU business just like it was last year.
45. [Q&A · Timothy Arcuri, UBS, Analyst] So I kind of wonder could you give us some milestones in terms of how much server CPU could grow this year, how back end loaded.
46. [Q&A · Timothy Arcuri, UBS, Analyst] It could be is it is like up 30% this year for your server CPU business year over year.
47. [Q&A · Lisa Su, President and Chief Executive Officer] Yeah, I mean, I think Tim, I think the best way to say it is our data center segment, is on a very, very strong ramp as we go through the back half of the year.
48. [Q&A · Lisa Su, President and Chief Executive Officer] Server CPUs, certainly.
49. [Q&A · Lisa Su, President and Chief Executive Officer] Data center GPUs, for sure.
50. [Q&A · Joe Moore, Morgan Stanley, Analyst] And then a separate follow-up on the Turin transition on server.
51. [Q&A · Joe Moore, Morgan Stanley, Analyst] How quickly do you think you might see that product ramp within your server portfolio?
52. [Q&A · Stacy Rasgon, AllianceBernstein, Analyst] You've got traditional data center up.
53. [Q&A · Stacy Rasgon, AllianceBernstein, Analyst] Gaming is going to be down, but I'd hazard a guess that the client and traditional data center like offset it, if not more.
54. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] So I think in general, it is more, the data center GPU ramp.
55. [Q&A · Stacy Rasgon, AllianceBernstein, Analyst] For my second question, I wanted to look at the near-term data center profitability.
56. [Q&A · Stacy Rasgon, AllianceBernstein, Analyst] Is that just the margins of the GPUs filtering in relative to the CPUs?
57. [Q&A · Stacy Rasgon, AllianceBernstein, Analyst] And I know you said GPUs would eventually be above corporate average?
58. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] I think you're right, is the GPU gross margin right now is below the data center gross margin level.
59. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] On the gross margin side, going back to your question is, we said in the past and we continue to believe the case is data center GPU gross margin over time will be accretive to corporate average, but it will take a while to get to the silver level of gross margin.
60. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] On your data center GPU segment and the faster time to production shipments, given you just upped your full-year GPU outlook, how much of it is faster bring up of your customers frameworks driven by your latest ROCm software platform and maybe stronger collaboration with your customers engineers just to get them to call faster?
61. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] So similar to the PC client business, right, which declined at the low end of the seasonal range, if I make certain assumptions around your data center GPU business, I expect that out of data center, it looks like your server CPU business was also down at the lower end of the seasonal range.
62. [Q&A · Harlan Sur, JPMorgan Chase and Company, Analyst] But anything else that drove the slightly better seasonal pattern in March for data center server?
63. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] I think the server business has been performing really well year over year.
64. [Q&A · Lisa Su, President and Chief Executive Officer] When we look at our server CPU, sort of ASPs, they're actually very stable.
65. [Q&A · Harsh Kumar, Piper Sandler, Analyst] So we recently hosted a very large custom GPU company for a call, and they talked about kind of mega data centers coming up in the near to mid-term, talking about nodes potentially in the 100,000-plus range and maybe up to a million.
66. [Q&A · Harsh Kumar, Piper Sandler, Analyst] So as we look out at these kinds of data centers, from an architectural standpoint, is that a situation where winner takes all where if somebody gets in, they kind of get all the sockets?
67. [Q&A · Harsh Kumar, Piper Sandler, Analyst] Just help us understand how something like that would play out if there's a chance for more than one competitor to play in such a large data center.
68. [Q&A · Jean Hu, Executive Vice President, Chief Financial Officer and Treasurer] I think the most important thing is we did say data center is going to grow double digit sequentially.
