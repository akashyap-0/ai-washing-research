# Broadcom — FY23_Q1 Earnings Call (transcript)

- **Company:** Broadcom (AVGO); fiscal year ends October (SEC fiscalYearEnd 1101)
- **Ticker:** AVGO
- **CIK:** 0001730168
- **Period:** FY23_Q1 (call held March 2, 2023; date from page date line)
- **Calendar quarter:** 2022 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/03/02/broadcom-avgo-q1-2023-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** 565ce5024d6842937e72846470505dc33991368e8d17e01ff874af767e2ac36d
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**43 AI sentences of 425 total**
(Borderline, listed at the end: 0 automation/robotics, 29 infrastructure, none containing an AI term.)

## Prepared remarks

### Hock Tan, President and Chief Executive Officer
1. Keep in mind that at hyperscalers, a growing portion of our switches have been deployed within the AI networks, which are separate from the traditional x86 CPU scale outrunning existing workloads.
2. Tomorrow, we generated AI using large-scale -- large language, I should say, models with billions of parameters.
3. We have to run thousands of AI engines in tower enabling large and synchronized bus of data at speeds of 400 and 800 gig.
4. So, as you know, such AI networks are already being deployed at certain hyperscalers through our Jericho 2 switches and Ramon Fabric.
5. In fact, in 2022, we estimated our Ethernet switch shipments deployed in AI was over $200 million.
6. We have been investing in a new generation of this lossless low-latency Ethernet fabric designed specifically to handle such data and compute-intensive AI workloads.
7. Of course, additionally, the exciting growth prospects for generative AI are driving our compute offload accelerated business at hyperscalers.

## Q&A

### Harsh Kumar, Piper Sandler, Analyst
1. Hock, you mentioned generative models in your commentary.
2. I wanted to understand the difference between what you're doing in AI so far versus maybe what our understanding of generative is.
3. You talked about $200 million in Ethernet related to AI.
4. Is that largely generated because we've heard other companies say that for large part, the generated models are using it for the bank? ⚑ uncertain
5. Maybe help us think about how we think of Avago's place or Broadcom's place in the generative process.

### Hock Tan, President and Chief Executive Officer
6. In 2022, generative is just barely starting to kick off.
7. But they exist AI networks within the hyperscalers, particularly in fairly significant volume.
8. As we step up to large language models in AI, generative AI, in particular, coming into play.
9. All AI engines together, whether they're GPUs, AI, or TPUs, or other AI engines.
10. The network becomes now potentially a critical part of this whole AI phenomenon in hardware.
11. To make it work, you've got to put together many regs of AI engines in parallel, very similar to what we have been doing -- hyperscalers have been doing on CPUs to make them run faster, high performance as Moore's Law comes to an end and doesn't make any difference here in the form of AI engine.
12. So, network becomes a problem, and becomes the constrained network becomes a very key part of fulfilling generative Adrean.
13. And what we are saying -- what I'm saying in my comments is, last year, 2022, in this -- and these are more what you call the AI workloads that are running in hyperscale, and the advent of generative AI is still relatively fresh and new.
14. We're doing $200 million as far as we could estimate of silicon, Ethernet switches, and fabric that goes into those AI networks as far as we could identify in hyperscalers.
15. With generative AI and the urgency and excitement of it coming in that we are seeing today.

### Harlan Sur, JPMorgan Chase and Company, Analyst
16. Hock, as your cloud customers are now aggressively focused on generative AI development and deployment across their data center footprint, right?
17. This is driving strong AI-focused ethernet switch port demand and demand for our compute offload as like TPU for this year, as you mentioned. ⚑ context-dependent
18. But from a new product ramp and design win funnel perspective, is this also causing your cloud customers to want to pull forward some of your future programs like Tomahawk 5 or Jericho 3 next-gen switching and routing products and/or pulling the design and tape out of their next-generation compute offload AI ASIC programs?

### Hock Tan, President and Chief Executive Officer
19. Yes, which is accounting for the color in my commentary about both net -- generative AI-based network and pushing us to develop a new generation altogether of Ethernet switching that can support this kind of very compute and data-intensive workloads.

