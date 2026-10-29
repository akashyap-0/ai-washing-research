# Arista Networks — 2023_Q3 Earnings Call (transcript)

- **Company:** Arista Networks (ANET); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** ANET
- **CIK:** 0001596532
- **Period:** 2023_Q3 (call held October 30, 2023; date from page date line)
- **Calendar quarter:** 2023 Q3 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/10/30/arista-networks-anet-q3-2023-earnings-call-transcr/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** c0ce9513d84469f5676d3587ca7c2ba0404d467ac1cc2e9fcdc4077d6fc1aa6f
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**40 AI sentences of 546 total**
(Borderline, listed at the end: 1 automation/robotics, 21 infrastructure, none containing an AI term.)

## Prepared remarks

### Liz Stine, Director, Investor Relations
1. During the course of this conference call, Arista Networks' management will make forward-looking statements, including those relating to our financial outlook for the fourth quarter of the 2023 fiscal year, longer-term financial outlook for 2024 and beyond, our total addressable market and strategy for addressing these market opportunities, including AI, customer demand trends, supply chain constraints, component costs, manufacturing output, inventory management, and inflationary pressures on our business, lead time, product innovation, working capital optimization, and the benefits of acquisitions, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K, and which could cause actual results to differ materially from those anticipated by these statements. ⚑ uncertain: safe-harbor

### Jayshree Ullal, President and Chief Executive Officer
2. During the past year, our cloud titan customers have been planning a different mix of AI networking and classic cloud networking for their compute and storage clusters.
3. Looking ahead, we will combine cloud and AI customer spend into one category called cloud and AI titan sector.
4. This new cloud and AI titan sector is projected to represent greater than 40% of our total revenue mix due to the favorable AI investments expected in the future. ⚑ context-dependent
5. Arista's ethernet modular switch coupled with EOS created a perfect combination of a phishing platform with real-time telemetry, leveraging our EOS state-driven publish/subscribe model. ⚑ uncertain
6. Our next win showcases our expansion of Arista in the public sector with their AI initiative.
7. This grant-funded project utilizes Arista's simplified operational models with CloudVision. ⚑ uncertain ⚑ context-dependent
8. New AI workloads require high scale, high radix, high bandwidth, and low latency, as well as a need for granular visibility.
9. This build out of a single EVPN VXLAN-based 400 gig fabric is based on deep buffer spines and underscores the importance of a lossless architecture for AI networking. ⚑ context-dependent
10. The customer was able to leverage the Arista Validated Design models, AVD, all the way from data center into the campus network. ⚑ uncertain
11. These three customers illustrate our power of the platform and software innovations for a modern network model with a low total cost of operation. ⚑ uncertain ⚑ context-dependent

## Q&A

### Jayshree Ullal, President and Chief Executive Officer
1. We continue to see good momentum on enterprise, and we continue to see a good, you know, expected push on the combination of both cloud and AI together.

### Antoine Chkaiban, New Street Research, Analyst
2. So, accelerated AI cluster deployment is clearly waiting on traditional infrastructure deployment this year.

### Jayshree Ullal, President and Chief Executive Officer
3. And as we said last year, many of our customers are favoring spending more on the back end with AI, which doesn't mean they stopped spending on front end, but they've clearly prioritized and doubled down on AI this year.
4. My guess is as we look at the next few years, they'll continue to double down on AI, but you cannot build an AI back-end cluster without thinking of the front end.
5. So, we'll see a full cycle here where, while today the focus is greatly on AI and the back end of the network, in the future, we expect to see more investments in the front end as well.

### Anshul Sadana, Chief Operating Officer and Senior Vice President
6. AI is everyone's priority right now, and the rest will get touched at the right time.

