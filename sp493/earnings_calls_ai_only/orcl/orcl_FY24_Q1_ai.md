# Oracle Corporation — FY24_Q1 Earnings Call (transcript)

- **Company:** Oracle Corporation (ORCL); fiscal year ends May (SEC fiscalYearEnd 0531)
- **Ticker:** ORCL
- **CIK:** 0001341439
- **Period:** FY24_Q1 (call held September 11, 2023; date from page date line)
- **Calendar quarter:** 2023 Q3 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/09/11/oracle-orcl-q1-2024-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-29 (S&P 493 pull, half 1)
- **Source SHA-256:** 9c74fe1a19a002bdabdd18dfdf376042b442f3ba6215051f8ea8030d0dadd51a
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**34 AI sentences of 301 total**
(Borderline, listed at the end: 11 automation/robotics, 13 infrastructure, none containing an AI term.)

Source/parse flags: 301 units, outside the typical 400-900.

## Prepared remarks

### Safra Catz, Chief Executive Officer
1. Next week, we have Oracle CloudWorld, which will showcase the latest innovations including AI on OCI, the progress of Oracle Autonomous Database, our multi-cloud strategy, the use of Oracle Analytics throughout our portfolio to drive better decision-making, and the use of generative AI to differentiate Fusion, NetSuite, and our Industry application.
2. Total cloud services and license support revenue for the quarter was 9.5 billion, up 12% driven again by our strategic cloud applications, Autonomous Database, and our Gen 2 OCI. ⚑ uncertain
3. OCI consumption revenue was up 91%, Exadata cloud services revenue was up 46% and Autonomous Database was up 42%. ⚑ uncertain

### Larry Ellison, Chairman and Chief Technology Officer
4. So, is generative AI the most important new computer technology ever?
5. Self-driving cars, computer-designed antiviral drugs, voice user interfaces -- generative AI is changing the automobile industry, the pharmaceutical industry, how people communicate with their computers.
6. Generative AI is changing everything.
7. As of today, AI development companies have signed contracts to purchase more than $4 billion of AI training capacity in Oracle's Generation 2 Cloud.
8. That's twice as much AI training as we had booked at the end of the last Q4. ⚑ context-dependent
9. I'm also very pleased to announce that XAI has signed a contract to do training in Oracle's Gen 2 Cloud.
10. The largest -- the largest AI technology companies and the leading AI start-ups continue to expand their business with Oracle for one simple reason: Oracle's RDMA-interconnected Nvidia superclusters train AI models at twice the speed and much less than half the cost of other clouds.
11. But growth in our AI cloud infrastructure business is not the only exciting news we have to report at Oracle.

## Q&A

### Brad Zelnick, Deutsche Bank, Analyst
1. And I recently heard someone say we're moving from a world of data gravity to one of AI gravity.
2. But with AI and other use cases attracting more and more data to central clouds, with many vendors preaching data sharing instead of what used to be making multiple copies of things and keeping them synchronized, does AI plus cloud in any way break what we've always understood about data gravity?

### Larry Ellison, Chairman and Chief Technology Officer
3. Well, you know, you can't build any of these AI models without enormous amounts of training data.
4. So, if anything, what -- what AI -- generative AI has shown that the big issue about training one of these models is just getting -- that this vast amount of data ingested into your GPU supercluster, it is a huge data problem in a sense you need so much data to, you know, train OpenAI, to train ChatGPT 3.5.
5. And to specialize -- then you take something like ChatGPT 4.0 and you want to specialize it, you need specialized training data from electronic health records.
6. And we have partners imaging, for example, that is ingesting huge amounts of image data to train their AI models.
7. We have Ronin, another partner of ours in AI, ingesting huge amounts of electronic health records to train their models.
8. AI doesn't work without getting access to and ingesting enormous amounts of data.
9. So, in terms of a shift away from data or a change in gravity to AI, AI is utterly dependent upon vast amounts of training data.
10. Trillions of elements went into building ChatGPT 3.5, multiple times that for ChatGPT 4.0 because you had to deal with all the image data and ingest all of that to train -- to train image recognition.
11. And Oracle's new vector database will contain highly specialized training data like electronic health records while keeping that data anonymized and private yet still training the specialized models that can -- that can help doctors improve their diagnostic capability and their treatment prescriptions for cancer and heart disease and all sorts of other diseases.

### Larry Ellison, Chairman and Chief Technology Officer
12. So, the non-blocking ultra-fast RDMA network is not only useful for AI -- training AI models; it's useful for almost everything.

