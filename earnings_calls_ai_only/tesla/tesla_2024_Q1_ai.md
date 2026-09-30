# Tesla, Inc. (TSLA) — 2024 Q1 Earnings Call (transcript)

- **Company:** Tesla, Inc. (TSLA)
- **Period:** 2024 Q1
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2024/04/23/tesla-tsla-q1-2024-earnings-call-transcript/
- **Note:** the company does not publish an official transcript. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing.
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**71 AI sentences of 629 total**
(Borderline, listed at the end: 7 automation/robotics, 16 infrastructure, none containing an AI term.)

## Prepared remarks

### Elon Musk, Chief Executive Officer and Product Architect
1. We also continue to expand our AI training capacity in Q1 more than doubling our training compute sequentially.
2. Regarding FSD Version 12, which is the pure AI-based self-driving, if you haven't experienced this, I strongly urge you to try it out, it's profound.
3. And we've now turned that on for all cars with the cameras and inference computer everything from Hardware 3 on in North America. ⚑ uncertain
4. So, we now have over 300 billion miles that have been driven with FSD V12 since the launch of full self-driving -- supervised full self-driving. ⚑ uncertain
5. It's become very clear that the vision-based approach with end-to-end neural networks is the right solution for scalable autonomy. ⚑ context-dependent
6. Our entire road network is designed for biological neural nets and eyes.
7. So, naturally, cameras and digital neural nets are the solution to our current road system.
8. And as we've announced, we will be showcasing our purpose-built robotaxi or Cybercab in August. ⚑ uncertain
9. Regarding AI compute, over the past few months, we've been actively working on expanding Tesla's core AI infrastructure.
10. We've installed and commissioned, meaning they're actually working 35,000 H100 computers or GPUs. ⚑ uncertain
11. So, in conclusion, we're super excited about our autonomy road map. ⚑ uncertain
12. And we're really headed for an electric vehicle and autonomous future. ⚑ uncertain
13. And I go back to something I said several years ago that in the future, gasoline cars that are not autonomous will be like riding a horse and using a flip phone. ⚑ uncertain

### Vaibhav Taneja, Chief Financial Officer
14. The impact of pricing actions was largely offset by reductions in per-unit costs and the recognition of revenue from Autopilot feature for certain vehicles in the U.S. that previously did not have that functionality. ⚑ uncertain
15. On the operating expense front, we saw a sequential increase from our AI initiatives, continued investment in future projects, marketing, and other activities.
16. The primary driver of this was an increase in inventory from a mismatch between builds and deliveries as discussed before, and our elevated spend on capex across various initiatives, including AI compute.
17. The savings from these initiatives, including our cost reductions will help improve our overall profitability and ultimately enable us to increase the scale of our investments in AI.

### Elon Musk, Chief Executive Officer and Product Architect
18. And I think Tesla is best positioned of any humanoid robot maker to be able to reach volume production with efficient inference on the robot itself. ⚑ uncertain
19. I mean, this, perhaps, is a point that is worth emphasizing Tesla's AI inference efficiency is vastly better than any other company.
20. There's no company even close to the inference efficiency of Tesla. ⚑ uncertain
21. We've had to do that because we were constrained by the inference hardware in the car. ⚑ uncertain
22. Martin Viecha The third question is, what is the current assessment of the pathway toward regulatory approval for unsupervised FSD in the U.S.? ⚑ uncertain

### Lars Moravy, Vice President, Vehicle Engineering
23. There are a handful of states that already have adopted autonomous vehicle laws. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
24. It's actually been pretty helpful that the autonomous car companies have been cutting a path through the regulatory jungle. ⚑ uncertain ⚑ context-dependent
25. I think if you've got at scale, a statistically significant amount of data that shows conclusively that the autonomous car has, let's say, half the accident rate of a human-driven car, I think that's difficult to ignore because at that point, stopping autonomy means killing people. ⚑ uncertain
26. So, I actually do not think that there will be significant regulatory barriers provided, there was conclusive data that the autonomous car is safer than a human-driven car. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
27. I think there's also some potential here for an AWS element down the road where if we've got very powerful inference because we've got a Hardware 3 in the cars, but now all cars are being made with Hardware 4. ⚑ uncertain
28. And there's a potential to run -- when the car is not moving to actually run distributed inference. ⚑ uncertain
29. So, kind of like AWS, but distributed inference. ⚑ uncertain
30. Like it takes a lot of computers to train an AI model, but many orders of magnitude less compute to run it.
31. So, if you can imagine future, perhaps where there's a fleet of 100 million Teslas, and on average, they've got like maybe a kilowatt of inference compute.
32. That's 100 gigawatts of inference compute distributed all around the world. ⚑ context-dependent
33. It's pretty hard to put together 100 gigawatts of AI compute. ⚑ context-dependent
34. And even in an autonomous future where the car is, perhaps, used instead of being used 10 hours a week, it is used 50 hours a week. ⚑ uncertain
35. That still leaves over 100 hours a week where the car inference computer could be doing something else. ⚑ uncertain ⚑ context-dependent