### Jayshree Ullal, President and Chief Executive Officer
7. Today, if I look at the five major designs for AI networking, one of them is still very InfiniBand dominated, all the others we're looking at are adopting a dual strategy of both Ethernet and InfiniBand.
8. So, I think AI networking is going to become more and more favorable to Ethernet, particularly with the Ultra Ethernet Consortium and the work they're doing to define a spec, you're going to see more products based on UEC.

### Jayshree Ullal, President and Chief Executive Officer
9. I think one thing to just add is the entropy and efficiency of these large language models and the job completion time is becoming so critical that it's not just about packet latency, it's really about end-to-end latency.

### Aaron Rakers, Wells Fargo Securities, Analyst
10. I know, Jayshree, last quarter, I think it was you commented that you'd expect to see pilot deployments for these AI opportunities in '24 and then meaningful volume in 2025.
11. And then, on that, can you give us some context of how you see network spend intensity for these AI fabrics relative to -- I think in the past, it's been kind of high single-digit percent of compute spend on networking in classical cloud infrastructure environments?

### Sebastien Naji, William Blair, Analyst
12. I wanted to ask about the change in revenue breakdown and the inclusion of OCI in this new cloud titan and AI segment.

### Jayshree Ullal, President and Chief Executive Officer
13. So, I think OCI has become a meaningful top-tier cloud customer, and they belong in the cloud titan category in addition to their AI investments as well.

### Meta Marshall, Morgan Stanley, Analyst
14. Jayshree or Anshul, maybe just some commentary on the Tier 2 and specialty providers and just what you're seeing in terms of other people kind of building out some of these AI clusters.

### Jayshree Ullal, President and Chief Executive Officer
15. So, a lot of customers are trying AI for small clusters, not too different from what we saw with HPC clusters back in the day.

### Atif Malik, Citi, Analyst
16. And one of your peers has talked about 500 million in AI orders, whether it's custom chip.

### Jayshree Ullal, President and Chief Executive Officer
17. And what Broadcom has done in building that portfolio not only for cloud networking, but for campus and AI is impressive.
18. But our systemwide features, whether it's in dynamic load balancing or latency analyzer, to really improve the job completion time and deal with that frequent communication and generative AI is also fundamentally important.

### Tim Long, Barclays, Analyst
19. I just wanted to hit on the cloud titan vertical or cloud titan AI vertical now, if I could.

### Jayshree Ullal, President and Chief Executive Officer
20. [Inaudible] you know, while we expect, due to many of the capex news you've seen and shift in AI spending, that it's possible they come down, but they're still going to be very strong north of 10% contributors to our 2023 results.

### David Vogt, UBS, Analyst
21. So, if I think about your market sector trend update, how much of the shift to that 40% to 45% cloud and AI titans reflects the inclusion of new AI use cases going forward and the shift of Oracle combined with maybe some normalization at Meta and Microsoft?

### Jayshree Ullal, President and Chief Executive Officer
22. And both their cloud spend, OCI and AI, is significant, both as a company and for Arista.
23. We're simply saying AI is going to become such an important component of all our cloud types that it's now a combined vertical.

### Ita Brennan, Chief Financial Officer
24. It's really more about the future and how do you think AI will impact these numbers going forward. ⚑ context-dependent

### Jayshree Ullal, President and Chief Executive Officer
25. Yeah, AI is too small to impact as much right now, right?

### Jayshree Ullal, President and Chief Executive Officer
26. And then, obviously, the mix changes from time to time, especially with the cloud and AI.

### Jayshree Ullal, President and Chief Executive Officer
27. Powering the internet, powering the cloud, powering the AI, these are hard problems.
28. It's how we enable the chip to do these complicated routing algorithms. ⚑ uncertain ⚑ context-dependent

### Liz Stine, Director, Investor Relations
29. As a reminder, Arista will be hosting our 2023 Cloud and AI Innovators Analyst Day on Thursday, November 9th.

## Borderline: automation/robotics without an AI term

