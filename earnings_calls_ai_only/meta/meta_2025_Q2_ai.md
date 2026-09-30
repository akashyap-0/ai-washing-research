# Meta Platforms, Inc. — Q2 2025 Earnings Call (transcript)

- **Company:** Meta Platforms (META)
- **Period:** Q2 2025
- **Source:** official transcript published on Meta Investor Relations — https://s21.q4cdn.com/399680738/files/doc_financials/2025/q2/META-Q2-2025-Earnings-Call-Transcript.pdf
- **Note:** this is the main earnings call; Meta also publishes a separate "Follow Up Call" transcript each quarter (not included here)
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**112 AI sentences of 451 total**
(Borderline, listed at the end: 0 automation/robotics, 33 infrastructure, none containing an AI term.)

## Prepared remarks

### Mark Zuckerberg, CEO
1. Our business continues to perform very well, which enables us to invest heavily in our AI efforts.
2. Over the last few months we have begun to see glimpses of our AI systems improving themselves.
3. Developing superintelligence -- which we define as AI that surpasses human intelligence in every way -- we think is now in sight.
4. Meta's vision is to bring personal superintelligence to everyone -- so that people can direct it towards what they value in their own lives.
5. A lot has been written about the economic and scientific advances that superintelligence can bring.
6. But I think that if history is a guide, then an even more important role will be how superintelligence empowers people to be more creative, develop culture and communities, connect with each other, and lead more fulfilling lives.
7. To build this future, we've established Meta Superintelligence Labs, which includes our foundations, product, and FAIR teams, as well as a new lab that is focused on developing the next generation of our models.
8. We're making good progress towards Llama 4.1 and 4.2 -- and in parallel, we're also working on our next generation of models that will push the frontier in the next year or so.
9. Alexandr Wang is leading the overall team, Nat Friedman is leading our AI products and applied research, and Shengjia Zhao is Chief Scientist for the new effort.
10. They're all incredibly talented leaders and I'm excited to work closely with them and the world-class group of AI researchers, and infrastructure and data engineers that we're assembling. ⚑ context-dependent
11. I've spent a lot of time building this team this quarter, and the reason that so many people are excited to join is because Meta has all the ingredients required to build leading models and deliver them to billions of people. ⚑ uncertain
12. We're making all these investments because we have conviction that superintelligence is going to improve every aspect of what we do.
13. From a business perspective, I mentioned last quarter that there are five basic opportunities that we're pursuing: improved advertising, more engaging experiences, business messaging, Meta AI, and AI devices.
14. On advertising, the strong performance this quarter is largely thanks to AI unlocking greater efficiency and gains across our ads system.
15. This quarter, we expanded our new AI -powered recommendation model for ads to new surfaces and improved its performance  by using more signals and a longer context.
16. We're also seeing good progress with AI for ad creative -- with a meaningful percent of our ad revenue now coming from campaigns using one of our Generative AI features.
17. AI is significantly improving our ability to show people content that they’re going to find interesting and useful.
18. Advancements in our recommendation systems have improved quality so much that it has led to a 5% increase in time spent on Facebook and 6% on Instagram just this quarter. ⚑ uncertain
19. We're seeing early progress with the launch of our AI video editing tools across Meta AI and our new Edits app, and there's a lot more to do here.
20. I've talked before about how I believe every business will soon have a business AI just like they have an email address, social media account, and website.
21. We're starting to see some product market fit in a numb er of countries where we're testing these agents, and we're integrating these business AIs into ads on Facebook and Instagram, as well as directly into e-commerce websites.
22. The fourth opportunity is Meta AI.
23. Our focus is now deepening the experience and making Meta AI the leading personal AI.
24. As we continue improving our models we see engagement grow, so our next generation of models is going to continue to really help here. ⚑ uncertain
25. The fifth opportunity is AI devices.
26. We're also launching new performance AI glasses with the Oakley Meta HSTNs.
27. The percent of people using Meta AI is growing and we're seeing new users' AI retention increase too, which is a good sign for that continued use.
28. I think that AI glasses are going to be the main way that we integrate superintelligence into our day-to-day lives, so it's important to have all these different styles that appeal to different people in different settings.
29. Strong business performance and real momentum in assembling both the talent and the compute needed to build personal superintelligence for everyone.

