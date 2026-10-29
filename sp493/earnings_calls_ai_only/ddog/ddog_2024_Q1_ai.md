# Datadog — 2024_Q1 Earnings Call (transcript)

- **Company:** Datadog (DDOG); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** DDOG
- **CIK:** 0001561550
- **Period:** 2024_Q1 (call held May 7, 2024; date from page date line)
- **Calendar quarter:** 2024 Q1 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/05/07/datadog-ddog-q1-2024-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** d516854ffe3547f23990f24b420fabea6c484c4096a9657e43183b88d3c13fe5
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**32 AI sentences of 556 total**
(Borderline, listed at the end: 2 automation/robotics, 12 infrastructure, none containing an AI term.)

## Prepared remarks

### Olivier Pomel, Co-Founder and Chief Executive Officer
1. We also kept supporting our customers' adoption of new technologies including next-gen AI and large language models.
2. In the next-gen AI space, we announced general availability of Bits AI for incident management.
3. By using Bits AI for incident management, incident responders get auto-generated incident summaries to quickly understand the context and scope of a complex incident.
4. End users can also query Bits AI to ask about related incidents and perform tasks on the fly from incident creation to resolution.
5. We are also continuing to see more interest in AI for our customers.
6. To have customers understand AI technologies and bring them into production applications, our AI integrations allow customers to pull their AI data into the Datadog platform.
7. And today, about 2,000 of our customers are using one or more of these AI integrations.
8. And we've continued to keep up with the rapid innovation in this space, for example, adding a new integration in Q1 with the NVIDIA Triton Inference Server. ⚑ uncertain
9. And by combining Event Management with Watchdog, Bits AI, and Workflow Automation, Datadog now provides a full AIOps solution that helps teams automate remediation, proactively prevent outages, and reduce the impact of incidents.
10. Meanwhile, we are seeing continued experimentation with new technologies, including a growing adoption of AI, which we believe will be an accelerator of technical innovation and cloud migration over time.

## Q&A

### Sanjit Singh, Morgan Stanley, Analyst
1. But when we think about the tailwinds of, like, cloud migrations, and also AI workloads starting to -- to come on board, how does that -- how is that playing out in Datadog's business, versus what we may be seeing from, like, the hyperscalers who seem to be accelerating to a higher degree?

### Olivier Pomel, Co-Founder and Chief Executive Officer
2. We're also very exposed to the same tailwinds of obviously cloud migration but also AI adoption.
3. And we'll say also on AI adoption that some of the revenue jumps you might see from the cloud providers might relate to supply of GPUs coming online and a lot of training clusters being provisioned.
4. We tend to be more correlated with the live applications, products, and applications and inference workloads that tend to follow after that and that are more tied to all of these applications going into production.

### Mark Murphy, JPMorgan Chase and Company, Analyst
5. Olivier, I'm wondering how commonly are customers in your gen AI cohort using Datadog to monitor for bias and hallucinations within their AI models as opposed to just keeping the systems running.
6. And also, do you see more concentration of customers within that cohort, or is there actually more diversity as more of the models move beyond the training stage and into the inferencing stage? ⚑ uncertain

### Olivier Pomel, Co-Founder and Chief Executive Officer
7. The -- the customers we have that are the most scaled on AI workloads are the model providers themselves, and they tend to have their own infrastructure for monitoring the quality of the models.
8. But we think they're a good bellwether in terms of what the adoption of AI is going to be from all the other companies.
9. And we definitely see a trend where customers start with their API-driven or API-accessible model build applications and then offload some of that application to other models that typically come from the open source and they might -- they might train, fine-tune themselves to get to a lower cost and lower time to respond. ⚑ uncertain

### Olivier Pomel, Co-Founder and Chief Executive Officer
10. And there's a -- there's a model that is associated with that. ⚑ uncertain

