# Arista Networks — 2023_Q2 Earnings Call (transcript)

- **Company:** Arista Networks (ANET); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** ANET
- **CIK:** 0001596532
- **Period:** 2023_Q2 (call held July 31, 2023; date from page date line)
- **Calendar quarter:** 2023 Q2 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/07/31/arista-networks-anet-q2-2023-earnings-call-transcr/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** aa75db7afc76855f0079e0ed7743af18fa62cbb4de46abcfc85205044d2a93f6
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**43 AI sentences of 534 total**
(Borderline, listed at the end: 3 automation/robotics, 24 infrastructure, none containing an AI term.)

## Prepared remarks

### Liz Stine, Director, Investor Relations
1. During the course of this conference call, Arista Networks management will make forward-looking statements, including those relating to our financial outlook for the third quarter of the 2023 fiscal year longer-term financial outlooks for 2023 and beyond, our total addressable market and strategy for addressing these market opportunities, including AI, customer demand trends, supply chain constraints, component costs, manufacturing output, inventory management and inflationary pressures on our business, lead times, product innovation, working capital optimization, and the benefits of acquisitions, which are subject to the risks and uncertainties that we discuss in detail in our documents filed with the SEC, specifically in our most recent Form 10-Q and Form 10-K, and which could cause actual results to differ materially from those anticipated by these statements. ⚑ uncertain: safe-harbor

### Jayshree Ullal, President and Chief Executive Officer
2. As we surpassed 75 million cumulative cloud networking ports, we are experiencing three refresh cycles with our customers, 100 gigabit migration in the enterprises 200 and 400 gigabit migration in the cloud, and 400 going to 800 gigabits for AI workloads.
3. Each customer brings a different business and mix of AI networking and classic cloud networking for their compute and storage clusters.
4. Therefore, we expect near-term cloud cycling demand to moderate with spend favoring their AI investments.
5. The AI opportunity is exciting.
6. As our largest cloud customers review their classic cloud and AI networking plans, Arista is adapting to these changes, thereby doubling down on our investments in AI.
7. Arista is a proud founding member of the Ultra Ethernet consortium that is on a mission to build open, multivendor AI networking at scale based on proven Ethernet and IP.
8. There a lot of software and EOS considerations for AI.
9. AI traffic and performance demands are different as it comprises of a small number of synchronized high-banded loans, making them prone to collisions that slow down the job completion time of AI cluster.
10. As we connect thousands of GPUs, generating billions of parameters of petoscale clusters, Arista's EOS capabilities must also scale along with our AI spine and leaf platforms to achieve that consistent performance and throughput.
11. Customers can now pick and choose programmable packet header field for better entropy and efficient lower balancing of their AI workloads.
12. Network visibility is also important in the training phase for large data sets to improve the accuracy of large language models.
13. Arista's new AI analyzer monitors and reports traffic counters at microsecond-level windows to detect and address microbots.
14. Our AI strategy and platforms are resonating well with our early customers.
15. Presently, in 2023, we are in the middle of trials for back-end AI networks, leading to pilots in 2024.
16. In the decade ahead, AI networking will become an extension of cloud networking to form a cohesive and seamless front-end and back-end network.

## Q&A

### Jayshree Ullal, President and Chief Executive Officer
1. There's the classic cloud networking, and then the AI.
2. So, we're reconciling how we double down more on AI, which we are feeling stronger and stronger about.

### Tim Long, Barclays, Analyst
3. Jayshree, I was hoping you could dig more into some of the comments around AI.
4. One, do you see that the move to AI expanding or diversifying more your cloud titan or cloud customers?