### Stacy Rasgon, AllianceBernstein, Analyst
20. I just wanted to verify, Hock, did you say that you started hearing urgency from your hyperscale customers around the AI in the last 90 days?
21. I guess given the lead times, is that more of a second-half kind of thing when that contributes to the model? ⚑ uncertain

### Hock Tan, President and Chief Executive Officer
22. But having said that, no, we're still working through timing of when our customers need those urgent -- those products in a fairly urgent manner and our ability to obviously want to be very, very helpful to help customers launch aggressively into generative AI.

### Vijay Rakesh, Mizuho Securities, Analyst
23. Hey, Hock, just a quick question on -- you talked about generative AI.
24. Just wondering, as you look at the workload, what percent of workload would be on generative AI, like exiting calendar '23 or '24?

### Hock Tan, President and Chief Executive Officer
25. OK. Well, it's -- I'm sure I don't need to elaborate on what we all hear about on generative AI.
26. And I think it's still early innings on generative AI.
27. And with generative AI, as I said, with many more -- much more billions of parameters that come into the models that they're doing.
28. You're talking about scale out of data centers driving AI engines network together in a manner that we probably have not seen before.
29. As evidenced by the fact that we have and deploy technology to support AI networks even today to certain hyperscalers, where we're talking about at least hundreds and on thousands of AI engines, AI service network together and working in a synchronous manner.
30. And I emphasize the word system performance of an AI data center.

### Pierre Ferragu, New Street Advisors, Analyst
31. So, if I look at your networking division, if you grow like at least $600 million this year in AI and if you have computer flood division growth by the billion, that might well represent all your growth in networking.
32. So, that would mean the only thing that is really growing and that we bring a lot this year in that space is AI.
33. So, my question at the end of the day is, is it fair to say that in these large data centers this year on the AI is growing?

### Hock Tan, President and Chief Executive Officer
34. I don't even sell them GPUs, by the way, but I know what you know out there, which is in certain areas of their business, we're seeing some of these hyperscalers bringing on a sense of urgency and focus and, of course, spending to be up to speed and to not be left behind as we see the excitement hype perhaps in pushing applications and workloads in generative AI.

### Pierre Ferragu, New Street Advisors, Analyst
35. And just to clarify specifically on what you are doing, is that fair to assume that the majority -- a very large majority of your growth this year in networking is going to come from AI, which you have $600 million coming from AIs and $1 billion coming from flesh.

