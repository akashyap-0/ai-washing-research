# Datadog — 2023_Q4 Earnings Call (transcript)

- **Company:** Datadog (DDOG); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** DDOG
- **CIK:** 0001561550
- **Period:** 2023_Q4 (call held February 13, 2024; date from page date line)
- **Calendar quarter:** 2023 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/02/13/datadog-ddog-q4-2023-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** 18f53d78883882733ca8d24ca4457ae0ea8107199b12eff9e9a45573c5248793
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**37 AI sentences of 594 total**
(Borderline, listed at the end: 3 automation/robotics, 11 infrastructure, none containing an AI term.)

## Prepared remarks

### Olivier Pomel, Co-Founder and Chief Executive Officer
1. In observability, we now have more than 700 integrations, allowing our customers to benefit from the latest AWS, Azure, and GCP abilities as well as from the newly emerging AI stack.
2. We continue to see increasing engagement there with the use of our next-gen AI integrations growing 75% sequentially in Q4.
3. In the generative AI and LLM space, we continue to add capability to Bits AI, our natural language incident management copilot.
4. And we are advancing LLM observability to help customers investigate where they can safely deploy and manage their models in production.
5. Today, about 3% of our ARR comes from next-gen AI native customers, but we believe the opportunity is far larger in the future as customers of every industry and every size start deploying AI functionality in production.
6. We see AI adoption as an additional driver of investment and accelerator of technical innovation and cloud migration.

## Q&A

### Olivier Pomel, Co-Founder and Chief Executive Officer
1. On the other hand, they might be the first ones to fully leverage AI and deploy it in production.

### Mark Murphy, JPMorgan Chase and Company, Analyst
2. And just as a follow-up, if you think about the very long term, would you think attach rates of observability will end up being higher or lower for these AI workloads versus traditional workloads?
3. Because on the surface, with AI, it's bringing the risk of hallucinations and bias.
4. It's also more computationally intensive, and there's more value to unlock if the LLM runs reliably and creates that kind of great user experiences. ⚑ context-dependent

### Olivier Pomel, Co-Founder and Chief Executive Officer
5. AI just adds more complexity.

### Olivier Pomel, Co-Founder and Chief Executive Officer
6. AI is going to accelerate.

### David Obstler, Chief Financial Officer
7. We have -- if you look at our larger customers and you just look at the trend over time, you can see that in the land-and-expand model, we have had an increase of average customer size with us in the group over $100,000. ⚑ uncertain

### Fred Havemeyer, Macquarie Group, Analyst
8. There's been quite a lot of, at this point, let's say, testing development, but a lot of interesting development with like autonomous agents for DevOps-related tasks. ⚑ uncertain
9. So, I'm curious, as you're considering the opportunity and potentially some of the risks also around generative AI and perhaps like agentic usage of large language models, how are you thinking that Datadog is positioned strategically, both from a product and perhaps pricing perspective around this technology trend?

### Olivier Pomel, Co-Founder and Chief Executive Officer
10. But we -- so we've been actively building on our Bits AI assistant.
11. And we also see a lot of demand and expectations on the customer side for incorporating generative AI in the product.

### Fred Havemeyer, Macquarie Group, Analyst
12. But I think last quarter, we got an update on where GenAI-related operations were contributing to the business.
13. Would you have into Q4 any data or points you could share about how much generative AI use cases are contributing?

### Olivier Pomel, Co-Founder and Chief Executive Officer
14. Yes, we said -- so, we said 3% of our ARR comes from the AI-native companies.
15. And look, it's hard for us to wrap our arms exactly around what is GenAI, what is not among our customer base and their workload.
16. So, the way we chose to do it is we looked at a smaller number of companies that we know are substantially all based on AI, so these are companies like the modal providers and things like that.
17. I know one number that everyone has been thinking about is one cloud, in particular, Microsoft, disclosed that 6% of their growth was attributable to AI.
18. If I look at our Azure business in particular, there is substantially more than 6% that is attributable to AI native as part of our Azure business.

### Patrick Colville, Scotiabank, Analyst
19. I would like to actually double-click on this kind of ARR from AI-native companies.
20. I mean, my question is like are the product SKUs, these kind of GenAI companies are adopting, are they similar or are they different to the kind of other customer cohorts?
21. And then, I guess, when I think about GenAI, I think we can all agree that these are pretty -- typically pretty computerly intensive workloads.
22. So, how does GenAI -- how do these companies kind of impact the financial model in -- versus traditional kind of -- your other customer cohorts?

### Olivier Pomel, Co-Founder and Chief Executive Officer
23. It's worth noting that they're in a bit of a separate world because they're largely the builders of the models. ⚑ uncertain ⚑ context-dependent
24. So, all the tooling required to understand the models and -- that's less applicable to them. ⚑ uncertain
25. And we see also where we see the bulk of the opportunity in the longer term, not in the handful of model providers that everybody is going to use. ⚑ uncertain
26. In terms of the economics, look, we -- so there's two parts to the AI workloads today.
27. There's training and there's inference. ⚑ uncertain
28. There's only a few that are scaling with inference. ⚑ uncertain
29. The ones that are scaling with inference are the ones that are driving our ARR because we are -- we don't -- we're not really present on the training side, but we're very present on the inference side. ⚑ uncertain
30. And I think that also lines up with what you might see from some of the cloud providers, where a lot of the players or some of the players that are scaling the most are on Azure today on the inference side, whereas a lot of the other players still largely trading on some of the other clouds. ⚑ uncertain

### Olivier Pomel, Co-Founder and Chief Executive Officer
31. The beauty of our model is that it is usage-driven and we benefit from the move to the cloud of our customers and the way they care. ⚑ uncertain

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] In cloud service management, we made workflow automation generally available, enabling customers to easily automate and orchestrate processes across operations and security.
2. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] So, we -- it's become more pronounced starting last year, I think, because companies put -- wanted to see some cost control, and maybe they automated some processes to downscale or shut things down at the end of the year.
3. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] There's a number of ways for us to build on that and to do more to automate work for our customers, and that's something we're working on.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] Note, for example, that the ARR for products outside of infrastructure monitoring, APM suite, and log management grew by more than 75% year over year.
2. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] We announced cloud infrastructure entitlement management to have customers prevent identity and access management security issues.
3. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] We launched our latest data center in Japan to have customers comply with local data privacy laws.
4. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] With this renewal, this customer expects to use 15 Datadog products, and we'll consolidate what used to be 10 separate tools, including the replacement of three commercial products across infrastructure monitoring, APM, and RUM.
5. [Prepared remarks · David Obstler, Chief Financial Officer] And after taking into consideration capital expenditures and capitalized software, free cash flow was $201 million with a free cash flow margin of 34%.
6. [Prepared remarks · David Obstler, Chief Financial Officer] Finally, we expect capital expenditures and capitalized software together to be in the 3% to 4% of revenue range in fiscal year 2024.
7. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] For example, we package some of our security products directly into our infrastructure and APM products.
8. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] We have a new tier called DevSecOps for both APM and infrastructure, and these are great ways for us to actually bring those products into the conversation, make them easier for customer to discover and also make them easier for the sales force to bring up and to sell.
9. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] For infrastructure security and application security, this tends to be the DevOps teams that start buying with some involvement on the security teams on their end.
10. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] In most situations, we start side by side with other things because customers are going to have other security solutions, and they typically have a patchwork of a lot of different things, which is not very different from the situation when we started selling our infrastructure and APM products, I would say, seven, eight, 10 years ago.
11. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] These are infrastructure, APM logs, profiling these kind of things that they are -- or really the monitoring, these kind of things that these customers are using.
