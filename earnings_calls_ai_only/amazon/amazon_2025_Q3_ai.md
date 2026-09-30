# Amazon.com, Inc. — Q3 2025 Earnings Call (transcript)

- **Company:** Amazon (AMZN)
- **Period:** Q3 2025 (quarter ends calendar Q3 2025; call held the following month)
- **Audio source:** https://s2.q4cdn.com/299287126/files/doc_financials/2025/q3/Amazon-Quarterly-Earnings-Report-Q3-2025-Full-Call-v1.mp3
- **Transcription:** machine transcript (faster-whisper small.en), no speaker labels; expect errors on names and numbers
- **Audio duration:** 50 min
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**76 AI sentences of 451 total**
(Borderline, listed at the end: 7 automation/robotics, 10 infrastructure, none containing an AI term.)

Source/parse flags: machine transcript (Whisper), no speaker labels.

## Prepared remarks

### Speaker not labeled
1. Customers want to be running their core and AI workloads in AWS, giving it stronger functionality, security, and operational performance.
2. We're bringing this same building block approach to AI.
3. SageMaker makes it much simpler for companies to build and deploy their own foundation models.
4. Bedrock gives customers leading selection of foundation models and superior price performance to deploy inference into their next generation applications.
5. A lot of the future value companies will get from AI will be in the form of agents.
6. Companies will both create their own agents and use agents from other companies. ⚑ uncertain
7. It's why we launched Strands to make it much easier to create agents from any foundation model that builders desire. ⚑ context-dependent
8. For companies who successfully built agents, they've hesitated putting them into production because they lack secure, scalable, runtime services or memory or observability built specifically for agents. ⚑ uncertain
9. It's why we launched Agent Core, a set of infrastructure building blocks that allow builders to deploy secure, scalable agents. ⚑ uncertain ⚑ context-dependent
10. Ericsson used Agent Core to deliver AI agents across their workforce.
11. Sony used it to build an agentic AI platform with enterprise level security, observability and scalability.
12. And Cohere Health is using Agent Core to deploy agents that will reduce medical review times by up to 30 to 40%. ⚑ uncertain
13. Agent Core's SDK has already been downloaded over a million times. ⚑ uncertain
14. Companies will also use others agents and AWS continues to build many of the agents we believe builders will use in the future. ⚑ uncertain
15. For coding, we've recently opened up our agentic coding IDE called Kiro.
16. It's processed trillions of tokens thus far, weekly actives are growing fast, and developers love its unique spec and tool calling capabilities. ⚑ uncertain ⚑ context-dependent
17. For migration and transformation, we offer an agent called Transform. ⚑ uncertain
18. For business customers, we've recently launched Quicksweet to bring a consumer AI-like experience to work, making it easy to find insights, conduct deep research, automate tasks, visualize data and take actions.
19. And for contact centers, we offer Amazon Connect, which creates a more personalized and efficient experience for contact center agents, managers, and their customers. ⚑ uncertain
20. Connect has recently crested a billion dollar annualized revenue run rate, with 12 billion minutes of customer interactions being handled by AI in the last year, and is being used by large enterprises like Capital One, Toyota,
21. As a result, AWS is where the preponderance of companies' data and workloads reside, and part of why most companies want to run AI and AWS.
22. We've recently brought Project Rainier online, our massive AI compute cluster spanning multiple US data centers and containing nearly 500,000 of our Tranium 2 chips.
23. Anthropic is using it now to build and deploy its industry-leading AI model,
24. Claude, which we expect to be on more than 1 million Tranium 2 chips by year-end.
25. We're building Bedrock to be the biggest inference engine in the world, and in the long run believe Bedrock could be as big a business for AWS as EC2, and the majority of token usage in Amazon Bedrock is already running on Tranium.
26. The stores team is also innovating rapidly with AI.
27. For example, Rufus, our AI-powered shopping assistant, has had 250 million active customers this year with monthly users up 140% year-over-year, interactions up 210% year-over-year, and customers using Rufus during a shopping trip being 60% more likely to complete a purchase.
28. Our generative AI-powered audio feature that combines product summaries and reviews to make shopping easier has expanded from hundreds of products at launch to millions of products and millions of customers have used it streaming almost 3 million minutes.
29. In Amazon Lens, an AI-powered visual search tool that lets customers find products with their phone's camera, a screenshot, or a barcode now includes Lens Live, which instantly scans products and shows real-time matches in a swipeable carousel.
30. Finally, we're continuing to innovate for advertisers with AI.
31. For example, in September, we announced an agentic AI tool in Creative Studio that plans and executes the entire creative process in a matter of hours instead of weeks.
32. We continue to be energized by the response to Alexa Plus. ⚑ uncertain
33. Compared to what we call the classic Alexa experience, Alexa Plus customers are talking to Alexa two times more, those interactions are much longer, and they're covering a broader range of topics. ⚑ uncertain
34. They're using Alexa ⚑ uncertain ⚑ context-dependent
35. Finally, Zug's Robo Taxis are available to riders in Las Vegas, and we've announced Washington DC as the eighth testing location. ⚑ uncertain
36. The innovations will announce the reinvent in December, the positive customer response to our AI-powered experiences, all the guests we'll be delivering throughout the holiday season and a lot more.
37. We're committed to building innovative services and features for our sellers, including our ongoing advancements in generative AI.
38. Today, more than 1.3 million sellers have used our generative AI capabilities to more quickly launch high-quality listings.
39. We will also build on the gains from our regionalized network through algorithmic improvements, as well as launching robotics and automation. ⚑ uncertain
40. This is an acceleration of 270 basis points compared to last quarter, driven by strong growth across both our AI and core services and more capacity which has come online to support customer demand. ⚑ context-dependent
41. We are expanding our data center footprint largely to accommodate Gen AI and to the extent those assets were placed into service, the related depreciation does impact our margins.
42. AI and core services and in custom silicon like Tranium, as well as tech infrastructure to support our North America and international segments.
43. We'll continue to make significant investments, especially in AI, as we believe it to be a massive opportunity with the potential for strong returns on invested capital over the long term.
44. While we primarily focus our comments on operating income, our third quarter net income of $21.2 billion includes a pre-tax gain of $9.5 billion related to our investment in anthropic.

