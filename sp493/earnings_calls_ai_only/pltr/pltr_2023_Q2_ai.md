# Palantir Technologies — 2023_Q2 Earnings Call (transcript)

- **Company:** Palantir Technologies (PLTR); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** PLTR
- **CIK:** 0001321655
- **Period:** 2023_Q2 (call held August 7, 2023; date from page date line)
- **Calendar quarter:** 2023 Q2 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/08/07/palantir-technologies-pltr-q2-2023-earnings-call-t/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 2)
- **Source SHA-256:** 2529a65bfc9db57b78818b2001ce13d0cc82e6eec833dfb4b53a846fce261a11
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**69 AI sentences of 458 total**
(Borderline, listed at the end: 0 automation/robotics, 3 infrastructure, none containing an AI term.)

Source/parse flags: Q&A start not detected.

## Prepared remarks

### Alex Karp, Chief Executive Officer
1. Through the course of the last 20 years, we built what is inarguably one of the most interesting, impactful product offerings in the world, PGE, Foundry, our target selection platform, Apollo. ⚑ uncertain
2. In a weird way, in the last couple of months since we launched AIP, since we had AIPCon, we have seen the way in which technologies we built that seem to be of moderate utility were built almost in anticipation of the AI revolution, both algorithmatic and large language models.
3. We see a market, especially in the U.S., which is hungry for an ability to apply AI, both large language models and algorithms, to transform our businesses.
4. So buying Foundry appeared to many institutions is, well, of course, it's the best product, but it's -- it would require us to change how we function or change how we procure software. ⚑ uncertain
5. By the way, the large language model revolution has changed Palantir's relationships institutions because we were misaligned for years and years with IT all globally.
6. But the way in which you actually can process large language models to get more exact, more precise, more operationally valuable insights, the way you can actually write them safely into your enterprise, meaning you can control your enterprise, the way you can turn them into logic that allows you to power your enterprise, both in the read/write function with governance that is mandated by law or by ethics, we provide -- those ways of working are exactly the ways we always thought one would have to work.
7. So in the natural state, you would have something like Foundry, you would have an Ontology, you would have AIP. ⚑ uncertain
8. That state is apparent to people because of the enormous power, the power to accelerate time, change your business using large language models. ⚑ context-dependent
9. Now in -- while continuing to focus on that, we can focus on, OK, but given that we've built these precursor technologies, given that our product has moved from being nascent to having thousands of users, the AIP product, given that we believe that the reception to this is unlike anything we've seen in PGE, Foundry, Apollo, target selection, and given the receptivity of the market, also not to mention that we have been profitable now, we expect to be eligible for the S&P for several quarters. ⚑ uncertain

### Ryan Taylor, Chief Business Affairs and Legal Officer
10. This is a testament to our steadfast focus and commitment to delivering results and impact for our partners, all while innovating against the AI opportunities ahead. ⚑ context-dependent
11. Last quarter, we hosted AIPCon, which convened over 150 unique organizations, as we formally launched our new AIP product offering, and customers demonstrated how we're partnering with them to unlock the value of AI.
12. Power's chief digital and technology officer asserted that the advantage comes not from the AI models you can build but rather how you apply them to the data you have and deploy it into applications.
13. The CEO of Novartis was recently interviewed on CNBC, discussing our partnership in which we created an integrated data lake that they are now leveraging to move AI forward quickly within the company, which the CEO calls Novartis' "fundamental advantage" over its peers.
14. Looking at both existing and new customers, AIP is the solution for organizations who want to wheel the LLM securely in their enterprise.
15. Foundry is being used at numerous healthcare facilities to generate nurse schedules and forecast patient placements, among other applications. ⚑ uncertain
16. For example, with Foundry, HCA now generates nurse schedules in one hour each month instead of 10 to 20. ⚑ uncertain