1. [Q&A · Anshul Sadana, Chief Operating Officer and Senior Vice President] And as Jayshree mentioned, both data center and campus, customers are coming to us for the automation for the higher quality, for the visibility, that we're able to bring to them across the board in one architecture, one OS, and one CloudVision.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] Our historic classification of our cloud titan customers has been based on industry definition of customers with or likely to attain greater than 1 million installed compute servers.
2. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] The power of our one consistent software stack across a breadth of use cases, be the WAN routing, campus, branch, or data center infrastructure, is truly unmatched by our industry peers.
3. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] Our first customer win is an international one where the customer is providing services for their interconnect of high-performance compute, HPC, clusters, which are often its foundation for GPU as a service offering.
4. [Prepared remarks · Ita Brennan, Chief Financial Officer] Capital expenditures for the quarter were 11.2 million.
5. [Q&A · Samik Chatterjee, JPMorgan Chase and Company, Analyst] I know some of the cloud companies have talked about their capex outlook for next year as well.
6. [Q&A · Antoine Chkaiban, New Street Research, Analyst] And I'm keen to hear how sustainable you think this is, because the vast majority of workloads still run on traditional infrastructure, right?
7. [Q&A · Antoine Chkaiban, New Street Research, Analyst] So, is it fair to expect a rebound in traditional infrastructure spend next year?
8. [Q&A · Amit Daryanani, Evercore ISI, Analyst] But maybe you can talk about, is the strength more coming from campus versus the data center side, maybe just qualitatively where you're seeing better trends?
9. [Q&A · Amit Daryanani, Evercore ISI, Analyst] And to the extent, you can talk about campus versus the data center that would be really helpful.
10. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And back in 2020, we had a small enterprise business and it was largely comprised of, as you rightly pointed out, data center and some high-performance compute and low-latency HFT.
11. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And to your question on data center versus campus, the answer is yes to both.
12. [Q&A · Jayshree Ullal, President and Chief Executive Officer] We actually see one uniform architecture where you can have a universal spine that connects into a wired leaf, a wireless leaf, a storage cluster, a compute cluster, a border leaf for routing, and WAN transit.
13. [Q&A · Ben Bollin, Cleveland Research, Analyst] I was hoping you might be able to comment a little bit about your thoughts as you make progress in the backend network around GPU cluster opportunity, how you see that developing versus what you've shared with us previously?
14. [Q&A · Anshul Sadana, Chief Operating Officer and Senior Vice President] There's a lot of fine-tuning needed in these back-end networks to get the maximum utilization of GPUs.
15. [Q&A · Jayshree Ullal, President and Chief Executive Officer] Coming back to this networking spend versus the rest of the GPUs, etc., I would say it started to get higher and higher with 100 gig, 400 gig, 800 gig, where the optics and the switches are more than 10%, perhaps, even 15%, in some cases 20%.
16. [Q&A · Anshul Sadana, Chief Operating Officer and Senior Vice President] Many companies are trying to build these clusters, maybe not hundreds of thousands of GPUs, but thousands of GPUs together in their real estate if they can get them.
17. [Q&A · Jayshree Ullal, President and Chief Executive Officer] I think they're also waiting for GPUs like everyone else is.
18. [Q&A · Atif Malik, Citi, Analyst] Jayshree, at the recent Open Compute Project Conference, Marvell and Broadcom, leading Ethernet switch merchant chip providers, sounded very confident in terms of Ethernet adoption at hyperscalers like Meta and Oracle as well.
19. [Q&A · Anshul Sadana, Chief Operating Officer and Senior Vice President] And now, the whole world can upgrade the high-frequency trading infrastructure going from 10 to 25.
20. [Q&A · Jayshree Ullal, President and Chief Executive Officer] Where the value really comes in, and again, I alluded to this, is capex versus opex.
21. [Q&A · Jayshree Ullal, President and Chief Executive Officer] Let me just say how innocently we reported this, which is Oracle is a greater than $1 million installed server company right now.
