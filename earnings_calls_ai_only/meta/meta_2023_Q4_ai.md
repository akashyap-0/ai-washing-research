# Meta Platforms, Inc. — Q4 2023 Earnings Call (transcript)

- **Company:** Meta Platforms (META)
- **Period:** Q4 2023
- **Source:** official transcript published on Meta Investor Relations — https://s21.q4cdn.com/399680738/files/doc_financials/2023/q4/META-Q4-2023-Earnings-Call-Transcript.pdf
- **Note:** this is the main earnings call; Meta also publishes a separate "Follow Up Call" transcript each quarter (not included here)
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**83 AI sentences of 467 total**
(Borderline, listed at the end: 5 automation/robotics, 18 infrastructure, none containing an AI term.)

## Prepared remarks

### Mark Zuckerberg, CEO
1. 2023 was our "year of efficiency" which focused on making Meta a stronger technology company and improving our business to give us the stability to deliver our ambitious long-term vision for AI and the metaverse.
2. And last year, not only did we achieve our efficiency goals, but we returned to strong revenue growth, saw strong engagement across our apps, shipped a number of exciting new products like Threads, Ray-Ban Meta smart glasses, and mixed reality in Quest 3, and of course established a world-class AI effort that is going to be the foundation for many of our future products.
3. Now, moving forward, a major goal will be building the most popular and most advanced AI products and services.
4. And if we succeed, everyone who uses our services will have a world-class AI assistant to help get things done, every creator will have an AI that their community can engage with, every business will have an AI that their customers can interact with to buy goods and get support, and every developer will have a state-of-the-art open source model to build with.
5. I also think everyone will want a new category of computing devices that let you frictionlessly interact with AIs that can see what you see and hear what you hear, like smart glasses.
6. Previously I thought that because many of the tools were social, commerce, or maybe media-oriented that it might be possible to deliver these products by solving only a subset of AI's challenges.
7. But now it's clear that we’re going to need our models to be able to reason, plan, code, remember, and many other cognitive abilities in order to provide the best versions of the services that we envision. ⚑ uncertain
8. I recently shared that by the end of this year we'll have about 350k H100s and including other GPUs that’ll be around 600k H100 equivalents of compute. ⚑ uncertain
9. We initially under-built our GPU clusters for Reels, and when we were going through that I decided that we should build enough capacity to support both Reels and another Reels-sized AI service that we expected to emerge so we wouldn't be in that situation again.
10. Going forward, we think that training and operating future models will be even more compute intensive.
11. We don't have a clear expectation for exactly how much this will be yet, but the trend has been that state-of-the-art large language models have been trained on roughly 10x the amount of compute each year.
12. Our training clusters are only part of our overall infrastructure and the rest obviously isn't growing as quickly.
13. In the case of AI, the general infrastructure includes our Llama models, including Llama 3 which is training now and is looking great so far, as well as industry-standard tools like PyTorch that we've developed.
14. The short version is that open sourcing improves our models, and because there's still significant work to turn our models into products, because there will be other open source models available anyway, we find that there are mostly advantages to being the open source leader and it doesn't remove differentiation from our products much anyway.
15. This is a big deal because safety is one of the most important issues in AI. ⚑ context-dependent
16. And again, we typically have unique data and build unique product integrations anyway, so providing infrastructure like Llama as open source doesn't reduce our main advantages.
17. While we're working on today's products and models, we're also working on the research we need to advance for Llama 5, 6, and 7 in the coming years and beyond to develop full general intelligence.
18. But it's also important to have clear launch vehicles like future Llama models that help focus our work.
19. When people think about data, they typically think about the corpus that you might use to train a model up front.
20. But even more important than the upfront training corpus is the ability to establish the right feedback loops with hundreds of millions of people interacting with AI services across our products.
21. And this feedback is a big part of how we've improved our AI systems so quickly with Reels and ads, especially over the last couple of years when we had to rearchitect it around new rules.
22. When we decide that a new technology like AI-recommended Reels is going to be an important part of the future, we're not shy about having multiple teams experimenting with different versions across our apps until we get it right -- and then we learn what works and we roll it out to everyone.
23. We started doing that with our AI services in the fall, launching Meta AI, our assistant, AI Studio, which is the precursor to Creator AIs, our alpha with business AIs, and then the Ray-Ban Meta smart glasses.
24. Although in this case, the way that business AIs will help business messaging grow in WhatsApp, Messenger, and Instagram is pretty clear.
25. We have two major parts of our long term vision, and in addition to AI the other part is the metaverse.
26. We've invested heavily in both AI and the metaverse for a long time, and we will continue to do so.
27. These days there are a lot of questions, more about AI that I get, and that field is moving very quickly, but I still expect this next generation of AR, MR, and VR computing platforms to deliver a realistic sense of presence that will be the foundation for the future of social experiences and almost every other category as well. ⚑ context-dependent
28. This is another example of applying the long-term playbook I discussed earlier with AI, but in another area. ⚑ context-dependent
29. The experience is just a lot better with Meta AI in there, as well as a higher resolution camera, better audio, and more.
30. We also have an exciting roadmap of software improvements ahead, starting with rolling out multimodal AI and then some other really exciting new AI features later in the year.
31. I said this before, but I think that people are going to want new categories of devices that let you frictionlessly engage with AIs frequently throughout the day without having to take out your phone and press a button and point it at what you want it to see.
32. I think that smart glasses are going to be a compelling form factor for this, and it's a good example of how our AI and metaverse visions are connected.
33. In addition to AI and the metaverse, we're continuing to improve our apps and ads businesses as well.

