# Datadog — 2024_Q2 Earnings Call (transcript)

- **Company:** Datadog (DDOG); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** DDOG
- **CIK:** 0001561550
- **Period:** 2024_Q2 (call held August 8, 2024; date from page date line)
- **Calendar quarter:** 2024 Q2 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/08/08/datadog-ddog-q2-2024-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** b6cf5cc039f6bb38e8c30472a82a853a354dea8d4c5085f3ea1f245103e9147e
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**42 AI sentences of 608 total**
(Borderline, listed at the end: 5 automation/robotics, 8 infrastructure, none containing an AI term.)

## Prepared remarks

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
1. In the next-gen AI space, we announced the general availability of LLM Observability, which allows application developers and machine learning engineers to efficiently monitor, troubleshoot, and secure LLM applications.
2. With LLM Observability, companies can accelerate the deployment of AI applications into production environments and reliably operate and scale them.
3. We also expanded Bits AI with new capabilities.
4. As a reminder, Bits AI is a Datadog built-in AI copilot.
5. In addition to being able to summarize incidents and answer questions, we previewed at DASH the ability for Bits AI to operate as an agent and perform autonomous investigations.
6. With this capability, this AI proactively surfaces key information and performs complex tasks such as investigating alerts and coordinating incident response.
7. Taking a step back and looking at our customer base, we continue to see a lot of excitement around AI technologies.
8. Our customers are telling us that they are leveling up on AI and ramping experimentations with the goal of delivering additional business value with AI.
9. Today, about 2,500 customers use one or more of our AI integrations to get visibility into their increasing use of AI.
10. We also continue to grow our business with AI-native customers, which increased to over 4% of our ARR in June.
11. I will note that, over time, we think this metric will become less relevant as AI usage and production broadens beyond this group of customers.
12. Last but not least, we announced Toto, our first foundational model for time series forecasting, which delivered state-of-the-art performance on all 11 benchmarks.
13. In addition to the technical innovations devised by our research team, Toto derives its record performance from the quality of our training dataset and points to our unique ability to train, build, and incorporate AI models into our platform that will meaningfully improve operations for our customers.
14. Moving on from AI.
15. Moving and transforming large amounts of data has grown in importance and become a mission-critical capability for many businesses, a trend that we believe will continue with the adoption of AI.
16. For our customers using OpenTelemetry, the Datadog agent will embed a fully configurable OpenTelemetry Collector, giving Otel customers access to Datadog products such as container network and universal service monitoring and offering our customers what we believe will be the best fully managed OpenTelemetry experience in the market. ⚑ uncertain
17. And for instances where customers can't or don't want to deploy agents, our new agentless scanning capability provides visibility into risks and vulnerabilities within host, containers, and several functions without requiring agents to be installed. ⚑ uncertain
18. We are seeing continued experimentation with new technologies, including next-gen AI, and we believe this is just one of the many factors that will drive greater use of the cloud and next-gen infrastructure.
19. As indicated by our many announcements at our DASH user conference, we are delivering rapid innovation at scale, and we are helping our customers every day to deploy and scale the model environment with confidence across observability, digital experience, cloud security, cloud service management, software delivery, and product analytics. ⚑ uncertain
20. Yanbing has more than 25 years of product, technology, and engineering experience, spanning enterprise software, cloud infrastructure and AI at companies such as VMware, Google, and Aurora.

## Q&A

### Mark Murphy, Analyst
1. Olivier, it's great to see the announcement of LLM Observability reaching GA.
2. There -- I think we're all looking at this tremendous wave of hyperscaler commitments that are going to be ramping in the second half of this year, and it's all for training of these next-gen AI models.
3. And since you're more exposed to the -- excuse me, since you're less exposed to that training and you're more driven by the inferencing, I'm wondering if you could just help us understand how the spending pattern or activity changes as the AI models go live and reach the inferencing stage.
4. I'm basically looking for any way to assess how much spending is ultimately going to develop into the inferencing where you have an opportunity. ⚑ uncertain

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
5. I mean, we named a couple as early customers of LLM Observability.
6. I would say the best proxy you can get from the future demand there is the growth of the model providers and the AI natives because they tend to be the ones that currently are being used to provide AI functionality into other applications and largely in production environment.