### Mark Moerdler, AllianceBernstein, Analyst
13. The top-of-mind questions I'm getting are related to AI in general, as you'd expect, and more specifically as it relates to Oracle, what the impact of AI will be on OCI Gen 2.
14. The first is the profitability of AI supercomputers and whether, as some clients try to tell me, it's low-calorie, empty-calorie revenue, or can you maintain margins as this business grows?
15. And is it strong enough that this workloads transition from model training to inferencing and grounding, could AI compute create a revenue air pocket?

### Larry Ellison, Chairman and Chief Technology Officer
16. Well, if you're -- you're constantly training these models.
17. And for your AI models to be relevant, they have to be up to date.
18. So, it's not that you train and then do nothing but inferencing thereafter. ⚑ uncertain
19. So, your training and your inferencing sit right next to each other. ⚑ uncertain
20. As long as we can do this stuff twice as fast as everybody else, that's on the -- by the way, not just on the training side, that's also on the inferencing side, then we're going to be half the cost or better. ⚑ uncertain
21. So, we think we're going to be very very competitive across the board, whether it's training or in inferencing. ⚑ uncertain
22. And it applies to inferencing as well as -- as well as training. ⚑ uncertain

### Larry Ellison, Chairman and Chief Technology Officer
23. The new Cerner system is being generated -- as you know, generative AI generates code.

## Borderline: automation/robotics without an AI term

1. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] It's useful for -- in terms of the automation level we have in our data centers.
2. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] Our data centers are 100% automated.
3. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] Our data centers are -- because they're all -- they're identical, the only way we could automate them was to make them all the same.
4. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] They all have the same automation, and that automation allows us to put these data centers in very small countries.
5. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] And again, it's because of the extreme reliability and security that we get with all of the automation that's included, you know, with our data center.
6. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] And we have an important partnership with JPMorgan Chase, where one -- and -- and we'll be announcing some more partnerships in the financial community at the upcoming CloudWorld where we automate a lot of e-commerce, B2B, e-commerce, right in the cloud.
7. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] We automate that entirely in the cloud.
8. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] No one -- we've done a great job as an industry automating e-commerce for B2C.
9. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] In the cloud, you can get all the parties together, the shippers, the insurance company, the manufacturers, the purchasers, and we can automate that entirely within the Oracle Cloud; one ERP system talking to another, talking to their bank, talking to their insurance, doing a loan origination, getting the -- getting -- getting it shipped and insured.
10. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] Now, as far as GPUs, is that our GPUs are a low-margin business, not for -- 100% automated cloud with very very low costs.
11. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] One of the things we're doing -- we did with our data centers is we automated them.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Safra Catz, Chief Executive Officer] Infrastructure subscription revenues, which includes license support, were 5.1 billion, up 14%.
2. [Prepared remarks · Safra Catz, Chief Executive Officer] Infrastructure Cloud Services revenue was up 64%.
3. [Prepared remarks · Safra Catz, Chief Executive Officer] Excluding legacy hosting services, Gen 2 Infrastructure Cloud Services revenue grew 72% with an annualized revenue of 5.6 billion.
4. [Prepared remarks · Safra Catz, Chief Executive Officer] And while we've continued to build data center capacity, we've also seen our IaaS margins go higher as these new cloud regions fill up.
5. [Prepared remarks · Safra Catz, Chief Executive Officer] Capital expenditures were 8.3 billion over the last four quarters, and we're clearly beginning to see the cash flow benefits stemming from our cloud transformation.
6. [Prepared remarks · Safra Catz, Chief Executive Officer] Capex was 1.3 billion in Q1 as we continue to build capacity for bookings and our customers' growing needs.
7. [Prepared remarks · Safra Catz, Chief Executive Officer] Given the demand we have and see in the pipeline, I expect the fiscal year 2024 capex will be similar to this past year's capex.
8. [Prepared remarks · Safra Catz, Chief Executive Officer] Because we have far more demand than we can supply, our biggest challenge is building data centers as quickly as possible.
9. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] Well, again, our -- you know, we have -- we're on our second generation of data center and -- and our second generation of cloud.
10. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] We don't have that in our data center.
11. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] We expect to have many many more data centers than any other cloud provider, but we also put those data centers --- customers.
12. [Q&A · Larry Ellison, Chairman and Chief Technology Officer] We think, in some cases, our prices for GPU training, which are very profitable, by the way, for us but are often lower -- you know, our prices are lower than the costs of other hyperscalers doing the training.
13. [Q&A · Safra Catz, Chief Executive Officer] All of it is dependent on us getting our data centers filled up and built out as fast as possible.