### Ashok Elluswamy, Director, Autopilot Software
36. We have multiple years of validating the safety for in any given week, we train hundreds of neural networks that can produce different trajectories for how to drive the car, replay them through the millions of clips that we have already collected from our users and our own QA those are like critical events, like someone jumping out in front or like other critical events that we have gathered database over many, many years, and we replay through all of them to make sure that we are net improving safety.
37. And especially with the new V12 architecture, all of this is automatically improving without requiring much engineering interventions in the sense that engineers don't have to be creative and like how they code the algorithms. ⚑ uncertain
38. We add it to the neural network, and it learns from that trained data automatically instead of some engineers saying that, oh, here, you must rotate the steering wheel by this much or something like that.
39. There's no hard inference conditions. ⚑ uncertain
40. Everything is neural network.

### Elon Musk, Chief Executive Officer and Product Architect
41. So, if we look at, say, 12.4 and 12.5, which are really -- could arguably even be Version 13, Version 14 because it's pretty close to a total retrain of the neural nets in each case are substantially different.

### Ashok Elluswamy, Director, Autopilot Software
42. You can increase the amount of data you use to train the neural network and that also gives similar gains and you can also scale up by training compute, you can train it for much longer and one more GPUs or more dojo nodes that also gives better performance, and you can also have architecture scaling where you count with better architectures for the same amount of compute produce better results.
43. So, a combination of model size scaling, data scaling, training compute scaling and the architecture scaling, we can basically extrapolate, OK, with the continue scaling based at this ratio, we can perfect big future performance.

### Elon Musk, Chief Executive Officer and Product Architect
44. But really, the way to think of Tesla is almost entirely in terms of solving autonomy and being able to turn on that autonomy for a gigantic fleet. ⚑ uncertain
45. And I think it might be the biggest asset value appreciation history when that day happens when you can do unsupervised full self-driving. ⚑ uncertain

### Lars Moravy, Vice President, Vehicle Engineering
46. The next question, have any of the legacy automakers contacted Tesla about possibly licensing FSD in the future? ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
47. We're in conversations with one major automaker regarding licensing FSD. ⚑ uncertain
48. The next question is about the robotaxi. ⚑ uncertain

### Lars Moravy, Vice President, Vehicle Engineering
49. So, our favorite, can we make FSD transfer permanent until FSD is fully delivered with Level 5 autonomy? ⚑ uncertain

## Q&A

### Adam Jonas, Morgan Stanley, Analyst
1. If you had nailed execution, assuming that you nail execution on your next-gen cheaper vehicles, more aggressive giga castings, I don't want to say one piece, but getting closer to, say, one-piece structural pack, unboxed, 300-mile range, $25,000 price point, putting aside robotaxi, those features unique to you. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
2. Like really, we should be thought of as an AI or robotics company.
3. So, I mean, if somebody doesn't believe Tesla is going to solve autonomy, I think they should not be an investor in the company. ⚑ uncertain

### Vaibhav Taneja, Chief Financial Officer
4. I think that's the key thing to remember, right, especially if you look at FSD Supervised, if you didn't believe in autonomy, this should give you a review that this is coming. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
5. If you've not tried the FSD 12.3, and like I said, 12.4 is going to be significantly better and 12.5 even better than that. ⚑ uncertain

### Vaibhav Taneja, Chief Financial Officer
6. But here, we have more than a car company because the cars can be autonomous. ⚑ uncertain

### Ashok Elluswamy, Director, Autopilot Software
7. This is all in addition to Testa AI community is just like increasing -- improving rapidly. ⚑ context-dependent

### Alex Potter, Piper Sandler, Analyst
8. The thesis hinges completely on AI, the future of AI, full self-driving neural net training, all of these things.

### Elon Musk, Chief Executive Officer and Product Architect
9. Well, I think no matter what Tesla -- even if I get kidnapped by aliens tomorrow, Tesla will solve autonomy, maybe a little slower, but it would solve autonomy for vehicles at least. ⚑ uncertain
10. I don't know if we would win on with respect to Optimus or with respect to future products, but it would that -- that there's enough momentum for Tesla to solve autonomy even if I disappeared for vehicles. ⚑ uncertain

### Mark Delaney, Goldman Sachs, Analyst
11. The company previously characterized potential FSD licensing discussions in the early phase and some OEMs had not really been believing in it. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
12. I think we've now with 12.3, if you just have the car drive you around, it is obvious that our solution with a relatively low-cost inference computer and standard cameras can achieve self-driving. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
13. So, it really just be a case of having them use the same cameras and inference computer and licensing our software. ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
14. even though all you need is cameras and our inference computer. ⚑ uncertain

### George Gianarikas, Canaccord Genuity, Analyst
15. First, could you please help us understand some of the timing of launching FSD in additional geographies, including maybe clarifying your recent comment about China? ⚑ uncertain

### George Gianarikas, Canaccord Genuity, Analyst
16. And FSD new markets? ⚑ uncertain

