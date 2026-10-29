# Arista Networks — 2023_Q4 Earnings Call (transcript)

- **Company:** Arista Networks (ANET); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** ANET
- **CIK:** 0001596532
- **Period:** 2023_Q4 (call held February 12, 2024; date from page date line)
- **Calendar quarter:** 2023 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/02/12/arista-networks-anet-q4-2023-earnings-call-transcr/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** b431013f795f9c995346546f71b0707d394036dd384df949cf81ef0be6aff5bf
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**50 AI sentences of 456 total**
(Borderline, listed at the end: 1 automation/robotics, 19 infrastructure, none containing an AI term.)

## Prepared remarks

### Liz Stine, Director, Investor Relations
1. During the course of this conference call, Arista Networks management will make forward-looking statements, including those relating to our financial outlook for the first quarter of the 2024 fiscal year, longer-term financial outlook for 2024 and beyond, our total addressable market and strategy for addressing these market opportunities, including AI, customer demand trends, supply chain constraints, component costs, manufacturing output, inventory management, and inflationary pressures on our business, lead times, product innovation, working capital optimization and the benefits of acquisitions, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K and which could cause actual results to differ materially from those anticipated by these statements. ⚑ uncertain: safe-harbor

### Jayshree Ullal, President and Chief Executive Officer
2. Despite multiple capex reductions last year and the normal volatility of cloud titan and AI pivots, we cherish our privileged status with both M&M.
3. Speaking of AI, in fall of 2023, Andy and I attended the 50th golden anniversary of Ethernet at the Computer History Museum.
4. It truly is a reminder of how civilian widely deployed Ethernet is with the speed increasing by orders of magnitude from a shared collision 2.95 megabits for file, print, and share to a terabyte Ethernet switching in the AI and ML era. ⚑ context-dependent
5. AI workloads are placing greater demands on Ethernet as they are both data and compute-intensive across thousands of processes today.
6. Basically, AI at scale needs Ethernet at scale.
7. AI workloads cannot tolerate the delays in the network because the job can only be completed after all flows are successfully delivered to the GPU clusters.
8. All it takes is one culprit or worst-case link to throttle an entire AI workload.
9. AI network topology needs packet SPRING to allow every flow to simultaneously access all parts of the destination.
10. Key to an AI job completion is the rapid and reliable bulk transfer with flexible ordering using Ethernet links to optimally balance AI-intensive operations, unlike the rigid ordering of InfiniBand.
11. In AI networks, there's a common in-cost congestion problem whereby multiple uncoordinated senders can send traffic to the receiver simultaneously.
12. In terms of annual 2023 product lines, our core, which consists of cloud, AI, and data center products, are built upon our highly differentiated Arista extensible operating software system stack.
13. We expect both 400- and 800-gigabit Ethernet will emerge as important pilots for AI back-end GPU clusters.
14. We are cautiously optimistic about achieving our AI revenue goal of at least $750 million in AI networking in 2025.
15. While 2023's headline has been mostly about AI, we are pleased with the momentum of enterprise and provider customers as well.
16. We have more than doubled our enterprise revenue in the last three years and we are becoming the gold standard for client-to-cloud-to-AI networking with one EOS and one CloudVision foundation.
17. Three principles continue to differentiate us as we are poised to be a market share gainer in the enterprise: one, best-in-class, highly available proactive products with resilience and hitless upgrades at multiple levels; two, zero-touch automation for predictive client-to-cloud one-click operations that relies less on human staff or manual operations and is instead software-driven; and finally, prescriptive insights based on AI/ML Autonomous Virtual Assist, AVA, algorithms for increased security, observability and root cause analysis.

## Q&A

### Aaron Rakers, Wells Fargo Securities, Analyst
1. I guess my question is, Jayshree, just obviously, the focus on AI and the build-out of back-end networks based on 400-, 800-gig Ethernet.
2. And just remind us of the cadence of kind of product cycles that really set the table for Arista and this AI opportunity as we move through '24 and particularly into '25.

### Jayshree Ullal, President and Chief Executive Officer
3. So, our AI performance continues to track well for the $750 million revenue goal that we set last November at Analyst Day.
4. But if I look at the last year, which maybe last 12 months is a better indication, we have participated in a large number of AI bids and when I say large, I should say they are large AI bids, but there are a small number of customers actually to be more clear.
5. And in the last four out of five, AI networking clusters we have participated on Ethernet versus InfiniBand, Arista has won all four of them for Ethernet, one of them still stays on InfiniBand.

