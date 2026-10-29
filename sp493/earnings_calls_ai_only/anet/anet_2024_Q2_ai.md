# Arista Networks — 2024_Q2 Earnings Call (transcript)

- **Company:** Arista Networks (ANET); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** ANET
- **CIK:** 0001596532
- **Period:** 2024_Q2 (call held July 30, 2024; date from page date line)
- **Calendar quarter:** 2024 Q2 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/07/31/arista-networks-anet-q2-2024-earnings-call-transcr/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** f416011937a882bb5e4deb764d42be8b5e63b1de3e4aa603c13ecc6ff1009e28
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**62 AI sentences of 620 total**
(Borderline, listed at the end: 2 automation/robotics, 37 infrastructure, none containing an AI term.)

## Prepared remarks

### Liz Stine, Director, Investor Relations
1. During the course of this conference call, Arista Networks management will make forward-looking statements, including those relating to our financial outlook for the third quarter of the 2024 fiscal year, longer-term financial outlooks for 2024 and beyond, our total addressable market and strategy for addressing these market opportunities, including AI, customer demand trends, supply chain constraints, component costs, manufacturing output, inventory management, and inflationary pressures on our business, lead times, product innovation, working capital optimization, and the benefits of acquisitions, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K and which could cause actual results to differ materially from those anticipated by these statements. ⚑ uncertain: safe-harbor

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
2. In June 2024, we launched Arista's Etherlink AI platforms that are ultra-Ethernet consortium compatible, validating the migration from InfiniBand to Ethernet.
3. The AI portfolio consists of the 7060X6 AI switch that supports 64 800-gig or 128 400-gig Ethernet ports with a capacity of 51 terabits per second.
4. The 7800 R4-AI Spine is our fourth generation of Arista's flagship 7800, offering 100% nonblocking throughput with a proven virtual output queuing architecture.
5. The 7700 R4-AI distributed Etherlink switch is a unique product offering with a massively parallel distributed scheduling and congestion-free traffic spraying fabric.
6. The 7700 represents the first in a new series of ultra-scalable intelligent distributed systems that can deliver the highest consistent throughput for very large AI clusters.
7. And then there was cloud and routing in the 2015 era, followed by WAN and Campus in the 2020 era, and now AI in our fifth generation in 2025 era.
8. We are quite pleased with our progress across cloud, AI, campus, and enterprise customers.

### Ashwin Kohli, Senior Vice President-Customer Engineering
9. The first example is an AI enterprise win with a large Tier 2 cloud provider, which has been heavily investing in GPUs to increase their revenue and penetrate new markets.
10. However, it was being connected to their legacy networking vendor, which resulted in them having significant performance and scale issues with their AI applications.
11. Our technical partnership resulted in deploying a two-step migration path to alleviate the current issues using 400-gig 7080s, eventually migrating them to an 800-gig AI Ethernet link in the future.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
12. Well, 40 years later, we're seeing the same cycle come true again with the collective nature of AI training models mandating a lossless highly available network to seamlessly connect every AI accelerator in the cluster to one another for peak job completion times.
13. Our AI networks also connect trained models to end users and other multi-tenant systems in the front-end data center, such as storage, enabling the AI system to become more than the sum of its parts.
14. We believe data centers are evolving to holistic AI centers, where the network is the epicenter of AI management for acceleration of applications, compute, storage, and the wide area network.
15. AI centers need a foundational data architecture to deal with the multimodal AI datasets that run on our differentiated EOS network data link systems.
16. Arista showcased a technology demonstration of our EOS-based AI agent that can be on the NIC itself or alternatively, inside the host.
17. Our networking platforms are becoming the epicenter of all digital transactions, be they campus center, data center, WAN centers, or AI centers.

### Chantelle Breithaupt, Chief Financial Officer
18. Our existing innovative product portfolio, along with our new product introductions, are well suited for our cloud, AI enterprise, and providers customers.

## Q&A

### Michael Ng, Goldman Sachs, Analyst
1. As we head into next-generation GPUs with Blackwell and the NVL72, there's been some discussion about whether these systems may be less modular in some of its components, particularly for back-end networking. ⚑ uncertain
2. I was just wondering if you could share your views and provide some clarity on the vendor modularity of Blackwell, particularly as it relates to networking. ⚑ uncertain

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
3. And therefore, our timely introduction of these 800-gig products will be required, especially more for Blackwell. ⚑ uncertain
4. In terms of its connection and modularity with NVLink and 72 port, there's always been a market for what I call scale up, where you're connecting the GPUs internally in a server and the density of those GPUs connecting in the past has been more PCIe and XL and now NVLink, and there's a new consortium now for called UAL that's going to specify that, I believe, eventually, by the way, even there, Ethernet will win. ⚑ uncertain
5. And so, that density depends more on the AI accelerator and how they choose to connect.

### Aaron Rakers, Analyst
6. Is that related to these AI opportunities?