### Susan Li, CFO
34. We’re also making good progress in areas that have the potential to grow people’s engagement with our products in the longer-term, such as Threads and generative AI.
35. With generative AI, we fully rolled out our Meta AI assistant and other AI chat experiences in the US at the end of the year and began testing more than 20 gen AI features across our Family of Apps.
36. Our big areas of focus in 2024 will be working towards the launch of Llama 3, expanding the usefulness of our Meta AI assistant, and progressing on our AI studio roadmap to make it easier for anyone to create an AI.
37. To do this, we’re focused on three areas: The first is AI.
38. We continue to leverage AI across our ads systems and product suite.
39. We’re delivering continued performance gains from ranking improvements as we adopt larger and more advanced models and this will remain an ongoing area of investment in 2024. ⚑ uncertain
40. We’re also building out our Advantage+ portfolio of solutions to help advertisers leverage AI to automate their advertising campaigns.
41. On the ads creative side, we completed the global roll out of two of our generative AI features in Q4 - text variations and image expansion - and plan to broaden availability of our background generation feature later in Q1.
42. We’re also progressing with our early testing on WhatsApp and Messenger of AIs for businesses that can provide conversational support in chat.
43. We are in the fortunate position of being able to invest in many organic opportunities to improve the performance of our core business in the near-term while also making two significant longer time horizon investments in AI and Reality Labs.
44. AI is a growing area of investment for us in 2024 as we hire to support our roadmap.
45. We’re also investing more in our AI infrastructure capacity this year, and given many of our ambitious forward-looking plans will rely on having sufficient compute capacity, we expect this to be an area we invest more aggressively in over the coming years.
46. We expect growth will be driven by investments in servers, including both AI and non-AI hardware, and data centers as we ramp up construction on sites with our previously announced new data center architecture.
47. Our updated outlook reflects our evolving understanding of our AI capacity demands as we anticipate what we may need for the next generations of foundational research and product development.
48. While we are not providing guidance for years beyond 2024, we expect our ambitious long-term AI research and product development efforts will require growing infrastructure investments beyond this year.
49. We will look to build on our priorities in each of those areas in 2024 while advancing our ambitious, longer-term efforts in AI and Reality Labs.

## Q&A

### Brian Nowak, Morgan Stanley
1. Let me ask you one about sort of the advertising business and all of the new machine learning and new GenAI ad tools that you built and rolled out the last year or so.

### Susan Li, CFO
2. And then finally, continuing to really use AI in important ways across our ads platform.
3. For a long time, we have invested in building larger and more advanced models that have resulted in more accurate predictions of relevant ads for people and improved performance for advertisers. ⚑ uncertain
4. And then, of course, we're investing a lot in AI-powered tools and products.

