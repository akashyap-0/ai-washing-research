# Arista Networks — 2024_Q3 Earnings Call (transcript)

- **Company:** Arista Networks (ANET); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** ANET
- **CIK:** 0001596532
- **Period:** 2024_Q3 (call held November 7, 2024; date from page date line)
- **Calendar quarter:** 2024 Q3 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/11/07/arista-networks-anet-q3-2024-earnings-call-transcr/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** c095d377190ee4fd35a435f81ba8396fb98c46b956067c87efb901a80b117923
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**58 AI sentences of 473 total**
(Borderline, listed at the end: 1 automation/robotics, 24 infrastructure, none containing an AI term.)

## Prepared remarks

### Liz Stine, Director, Investor Relations
1. During the course of this conference call, Arista Networks' management will make forward-looking statements, including those relating to our financial outlook for the fourth quarter of the 2024 fiscal year; longer-term business model and financial outlooks for 2025 and beyond; our total addressable market and strategy for addressing these market opportunities, including AI, customer demand trends, supply chain constraints, component costs, manufacturing output, inventory management, and inflationary pressures on our business; lead times, product innovation, working capital optimization, and the benefits of acquisitions, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K and which could cause actual results to differ materially from those anticipated by these statements. ⚑ uncertain: safe-harbor

### Jayshree V. Ullal, Chair and Chief Executive Officer
2. This can be a data center, a campus center, a WAN center, or an AI center. ⚑ context-dependent
3. We provide customers the state foundation for data for AI and machine learning, without which AI and ML would just be buzzwords.
4. Arista is well-positioned with the right network architecture for client-to-campus data center cloud and AI networking.
5. Three principles guide us and differentiate us in bringing this data-driven networking: number one, best-in-class, highly available proactive products with resilience and hitless upgrade built in at multiple levels; two, zero-touch automation and telemetry with predictive client-to-cloud one click operations with that granular visibility that relies less on human staff; number three, prescriptive insights for deeper AI for networking, delivering AI ops and AVA algorithms for security, observability, and root cause analysis.
6. Networking for AI is gaining a lot of traction as we move from trials in 2023 to more pilots in 2024, connecting to thousands of GPUs.
7. In our vernacular, Arista AI centers are made up of both the back-end clusters and front-end networks.
8. AI traffic differs greatly from cloud workloads in terms of diversity, duration, and size of flow.
9. The fidelity of AI traffic flows with the slowest flow matters, and one slow flow can slow down the entire job completion time is a crucial factor in networking.
10. Our AI centers connect seamlessly from the back end to the front end of compute, storage, WAN, and classic cloud networks.
11. Arista is emerging as a pioneer in scale-out Ethernet, accelerated networking for large scale training, and AI workloads.
12. Our new Ethernet portfolio with wire-speed 800-gig throughput and non-blocking performance scales from single-tier to efficient two-tier networks for over 100,000 GPUs, potentially even a million AI accelerators with multiple tiers.
13. Our accelerated AI networking portfolio consists of three families with over 20 switching products and not just one-point switch.
14. And while it may physically look like and be cable like a two-tier leaf and spine network, DES provides a single-stage forwarding with highly efficient spine fabric, eliminating the need for tuning and encouraging fast failover for large AI accelerator-based clusters.
15. It complements our Arista flagship 7800 AI spine for the ultimate scale with differentiated fare and fully scheduled cell-spraying architecture with a virtual output queueing fabric, saving valuable AI processor resources and improving job completion time. ⚑ context-dependent

### John McCool, Senior Vice President, Chief Platform Officer
16. I'm pleased to report Arista 7700R4 Distributed Etherlinck Switch to 7800R4 spine, along with the 7060X6 AI leaf that we announced in June, have entered into production, providing our customers the broadest set of 800-gigabit-per-second Ethernet products for their AI networks.
17. This broad range of Ethernet platforms allows our customers to optimize density and minimize tiers to best match the requirements of their AI workload. ⚑ context-dependent
18. As our customers continue with AI deployments, they're also preparing their front-end networks.
19. New AI clusters require new high-speed port connections into the existing backbone.
20. In addition, we will increase our on-hand inventory to respond to the rapid deployment of new AI networks and reduce overall lead times as we move into next year.
21. Next-generation data centers integrating AI will contend with significant increases in power consumption while looking to double network performance.
22. These attributes give us confidence that we will continue to execute on our road map in this rapidly evolving AI networking segment. ⚑ context-dependent