### Shyam Sankar, Chief Operating Officer
17. At AIPCon this past June, we introduced Palantir's AI platform, a core set of technologies designed to bring LLMs to your enterprise to supercharge and accelerate your experiences.
18. From integrating data and hydrating your ontology to building AI-enabled applications and human agent teams with copilots.
19. AIP enables you to deploy LLMs anchored in your data on your private network and to safely orchestrate your enterprise with tools, actions, and other AI models, all of this in a controlled, governed, and trusted AI operating system.
20. The accelerating pace of AI developments continues to be awe-inspiring.
21. It is, in many ways, easier to define an LLM by what it is not. ⚑ context-dependent
22. It is not algorithmic reasoning. ⚑ uncertain ⚑ context-dependent
23. Algorithmic reasoning operates as a process so well specified that there is no ambiguity in its execution, like traditional code. ⚑ uncertain
24. Large language models occupy a middle ground between algorithmic reasoning and human thought.
25. They are not good at executing algorithms, yet they can be instructed in ordinary pros. ⚑ uncertain ⚑ context-dependent
26. They are something else, non-algorithmic compute. ⚑ uncertain ⚑ context-dependent
27. I'm going to unpack some of the foundational engineering challenges that we've solved to manage and harness the stochasticity of these models and to enable the acceleration in our products. ⚑ uncertain
28. AIP and LLMs radically accelerate the solutions.
29. To name a few, a nurse shift handoff copilot for HCA, our pharmacokinetics translation assistant for Novartis, an inventory balancer copilot for a plant-based protein company, a supply chain copilot for a major beverage company.
30. Our warranty claims copilot for a U.S. auto manufacturer has made analysts twice as productive, saving them three to four hours a day.
31. Power's CTO Bernardo said at AIPCon, "The beauty of having Foundry and AIP is that you can build this really, really quickly," so we built this in a matter of days and iterate it in a couple of weeks. ⚑ uncertain
32. To get the precision of calculus and the power of statistics, LLMs need to be paired with algorithmic and software tools.
33. For example, models of forward inventory or an action registry to execute enterprise functions, a rich semantic layer to define the proper grounding and crucial primitives like scenarios that allow LLM to stage changes on branches.
34. LLMs can't, for example, calculate profitability or expected lead times, but they don't have to.
35. It elegantly integrates LLMs into the calculus of your enterprise to accelerate the workflows that matter. ⚑ context-dependent
36. AIP Terminal is the command line for your AI operating system, enabling you to dynamically wield your ontology tools and applications for ad hoc exploration and problem solving.
37. AIP Logic enables you to build LLM-backed functions with rich tool composition in its developer tool chain.
38. And AIP Automate lets you turn those logic functions into agents, copilots, and automations.
39. One more item in this suite I want to highlight, AIP Assist, which accelerates all of today's uses and users of AIP, Gotham, and Foundry by providing help and helpers dynamically. ⚑ uncertain
40. We continue to invest in capabilities, delivering the next level of deterrents through the AI-enabled kill chain, inclusive of an integrated coalition deterrent.

### Ana Soro
41. Our first question is from Gaurav who asks, what are some of the AI advantages Palantir has that none of the other companies can compete with?

### Shyam Sankar, Chief Operating Officer
42. Palantir is optimally positioned for AI because the value is going to accrete to the incumbents.
43. The problems that you should be solving with LLMs haven't changed.
44. It's the same problems you should be solving before you had LLMs, and the two decades of experience we have and the knowledge of applying it means that we can solve those problems substantially more quickly. ⚑ context-dependent
45. In other words, we've built the infrastructure you really need for LLMs to be valuable in your enterprise, if you want to write profits and not poems with them.
46. And I think one way you can think about this is LLMs and Excel, like the LLMs are going to make Excel more valuable and useful.
47. The LLMs that we've been building with our customers in the field in the last 10 weeks I've been out there with our customers, we deployed over 15 copilots.
48. I talked earlier in the remarks about how LLMs are statistics, not calculus.
49. Why on earth would you ask a question of one LLM, when you can ask KLLMs?
50. And you can use this to actually wield these LLMs for decisive operational advantage in the enterprise when you have this sort of framework.