### Mark Zuckerberg, CEO
5. So the themes for the year of efficiency were to make us a stronger technology company by becoming leaner and more balanced towards our engineering work and more streamlined and to improve our financial performance, primarily with the goal of providing stability so we can invest in these long-term, ambitious visions around AI and metaverse over what we see as the coming decade or more as these things play out.
6. And we want the ability to be able to surge investment on things like building out larger training clusters or just making different investments where that's necessary.

### Susan Li, CFO
7. So, we -- we're really continuing to evolve our AI roadmaps and ambitions and our understanding of the capacity demands that we might have as we train the next generations of foundation models and to support all of the associated product development going forward.
8. But our expectation is, generally, that we will need to invest more to support our AI work in the years ahead, and we're seeing some of that reflected in 2024.

### Mark Shmulik, AllianceBernstein
9. Mark, you mentioned at the top of the call this vision, kind of everyone having a Meta AI assistant to kind of get things done.
10. But given kind of the pace of innovation around AI that you've seen, has that timeline changed?

### Mark Zuckerberg, CEO
11. I do think that AI is going to make all of the products and services that we use and make better.
12. And now it seems quite possible that smart glasses that have AI assistants built in will be the killer app, and that the holograms and sense of presence will come later as a -- maybe on the same time horizon we were talking about before but could end up being just as important as we expected.
13. We always kind of expected that as part of building glasses or any of these platforms that having an AI assistant would be a foundational part of it.

### Susan Li, CFO
14. And we'll continue to focus on deepening integrations with partners and leveraging AI to make Shops ads even more performant.

### Mark Zuckerberg, CEO
15. The whole reason why we moved FAIR is basically to be closer to the GenAI group.
16. The GenAI group basically builds our Llama launch vehicles and products, but also conducts a fair amount of research, too, especially things that are going to be coming into the upcoming versions of Llama.
17. A lot of last year and the work that we're doing with Llama 3 is basically making sure that we can scale our efforts to really produce state-of-the-art models.
18. But once we get past that, there's a lot more kind of different research that I think we're going to be doing that's going to take our foundation models in potentially different directions than other players in the industry are going to go in because we're focused on specific vision for what we're building.
19. So it's really important as we think about what's going to be in Llama 5 or 6 or 7 and what cognitive abilities we want in there and what modalities we want to build into future multimodal versions of the models, we need to be doing that work in advance and to research those things.
20. And it helps to -- and even though FAIR and GenAI will continue to be two kind of separate groups on different time horizons, I think to have some level of alignment between -- on the vision of what we're building between the two of them, so that way, the FAIR team can have in mind, hey, if we research this, then maybe it can intercept Llama 6 or something.
21. It's one of the reasons why I talked about, we did open-ended research in AI for a while. ⚑ context-dependent
22. But having a clear product target with these AI agents, I think, is really going to help focus the work and give us a feedback loop that's going to increase the productivity and output that we get dramatically.

### Ron Josey, Citi
23. Just talk to us how you might see this unfold maybe with AI Studio and any timing would be helpful.

### Susan Li, CFO
24. I was going to take the second question, I think, which was around the rollout of some of the GenAI features from a monetization perspective.
25. And we're -- first of all, I would say that we don't expect our GenAI products to be a meaningful 2024 driver of revenue.
26. Over a longer timeframe, the GenAI features that we're bringing to business messaging, which I think was where your question originated, we think really represents a compelling opportunity.
27. We're testing AI chats on a very small scale today with a few businesses, but it will take time to continue making those AIs increasingly useful.
28. I'd say one other thing is just on the consumer side, again, we think GenAI can make it easier for people to produce compelling content across all of our apps, including our messaging apps.
29. And our AI assistant certainly provides also added utility.

### Ross Sandler, Barclays
30. Mark, just curious what you're seeing with Meta AI at this stage.
31. Which of the apps in the Family of Apps have seen engagement increase from Meta AI? ⚑ context-dependent
32. And do you think that there could be increased commercial activity as either your AI agent or some of the other ones out there get more usage within your apps?