### Susan Li, CFO
30. This was partially offset by continued hiring in priority areas of monetization, infrastructure, Reality Labs, AI, as well as regulation and compliance. ⚑ context-dependent
31. We also made $15.1 billion in non -marketable equity investments in the second quarter, which includes our minority investment in Scale AI along with other investment activities.
32. Within our Reality Labs segment, Q2 revenue was $370 million, up 5% year -over-year due to increased sales of AI glasses, partially offset by lower Quest sales.
33. On the first, daily actives continue to grow across Facebook, Instagram and WhatsApp as we make additional improvements to our recommendation systems and product experiences. ⚑ uncertain
34. We expect to deliver additional improvements throughout the year as we further scale up our models and make recommendations more adaptive to a person’s interests within their session. ⚑ uncertain
35. Our research efforts to develop cross-surface foundation recommendation models continue to progress.
36. We are also seeing promising results from using LLMs in Threads recommendation systems.
37. The incorporation of LLMs are now driving a meaningful share of the ranking-related time spent gains on Threads.
38. We’re now exploring how to extend the use of LLMs in recommendation systems to our other apps.
39. We’re leveraging Llama in several other back-end processes as well, including actioning bug reports so we can identify and resolve recurring issues more quickly and efficiently.
40. The primary way we’re using Llama in our apps today is to power Meta AI, which is now available in over 200 countries and territories.
41. WhatsApp continues to be the largest driver of queries as people message Meta AI directly for tasks such as information gathering, homework assistance, and generating images.
42. Outside of WhatsApp, we’re seeing Meta AI become an increasingly valuable complement to our content discovery engines.
43. Meta AI usage on Facebook is expanding as people use it to ask about posts they see in Feed and find content across our platform in Search.
44. Another way we expect Meta AI will help with content discovery is through the automatic translation and dubbing of foreign-language content into the audience’s local language.
45. The Andromeda model architecture we began introducing in the second half of 2024 powers the ads retrieval stage of our ads system, where we select the few thousand most relevant ads from tens of millions of potential candidates. ⚑ uncertain
46. In Q2, we made enhancements  to Andromeda that enabled it to select more relevant and more personalized ads candidates, while also expanding coverage to Facebook Reels. ⚑ uncertain
47. Our new Generative Ads Recommendation System, or GEM, powers the ranking stage of our ads system, which is the part of the process after ads retrieval where we determine which ads to show someone from candidates suggested by our retrieval engine.
48. In Q2, we  improved the performance of GEM by further scaling our training capacity and adding organic and ads engagement data on Instagram.
49. Finally, we expanded coverage of our Lattice model architecture in Q2. ⚑ uncertain
50. We first began deploying Lattice in 2023 with our later stage ads ranking efforts, allowing us to run significantly larger models that generalize learnings across objectives and surfaces in place of numerous, smaller ads models that have historically been optimized for individual objectives and surfaces. ⚑ uncertain
51. In April, we began deploying Lattice to earlier stage ads ranking models as well.
52. This is leading not only to greater capacity and engineering efficiency, but also improved performance, with the recent Lattice deployments driving a nearly 4% increase in ad conversions across Facebook Feed and Reels in Q2. ⚑ uncertain ⚑ context-dependent
53. Here, we’re seeing strong momentum with our Advantage+ suite of AI powered solutions.
54. Within our Advantage+ creative suite, adoption of gen AI ad creative tools continues to broaden.
55. In Q2, we started testing AI-powered translations so that advertisers can automatically translate the caption of their ads to 10 different languages.
56. Within AI, we’ve had a particular emphasis on recruiting leading talent within the industry as we build out Meta Superintelligence Labs to accelerate our AI model development and product initiatives.
57. We continue to see very compelling returns from our AI capacity investments in our core ads and organic engagement initiatives, and expect to continue investing significantly there in 2026.
58. We also expect that developing leading AI infrastructure will be a core advantage in developing the best AI models and product experiences, so we expect to ramp our investments significantly in 2026 to support that work.
59. While the infrastructure planning process remains highly dynamic, we currently expect another year of similarly significant capex dollar growth in 2026 as we continue aggressively pursuing opportunities to bring additional capacity online to meet the needs of our AI efforts and business operations.
60. We have appealed the European Commission’s DMA decision but any modifications to our model may be imposed during the appeal process. ⚑ uncertain
61. We expect the significant investments we’re making now will allow us to continue leveraging advances in AI to extend those gains and unlock a new set of opportunities in the years to come.

## Q&A

### Eric Sheridan
1. Mark, when you think about where the AI parts of your business have been evolving over the last three to six months, I wanted to know what your key learnings were as you went deep into that strategy that inform some of the shifts in both talent, acquisition and compute.

