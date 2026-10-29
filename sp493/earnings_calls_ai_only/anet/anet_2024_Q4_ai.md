# Arista Networks — 2024_Q4 Earnings Call (transcript)

- **Company:** Arista Networks (ANET); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** ANET
- **CIK:** 0001596532
- **Period:** 2024_Q4 (call held February 18, 2025; date from page date line)
- **Calendar quarter:** 2024 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2025/02/18/arista-networks-anet-q4-2024-earnings-call-transcr/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** 98489d8a4ded5f3bf1be776933a5e9fcd95c397d3096b537338dfce99870fb14
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**61 AI sentences of 585 total**
(Borderline, listed at the end: 1 automation/robotics, 29 infrastructure, none containing an AI term.)

## Prepared remarks

### Rudolph Araujo, Vice President, Security Product Strategy and Marketing
1. Our total addressable market and strategy for addressing these market opportunities, including AI, customer demand trends, supply chain constraints, component costs, manufacturing output, inventory management, and inflationary pressures on our business, lead times, product innovation, working capital optimization, and the benefits of acquisitions, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K and which could cause actual results to differ materially from those anticipated by these statements. ⚑ uncertain: safe-harbor

### Jayshree V. Ullal, Chair and Chief Executive Officer
2. With the momentum of generative AI, we have achieved well beyond that at almost 20% growth, achieving a record revenue of 7 billion, coupled with a non-GAAP operating margin of 47.5%.
3. Our cloud and AI titans contributed significantly at approximately 48%, keeping in mind that Oracle is a new member of this category.
4. It has spanned over 14 years as we collaborate deeply with joint engineering and innovative AI and cloud products. ⚑ context-dependent
5. In terms of annual 2024 product lines, our core cloud AI and data center products are built on a highly differentiated extensible OS stack and is successfully deployed across 10-, 25-, 100-, 200-, 400-, and 800-gigabit Ethernet speeds.
6. It delivers power efficiency, high availability, automation, and agility as the data centers demand insatiable bandwidth capacity and network speeds for both front-end and back-end storage compute and AI zones. ⚑ context-dependent
7. In 2024, we expect 800-gigabit Ethernet to emerge as an AI back-end cluster in 2025.
8. We remain optimistic about achieving our AI revenue goals of 1.5 billion in AI centers, which includes the $750 million in AI back-end clusters in 2025.
9. Our network adjacencies market comprised of routing, replacing routers, and the cognitive AI-driven campus is going well.
10. While the 2024 headline has clearly been about generative AI, Arista continues to diversify its business globally with multiple use cases and verticals.
11. We are viewed as the modern network innovator of choice for client to campus, to cloud, and AI networking, ideally positioned with our differentiated foundation.
12. These centers of data, as we call it, can reside in the campus, as a campus center or data center or WAN centers or AI centers, regardless of their locations. ⚑ context-dependent
13. Networking for AI is also gaining traction as we move into 2025, building some of the world's greatest Arista AI centers at production scale.
14. And as I've shared with you often, the fidelity of the AI traffic differs greatly from cloud workloads in terms of diversity, duration, and size of flow.
15. Just one slow flow can slow the entire job completion time for a training workload.
16. Therefore, Arista AI centers seamlessly connect to the front end of compute, storage, WAN, and classic cloud networks with our back-end Arista Etherlink portfolio.
17. This AI-accelerated networking portfolio consists of three families and over 20 Etherlink switches, not just one point switch. ⚑ context-dependent
18. Our AI for networking strategy is also doing well, and it's about curating the data for higher-level network functions.

### Chantelle Breithaupt, Chief Financial Officer
19. As mentioned in prior quarters, this expected activity represents purchases for chips related to new products and AI deployments.
20. This reflects our combined outlook for cloud, AI, enterprise, and cloud specialty providers, along with a recognition of the volatility that we have seen in the market since the beginning of the year. ⚑ context-dependent

## Q&A

### Mike Ng, Goldman Sachs, Analyst
1. And, you know, how do you expect the risk of switches in the AI back end to be rolled out into production?

### Jayshree V. Ullal, Chair and Chief Executive Officer
2. first, I want to say Arista is still committed to four out of our five AI clusters that I mentioned in prior calls.

### Amit Daryanani, Analyst
3. But can you maybe just share your perspective that when it comes to AI networks, especially the back-end networks, you know, how do you see the mix evolving white box versus OEM solutions?