### Hock Tan, President and Chief Executive Officer
36. Don't forget, generally AI is still early stage.

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Hock Tan, President and Chief Executive Officer] While as we expected, infrastructure software declined 1% year on year to $1.8 billion, even as our core software sustained growth of 5% year on year.
2. [Prepared remarks · Hock Tan, President and Chief Executive Officer] From our view, infrastructure spending continues to be up particularly in service providers, even as hyperscale and enterprise sustain.
3. [Prepared remarks · Hock Tan, President and Chief Executive Officer] Spending in technology for infrastructure has been strong, showing double-digit growth for nine consecutive quarters.
4. [Prepared remarks · Hock Tan, President and Chief Executive Officer] Moving on next to our server storage connectivity revenue.
5. [Prepared remarks · Hock Tan, President and Chief Executive Officer] After four consecutive quarters of such increases, this transition, however, is significantly complete, and we expect that in Q2 on a year-on-year basis, server storage connectivity revenue will moderate toward 20% year-on-year growth.
6. [Prepared remarks · Hock Tan, President and Chief Executive Officer] In Q1, infrastructure software revenue of $1.8 billion declined 1% year on year and represented 20% of total revenue.
7. [Prepared remarks · Hock Tan, President and Chief Executive Officer] In Q2, we expect our infrastructure software segment revenue to be up low to mid-single-digit percentage year on year as the stable core software growth continues to be partially offset now by weakness in Brocade.
8. [Prepared remarks · Kirsten Spears, Chief Financial Officer] Moving to the P&L for our Infrastructure Software reportable segment.
9. [Prepared remarks · Kirsten Spears, Chief Financial Officer] Revenue for infrastructure software was $1.8 billion, down 1% year on year and represented 20% of revenue.
10. [Prepared remarks · Kirsten Spears, Chief Financial Officer] Gross margins for infrastructure software were 91% in the quarter and operating expenses were $346 million in the quarter, down 1% year over year.
11. [Prepared remarks · Kirsten Spears, Chief Financial Officer] Infrastructure Software operating margin was 72% in Q1, and operating profit was stable year on year.
12. [Prepared remarks · Kirsten Spears, Chief Financial Officer] We spent $103 million on capital expenditures.
13. [Q&A · Harsh Kumar, Piper Sandler, Analyst] And then you talked about $2 billion in compute offload going to sort of $3 billion.
14. [Q&A · Hock Tan, President and Chief Executive Officer] And one we're trying to say is very similar to CPUs, traditional CPUs in traditional workloads in those same data centers.
15. [Q&A · Hock Tan, President and Chief Executive Officer] We've constrained on performance of those silicon CPUs and Moore's Law, we're starting to see scale-out buying positioning rows and rows of server CPUs and networking them together to work closely in parallel.
16. [Q&A · Hock Tan, President and Chief Executive Officer] GPUs are starting to be strung together in hundreds, soon to be thousands of racks, and working in parallel.
17. [Q&A · Hock Tan, President and Chief Executive Officer] And basically, those GPUs work in parallel in fairly synchronous manner to basically run and do what we call bulk parametric exchange.
18. [Q&A · Hock Tan, President and Chief Executive Officer] Basically, run GPUs together.
19. [Q&A · Hock Tan, President and Chief Executive Officer] We have typically not want to talk much about compute offload, which is another way of saying, yes, these are very related to some of the engines that certain -- that are fairly customized dedicated to certain hyperscalers.
20. [Q&A · Hock Tan, President and Chief Executive Officer] So, that's -- we are in early innings, which is why we think we have time to come -- to start to work on even a new generation of switches in Ethernet that are specifically designed dedicated to this kind of workloads, which are very different from the normal workloads that we see today traditionally in data centers.
21. [Q&A · Ross Seymore, Deutsche Bank, Analyst] I wanted to go into the compute offload number that you talked about, Hacksta $2 billion last fiscal year going to $3 billion this year.
22. [Q&A · Ross Seymore, Deutsche Bank, Analyst] But generally speaking, can you just talk about the breadth and types of compute offload and how that's changing in the mix from the $2 billion last year to $3 billion this year?
23. [Q&A · Hock Tan, President and Chief Executive Officer] But as I said, it includes some of the engines, the compute engines and some are related components that support this engine.
24. [Q&A · Pierre Ferragu, New Street Advisors, Analyst] And when I look at outside of Bocom, what we've seen is memory and ACP servers are having a very difficult time at the moment, we expect a recovery in the second half, while the GPU segment of the market is actually in very, very good saving growing very well and accelerating again.
25. [Q&A · Pierre Ferragu, New Street Advisors, Analyst] Or do you think the general-purpose parts infrastructure like centered around x86 or similar or general purpose CPUs still is a very good growth market?
26. [Q&A · Hock Tan, President and Chief Executive Officer] But right now, last quarter, this quarter, yes, traditional data centers scale-out in networking and deployment in networking continues to be strong and sustained in hyperscalers as well, I might indicate in the enterprise.
27. [Q&A · Karl Ackerman, Exane BNP Paribas, Analyst] You obviously have more weighting toward fiber and sell into the infrastructure portion.
28. [Q&A · Karl Ackerman, Exane BNP Paribas, Analyst] And so, I was hoping you could discuss how you're thinking about the growth of your fiber business within broadband both from an infrastructure side and a consumer equipment standpoint as governments begin to deploy funds for broadband infrastructure.
29. [Q&A · Hock Tan, President and Chief Executive Officer] And content increases come to not just unit deployment of those gateways and infrastructure, but also the fact that a lot of these deployments come with very high attach rates of WiFi 6 and 6E.
