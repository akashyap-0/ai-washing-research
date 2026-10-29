# Datadog — 2023_Q3 Earnings Call (transcript)

- **Company:** Datadog (DDOG); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** DDOG
- **CIK:** 0001561550
- **Period:** 2023_Q3 (call held November 7, 2023; date from page date line)
- **Calendar quarter:** 2023 Q3 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/11/07/datadog-ddog-q3-2023-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** d0f7a1df8659d31d1ca7ed6b90cf4fce74f231d42ce1cfd4d783b4e0809b161e
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**38 AI sentences of 517 total**
(Borderline, listed at the end: 0 automation/robotics, 15 infrastructure, none containing an AI term.)

## Prepared remarks

### Olivier Pomel, Co-Founder and Chief Executive Officer
1. With our land-and-expand model, we expect new logos to turn into much larger customers over time as they lean into the cloud and add up more of our products. ⚑ uncertain
2. Today, our infrastructure products cover monitoring the performance of hosts, networks, containers, Kubernetes deployment, serverless functions, and other aspects of infrastructure in the cloud, as well as a full set of AI and machine learning tools to help our customers separate signal from noise.
3. With a simple per-host price and a single agent deployed, customers get end-to-end visibility into performance, availability, and security issues in one place. ⚑ uncertain
4. Customers can instrument cloud applications for both performance and vulnerability issues in one single package, enabled with the same unified agent used for infrastructure DevSecOps. ⚑ uncertain
5. Finally, we continue to be excited about the opportunity in generative AI and large language models.
6. First, we believe adopting next-gen AI will require the use of cloud and other modern technologies and drive additional growth in cloud workloads.
7. So, we are continuing to invest by integrating with more components at every layer of the new AI stack and by developing our own LLM observability products.
8. And while we see signs of AI adoption across large parts of our customer base, in the near term, we continue to see AI-related usage manifests itself most accurately with next-gen AI-native customers, who contributed about 2.5% of our ARR this quarter.
9. In the mid to long term, we expect customers of all industries and sizes to keep adding value to their products using AI and to get their early exploration -- to get from early exploration to development and into production, thus driving larger cloud and observability usage across our customer base.
10. Besides observing the AI stack, we also expect to keep adding value to our own platform using AI.
11. Datadog's unified platform and purely SaaS model, combined with strong multiproduct adoption by our customers, generates a large amount of deep and precise observability data. ⚑ uncertain
12. We believe combining AI capabilities with this broad dataset will allow us to deliver differentiated value to customers.
13. And we are working to productize this differentiated value through recently announced capabilities such as our Bits AI assistant, AI-generated synthetic test, and AI-led error analysis and resolution.

## Q&A

### Mark Murphy, JPMorgan Chase and Company, Analyst
1. Olivier, I'm interested in your mention of 2.5% of ARR being driven by the native AI providers.
2. Should we think of that mostly consisting of OpenAI, Llama, Anthropic, Cohere, etc., or are you meaning that as a slightly different reference?

### Olivier Pomel, Co-Founder and Chief Executive Officer
3. So, it's a number of companies that -- without naming anyone, so they tend to be model providers, but not just in -- on the language side, like model providers on the language, image side, like there's a number of different -- or video side. ⚑ uncertain
4. There's a lot of different types of companies there, even some "copilot-type" companies.
5. And the reason we included that in the script is we -- today, we see the usage growth related directly to AI coming mostly from these customers that provide models to others.
6. Whereas we see broad usage of AI functionality across the customer base but at lower volumes, and it corresponds to the fact that for most customers or most enterprises, really, they're still in the early stages of developing and shipping AI applications.
7. So, for now, the usage is concentrated among the model providers. ⚑ uncertain

### Olivier Pomel, Co-Founder and Chief Executive Officer
8. One interesting tidbit if you -- as I know many of you are trying to understand what the AI landscape is made of.
9. Interestingly enough, the -- when we look at our cohort of customers that are -- that we consider to be AI-native and built largely on the AI and AI providers, they tend to be on different clouds.

### Sanjit Singh, Morgan Stanley, Analyst
10. Olivier, the company's been innovating throughout this downturn quite aggressively across core observability, security, as well as AI.

### Kash Rangan, Goldman Sachs, Analyst
11. One is with respect to LLM monitoring, which was demoed at the DASH conference, which was, I thought, absolutely fascinating.
12. I know you quantified, Oli, 2.5 percentage points of growth coming from generative AI workloads.
13. How do we think about the revenue opportunity for LLM monitoring that it's at an early stage?