## Q&A

### Speaker not labeled
1. And you see really big projects at scale now like our project Rainier that we're doing with Anthropic, where they're trading the next version of Claude on top of Tranium 2 on 500,000 Tranium 2 chips, going to a million Tranium 2 chips by the end of the year.
2. But because Tranium is 30% to 40% more price performance than other options out there, and because as customers, as they start to contemplate broader scale of their production workloads, moving to being AI focused and using inference, they badly care about price performance.
3. And you're seeing it again on the custom silicon on the AI side with Tranium, which is about the same amount of price performance benefit for customers relative to other GPU options.
4. And our customers to be able to use AI as expansively as they want.
5. And as we have more proof points, like we have with Project Rainier with what Anthropic is doing on Tranium 2, it builds increasing credibility for Tranium.
6. And do you expect Rainier to expand beyond Anthropic?
7. Anthropic around Project Rainier is it really is the Tranium 2 chip, which we've built a very, first of all, we built a very large cluster that they can use in a very expansive way.
8. And I think that Project Rainier is something that is specific for Anthropic, but we have a lot of other customers who are interested in employing large clusters of
9. Are you seeing the level of efficiencies that you're getting from AI such that you can keep headcount relatively flattish for the foreseeable future?
10. And it's not even really AI driven, not right now, at least it really, it's culture.
11. AI across your operations.
12. How does Amazon think about agentic commerce going forward and how do you think Amazon will serve customers using agents to purchase goods on Amazon in the future?
13. Yeah, I'm very excited about and as a business, we're very excited about in the long term, the prospect of agentic commerce.
14. And I think AI and agentic commerce are going to change the experience online where that experience where you're narrowing what you want when you don't know is going to get better online than it even is in physical environments.
15. Now, we obviously have our own efforts here in agentic commerce.
16. But we're also having conversations with and expect over time to partner with third party agents. ⚑ uncertain
17. And third party agents are a very small subset of that. ⚑ uncertain
18. But I do think that the exciting part of this and the promise is that AI and agentic commerce solutions are going to expand the amount of shopping that happens online.
19. I guess first on AWS, following up there, how much of this acceleration is driven by core infrastructure versus AI workload monetization?
20. Agent Core are becoming and bringing enterprises to AWS to build agents. ⚑ uncertain
21. And we see the growth in both our AI area where we see it in inference, we see it in training, we see it in the use of our Tranium custom silicon.
22. Bedrock continues to grow really quickly.
23. I think that the number of companies who are working on building agents is very significant. ⚑ uncertain
24. I do believe that a lot of the value that companies will realize over time in AI will come from agents.
25. And I think that building agents today is still harder than it should be. ⚑ uncertain
26. You need tools to make it easier, which is why we built Strands, which is an open source capability that lets people build agents from any model that they can imagine. ⚑ uncertain
27. But even more so, when you talk to enterprises or companies that care a lot about security and scale, they're starting to build agents and they don't really feel like they've had building blocks that allow them to have the type of secure scalable agents that they need to bet their businesses and their customer experiences and their data on. ⚑ uncertain
28. And that was really the inspiration behind Agent Core, was to build another set of primitive building blocks like we built in the early days of AWS, where it was compute and storage and database. ⚑ uncertain
29. We defined a set of building blocks that you needed to be able to deploy agents securely and scalably that we provide in Agent Core. ⚑ uncertain
30. It's changing their timeframe and their receptivity to building agents. ⚑ uncertain ⚑ context-dependent
31. So I do think the combination of what we're doing to enable agents to be built and run securely and scalably, as well as some of the agents that we're building ourselves that our customers are excited about, are compelling for them. ⚑ uncertain
32. And I think AI is going to only accelerate that.