### Jayshree Ullal, President and Chief Executive Officer
6. To kind of go hand-in-hand, but as you know, in AI, we've been waiting for the GPUs.

### Sebastien Naji, Wedbush Securities, Analyst
7. Can you maybe articulate why you believe in the world of AI networks, more of the market would not move to white box or vice versa, maybe why more of the market would move away from white box?

### Jayshree Ullal, President and Chief Executive Officer
8. They're still mission-critical, and they're even more mission-critical for AI. ⚑ context-dependent

### Matt Niknam, Deutsche Bank, Analyst
9. So, can you talk a little bit about how you view the value of such scale in order to maybe better serve and target both the cloud and AI -- Titan as well as enterprise verticals?

### Jayshree Ullal, President and Chief Executive Officer
10. I think on the cloud and AI, we feel pretty bulked up to deal with those customers because they don't look for size and bulk.
11. They look for, as you know, networking innovation capabilities, and this has been Arista's heritage for 10 years and we'll continue to be with the AI cycle for the next foreseeable 10 years. ⚑ context-dependent

### Jayshree Ullal, President and Chief Executive Officer
12. And Meta, to answer your question on enterprise and AI activity, I think Arista continues to drive the concept of EOS, multi-domain routing, campus, high availability, mission-critical enterprises for multiple verticals.
13. On the AI side, we continue to track well.

### Ittai Kidron, Oppenheimer and Company, Analyst
14. It feels like half of it can already come from the AI networking, given your '25 targets, and you seem very comfortable about your '25 targets, I would think your '24 should be comfortable as well. ⚑ context-dependent
15. So, why -- if I assume that $200 million, $300 million come from AI networking this year, why should the rest of the business generate only $300 million to get to your annual targets?

### Jayshree Ullal, President and Chief Executive Officer
16. AI is going to come.

### Chantelle Breithaupt, Incoming Chief Financial Officer
17. I think that Jayshree very eloquently put in the sense of '23, '24, '25 on what we expect from AI going from trials to pilots to production.

### Jayshree Ullal, President and Chief Executive Officer
18. So, all this, I think, customers are looking for that innovation, modern network model, CI/CD principles, bringing DevOps, NetOps, SecOps, all of this together. ⚑ uncertain

### Atif Malik, Citi, Analyst
19. Now, your networking competitor announced a collaboration with NVIDIA on Ethernet AI enterprise solutions last week.

### Jayshree Ullal, President and Chief Executive Officer
20. It is vital to get a complete AI network design going. ⚑ context-dependent

### Tim Long, Barclays, Analyst
21. So, I wanted to follow up a little bit more on that AI, Jayshree.

### Jayshree Ullal, President and Chief Executive Officer
22. So, let me just step back and say the first real consultative approach from Arista is to provide our expertise on how to build a robust back-end AI network.
23. And so, the whole discussion of Ethernet become -- versus InfiniBand becomes really important because as you may recall, a year ago, I told you we were outside looking in, everybody had an Ethernet -- everybody had an InfiniBand HPC cluster that was kind of getting bundled into AI.
24. And the popular product we are seeing right now and the back-end cluster for our AI is the Arista 7800 AI spine, which in a single chassis with north of 500 terabits of capacity can give you a substantial number of ports, 400 or 800.
25. And of course, as we shared with you at the Analyst Day, we can expand that to a two-tier AI leaf and spine with a 16-way CMP to support close to 10,000 GPUs nonblocking, this lossless architecture for Ethernet.
26. And then the overlay we will have on that with the Ultra Ethernet Consortium in terms of congestion controls, packet SPRING, and working with a suite of UEC mix is what I think will make Ethernet the default standard for AI networking going forward.
27. So, probably our AI won't be.
28. But today's models are moving very rapidly, relying on a high bandwidth, predictable latency, the focus on application performance requires you to be sole-sourced initially. ⚑ uncertain
29. And over time, I'm sure it'll move to multiple sources, but I think Arista is very well-positioned for the first innings of AI networking, just like we were for the cloud networking decade.
30. And one other thing I want to say is, although a lot of these customers are doing AI pivots, these AI pivots will result in revisiting the front-end cloud network, too.
31. So, this AI anatomy is being really well understood.
32. And so, this -- being actively involved has -- is going to pay a lot of dividends, but we're still very much in our first innings of AI.