### Mark Murphy, Analyst
7. A couple of the consumption-model software companies had recently commented that, in June and July, they were seeing more cloud cost control or optimization, specifically among the digital natives. ⚑ uncertain

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
8. And even when you look at the digital native, there's two stories depending on whether you talk about the AI natives or the others.
9. The AI natives are inflecting in a way that the others are not at this point.
10. So, today, we see this higher growth from AI natives and from traditional enterprises.

### Kirk Materne, Analyst
11. Olivier, I was wondering if you could just talk a little bit more about the LLM Observability product that Mark referenced.
12. When people are thinking about bringing on LLMs into their organization, do they want the observability product in place already?
13. Or are they testing out LLMs and then bringing you on after the fact?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
14. That being said, the way it works typically is customers build applications using developer tools, and there's a whole industry that has emerged around developer tools for -- and playgrounds and things like that for LLM. ⚑ context-dependent
15. When they start connecting the LLM to the rest of the application, then they start to need like visibility that includes the other components because the LLM doesn't work in a vacuum.
16. For the customers that use our LLM Observability product, they use us for the rest -- all the rest of their stack.
17. And it would make absolutely no sense for them to operate their LLMs in isolation completely separately and not have the visibility across the whole applications.

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
18. Some of the strength we see today has to do with the fact that to serve their -- the emergence of AI has reaffirmed for them the need to go to the cloud sooner rather than later so they can build the right kind of applications, they have the right kind of data available to build these applications.

### Jake Roberge, William Blair and Company, Analyst
19. And then you've talked a decent amount about the demand you're seeing from AI-native customers, but how are you thinking about driving growth with your own AI solutions, like Bits AI and LLM Observability, and when do you think those start to layer more meaningfully into the model?

### Olivier Pomel, Co-Founder, Chief Executive Officer, and Director
20. I mean, right now, the first area of direct application of Bits AI is in incident management and incident resolution, so that is tied more to the SKUs we're selling there in terms of incident management.
21. But Bits AI is not the only ingredient of that product.

### Yi Fu Lee, Cantor Fitzgerald, Analyst
22. In terms of the new products that were launched at DASH, a lot of stuff going on in LLM, AI apps, etc.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We introduced Kubernetes Autoscaling to allow customers to optimize for cost and performance by automatically rightsizing Kubernetes resources.
2. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We also announced Data Security, which allows our customers to automatically pinpoint sensitive data, starting in AWS today and expanding to other environments in the future.
3. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] This renewal support its customers' expansion into new use cases to have security embedded into the operations by using all of our cloud security products, to build a culture of cost accountability with cloud cost management, and to take action by using incident management and workflow automation.
4. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] Even though the fix in that case was very, very manual, there was really no good way to automate it.
5. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] So, longer term -- look, we think there's a very large opportunity for us to do a lot of automation we have with our customers.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] We announced the general availability of Flex Logs, which extends our logging without limit approach and allows our customers to scale storage and compute separately for cost efficiency.
2. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] And they expect to transition to modern infrastructure -- modern infrastructure, sorry, with confidence.
3. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] By moving to Datadog and replacing this tool, they expect to drive significant savings with log management and will benefit from our unified platform across infrastructure monitoring and APM.
4. [Prepared remarks · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] This longtime customer uses Datadog as its strategic observability partner, enabling full visibility across infrastructure, applications, logs, network, and their public content, with users spanning from hands-on keyboard engineers all the way to their C-level executives.
5. [Prepared remarks · David M. Obstler, Chief Financial Officer] And after taking into consideration capital expenditures and capitalized software, free cash flow was $144 million for a free cash flow margin of 22%.
6. [Prepared remarks · David M. Obstler, Chief Financial Officer] Finally, we continue to expect capital expenditures and capitalized software together to be in the 3% to 4% of revenues range in fiscal 2024.
7. [Q&A · Fatima Boolani, Analyst] And, David, as you all kind of roll out more what I would call resource-intensive or compute-intensive SKUs, like logs, Flex Logs, logs workspaces, I'm wondering if you can shed a little bit of light on how some of the gross margin characteristics differ by product pillar.
8. [Q&A · Olivier Pomel, Co-Founder, Chief Executive Officer, and Director] One is customers adopting our security suite, and data security is little by little becoming part of CNAPP and cloud infrastructure security in general.