### Jayshree V. Ullal, Chair and Chief Executive Officer
23. Critical to the rapid adoption of AI networking is the Ultra Ethernet Consortium specification expected imminently with Arista's key contributions as a founding member.
24. The UECE ecosystem for AI has evolved to over 97 members.
25. In our view, Ethernet is the only long-term viable direction for open standards-based AI networking.
26. Arista is building holistic AI centers powered by our unparalleled superiority of EOS and the depth of automation and visibility software provided by CloudVision.
27. Arista EOS delivers dynamic methods using cluster load balancing for congestion control and smart system upgrades where the traffic for AI continues to flow in the midst of an upgrade.
28. Arista continues to work with AI accelerators of all types, and we're agnostic to mix to bring advanced EOS visibility all the way down to the hosts.
29. This is quite a jump in 2024, influenced by faster AI pilots. ⚑ context-dependent
30. Within that 8 billion revenue target, we are quite confident in achieving our campus and AI back-end networking targets of 750 million each in 2025 that we set way back one or two years ago.
31. It's important to recognize, though, that the back end of AI will influence the front-end AI network and its ratios. ⚑ context-dependent
32. Our comprehensive AI center networking number is therefore likely to be double of our back-end target of 750 million, now aiming for approximately 1.5 billion in 2025.

### Chantelle Breithaupt, Chief Financial Officer
33. This is primarily driven by increased inventory in order to respond to the rapid deployment of AI networks and to reduce overall lead times as we move into 2025 mentioned in John's prepared remarks. ⚑ context-dependent
34. The expected revenue mix is forecasted to have an increased weighting of cloud and AI customers, placing the gross margin outlook at 60% to 62% and operating margin at approximately 43% to 44%.

## Q&A

### Samik Chatterjee, Analyst
1. So, if I take those two into account, it does imply that the ex sort of AI and ex campus business is only growing single digits next year.
2. So, just maybe have parse through that as to why there's a significant deterioration in the non-AI sort of non-campus business implied in the numbers and what maybe is driving that sort of -- in your expectations, what's driving that outlook?

### Jayshree V. Ullal, Chair and Chief Executive Officer
3. So, we don't want to get ahead of ourselves on how much better we can do and that's kind of how we started '24 either, and we were pleasantly surprised with the faster acceleration of AI pilots.
4. So, we definitely see that our large cloud customers are continuing to refresh on the cloud but are pivoting very aggressively to -- so it wouldn't surprise me if we grow faster in AI and faster in campus in the new center markets and slower in our classic markets called that data center and cloud.

### Antoine Chkaiban, Analyst
5. Can you maybe provide an update on the four major AI trials that you gave in the past?

### Tal Liani, Analyst
6. What is the outlook for white box participation in GenAI?

### Jayshree V. Ullal, Chair and Chief Executive Officer
7. If we didn't have the ability to connect to their GPUs, we wouldn't have all this AI networking demand.

### Simon Leopold, Analyst
8. I do want to sort of look at this competition or competitive landscape broadly in that what I'm trying to understand is how it may be changing with the advent of AI.

### Jayshree V. Ullal, Chair and Chief Executive Officer
9. So, since you asked me specifically about AI as opposed to cloud, let me parse this problem into two halves, the back end and the front end, right?
10. In fact, I am specifically aware of a couple of situations where the AI applications aren't even running on some of the industry peers you talked about, and they want to swap theirs for ours.
11. And overall, I would classify our performance in AI coming from being a now 12 years ago to where we are today.

### Ben Reitzes, Melius Research, Analyst
12. I wanted to ask a little bit more about the $750 million in AI for next year.

### Karl Ackerman, Analyst
13. Will it be deploying your new Etherlink switches and AI spine products on 800-gig ports?

### Jayshree V. Ullal, Chair and Chief Executive Officer
14. There's WAN center, and of course, there's a little bit of AI in there, too.

### Meta Marshall, Analyst
15. But just how are you thinking about kind of adding other either Tier 2 opportunities or sovereigns or just kind of some of these other customers that are investing heavily in AI and kind of how do you see those opportunities developing those for Arista?

### Jayshree V. Ullal, Chair and Chief Executive Officer
16. So, there are largest AI titans, if you will.
17. So, we're folding on the big five to the point that they really skew our numbers and they're very important to establish our beachhead, our innovation, and our market share in AI, but there's definitely more going on.