### Jayshree V. Ullal, Chair and Chief Executive Officer
4. When you look at the back end of an AI cluster, there are typically two components, the AI leaf and the AI spine.
5. The AI leaf connects to the GPUs and, therefore, is the first, if you will, point of connection.
6. And the AI spine aggregates all of these AI leafs.
7. Almost in all the back-end examples we've seen, the AI spine is generally 100% Arista-branded EOS.
8. The AI leaf can vary.
9. And we see a tremendous amount of differentiation not only, like I explained to you, in scale and routing features, but cluster load balancing, you know, AI visibility and analytics at real time, personnel queuing, congestion control, visibility, and most importantly, smart system upgrades because you sure don't want your GPUs to come down because you don't have the right software to accelerate so that the network provides the ideal foundation that if a GPU is in trouble, we can automatically give it a different connection and an alternate connection.

### Jayshree V. Ullal, Chair and Chief Executive Officer
10. Specific to the others we added in, they're not 10% customers, but they're doing very well, and we're happy with their cloud and AI use cases.

### Meta Marshall, Analyst
11. Maybe another topical question from investors just over the past month has been DeepSeek and just as you think about kind of this 1-1 ratio you've talked about on back end versus front end, you know, how you kind of see that changing as we've seen some of kind of the changes to kind of thoughts around training investments.

### Jayshree V. Ullal, Chair and Chief Executive Officer
12. Well, DeepSeek is -- certainly, DeepSeek is many stuff.
13. But I actually see this as a positive because, you know, I think you're now going to see a new class of CPUs, GPUs, AI accelerators, and -- where you can have substantial efficiency gains that go beyond training.
14. So, that could be some sort of inference or mixture of experts or reasoning and -- which lowers the token count and, therefore, the cost. ⚑ uncertain
15. And I think the eye-opening thing here for all of our experts who are building all these engineering models is there are many different types, and training isn't the only one. ⚑ uncertain
16. So, I think this is a nice evolution of how AI will not just be a back-end training only limited to five customers type phenomena, but will become more and more distributed across the range of CPUs and GPUs.

### Aaron Rakers, Analyst
17. You know, when you see announcements like Stargate, and obviously Stargate has the involvement of one of your neo cloud titan customers, how do you conceptualize the opportunity set for Arista vis-a-vis both back-end and front-end networking in deployments like that?
18. And then, do you have any thoughts on just the broader context of what you're seeing on sovereign AI opportunities in your business?

### Jayshree V. Ullal, Chair and Chief Executive Officer
19. Stargate and sovereign AI are not quite related.
20. But when you look at Stargate and projects like this, I think you'll start to see more of a vertical rack integration, where the processor, the scale-up, the scale-out, and all of the software to provide a single point of control and visibility starts to come more and more together.
21. But definitely, in '26 and '27, you're going to see a new class of AI accelerators for a new class of training and inference, which is extremely different than the current, more pluggable Lego type of version.

### Atif Malik, Analyst
22. Now, you are reiterating 750 million AI back-end sales this year despite the stalled or the fifth customer.
23. And also, if you can talk to the 70 billion TAM number for 2028, how much is AI?

### Jayshree V. Ullal, Chair and Chief Executive Officer
24. On the 70 billion TAM in 2028, I would roughly say a third is AI, a third is data center and cloud, and a third is campus and enterprise.

### Jayshree V. Ullal, Chair and Chief Executive Officer
25. And as we increased our guidance to 8.2 billion, I think we're going to see momentum, both in AI cloud and enterprises.

### Jayshree V. Ullal, Chair and Chief Executive Officer
26. And I have yet to see an AI spine deployment that is not EOS based.
27. And the 7800 is the AI spine flagship product that we have been deploying last year, this year, and in the future.
28. So, in my view, it's difficult to imagine a highly resilient system without Arista EOS in AI or non-AI use cases.
29. So, all in all, EOS is alive and well in AI and cloud use cases, except in certain specific use cases where the customer may have their own operations staff to do so.

### Jayshree V. Ullal, Chair and Chief Executive Officer
30. Yeah, no, listen we're always looking at three major threats: our classic cloud business, our AI, and the enterprise, you know, led by Ashwin and Chris is a very significant area of investment for us.

### Tal Liani, Analyst
31. Or do you start to see enterprises investing because of AI and applications for AI?

### Chantelle Breithaupt, Chief Financial Officer
32. I would say for the AI perspective, you know, speaking with the customers, it's great.
33. You know, they're working mostly with cloud service providers at the beginning kind of doing some training, and then they're deciding whether they bring that on-prem and inference, so they're making those decisions. ⚑ uncertain
34. So, I think those are early days, but we're having really great conversations for the AI part of that.