### Jake Roberge, William Blair and Company, Analyst
11. Hey, thanks for taking the questions, and great to hear that AI-native customers represented 3.5% of ARR.
12. I'm curious, though, what you're seeing on the demand front for your own AI products like AIOps and cloud service management.
13. And then, you mentioned that the model providers have built their own tools to monitor the training of their models.
14. As you start to roll out your own LLM oservability solutions, do you see that trend changing?

### Olivier Pomel, Co-Founder and Chief Executive Officer
15. So, I think everything's possible in the long run, but our focus is really on the -- the -- the vast majority of the customer base that's going to either use those API-based products or tune and run their own models. ⚑ uncertain

### Koji Ikeda, Bank of America Merrill Lynch, Analyst
16. I wanted to ask a question on AI.

### Olivier Pomel, Co-Founder and Chief Executive Officer
17. You know, I mean it was interesting for us to look at this small group of early native companies to get a sense of what might come next in the world of AI.
18. But I think as we -- as -- as we -- as time goes by and as AI adoption broadens, I think it becomes less and less relevant.
19. But the one thing I will say is we -- we try to compare our exposure to AI to what we see from the hyperscalers because they are upstream from us, you know, in that respect.
20. The hyperscaler that is the most open about it is -- or transparent in terms of numbers is Microsoft as they disclose how much of their growth comes from AI, you know, more specifically.
21. And the AI-driven part of our Azure business itself is also growing faster than what you see on the -- on the overall Azure numbers.

### Peter Weed, AllianceBernstein, Analyst
22. But, you know, as you look at that, do you see that as kind of a reflection of momentum in kind of the larger enterprise or rebound and kind of the digital native venture-backed community, you know, perhaps from that born in AI?

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] Event Management addresses this challenge by automatically reducing a massive volume of events and alerts into actionable insights.
2. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] These are then used to generate tickets, call an incident, or trigger an automated remediation.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] We continue to see robust growth in our three pillars of observability: infrastructure monitoring, APM, and log management, but we also have many younger products that are becoming more meaningful contributors to our business over time.
2. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] For example, our products outside of infrastructure monitoring, APM suite, and log management exceeded 200 million in ARR in Q1.
3. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] As a reminder, Flex Logs allow customers to easily scale storage and compute separately, which, in turn, allows for new very high-volume use cases in a cost-effective manner.
4. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] This customer was primarily using our infrastructure monitoring and APM suite, but its legacy logging solution was becoming cost-prohibitive while a lack of correlation across siloed teams was causing frustration and higher time to resolution.
5. [Prepared remarks · Olivier Pomel, Co-Founder and Chief Executive Officer] Finally, we signed a six-figure land with one of the world's largest communication infrastructure companies.
6. [Prepared remarks · David Obstler, Chief Financial Officer] After taking into consideration capital expenditures and capitalized software, free cash flow was $187 million for a free cash flow margin of 31%.
7. [Prepared remarks · David Obstler, Chief Financial Officer] And finally, we continue to expect capital expenditures and capitalized software together to be 3% to 4% of revenues in fiscal 2024.
8. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] We have products that don't tie one to one with infrastructure on their end, but in general, over the longer term, we are very exposed to the growth trend you will see with the cloud providers.
9. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] Yeah, so we have product for monitoring, not just the infrastructure, but what the LLMS are doing.
10. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] You know, in the same way that building infrastructure monitoring for the -- the cloud providers to use internally, you know, might be -- might not be an exact fit for the -- the rest of the world needs.
11. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] And if I go back to the example of hyperscalers, we actually have teams at the hyperscalers that use us for application or infrastructure or logs internally, even though they've built a lot of that tooling themselves.
12. [Q&A · Olivier Pomel, Co-Founder and Chief Executive Officer] One of the new pieces of functionality we've announced last week was a agentless scanning for -- for infrastructure security products, which we think is going to -- to help a lot of customers deploy our product much more broadly, much, much more quickly.