### Jayshree Ullal, President and Chief Executive Officer
5. So, when we think AI, there's clearly some ramifications of bandwidth on the front end of the network, but we're not counting that.
6. One is very, very small networks that are within the server where customers use PCIe, CXL, there is proprietary NVIDIA-specific technologies like NVLink that our listed does not participate. ⚑ uncertain
7. Then there's more medium clusters, you can think generitive IPI [Inaudible] inference where they may well get built on Ethernet. ⚑ uncertain
8. For the extremely large clusters with large-language training models, especially with the advent of ChatGPT 3 and 4, you're not talking about not just billion parameters but an aggregate of trillion parameters.
9. And neither technology, I want to say, were perfectly designed for AI.
10. So, I think the work we are doing with the UEC to improve Ethernet for AI is very important.

### Anshul Sadana, Senior Vice President, Chief Operating Officer
11. Meta, when you look at the cloud customers in the last few quarters, especially since the advent of ChatGPT, there's been a rotation in AI.
12. It's not that they're done with the upgrades or this is one of the upgrades, but they had to reprioritize their business and their deployments for AI. ⚑ context-dependent

### Ita Brennan, Chief Financial Officer
13. So, I think we will see a nice mix of AI and classic cloud networking over time.

### Antoine Chkaiban, New Street Research, Analyst
14. Does the accelerated deployment of AI clusters potentially open the door to business with the other two hyperscalers as the complexity of the networks is increasing rapidly?

### Jayshree Ullal, President and Chief Executive Officer
15. I think the way to look at our AI opportunity is it's -- there's 10 years ahead of us.

### Jayshree Ullal, President and Chief Executive Officer
16. And the addition of AI to that use cases just gave us a whole lot of broad opportunity from front end to back end.
17. Both of these were not as strong for us three years ago, and they also represent AI opportunities, but as you know, they represent campus, routing, classical data center opportunities, and allow us to go target a much larger TAM, again, three years ago, it was probably 30 billion.

### Jayshree Ullal, President and Chief Executive Officer
18. So, as they go through that deployment and as they look at AI and as we bring in the enterprise and Tier 2 clouds, we've got a nice mix of things.

### Sebastien Naji, William Blair and Company, Analyst
19. And maybe just longer term, do you think that generative AI could help improve that visibility from where it's historically been just given that many of these hyperscalers have what seems like decent visibility into a pretty robust pipeline over the next few years?

### Jayshree Ullal, President and Chief Executive Officer
20. However, on AI, it is greater since it's an early cycle and we have to do a lot more joint development.

### Aaron Rakers, Wells Fargo Securities, Analyst
21. When do we start to see the materializing deployments of 800 gig and maybe that's tied to AI, maybe it's not, but just curious of when that cycle you believe really starts to kick in?

### Anshul Sadana, Senior Vice President, Chief Operating Officer
22. 51T and 800 gig, especially, are being puller by AI clusters, the AI teams, are very anxious to get their hands on it, move the data as quickly as possible, and reduce the job completion times.

### David Vogt, UBS, Analyst
23. But trying to kind of walk the bridge to get from where we are today to '25 where you're going to start to see more widespread AI deployments from a revenue recognition perspective.

### George Notter, Jefferies, Analyst
24. I guess I wanted to ask about your comments about 2025 participation in AI.
25. And then also I assume that you participate today with inferencing applications and that's by and large done on Ethernet. ⚑ uncertain