### Mark Zuckerberg, CEO
2. At a high level, I think that there are all these questions that people have about what are going to be the timelines to get to really strong AI or Superintelligence or whatever you want to call it.
3. And I think, certainly, some of the work that we’re seeing with teams internally being able to adapt Llama 4 to build autonomous AI agents that can help improve the Facebook algorithm to increase quality and engagement, or like.
4. And then I think we have this principle that we believe in across the company, which we tell people, take Superintelligence seriously.
5. So anyway, I think it’s basically just we’re continually observing how this works and what the trajectory or the pace of AI progress has been.

### Susan Li, CFO
6. And we also have some visibility into the compensation expense growth that we’ll recognize from the AI talent that we’re hiring this year.
7. After that, employee compensation is the next largest driver of expense growth in ’26, again, driven primarily in the investments that we’re making in technical talent including recognizing a full year of compensation expense for the AI talent we hire this year.
8. On the CapEx side, the big driver of our increased CapEx in ‘26 will be scaling GenAI capacity as we build out training capacity that’s going to drive higher spend across servers, networking, data centers next year.
9. We also expect that we’re going to continue investing significantly in core AI in 2026.

### Brian Nowak, Morgan Stanley
10. The first one, Mark, just to kind of go back to the intelligence labs and sort of the vision for Superintelligence.
11. As you sort of sit here now versus 12 months ago, can you just sort of walk us through any changes of technological constraints or technological gating factors that you are most focused on overcoming in the next 24 months that may have been different than they were in the past just to make sure you can really lead in the idea of Superintelligence over the next ten years?

### Mark Zuckerberg, CEO
12. But I think that for developing superintelligence at some level, you’re not just going to be learning from people because you’re trying to build something that is fundamentally smarter than people.
13. And it’s a bit of a different setup than we have on our other world-class machine learning systems.
14. But I think for this -- for the leading research on superintelligence, you really want the smallest group that can hold the whole thing in their head, which drives, I think, some of the physics around the team size and how -- and the dynamics around how that works.

### Susan Li, CFO
15. Brian, on the sort of forward-looking roadmap for the core recommendation engine. ⚑ uncertain
16. We’re also planning to scale up our models further and incorporate more advanced techniques that should improve the overall quality of recommendations. ⚑ uncertain
17. But we also have a lot of long-term bets in the hopper around areas like developing foundational models that will support recommendations across multiple services, incorporating LLMs more deeply into our recommendation systems.
18. And a big focus of this work is going to be on optimizing the systems to make them more efficient, so that we can continue to scale up the capacity that we use for our recommendation systems without eroding the ROI that we deliver. ⚑ uncertain

### Douglas Anmuth, JPMorgan
19. Mark, Meta has been a huge proponent of open source AI.
20. How has your thinking changed here at all, just as you pursue superintelligence and push for even greater returns on your significant infrastructure investments?

### Mark Zuckerberg, CEO
21. We’ve always open-sourced some of our models and not open sourced everything that we’ve done. ⚑ uncertain
22. So I would expect that we will continue to produce and share leading open source models.
23. One is that we’re getting models that are so big that they’re just not practical for a lot of other people to use. ⚑ uncertain
24. And then obviously as you approach real superintelligence, I think there is a whole different set of safety concerns that I think we need to take very seriously that I wrote about in my note this morning.

### Susan Li, CFO
25. We don’t have any finalized transactions to announce, but we generally believe that there will be models here that will attract significant external financing to support large-scale data center projects that are developed using our ability to build world-class infrastructure while providing us with flexibility should our infrastructure requirements change over time. ⚑ uncertain

### Justin Post, Bank of America
26. And then Susan, when you think about the ROI on this CapEx, I’m sure you have internal models, I’m sure you can’t share all that, but how are you thinking about the ROI? ⚑ uncertain

### Susan Li, CFO
27. Right now we are focused on ensuring that we have enough capacity for our internal use cases, which includes both all of the core AI work that we do to support the recommendation engine work on the organic content side, to support all the ads ranking and recommendation work.
28. And then, of course, to make sure that we are building the training capacity that we think we need in order to build frontier AI models.
29. And to make sure that we’re preparing ourselves for the types of inference use cases that we think might -- that we might have ahead of us as we eventually focus not only on developing frontier models, but also how we can expand into the kinds of consumer use cases that we think will be hopefully widely useful and engaging for our users.
30. So again, on the core AI side, we continue to see strong ROI.
31. On the GenAI side, we are clearly much, much earlier on the return curve and we don’t expect that the GenAI work is going to be a meaningful driver of revenue this year or next year.