### Ben Reitzes, Melius Research, Analyst
33. And then for 2025, AMD upped their TAM very significantly for AI and -- by a multiple.

## Borderline: automation/robotics without an AI term

1. [Q&A · Jayshree Ullal, President and Chief Executive Officer] There will be use cases where Arista's blue box or a stand-alone white box can run either SONiC or FBOSS, but many times, the EOS software stack is really, really something they depend on for availability, analytics, automation, and there's -- you can get your network for zero cost, but the cost of downtime is millions and millions of dollars.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] Our cloud networking products deliver power-efficient, high-availability zones without doubling the cost of redundancy as data centers demand insatiable bandwidth capacity and network speeds for both the front-end and back-end storage and compute clusters.
2. [Prepared remarks · Ita Brennan, Chief Financial Officer] Capital expenditures for the quarter were $6 million.
3. [Prepared remarks · Chantelle Breithaupt, Incoming Chief Financial Officer] And in 15 years, the annual bandwidth of the data centers has grown 350-fold.
4. [Prepared remarks · Chantelle Breithaupt, Incoming Chief Financial Officer] Our acceleration of the data center switching market in recent quarters is evidenced by our market share gains in the 20-plus percent range of both ports and dollars.
5. [Q&A · Tal Liani, Bank of America Merrill Lynch, Analyst] I'm trying to find -- because we don't have the backlog contribution of last year, I'm trying to kind of dissect the numbers and see what's the correlation with core data center business and traditional compute.
6. [Q&A · Tal Liani, Bank of America Merrill Lynch, Analyst] So, if service sales -- the service sales cycle is low, and we see some declines in servers, does it mean that at least in the short run, excluding the macro contribution, there is also a decline in the orders?
7. [Q&A · Tal Liani, Bank of America Merrill Lynch, Analyst] Just how does it work between server demand and switching demand?
8. [Q&A · Jayshree Ullal, President and Chief Executive Officer] But just to sort of answer your question on ratio of CPUs or for that matter, GPUs in the future to the network, typically, we have to have the CPUs or GPUs come in before we can outfit the network.
9. [Q&A · Jayshree Ullal, President and Chief Executive Officer] But I would say, generally, in the leaf architecture, they go hand in hand where you have to create a rack of 1,000 servers or whether they are CPUs and GPUs.
10. [Q&A · Jayshree Ullal, President and Chief Executive Officer] Look, I think white box is here to stay for a very long time if somebody just wants a throwaway commodity product, but how many people want to throw away commodity in the data center?
11. [Q&A · Jayshree Ullal, President and Chief Executive Officer] If I'm going to spend multimillion dollars on a GPU cluster, and the last thing I'm going to do is put a toy network in, right?
12. [Q&A · Jayshree Ullal, President and Chief Executive Officer] So, we have always embraced white box, we coexist with it, but it continues to be a relatively small use case in the larger mission-critical data centers for enterprise and cloud companies.
13. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And the last three years is a good example of how well we've done that both in the data center and in the campus.
14. [Q&A · Jayshree Ullal, President and Chief Executive Officer] I think we're moving from what I call trials, which is connecting hundreds of GPUs to pilots, which is connecting thousands of GPUs this year, and then we expect larger production clusters.
15. [Q&A · Jayshree Ullal, President and Chief Executive Officer] Specific to our partnership, you can be assured that we'll be working with the leading GPU vendors.
16. [Q&A · Jayshree Ullal, President and Chief Executive Officer] We will also be working with our partners in AMD and Intel so we will be the Switzerland of XPUs, whatever the GPU might be, and we look to supply the best network ever.
17. [Q&A · Jayshree Ullal, President and Chief Executive Officer] So, you can connect up to 1,000 GPUs just doing that.
18. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And if you take a deep look at the centerpiece of it, which is all the GPUs, they have to connect to something very reliable and this is really where we come in.
19. [Q&A · Ben Reitzes, Melius Research, Analyst] Microsoft, Meta, and Google have all raised their capex forecast for 2024.