### Olivier Pomel, Co-Founder and Chief Executive Officer
14. On the LLM upside, I think it's too early to tell how much the revenue opportunity there is in the tooling specific to the LLM ops.
15. What we know, though, is that the broader generative AI up and down the stack from the components themselves, the GPUs, all the way up to the models and the various things that are used to orchestrate them and store the data and move the data around, all of that is going to generate a lot of opportunity for us.
16. We said, right now, it's concentrated among the AI-native, largely model providers, but we see that it's going to broaden and concern a lot more of our customers down the road.

### Alex Zukin, Wolfe Research, Analyst
17. OK. And then maybe on the -- back on the AI question.
18. I guess maybe just can you drill a little bit deeper, within those AI-native companies, the criticality of their data [Inaudible] usage, meaning are you seeing something different where in a world where these applications become more prevalent, there's the opportunity to kind of expand wallet share as observability becomes even more important?

### Olivier Pomel, Co-Founder and Chief Executive Officer
19. On the other hand, if thanks to all the major advances of technology and all of the various open source and AI and, you know, you can just very quickly generate thousands of lines of code, ship them, and start operating them, you actually have no idea how these work, what they do, and you'll need a lot of tooling in observability to actually understand that and keep track of that and secure it and do everything you need to do with it over time.
20. In terms of the future growth of AI, look, I think like everyone, we're trying to guess how transformative it's going to be.
21. So, I -- again, today, we only see a tiny, tiny bit of it, which is early adoption by model providers and a lot of companies that are trying to scale up and experiment and figure out how it applies to their businesses and see what they can ship to use the technology. ⚑ uncertain

### Jake Roberge, William Blair and Company, Analyst
22. Olivier, you called out the 2.5 points from AI-native customers a few times, but you've also said that the broader customer base should start adding AI workloads to your platform over time.
23. When do you think that actually takes place when the broader customer base starts to impact that AI growth in more earnest?

### Olivier Pomel, Co-Founder and Chief Executive Officer
24. And -- but the other part is also that, right now, the innovation is largely concentrated among the model providers. ⚑ uncertain
25. We see a lot of demand and interest in other ways to host models and run models and custom models and things like that. ⚑ uncertain

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] First, our infrastructure monitoring ARR exceeded $1 billion.
2. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] And with Flex Logs, customers can easily scale storage and compute separately, allowing for new very high-volume logging use cases in a cost-effective manner.
3. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] And within our cloud security management product, we have introduced Cloud Infrastructure Entitlement Management, or CIEM, to help customers prevent identity and access management security issues.
4. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] First, with infrastructure DevSecOps, our customers can observe and secure their entire cloud environment in one package.
5. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] APM DevSecOps complements infrastructure DevSecOps by surfacing open-source and code-level security vulnerabilities alongside performance issues.
6. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] With this expansion, Datadog will bring all aspects of this customer's tech systems into one platform, including their applications, hybrid cloud, networks, installed IoT technology, point-of-sale systems, self-serve kiosks, fuel pumps, and corporate infrastructure.
7. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] This longtime customer has used Datadog for infrastructure metrics and will now expand to adopt seven Datadog products.
8. [Prepared remarks · David Obstler, Chief Financial Officer] After taking into consideration capital expenditures and capitalized software, free cash flow was $138 million for a free cash flow margin of 25%.
9. [Prepared remarks · David Obstler, Chief Financial Officer] And finally, we expect capital expenditures and capitalized software together to be in the 3% to 4% of revenue range in fiscal 2023.
10. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] You know, we mentioned a billion in infrastructure, half a billion in APM, half a billion in logs.
11. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] By far, the biggest area they can save in their cloud infrastructure is their cloud bill itself.
12. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] You know, we charge commensurate to the size of our customer's infrastructure.
13. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] You know, the -- when you look -- when you think of the whole spectrum of tools, the closer you get to the developer side, the harder it is to monetize, and the further you get toward operations and infrastructure, the easier it is to monetize.
14. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] And, you know, we -- again, we charge them an order of magnitude less than what they spend for their cloud infrastructure, maybe two orders of magnitude less than what they spend on their R&D.
15. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] And so, it's rational right now for most customers to rely on those instead of deploying their own infrastructure.