### Mark Shmulik, Bernstein
32. Mark, as you go after the Superintelligence vision, especially for those of us on the outside, what are kind of some of the markers or KPIs that you’re tracking on whether you’re on track and making progress?
33. And Susan, obviously AI is delivering great ROI today, all those investments and also building towards kind of longer-term goals.

### Mark Zuckerberg, CEO
34. In terms of what to look at, I mean what I’m going to look at internally, the quality of the people on the teams, the quality of the models that we’re producing, the rate of improvement of our other AI systems across the company and the extent to which the leading kind of foundation models that we’re building contribute to improving all of the other AI systems and kind of everything that we’re doing around the company.
35. And that, I think, is kind of always the way that we work is, whether we’re building some new social product or this something like Meta AI or a new product around this that we’re going to work on getting to leading scale, building the highest quality product , focused on that for a few years.
36. But I guess, on the flip side, we believe that if you are building superintelligence, you should use all of your GPUs to make it so that you’re serving your customers really well with that.

### Susan Li, CFO
37. But we really believe that this is a time for us to really make investments in the future of AI as I think it will open up both new opportunities for us in addition to strengthen our core business.

### Ronald Josey, Citi
38. Mark, I wanted to ask you on Meta AI and I think you talked about in the call just growing engagement overall, particularly on WhatsApp and now you have 1 billion users on the platform and the focus is now on driving personalization.
39. So I want to understand a little bit more how these next-gen models can help drive adoption here, particularly with Behemoth coming online at some point. ⚑ uncertain
40. And then as people are using Meta AI with WhatsApp, thoughts on search and queries and potentially monetizing that.

### Mark Zuckerberg, CEO
41. I’m not going to get super deep into the roadmap on this, but the basic -- we do see that as we continue improving the models behind Meta AI and post training and just engagement increases and as we swap in the updated models, when we go from Llama 4 to Llama 4.1 when we have that, we expect that just -- the models are inherently pretty general.

### Youssef Squali, Truist Securities
42. And as you leverage Meta AI, do you believe glasses will ultimately replace smartphones?
43. Or do you need a new form factor that’s AI first?

### Mark Zuckerberg, CEO
44. And then the use of Meta AI in them just continues to grow, and the percent of people who are using it for that on a daily basis is increasing, and that’s all good to see.
45. I mean I continue to think that glasses are basically going to be the ideal form factor for AI because you can let an AI see what you see throughout the day, hear what you hear, talk to you.
46. And that’s also going to unlock a lot of value where you can just interact with an AI assistant throughout the day in this multimodal way.
47. And I think in the future, if you don’t have glasses that have AI or some way to interact with AI, I think you’re kind of similarly probably be at a pretty significant cognitive disadvantage compared to other people who you’re working with, or competing against.
48. So the whole metaverse vision, I think, is going to end up being extremely important, too, and AI is going to accelerate that, too.
49. It’s just that if you’d asked me five years ago, whether we’d have kind of holograms that created immersive experiences or superintelligence first, I think most people would have thought that you’d get the holograms first. ⚑ context-dependent
50. And it’s this interesting kind of quirk of the tech industry that I think we’re going to end up having really strong AI first.