### Elon Musk, Chief Executive Officer and Product Architect
17. So, think about the end-to-end neural net-based autonomy is that just like a human, it actually works pretty well without modification in almost any market.
18. So, we plan on -- with the approval of the regulators, releasing it as a supervised autonomy system in any market that -- where we can get regulatory approval for that, which we think includes China. ⚑ uncertain

### Colin Rusch, Oppenheimer and Company, Analyst
19. Given the pursuit of Tesla really as a leader in AI for the physical world, in your comments around distributed inference, can you talk about what that approach is unlocking beyond what's happening in the vehicle right now?

### Ashok Elluswamy, Director, Autopilot Software
20. Like Elon mentioned, like the car, even when it's a full robotaxi, it's probably going to be used for 150 hours a week. ⚑ uncertain

### Ashok Elluswamy, Director, Autopilot Software
21. It could be more or less, but then there's certainly going to be some hours left for charging and cleaning and maintenance in that world, you can do a lot of other workloads, even right now, we are seeing, for example, the LLM companies have these batch workloads where they send a bunch of documents and those are run through pretty large neural networks and take a lot of compute to chunk through those workloads. ⚑ context-dependent

### Elon Musk, Chief Executive Officer and Product Architect
22. So, for the car, even if you're a kilowatt-level inference computer, which is crazy power compared to a phone. ⚑ uncertain

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Lars Moravy, Vice President, Vehicle Engineering] The second question is on Optimus.
2. [Prepared remarks · Lars Moravy, Vice President, Vehicle Engineering] So, what is the current status of Optimus?
3. [Prepared remarks · Elon Musk, Chief Executive Officer and Product Architect] We do think we will have Optimus in limited production in the natural factory itself, doing useful tasks before the end of this year.
4. [Prepared remarks · Elon Musk, Chief Executive Officer and Product Architect] As I've said before, I think Optimus will be more valuable than everything else combined.
5. [Prepared remarks · Elon Musk, Chief Executive Officer and Product Architect] Because if you've got a sentient humanoid robots that is able to navigate reality and do tasks at request, there is no meaningful limit to the size of the economy.
6. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] I'll be more reticent with respect to Optimus, if we have a super-sentient humanoid robot that can follow you indoors and that you can escape, we're talking terminator-level risk.
7. [Q&A · Lars Moravy, Vice President, Vehicle Engineering] I mean, in short, yes, I mean, like the on-box manufacturing method is certainly great and revolutionary, but with it comes some risks because new production lines and not, but all the subsystems we developed, whether it was powertrains, drive units, battery improvements in manufacturing and automation, thermal systems, seating, integration of interior components and reduction of LV controllers, all that's transferable, and that's what we're doing, trying to get it in their products as fast as possible.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Elon Musk, Chief Executive Officer and Product Architect] GPU is wrong word.
2. [Prepared remarks · Elon Musk, Chief Executive Officer and Product Architect] I always feel like a wince when I say GPU because it's not.
3. [Prepared remarks · Elon Musk, Chief Executive Officer and Product Architect] GPU stand -- G stands for graphics, and it doesn't do graphics.
4. [Prepared remarks · Vaibhav Taneja, Chief Financial Officer] We are also getting hyper-focused on capex efficiency and utilizing our installed capacity in a more efficient manner.
5. [Prepared remarks · Lars Moravy, Vice President, Vehicle Engineering] But as you mentioned, we're updating our future vehicle lineup to accelerate the launch of our low-cost vehicles in a more capex-efficient way.
6. [Prepared remarks · Lars Moravy, Vice President, Vehicle Engineering] These new vehicles we built on our existing lines and open capacity, and that's a major shift to utilize all our capacity with marginal capex before we go spend high capex.
7. [Q&A · Ashok Elluswamy, Director, Autopilot Software] And now that we have already paid for this compute in these cars, it might be wise to use them and not let them be like buying a lot of expensive machinery and leaving to them idle.
8. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] But they found that they had excess compute because the compute needs would spike to extreme levels for brief periods of the year and then they had idle compute for the rest of the year.
9. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] So, then what should they do to pull that excess compute for the rest of the year.
10. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] And then I mean if you get like to the 100 million vehicle level, which I think we will, at some point, get to, then -- and you've got a kilowatt of useable compute and maybe your own Hardware 6 or 7 by that time.
11. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] Then you really -- I think you could have on the order of 100 gigawatts of useful compute, which might be more than anyone, more than any company, probably more than any company.
12. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] We've already learned about deploying workloads to these compute nodes.
13. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] Well, you're just draining the battery on the phone, so like technically, I suppose like Apple would have the most amount of distributed compute, but you can't use it because you can't get the -- you can't just run the phone at full power and drain the battery.
14. [Q&A · Elon Musk, Chief Executive Officer and Product Architect] It could be plugged in or not like you could run for 10 hours and use 10 kilowatt hours of your kilowatt of compute power.
15. [Q&A · Lars Moravy, Vice President, Vehicle Engineering] Yes, it's exactly for data centers.
16. [Q&A · Vaibhav Taneja, Chief Financial Officer] And the capex is shared by the entire world.