### Mark Zuckerberg, CEO
33. I think having a good assistant is going to be one of the real values that this generation of AI creates as well as giving every creator an opportunity to have an assistant or agent that people can engage with and every business and agent and also allowing people to create a bunch of quirky and fun things as well.
34. But yes, I think Meta AI is going to be very important across the products.

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Susan Li, CFO] Advertisers can choose to automate part of the campaign creation set up process, such as who to show their ad to, with Advantage+ Audience.
2. [Prepared remarks · Susan Li, CFO] Or, they can automate their campaign completely using our end-to-end automation tool for driving online sales, Advantage+ Shopping, which continues to see strong growth.
3. [Prepared remarks · Susan Li, CFO] We’re also now exploring ways to apply this end-to-end automation to new objectives.
4. [Q&A · Susan Li, CFO] So we're really scaling our Advantage+ suite across all of the different offerings there, which really help to automate the ads creation process for different types of advertisers.
5. [Q&A · Susan Li, CFO] And then, of course, in the longer term, this is a place where we're excited about the opportunities for increased automation to really help businesses scale their ability to have conversations with their consumers.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Mark Zuckerberg, CEO] The first is world-class compute infrastructure.
2. [Prepared remarks · Mark Zuckerberg, CEO] And at the time the decision was somewhat controversial and we faced a lot of questions about capex spending, but I'm really glad that we did this.
3. [Prepared remarks · Mark Zuckerberg, CEO] In order to build the most advanced clusters, we're also designing novel data centers and designing our own custom silicon specialized for our workloads.
4. [Prepared remarks · Mark Zuckerberg, CEO] The second part of our playbook is open source software infrastructure.
5. [Prepared remarks · Mark Zuckerberg, CEO] Our long-standing strategy has been to build and open source general infrastructure while keeping our specific product implementations proprietary.
6. [Prepared remarks · Mark Zuckerberg, CEO] I know that some people have questions about how we benefit from open sourcing the results of our research and large amounts of compute, so I thought it might be useful to lay out the strategic benefits here.
7. [Prepared remarks · Mark Zuckerberg, CEO] First, open source software is typically safer and more secure, as well as more compute efficient to operate due to all the ongoing feedback, scrutiny, and development from the community.
8. [Prepared remarks · Mark Zuckerberg, CEO] Efficiency improvements and lowering the compute costs also benefit everyone including us.
9. [Prepared remarks · Mark Zuckerberg, CEO] This is why our long-standing strategy has been to open source general infrastructure and why I expect it to continue to be the right approach for us going forward.
10. [Prepared remarks · Susan Li, CFO] In terms of the specific line items: Cost of revenue decreased 8%, driven mainly by lower restructuring costs that were partially offset by higher infrastructure-related costs.
11. [Prepared remarks · Susan Li, CFO] Capital expenditures, including principal payments on finance leases, were $7.9 billion, driven by investments in servers, data centers and network infrastructure.
12. [Prepared remarks · Susan Li, CFO] We continue to expect a few factors to be drivers of total expense growth in 2024: First, we expect higher infrastructure-related costs this year.
13. [Prepared remarks · Susan Li, CFO] We also expect to incur higher operating costs from running a larger infrastructure footprint.
14. [Prepared remarks · Susan Li, CFO] Turning now to the capex outlook.
15. [Prepared remarks · Susan Li, CFO] We anticipate our full-year 2024 capital expenditures will be in the range of $30-37 billion, a $2 billion increase of the high end of our prior range.
16. [Q&A · Eric Sheridan, Goldman Sachs] And then Susan, I went back and looked, I don't think you've ever raised the high end of your CapEx guidance before, unless I'm mistaken.
17. [Q&A · Eric Sheridan, Goldman Sachs] But with a wide range like that in CapEx, what should we be monitoring for what would push you towards either the lower end or the higher end of that CapEx guidance as you move through 2024?
18. [Q&A · Susan Li, CFO] How quickly can we execute on the new data center architecture, how the supply chain turns out to unfold over the course of the year.