### Susan Li, CFO
51. So I mean the impact of the sort of increased compensation costs including SBC, of our AI hires this year is reflected in the revised 2025 expense outlook and in the comments I made about sort of the 2026, expense outlook.

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Mark Zuckerberg, CEO] The people who are joining us will have access to unparalleled compute as we build out several multi-GW clusters.
2. [Prepared remarks · Susan Li, CFO] In terms of the specific line items: Cost of revenue increased 16%, driven mostly by higher infrastructure costs and payments to partners, partially offset by a benefit from the previously announced extension of server useful lives.
3. [Prepared remarks · Susan Li, CFO] R&D increased 23%, mostly due to higher employee compensation and infrastructure costs.
4. [Prepared remarks · Susan Li, CFO] Capital expenditures, including principal payments on finance leases, were $17.0 billion, driven by investments in servers, data centers and network infrastructure.
5. [Prepared remarks · Susan Li, CFO] Family of Apps expenses were up 14%, mainly due to growth in employee compensation and infrastructure costs, partially offset by lower legal-related costs.
6. [Prepared remarks · Susan Li, CFO] Our primary focus remains investing capital back into the business, with infrastructure and talent being our top priorities.
7. [Prepared remarks · Susan Li, CFO] Next, infrastructure.
8. [Prepared remarks · Susan Li, CFO] We expect having sufficient compute capacity will be central to realizing many of the largest opportunities in front of us over the coming years.
9. [Prepared remarks · Susan Li, CFO] The largest single driver of growth will be infrastructure costs, driven by a sharp acceleration in depreciation expense growth and higher operating costs as we continue to scale up our infrastructure fleet.
10. [Prepared remarks · Susan Li, CFO] Aside from infrastructure, we expect the second largest driver of growth to be employee compensation as we add technical talent in priority areas and recognize a full year of compensation expenses for employees hired throughout 2025.
11. [Prepared remarks · Susan Li, CFO] Turning now to the capex outlook.
12. [Prepared remarks · Susan Li, CFO] We currently expect 2025 capital expenditures, including principal payments on finance leases, to be in the range of $66-72 billion, narrowed from our prior outlook of $64-72 billion and up approximately $30 billion year-over-year at the mid-point.
13. [Prepared remarks · Susan Li, CFO] In closing, this was another strong quarter for our business as our investments in infrastructure and technical talent continue to improve core ads performance and engagement on our platforms.
14. [Q&A · Eric Sheridan] And Susan, building on Mark’s comments on scaling talent and compute, I wanted to know if you could go a little bit deeper in how we should be thinking about those two components driving some of the commentary you’ve given around OpEx and CapEx over the next 12 to 18 months.
15. [Q&A · Mark Zuckerberg, CEO] And that I think informs a lot of the decisions from everything from the importance and value of having the absolute best and most elite talent dense team at the company to making sure that we have a leading compute fleet so that the people here can do – so that the researchers here have more compute per person to be able to leave their research and then roll it out to billions of people across our products, making sure that we build and drive these products through all the different things that we do.
16. [Q&A · Susan Li, CFO] But there are certain aspects that we have some visibility into today including the rough shape of our 2026 infrastructure plans.
17. [Q&A · Susan Li, CFO] And so those two things are part of why we gave a little bit of an early preview into the expectations for growth for 2026 total expenses as well as for 2026 CapEx.
18. [Q&A · Susan Li, CFO] So on the total expenses side, as I mentioned, we expect infrastructure will be the single largest contributor to 2026 expense growth.
19. [Q&A · Susan Li, CFO] That’s driven primarily by a sharp acceleration in depreciation expense growth in 2026, largely driven by recognizing incremental depreciation from assets that we purchased and placed in service in ‘26 as well as from infrastructure deployed through 2025 that we’ll recognize a full year of depreciation next year.
20. [Q&A · Susan Li, CFO] We also expect a greater mix of our CapEx to be in shorter-lived assets in 2025 and ‘26 than it has been in prior years.
21. [Q&A · Susan Li, CFO] So a lot going on, on the infrastructure side as it contributes to the 2026 total expense number.
22. [Q&A · Douglas Anmuth, JPMorgan] And then, Susan, your comments on ‘26 CapEx suggest more than $100 billion of spend next year potentially.
23. [Q&A · Mark Zuckerberg, CEO] And yes, I mean I think Susan will talk a little bit more about the infrastructure, but it really is a massive investment.
24. [Q&A · Mark Zuckerberg, CEO] But we do take very seriously that this is a just massive amount of capital to convert into many gigawatts of compute which we think is going to help us produce leading research and quality products and running the business, I do look for opportunities to basically convert capital into quality of products that we can deliver for people.
25. [Q&A · Susan Li, CFO] Doug, on your second question about how we expect to finance the growing CapEx next year.
26. [Q&A · Susan Li, CFO] We certainly expect that we will finance some large share of that ourselves, but we’re also exploring ways to work with financial partners to codevelop data centers.
27. [Q&A · Justin Post, Bank of America] I’ll ask another one on the infrastructure.
28. [Q&A · Susan Li, CFO] So at present, we’re not really thinking about external use cases on the infrastructure, but I’d say it’s a good question.
29. [Q&A · Susan Li, CFO] On your second question, which is really around the sort of ROI on CapEx, there are a couple of things.
30. [Q&A · Susan Li, CFO] So we, again, are also -- I would say, the last thing I would add here is we are building the infrastructure with fungibility in mind.
31. [Q&A · Susan Li, CFO] Obviously there are a lot of things that you have to build up front in terms of the data center shells, the networking infrastructure, et cetera.
32. [Q&A · Susan Li, CFO] But we will be ordering servers, which ultimately will be the biggest bulk of CapEx spend as we need them and when we need them and making sort of the best decisions at those times in terms of figuring out where the capacity will go to use.
33. [Q&A · Mark Zuckerberg, CEO] And we think that there’s going to be a much higher return than we can do by generating that directly rather than just kind of renting or leasing out the infrastructure at other companies.