### Aaron Rakers, Analyst
18. I wanted to kind of segue off the competitive landscape and just ask you about when I look at your 2025 outlook as well as the midterm model that you provided, it looks like you're making some assumptions of some margin declines. ⚑ uncertain

### Atif Malik, Analyst
19. What signs are you looking for to see the lift from AI on the front end or classic cloud from the pressure on the bandwidth?

### Jayshree V. Ullal, Chair and Chief Executive Officer
20. Now, listen, I think it all depends on Atif their approach to AI.
21. If they just want to build a back-end cluster and prove something out, they just look for the highest job training completion and intense training models.
22. That will include AI, but it will include other things as well. ⚑ context-dependent
23. It won't be unique to AI. ⚑ context-dependent
24. Don't know how to exactly count that as pure AI, which is why I qualify it by saying increasingly, if you start having inference training, front-end storage, when classic cloud all come together, the AI -- the pure AI number becomes difficult to track.

## Borderline: automation/robotics without an AI term

1. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] John alluded to this, there's a tremendous amount of scale with L2, L3, EVPN, VXLAN, visibility, telemetry, automation routing at scale, encryption at scale.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Jayshree V. Ullal, Chair and Chief Executive Officer] At the recent OCP in mid-October 2024, we officially launched a very unique platform, the Distributed Etherlink 7700, to build two-tier networks for up to 10,000 GPU clusters.
2. [Prepared remarks · John McCool, Senior Vice President, Chief Platform Officer] Together with 800-gigabit-per-second parallel optics, our customers are able to connect two 400-gigabit-per-second GPUs to each port, increasing the deployment density over current switching solutions.
3. [Prepared remarks · John McCool, Senior Vice President, Chief Platform Officer] Our experience in co-design with the leading cloud companies provides insight into the variety of switch configurations required for these tightly coupled data center environments.
4. [Prepared remarks · Chantelle Breithaupt, Chief Financial Officer] Capital expenditures for the quarter were $7 million.
5. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] Three of the customers are moving from trials to pilots this year, inspecting those three to become 50,000 to 100,000 GPU clusters in 2025.
6. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] In 2025, they're awaiting new GPUs, and they've got some challenges on power cooling, etc.
7. [Q&A · Tal Liani, Analyst] NVIDIA in the last quarter the launch of the Spectrum X, it shows that in data center switching their market share went from like 4% to 15%.
8. [Q&A · Tal Liani, Analyst] Is it going to be higher or lower than in front-end data centers?
9. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And whether it's the large scale-out Ethernet working customers like the Titans or even the smaller enterprises, we're seeing a lot of smaller GPU clusters with the enterprise.
10. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] We certainly welcome NVIDIA as a partner on the GPU side and a fierce competitor, and we look to compete with them on the Ethernet switching.
11. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] At the back end, we're natively connecting to GPUs.
12. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And there can be many times, we just don't see it because somebody just muddles it in the GPU in particular, NVIDIA.
13. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And this, what I would call accelerated networking portfolio complements NVIDIA's accelerated compute portfolio.
14. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, our enterprise opportunity now, we don't just characterize as data center.
15. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] There's data center.
16. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] They go, "Oh, OK, I can have the same spine from my data center and campus.
17. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] Our weakest partly because we are data center folks, and we're still learning how to sell radio is the WiFi that we plan to fix that, and this is where the extra coverage will come in.
18. [Q&A · Chantelle Breithaupt, Chief Financial Officer] I think where we're seeing some strength data center and campus, I would say financials, healthcare, media, retail.
19. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, we're not saying these five are the be-all, end-all, but these are the five we predict can go to 100,000 GPUs and more.
20. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] By the way, we do have at least 10 to 15 trials going on in the classic enterprise, too, but they're much smaller GPU counts, so we don't talk about it.
21. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] And then the 7700 is kind of the best of both worlds that gives you all the capabilities of the 7800 in a mini configuration up to 10,000 GPUs.
22. [Q&A · Jayshree V. Ullal, Chair and Chief Executive Officer] So, I think we know less about how to qualify that, but it could be very promising, and it could be a fast accelerator in the next couple of years.
23. [Q&A · John McCool, Senior Vice President, Chief Platform Officer] Between the 7060 and the 7800, we do see people that are optimizing a mix of both of those products in the same deployment, so they can get the minimum number of tiers but have the maximum amount of GPUs that fit their use case.
24. [Q&A · John McCool, Senior Vice President, Chief Platform Officer] So, we do see a lot of tailoring now around the size of the deployments based on how many GPUs they want to deploy their data center.