### Meta Marshall, Analyst
7. Jayshree, last quarter, you had mentioned kind of four major AI trials that you guys were a part of.
8. Just trying to get a sense of maybe if that Tier 2 win was a part of those AI trials.
9. Or just any update on where those four AI trials stand or what the current count of AI trials is currently?

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
10. First of all, all four trials are largely in what I call cloud and AI titans.
11. But in addition to that, we have tens of smaller customers who are starting to do AI pilots.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
12. They're about to build an AI cluster. ⚑ context-dependent

### Atif Malik, Citi, Analyst
13. And how does that relate to the $750 million AI networking revenue number you have provided for next year?

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
14. Our AI TAM, which we count in a more narrow fashion as how much of InfiniBand will move to Ethernet on the back end.
15. We don't count the AI TAM that's already in the front end, which is part and parcel of our data center.
16. So, these four are the building blocks that I call the campus center, data center, AI center, and WAN center.

### Antoine Chkaiban, New Street Research, Analyst
17. I'd like actually to ask about the non-AI component of your Cloud and AI segment.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
18. We saw that there was a lot of pivot going on from the classic cloud, as I like to call it, to the AI in terms of spend.
19. And we continue to see favorable preferences to AI spend in many of our large cloud customers.
20. So, while we think AI will grow faster than cloud, we're betting on classic cloud continuing to be an important aspect of our contributions.

### Chantelle Breithaupt, Chief Financial Officer
21. They all have different timings because they're unique to the customer, the use case, AI, classic cloud, etc.. ⚑ context-dependent

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
22. And I think it's fair to say if it's AI, it takes longer, if it's classic cloud, it's shorter.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
23. And finally, the AI trials you talked about, they tend to be smaller, but it's a representation of the confidence the customer has.
24. But when it comes to the mission-critical networks, they've recognized the importance of best-of-breed reliability, availability, performance, no loss, and familiarity with the data center is naturally leading to pilots and trials on the AI side with us.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
25. For this AI center, as we call it, is going to be a conglomeration of both the front and the back.
26. So, if I were to fast forward three, four years from now, I think the AI center is a supercenter of both the front end and the back end.
27. But if I were to fast forward, I think there may be many more edge use cases, many more inference use cases and many more small-scale training use cases which will make that distinction difficult to make. ⚑ uncertain

### Alex Henderson, Analyst
28. Clearly, there's an enormous amount of spending going into the AI front end, back end networking elements, as well as the GPUs.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
29. I would say there's such a heavy bias in the cloud titans toward training and super training and the bigger and better the GPUs, the billion parameters, the OpenAI, ChatGPT, and Llamas that you're absolutely right that at some level, the classic cloud, what you call traditional, I'm still calling classic, is a little bit neglected last year and this year.
30. Having said that, I think once the training models are established, I believe this will come back, and it will sort of be a vicious cycle that feeds on each other.
31. But at the moment, we're seeing more activity on the AI and more moderate activity on the cloud.

### Alex Henderson, Analyst
32. Does the reacceleration of application growth excluding the AI play into that?

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
33. I don't know how to measure it, but I think the more AI back end we put in, we expect that to have a pressure on the front end of x percent.
34. But absolutely, as the two holistically come together to form this AI center, I believe the front end will have pressure.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
35. Now in Microsoft and Meta, how they will pivot to AI and how they will reduce the spend and all that things, that movie will play out in the next six months.
36. And we expect to do well with them, both in cloud and AI, depending on their priorities, of course.

### Tim Long, Analyst
37. Thank you, maybe we'll go over to the software services, the AI stuff has been beaten up a little bit here.

### Sebastien Naji, William Blair, Analyst
38. Hey, thanks for taking the question and sorry to bring you guys back to the AI conversation, but this one is a little bit more high level.

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
39. Yes, so if you look at an AI network design, you can look at it through two lenses, just through the compute, in which case you look at scale up and you look at it strictly through how many processes there are.
40. But when we look at an AI network design, it's a number of GPUs or XTUs per workload.
41. Because the training models are definitely centered around job completion time.

### David Vogt, UBS, Analyst
42. You have a pretty strong ramp of AI likely next year.
43. So, just any color there in terms of what Q4 might look like from an AI perspective relative to your expectations from a glide path perspective?