### Antoine Chkaiban, Analyst
35. I'd love to get your latest perspective on what you're hearing from service providers in AI.
36. One of your competitors mentioned that they were seeing AI driving demand for service providers because they're building out their network in anticipation of an increase in traffic driven by AI.

### Jayshree V. Ullal, Chair and Chief Executive Officer
37. We are seeing a new class of Tier 2 specialty cloud providers emerge that want to provide AI as a service and want to be differentiated there.

### Jayshree V. Ullal, Chair and Chief Executive Officer
38. The state transitions because of AI are certainly getting faster.
39. In AI, we see that cycle being almost every two years.

### Jayshree V. Ullal, Chair and Chief Executive Officer
40. Now, as you get into 1.60, part of the reason, I think, it's going to be measured and thoughtful is many of our customers are still awaiting their own AI accelerators or Nvidia GPUs, which -- with liquid cooling that would actually push that kind of bandwidth.

### Jayshree V. Ullal, Chair and Chief Executive Officer
41. As we move forward, we see not only that we connect to them, that we can connect to AMD GPUs and built-in in-house AI accelerators.

## Borderline: automation/robotics without an AI term

1. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, using CloudVision as a management domain, we're seeing much, much more traction, be it for automation, zero trust security, or observability with our campus products.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Chantelle Breithaupt, Chief Financial Officer] Capital expenditures for the quarter were $12.5 million.
2. [Prepared remarks · Chantelle Breithaupt, Chief Financial Officer] In October, we began our initial construction work to build expanded facilities in Santa Clara, and we expect to incur approximately $100 million in capex during fiscal '25 for this project.
3. [Q&A · Mike Ng, Goldman Sachs, Analyst] You know, are the sale of these switches tied to the deployment of next-generation Nvidia chips or hyperscale custom ASICs on the compute side?
4. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] They are awaiting new GPUs and some funding, too, I think.
5. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] Three out of the four customers are expected to, this year, roll out a cumulative of 100,000 GPUs.
6. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And you can imagine, they're all pretty much one major Nvidia class of GPU.
7. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] It's -- they will be waiting for the next generation of GPUs.
8. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] The fifth one is stalled, and three out of the four are expected to be 100,000 GPUs this year.
9. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, tremendous amount of differentiation there and even more valid in a GPU, which costs typically five times as much as a CPU.
10. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] Keep in mind that our 2024 Meta numbers is influenced by more of their 2023 capex, and that was Meta's year of efficiency where their capex was down 15% to 20%.
11. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, you're probably seeing some correlation between their capex being down and our revenue numbers being slightly lower in '24.
12. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, what -- what I'm -- what I like about all these different options is Arista can scale out network for all kinds of XPUs and accelerators.
13. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] You know, if you look at how we have classically approached GPUs and collective libraries, you know, we've largely looked at it as two separate building blocks.
14. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] There's the vendor who provides the GPU, and then there's us who provides the scale-out networking.
15. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, as I said, we're well on our way, and three customers deploying a cumulative of 100,000 GPUs is going to help us with that number this year.
16. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, first of all, when you're buying these expensive GPUs that cost $25,000, they're like diamonds, right?
17. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] From a product point of view, you know, we have a natural trickle-down effect from our high end data center products to the cloud.
18. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And so, whether it's the enterprise data center or the campus, I've never seen our portfolio be as strong as it is today.
19. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And we're particularly getting traction there where our data center customers are already familiar with us.
20. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And they're using a data center spine, and they can extend that same universal spine to wired and wireless leaf.
21. [Q&A · Tal Liani, Analyst] Is it just regular growth of data centers?
22. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, Tal, on routing, routing has always been a critical part of our offerings for the cloud and data center where, as you rightly described, it was more of a software enhancement.
23. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And the use case there is not data center, it's not campus, it's all a WAN-routed fabric.
24. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] I think what happened with Arista is we were largely building features for the cloud and data center, which is 20% of the features.
25. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, new GPUs will require new bandwidth, and that's going to push it out a year or two.
26. [Q&A · Sebastien Naji, William Blair and Company, Analyst] And you talked about this a little bit, but there's been a lot of discussion over the last few months between, you know, the general purpose GPU clusters from Nvidia and then the custom ASIC solutions from some of your popular customers.
27. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] Thank you, Jensen, for the GPUs because that gives us an opportunity to connect to them.
28. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, Arista could be the scale-out network for all types of accelerators.
29. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] We'll be GPU agnostic.