### Ana Soro
51. Our next question is from Patrick who asks, how is the use of AI and LLMs benefited the sales cycle?

### Ryan Taylor, Chief Business Affairs and Legal Officer
52. And what we're seeing is with the emergence of LLM's AI capabilities, operators and organizations are looking at ways to deploy those within their organizations effectively against their missions and do so safely and securely.

### Alex Karp, Chief Executive Officer
53. We had built products, both Foundry and the Ontology branching and lots of ideas of how to manage large-scale data sets and then algorithms of classified setting. ⚑ uncertain
54. And if you look at what Shyam is saying and what Ryan is saying, what you're really seeing is American industry now has done five, six iterations, often within technologies with thick salesforces that kind of have been supported by the venture capital community, and quite frankly, by analysts looking for models they understood. ⚑ uncertain
55. We went deep on technology, that's Foundry. ⚑ uncertain

### Alex Karp, Chief Executive Officer
56. And the operators, so the people actually running the business in America realized the determinant variable for changing their margins, changing their profit, and outmaneuvering their competition is AI.
57. These problems can only be solved algorithmatically, but I can't solve them unless I have a governance structure that allows me to solve them because my board will go nuts." ⚑ uncertain ⚑ context-dependent
58. One of the advantages of AI is that if you want to do manufacturing, so you want to do Japanese manufacturing in America, you're actually having to use Japanese methodologies with American workers.
59. AI can actually allow you to manage the internal dynamics of your workforce so that you get the Japanese culture with American workers in the U.S., and this is just absolutely game-changing for our country.

### Shyam Sankar, Chief Operating Officer
60. And then when you can deliver 15 copilots in nine weeks, it's -- you just get so much more pull on that.

### Mariana Perez Mora, Bank of America Merrill Lynch, Analyst
61. And second, on the other conversations we're having with like 300-plus organizations, how many of those are willing to use it on a Foundry platform versus their own? ⚑ uncertain

### Shyam Sankar, Chief Operating Officer
62. We've done this with Gaia, with Foundry, with Apollo. ⚑ uncertain

### Alex Karp, Chief Executive Officer
63. People who don't have Foundry, how does it work? ⚑ uncertain

### Shyam Sankar, Chief Operating Officer
64. I think the real focus on the AIP product strategy is to make sure that you can use AIP without Gotham, Foundry or Apollo. ⚑ uncertain
65. When I think about the work we're doing with pharma companies and many of the AI models that they've already built, this actually helps them close that last mile where they feel like, look, we have these exquisite models.
66. And then you see these sort of hybrid architectures emerging where you have AIP, you have Foundry, you have their homegrown systems working quite harmoniously against the ambitious problem. ⚑ uncertain
67. And I think the good part about this because it's so generative right now is that there is no reference architecture.

### Alex Karp, Chief Executive Officer
68. So you do have an advantage if you already have Foundry because we've already kind of pre-taught you where the road is going to go. ⚑ uncertain
69. I need what Shyam's calling ontology's ability to interact with LLM.

## Q&A

_No AI sentences in this section._

## Borderline: automation/robotics without an AI term

_None._

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Ryan Taylor, Chief Business Affairs and Legal Officer] For example, Jacobs Engineering highlighted how AIP is enabling them to monitor current system conditions and conduct future infrastructure planning in real time versus the months of analysis it would have taken previously.
2. [Prepared remarks · Ryan Taylor, Chief Business Affairs and Legal Officer] In Q2, we closed deals in U.S. commercial in roughly 30 different industries, including across pharmaceuticals, energy, consumer staples, utilities, healthcare, construction, automotive, transportation infrastructure, the list goes on and spans industries and institutions at the core of today's society.
3. [Prepared remarks · Shyam Sankar, Chief Operating Officer] It's obvious the infrastructure we've built and how that enables you to actually accomplish these ambitious use cases.