### Jayshree V. Ullal, Chief Executive Officer and Chairperson
44. So, we expect to be single-digit small percentages of our total revenue in AI this year.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Ashwin Kohli, Senior Vice President-Customer Engineering] Their next top priority was to use automation, consistent end-to-end provisioning and visibility, which can be delivered by our CloudVision platform.
2. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Or they're trying to create a little oasis in the desert and prove that our post-pandemic campus is much better with a leaf/spine topology, wired/wireless connecting to it at leaf, and then enabling things like zero-touch automation, method segmentation, capabilities, analytics, etc..

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Jayshree V. Ullal, Chief Executive Officer and Chairperson] This is a rich portfolio of 800-gig products, not just a point product, but in fact, a complete portfolio that is both NIC and GPU agnostic.
2. [Prepared remarks · Ashwin Kohli, Senior Vice President-Customer Engineering] This customer is a large data center customer, which has deployed us for almost a decade.
3. [Prepared remarks · Ashwin Kohli, Senior Vice President-Customer Engineering] Given only three months' window, Arista leveraged the existing data center design and adapted this to the campus topology with a digital twin of the design in minimal time.
4. [Prepared remarks · Ashwin Kohli, Senior Vice President-Customer Engineering] The third example is the next win in the international arena of a large automotive manufacturer that due to its size and scale, previously had more than three different vendors in the data center, which created a very high level of complexity both from a technical and also from an operational perspective.
5. [Prepared remarks · Ashwin Kohli, Senior Vice President-Customer Engineering] The customer's key priority was to achieve a higher level of consistency across their infrastructure, which is now being delivered via a single EOS binary image and CloudVision solution from Arista.
6. [Prepared remarks · Ashwin Kohli, Senior Vice President-Customer Engineering] This simplification has led the customer to adopt Arista beyond the data center and extend the Arista solution into the routing component of the infrastructure, which included our 7500 R3 spine platforms.
7. [Prepared remarks · Chantelle Breithaupt, Chief Financial Officer] Capital expenditures for the quarter were $3.2 million.
8. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Michael, I think as the GPUs get faster and faster, obviously, the dependency on the network for higher throughput is clearly related.
9. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] So, they started about a few hundred GPUs, would you say?
10. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] But TAM consists of our data center TAM.
11. [Q&A · Antoine Chkaiban, New Street Research, Analyst] What can you tell us about how investments in traditional infrastructure are trending?
12. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] I think the migration to 100 gig data center is pretty solidly going on.
13. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] So, that's on the data center.
14. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] They may be using other GPUs, servers, etc..
15. [Q&A · Karl Ackerman, Analyst] So, there are several data points across the supply chain that indicate enterprise networking and traditional server units are beginning to recover.
16. [Q&A · Karl Ackerman, Analyst] How to think about the adoption or the growth of server and networking gear on for campus environments and what you're seeing there.
17. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] So, perhaps it may come as a surprise to you, but servers aren't always related to campus.
18. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Service tend to be dealing with more data center upgrades.
19. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] And again, it has a lot to do with the familiarity with us in the data center, and that's translating to more success in the campus.
20. [Q&A · Benjamin Bollin, Analyst] How quickly could that become a more realistic opportunity to capture more of that true fabric of overall compute resources?
21. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] So, we'll be able to track it as long as there's GPUs and strictly training use cases.
22. [Q&A · Alex Henderson, Analyst] But there is a rebounding growth rate of application that is ultimately driving the traditional business that has historically been called the CPU side of the data center.
23. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] And so, we do not count that in our $750 million number, to be accurate, to the only GPU native connections.
24. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Well, first, I just want to say, when you say competitive environment, it's complicated with NVIDIA because we really consider them a friend on the GPUs, as well as the mix, so not quite a competitor.
25. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] And so, I think it's fair to say that if a customer were bundling with their GPUs, then we wouldn't see it.
26. [Q&A · James Fish, Analyst] And really, I'm trying to understand if we're starting to see that core enterprise data center network refresh actually pick up versus kind of the share gains that you guys have historically seen.
27. [Q&A · James Fish, Analyst] And is there an underlying change in enterprise customer behavior, whether it's for the data center or Jayshree, I know you were talking about the campus earlier.
28. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] And probably a fourth category where some of them are disillusioned with the public cloud and want to repatriate some of their workloads back into the data center.
29. [Q&A · Ashwin Kohli, Senior Vice President-Customer Engineering] And so, to answer your question, from what I'm seeing from customers, they're kind of fed up with being deployed in the data center, specifically, something which is proprietary lock-in, right?
30. [Q&A · Ashwin Kohli, Senior Vice President-Customer Engineering] Something which does not give them the flexibility to join multiple use cases such as data center, campus, routing, and they want something that just works.
31. [Q&A · Ashwin Kohli, Senior Vice President-Customer Engineering] So, James, I would say the message is echoing successfully in our existing customers who are taking a risk not only in the single use case of data center, but expanding that across data center, campus, routing, WAN.
32. [Q&A · Sebastien Naji, William Blair, Analyst] You've talked about 15% of capex.
33. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Distribution and location of these GPUs are important.
34. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] But it all starts with number of GPUs, performance, and billions of parameters.
35. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] All this to say, a network design-centric approach has to be taken for these GPU clusters.
36. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Some of the GPUs, and you've seen this in public blogs published by some of our customers have already gone from tens of thousands to 24,000 and are heading toward 50,000 GPUs.
37. [Q&A · Jayshree V. Ullal, Chief Executive Officer and Chairperson] Next year, I think there will be many of them heading into tens of thousands aiming for 100,000 GPUs.