### Jayshree Ullal, President and Chief Executive Officer
26. So, I think you can look at 2023 as really a year of planning for AI, because as I said, there's tons and tons of GPUs being purchased.
27. And the planning basically is, how do they get the GPUs, what is their application, what is the size of the cluster, what is the time, what is the large language model datasets, etc., and what is their network foundation.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] The customer mandated a fully automated workflow.
2. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] When there is a single binary EOS image across all campus platforms complete with the universal API and built-in automation features, the customer was set on a path to continued campus modernization.
3. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] Arista demonstrated that the customer could use a single sign for both land and when to dramatically simplify and automate the whole environment within 30 days.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] During the past couple of years, we have enjoyed significant increase in cloud capex to support our cloud titan customers for their ever-growing needs, tech refresh, and expanded offerings.
2. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] One specific cloud typing customer has signaled a slowdown in capex from previously elevated levels.
3. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] In the noncloud enterprise category, we continue to experience good momentum in both data center and campus.
4. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] The next enterprise win involves both data center and campus with advanced EVPN, L3 VPN over VXLAN routing architecture instead of the traditional Layer 2 extension.
5. [Prepared remarks · Jayshree Ullal, President and Chief Executive Officer] The final win was in a large public sector, connecting redundant data centers to hundreds of campus locations with a large routing environment.
6. [Prepared remarks · Ita Brennan, Chief Financial Officer] Capital expenditures for the quarter were 11.6 million.
7. [Q&A · Jayshree Ullal, President and Chief Executive Officer] So, obviously, InfiniBand with 10, 15 years of similarity in an HPC environment is often being bundled with the GPU.
8. [Q&A · Anshul Sadana, Senior Vice President, Chief Operating Officer] And in the future, we believe they'll be back to adding and refreshing the standard computer infrastructure as well.
9. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And the reality is it'll be difficult to repeat the last two years of exceptional cloud capex for cloud networking.
10. [Q&A · Jayshree Ullal, President and Chief Executive Officer] They haven't had a high-quality, high supportive, very, very friendly software experience, a common leaf spine architecture across their data center campus routing in a long, long time.
11. [Q&A · Jayshree Ullal, President and Chief Executive Officer] So, our hybrid strategy continues to dominate the enterprise decisions for the data center.
12. [Q&A · Erik Suppiger, JMP Securities, Analyst] We hear a lot about them buying volumes of GPUs right now.
13. [Q&A · Erik Suppiger, JMP Securities, Analyst] At what point do their purchasing of GPUs translate into their demand for switches?
14. [Q&A · Anshul Sadana, Senior Vice President, Chief Operating Officer] There is no uniform recipe, but in general, when they're buying GPUs [Technical difficulty] to connect.
15. [Q&A · Jayshree Ullal, President and Chief Executive Officer] But generally speaking, we're focusing on things that are much larger than 200 or even 1,000 GPUs.
16. [Q&A · Jayshree Ullal, President and Chief Executive Officer] In some cases, where they just need to go quick and fast as I explained before, it would not be uncommon to just bundle their GPUs with an existing technology like InfiniBand.
17. [Q&A · Jayshree Ullal, President and Chief Executive Officer] Now, we expect next year this will translate to some, what I call, pilots, because majority of them will happen in '25, but in '24, you'll start seeing, what do you say, Anshul, maybe 4,000 to 8,000 GPUs, something like that?
18. [Q&A · Jayshree Ullal, President and Chief Executive Officer] In that range, OK. 4,000 to 8,000 GPUs at about 400 gig type clusters.
19. [Q&A · Jayshree Ullal, President and Chief Executive Officer] But the real test of why you buy these expensive GPUs in 2025, when you want to have not just 4,000 to 8,000, but 30,000, 50,000, maybe even 100,000, and this is why 2025 is so critical.
20. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And taking -- testing and taking out all the kinks out of the GPUs and networks is important because your network is so -- a good network is so pivotal to getting the most out of your GPUs.
21. [Q&A · Jayshree Ullal, President and Chief Executive Officer] If you have idling cycles on those GPUs, you wasted thousands, if not millions, of dollars.
22. [Q&A · Jayshree Ullal, President and Chief Executive Officer] And so, I think these next two years are crucial to getting the most out of these expensive GPUs and that's where the network really comes in.
23. [Q&A · Anshul Sadana, Senior Vice President, Chief Operating Officer] That has nothing to do with GPUs or our switches, which is does the customer have enough power and the site ready to deploy that many megawatts or gigawatts of capacity.
24. [Q&A · Anshul Sadana, Senior Vice President, Chief Operating Officer] This does not certainly turn on the key and you have thousands of GPUs.