## Borderline: automation/robotics without an AI term

1. [Q&A · Speaker not labeled] What did I know, Andy, if you could reflect on the opportunity that's continuing to present itself in terms of rolling out more robotics and automation, and the broader theme of physical
2. [Q&A · Speaker not labeled] Robotics is a very substantial area of investment for us.
3. [Q&A · Speaker not labeled] We have over a million robots in our fulfillment network at this point.
4. [Q&A · Speaker not labeled] Robotics are very important for us and for our customers and for our teammates because they improve safety, they boost productivity, they increase speed, and they let our human teammates focus on problem solving and what they do best.
5. [Q&A · Speaker not labeled] And we expect that our people will remain at the heart and the center of our fulfillment network, as they have from when we first started working on robotics.
6. [Q&A · Speaker not labeled] And we expect that over time, we will have a fulfillment network where robots and humans complement each other and work together.
7. [Q&A · Speaker not labeled] But I think you're going to continue to see us invest very significantly in robotics.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Speaker not labeled] It starts with AWS having much broader infrastructure functionality.
2. [Prepared remarks · Speaker not labeled] This capacity consists of power, data center, and chips, primarily our custom silicon
3. [Prepared remarks · Speaker not labeled] We're also continuing to invest in infrastructure to speed up rural deliveries and serve more customers in more communities.
4. [Prepared remarks · Speaker not labeled] The severance charge is recorded primarily in the technology and infrastructure, sales and marketing, in general, and administrative expense line items.
5. [Prepared remarks · Speaker not labeled] And by leveraging our existing infrastructure, we're now offering US customers the ability to order perishable groceries and receive them the same day in as little as five hours.
6. [Prepared remarks · Speaker not labeled] Now turning to our cash CapEx, which is $34.2 billion in Q3.
7. [Prepared remarks · Speaker not labeled] Looking ahead, we expect our full year cash CapEx to be approximately $125 billion in 2025 and we expect that amount will increase in 2026.
8. [Q&A · Speaker not labeled] That's an infrastructure feat that's hard to do at scale.
9. [Q&A · Speaker not labeled] And so some piece of it is the infrastructure capabilities that we've built over a long period of time in AWS that is unusual in the industry.
10. [Q&A · Speaker not labeled] And I think the other place we see a lot of growth in AWS also is just the number of enterprises who have gotten back to moving from on-premises infrastructure to the cloud.
