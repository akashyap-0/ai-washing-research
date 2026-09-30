# NVIDIA Corporation — Q2 FY24 Earnings Call (transcript)

- **Company:** NVIDIA (NVDA); fiscal year ends late January
- **Period:** Q2 FY24 (call held Aug 23, 2023)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2023/08/23/nvidia-nvda-q2-2024-earnings-call-transcript/
- **Note:** NVIDIA does not host an official transcript for this call. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing.
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**138 AI sentences of 470 total**
(Borderline, listed at the end: 1 automation/robotics, 56 infrastructure, none containing an AI term.)

## Prepared remarks

### Colette Kress, Executive Vice President, Chief Financial Officer
1. Data center compute revenue nearly tripled year on year driven primarily by accelerating demand for cloud from cloud service providers and large consumer internet companies for our HGX platform, the engine of generative and large language models.
2. Major companies including AWS, Google Cloud, Meta, Microsoft Azure, and Oracle Cloud, as well as a growing number of GPU cloud providers are deploying in-volume HGX systems based on our Hopper and Ampere architecture tensor core GPUs. ⚑ uncertain
3. Networking revenue almost doubled year on year driven by our end-to-end InfiniBand networking platform, the gold standard for AI.
4. There is tremendous demand for Nvidia accelerated computing and AI platforms.
5. Our data center supply chain, including HGX, with 35,000 parts and highly complex networking, has been built up over the past decade. ⚑ uncertain
6. By geography, data center growth was strongest in the U.S. as customers direct their capital investments to AI and accelerated computing.
7. Our cloud service providers drove exceptional strong demand for HGX systems in the quarter as they undertake a generational transition to upgrade their data center infrastructure for the new era of accelerated computing and AI.
8. The NVIDIA HGX platform is culminating of nearly two decades of full-stack innovation across silicon, systems, interconnects, networking, software, and algorithms. ⚑ uncertain
9. Instances powered by the NVIDIA H100 tensor core GPUs are now generally available at AWS, Microsoft Azure, and several GPU cloud providers, with others on the way shortly. ⚑ uncertain
10. Their investments in data center infrastructure purpose-built for AI are already generating significant returns.
11. For example, Meta recently highlighted that, since launching reels and AI recommendations, have driven a more than 24% increase in time spent on Instagram.
12. Enterprises are also racing to deploy generative AI, driving strong consumption of Nvidia-powered instances in the cloud, as well as demand for on-premise infrastructure.
13. Whether we serve customers in the cloud or on-prem through partners or direct, their applications can run seamlessly on Nvidia AI Enterprise software with access to our acceleration libraries, pre-trained models, and APIs.
14. We announced a partnership with Snowflake to provide enterprises with accelerated paths to create customized generative AI applications using their own proprietary data, all securely within the Snowflake data cloud.
15. With the NVIDIA NeMo platform for developing large language models, enterprises will be able to make custom LLMs for advanced AI services, including chatbots, search, and summarization right from the Snowflake data cloud.
16. Virtually every industry can benefit from generative AI.
17. For example, AI co-pilot, such as those just announced by Microsoft, can boost the productivity of over a billion office workers and tens of millions of software engineers.
18. Millions of professionals in legal services, sales, customer support, and education will be available to leverage AI systems trained in their fields.
19. We are seeing some of the earliest applications of generative AI in marketing, media, and entertainment.
20. WPP, the world's largest marketing and communication services organization, is developing a content engine using Nvidia Omniverse to enable artists and designers to integrate generative AI into 3D content creation.
21. WPP designers can create images from text prompts while responsibly train generative AI tools and content from Nvidia partners such as Adobe and Getty Images using NVIDIA Picasso, a foundry for custom generative AI models for visual design.
22. Visual content provider Shutterstock is also using NVIDIA Picasso to build tools and services that enable users to create 3D scene backgrounds with the help of generative AI.
23. We partnered with ServiceNow and Accenture to launch the AI Lighthouse program, fast-tracking the development of enterprise AI capabilities.
24. AI Lighthouse unites the ServiceNow enterprise automation platform and engine with Nvidia accelerated computing and with Accenture consulting and deployment services.
25. We are collaborating also with Hugging Face to simplify the creation of new and custom AI models for enterprises.
26. Hugging Face will offer a new service for enterprises to train and tune advanced AI models powered by NVIDIA DGX Cloud.
27. And just yesterday, VMware and Nvidia announce a major new enterprise offering called VMware Private AI Foundation with Nvidia, a fully integrated platform featuring AI software and accelerated computing from Nvidia, with multi-cloud software for enterprises running VMware.
28. VMware's hundreds of thousands of enterprise customers will have access to the infrastructure, AI, and cloud management software needed to customize models and run generative AI applications such as intelligent chatbot assistance, search, and summarization.
29. We also announced new NVIDIA AI Enterprise-ready servers featuring the new NVIDIA L40S GPU built for the industry-standard data center server ecosystem and BlueField-3 DPU data center infrastructure processor.
30. L40S is a universal data center processor designed for high-volume data center scaling out to accelerate the most compute-intensive applications including AI training and [Inaudible], 3D design and visualization, video processing, and NVIDIA Omniverse industrial digitalization.
31. NVIDIA AI Enterprise-ready servers are fully optimized for VMware Cloud Foundation and Private AI Foundation.
32. Nearly 100 configurations of NVIDIA AI Enterprise-ready servers will soon be available from the world's leading enterprise IT computing companies including Dell, HPE, and Lenovo.
33. The GH200 Grace Hopper Superchip, which combines our Arm-based Grace CPU with Hopper GPU, entered full production and will be available this quarter in OEM servers. ⚑ uncertain
34. And Nvidia and SoftBank are collaborating on a platform based on GH200 for generative AI and 5G/6G applications.
35. The second-generation version of our Grace Hopper Superchip with the latest HBM GPU memory will be available in Q2 of calendar 2024. ⚑ uncertain
36. We announced the DGX GH200, a new class of large memory AI supercomputer for giant AI language models, recommender systems, and data analytics.
37. This is the first use of the new NVIDIA NVLink Switch System enabling all of its 256 Grace Hopper superchips to work together as one, a huge jump compared to our prior generation connecting just eight GPUs on NVIDIA Link. ⚑ uncertain ⚑ context-dependent
38. DGX GH200 systems are expected to be available by the end of the year, Google Cloud, Meta, and Microsoft among the first to gain access. ⚑ uncertain
39. Strong networking growth was driven primarily by InfiniBand infrastructure to connect HGX GPU systems. ⚑ uncertain
40. Thanks to its end-to-end optimization and in-network computing capabilities, InfiniBand delivers more than double the performance of traditional Ethernet for AI.
41. For billions-of-dollar AI infrastructures, the value from the increased throughput of InfiniBand is worth hundreds of millions and pays for the network.
42. It is the network of choice for leading AI practitioners. ⚑ context-dependent
43. For Ethernet-based cloud data centers that seek to optimize their AI performance, we announced NVIDIA Spectrum-X, an accelerated networking platform designed to optimize Ethernet for AI workloads.
44. Spectrum-X couples the spectrum for the Ethernet switch with the BlueField-3 DPU, achieving 1.5x better overall AI performance and power efficiency versus traditional Ethernet.
45. We are bringing generative AI to games.
46. At Computex, we announced NVIDIA Avatar Cloud Engine [Inaudible] for games, a custom AI model foundry service.
47. It harnesses a number of NVIDIA Omniverse and AI technologies including NeMo Riva and Audio2Face. ⚑ context-dependent
48. These will include powerful new RTX systems with up to four NVIDIA RTX 6000 GPUs, providing more than 5,800 teraflops of AI performance and 192 gigabytes of GPU memory. ⚑ context-dependent
49. They can be configured with NVIDIA AI Enterprise or NVIDIA Omniverse Enterprise. ⚑ context-dependent
50. We also announced three new desktop workstation GPUs based on the Ada generation, the NVIDIA RTX 5000, 4500, and 4000, offering up to 2x the RT core throughput and up to 2x faster AI training performance compared to the previous generation.
51. In addition to traditional workloads such as 3D design and content creation, new workloads and generative AI, large language model development, and data science are expanding the opportunities in pro visualization for our RTX technology.
52. One of the key themes in Jensen's keynote at SIGGRAPH earlier this month was the convergence of graphics and AI.
53. This is where NVIDIA Omniverse is positioned. ⚑ uncertain ⚑ context-dependent
54. Omniverse is OpenUSD data platform. ⚑ uncertain
55. We announced new and upcoming Omniverse Cloud APIs, including RunUSD and ChatUSD to bring generative AI to OpenUSD workloads.
56. Solid year-on-year growth was driven by the ramp of self-driving platforms based on NVIDIA DRIVE Orin SoC with a number of new energy vehicle makers. ⚑ uncertain
57. Demand for our data center platform for AI is tremendous and broad-based across industries and customers.
58. We will attend the Jefferies Tech Summit on August 30th in Chicago, the Goldman Sachs Tech Conference on September 5th in San Francisco, the Evercore Semiconductor Conference on September 6th, as well as the Citi Tech Conference on September 10th, both in New York, and the BofA Virtual AI Conference on September 11th.

## Q&A

### Matt Ramsay, TD Cowen, Analyst
1. Jensen, I wanted to ask a question of you regarding the really quickly emerging application of -- of large model inference.
2. A lot of the smaller market -- smaller -- smaller model inference workloads have been done on ASICs or CPUs in the past.
3. And with many of these GPT and other really large models, there's this new workload that's accelerating super-duper quickly on -- on large model inference.
4. And I think your -- your Grace Hopper Superchip products and others are pretty well aligned for that. ⚑ uncertain
5. But could you maybe talk to us about how you're seeing the inference market segment between small model inference and large model inference and how your product portfolio is positioned for that?

### Jensen Huang, President and Chief Executive Officer
6. These large language models are -- are fairly -- are pretty phenomenal. ⚑ context-dependent
7. What happens is you create these large language models and you create as large as you can, and then you derive from it smaller versions of the model, essentially teach-your-student models.
8. And -- and so, when you see these smaller -- smaller models, it's very likely the case that they were derived from or distilled from or learned from larger models, and just as you have professors and teachers and students and so on, so forth. ⚑ uncertain
9. And so, you start from a very large model and it has to build -- it has a large amount of generality and generalization and -- and what's called zero-shot capability. ⚑ uncertain
10. And so, for a lot of applications and questions or skills that you haven't trained it specifically on, these large language models, miraculously, has the capability to perform them.
11. These smaller models might have excellent capabilities in a particular skill, but they don't generalize as well. ⚑ uncertain ⚑ context-dependent
12. And so, they all have their own -- own unique capabilities, but -- but you start from very large models. ⚑ uncertain

### Vivek Arya, Bank of America Merrill Lynch, Analyst
13. So, what is giving you the confidence that they can continue to carve out more of that pie for generative AI?
14. So, if I take your implied Q3 outlook of data center, 12 billion,13 billion, what does that say about how many servers are already AI accelerated?

### Colette Kress, Executive Vice President, Chief Financial Officer
15. It is a work across so many different suppliers, so many different parts of building, and -- and HGX many of our other new products that are coming to market. ⚑ uncertain ⚑ context-dependent

### Jensen Huang, President and Chief Executive Officer
16. And that trillion dollars of data centers is in the process of transitioning into accelerated computing and generative AI.
17. And so -- so, what you're seeing -- and then, all of a sudden enabled by generative AI -- enabled by accelerated computing, generative AI came along.
18. You're seeing the -- the data centers around the world are taking that capital spend and focusing it on the two most important trends of -- of computing today, accelerated computing and generative AI.

### Stacy Rasgon, AllianceBernstein, Analyst
19. I was wondering, Colette, if you could tell me like how much of data center in the quarter, maybe even the guidance, like, systems versus GPU, like DGX versus just the H100. ⚑ uncertain

### Colette Kress, Executive Vice President, Chief Financial Officer
20. Within the quarter, our HGX systems were a very significant part of our data center as well as our data center growth that we had seen. ⚑ uncertain
21. Those systems include our HGX of our Hopper architecture but also our Ampere architecture. ⚑ uncertain ⚑ context-dependent
22. But again, the largest driver of our revenue within this last quarter was definitely the HGX system. ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
23. The -- you -- you say it's H100, and I know you know what your -- your -- your mental image in your mind, but the H100 is 35,000 parts, 70 pounds, nearly a trillion transistors in combination; takes a robot to build -- well, many robots to build because it's 70 pounds to lift. ⚑ uncertain
24. And so -- so I think we -- you know, we call it H100 as if it's a chip that comes off of a fab, but H100s go -- go out really as HGX as they are the world's hyperscalers, and -- and they're really really quite large system components, if you will. ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
25. So, we have a runtime score in the AI enterprise.
26. And this is -- this is, if you will, the runtime that just about every company uses for the end-to-end of machine learning, from data processing, the training of any model that you -- that you like to do on any framework you like to do, the inference, and the deployment, the scaling it out into data center, could be a scale-out for a hyperscale data center, could be a scale-out for enterprise data center, for example, on VMware.
27. So, this runtime called NVIDIA AI Enterprise has something like 4,500 software packages, software libraries and has something like 10,000 dependencies among each other.
28. The flexibility, the versatility, and the performance of our architecture makes it possible for us to do all the things that I just said, you know, from data processing to training, to inference, for preprocessing of the data before you do the inference, to the post-processing of the data, tokenizing of -- of -- of -- of languages so that you could then train -- train with it. ⚑ uncertain
29. The amount of the workflow is much more intense than just training or inference. ⚑ uncertain
30. They use it for internal consumption, you know, to develop and train and operate recommender systems or search or data processing engines and whatnot, all the way to training and inference. ⚑ uncertain ⚑ context-dependent
31. And we've been working together for several years now and we're going to bring together -- together, we're going to bring generative AI to the world's enterprises all the way out to the edge.
32. And then, lastly, because of our scale and velocity, we were -- we were able to sustain this -- this really complex stack of software and hardware and networking and compute and across all of these different usage models and different computing environments. ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
33. H100 is designed for large-scale language models and processing, just very large models and a great deal of data.
34. L40S' focus is to be able to fine-tune models -- fine-tune pre-trained models and it'll do that incredibly well.
35. And that's the reason why HPE, Dell, and Lenovo, and some 20 other system makers building about 100 different configurations of enterprise servers are going to work with us to take generative AI to the world's enterprise.
36. It's, of course, large language models. ⚑ context-dependent
37. It's, of course, generative AI, but it's a different use case. ⚑ context-dependent

### Jensen Huang, President and Chief Executive Officer
38. The best way for companies to increase their throughput, improve their energy efficiency, improve their cost efficiency, is to divert their capital budget to accelerated computing and generative AI.
39. And -- and so, what you're seeing companies do now is recognizing this -- this, the tipping point here, recognizing the beginning of this transition, and diverting their capital investment to accelerated computing and generative AI.

### Toshi Hari, Goldman Sachs, Analyst
40. You know, given your position as the key enabler of AI, the breadth of engagements and the visibility you have into customer projects, I'm curious how confident you are that there will be enough applications or use cases for your customers to generate a reasonable return on their investments.

### Jensen Huang, President and Chief Executive Officer
41. And what kicked it into turbocharge is generative AI.
42. Going forward, the best way to invest in a data center is to divert the capital investment from general-purpose computing and focus it on generative AI and accelerated computing.
43. Generative AI provides a new way of generating productivity, a new way of generating new services to offer to your customers, and accelerated computing helps you save money and save power.
44. But you're seeing the regional GPU specialists -- service providers all over the world now, and -- and -- and because they all recognize the same thing, that the best way to invest your capital going forward is to put it into accelerated computing and generative AI.
45. And all of the generative AI libraries that we've been working on is now going to be offered as a special SKU by VMware's sales force, which is, as we all know, quite large because they reach some several hundred thousand VMware customers around the world.
46. And this new SKU is going to be called VMware Private AI Foundation.
47. And in combination with HPE, Dell, and Lenovo's new server offerings based on L40S, any -- any enterprise could have a state-of-the-art AI data center and be able to engage generative AI.

### Jensen Huang, President and Chief Executive Officer
48. And so, if you have a -- a single application, if you will, infrastructure or it's largely dedicated to large language models or large AI systems, InfiniBand is really -- really a terrific choice.
49. However, if you're -- if you're hosting for a lot of different users and -- and Ethernet is really important to the way you manage your data center, we have -- we have an excellent solution there that we just recently announced and it's called Spectrum X, where we're going to bring the capabilities, if you will, not all of it, but -- but some of it of the capabilities of InfiniBand, to Ethernet so that we can -- we can also, within the -- the environment of Ethernet, allow you to -- enable you to get excellent generative AI capabilities.

### Ben Reitzes, Melius Research, Analyst
50. My question is with regard to DGX Cloud. ⚑ uncertain

### Jensen Huang, President and Chief Executive Officer
51. DGX Cloud's strategy, let me start there. ⚑ uncertain
52. DGX Cloud's strategy is to -- to achieve several things: number one, to enable a really close partnership between us and the world's CSPs. ⚑ uncertain
53. We -- we recognize that -- that many of our -- we work with some 30,000 companies around the world, 15,000 of them are start-ups, thousands of them are generative AI companies.
54. And the fastest-growing segment, of course, is generative AI.
55. We're working with all of -- all of the world's AI start-ups.
56. And -- and so, we -- we built DGX Cloud as a footprint inside the world's leading clouds so that we could simultaneously work with all of our AI partners and help land them in -- easily in one of our cloud partners.
57. The second benefit is that it allows our CSPs and ourselves to work really closely together to improve the performance of hyperscale clouds, which is historically designed for multi-tenancy and not designed for high-performance distributed computing like generative AI.
58. And then, thirdly, of course, Nvidia uses very large infrastructures ourselves, and -- and our self-driving car team, our Nvidia research team, our generative AI team, our language model team.
59. And none of our -- none of our optimizing compilers are possible without our DGX systems. ⚑ uncertain
60. Even compilers these days require AI, and optimizing software and infrastructure software requires AI to -- to even develop.
61. It's been well publicized that our engineering uses AI to design our chips. ⚑ context-dependent
62. And so -- so, the internal -- our own consumption of AI, robotics team, so and so forth; Omniverse team, so on and so forth, all needs AI, and so -- all right?
63. So, our -- our internal consumption is quite large as well, and we land that in DGX Cloud. ⚑ uncertain
64. And it's a great way for us to engage and work closely with all of the AI ecosystem around the world.

### Colette Kress, Executive Vice President, Chief Financial Officer
65. And we are looking at NVIDIA AI Enterprise to be included with many of the products that we're selling, such as our DGX, such as our PCIe versions of our H100.

### Jensen Huang, President and Chief Executive Officer
66. The industry is simultaneously going through two platform transitions: accelerated computing and generative AI.
67. Accelerated computing enabled generative AI, which is now driving a platform shift in software and enabling new, never-before-possible applications.
68. Together, accelerated computing and generative AI are driving a broad-based computer industry platform shift.
69. Nvidia accelerates everything from data processing, training inference every AI model, real-time speech-to-computer vision, and giant recommenders to vector databases.
70. Nvidia has hundreds of millions of CUDA-compatible GPUs worldwide. ⚑ uncertain
71. Each has fundamentally unique computing models and ecosystems. ⚑ uncertain
72. Nvidia has achieved significant -- significant scale and is 100% invested in accelerated computing and generative AI.
73. We're upgrading and adding new products about every six months versus every two years to address the expanding universe of generative AI.
74. While we increase the output of H100 for training and inference of large language models, we're ramping up our new L40S universal GPU for scale -- for cloud scale-out and enterprise servers.
75. Spectrum X, which consists of our Ethernet switch, BlueField-3, supernet, and software helps customers who want the best possible AI performance on Ethernet infrastructures.
76. Customers are already working on next-generation, accelerated computing and generative AI with our Grace Hopper.
77. We're extending NVIDIA AI to the world's enterprises that demand generative AI but with the model privacy, security, and sovereignty.
78. Together with the world's leading enterprise IT companies, Accenture, Adobe, Getty, Hugging Face, Snowflake, ServiceNow, VMware, and WPP; and our enterprise system partners, Dell, HPE, and Lenovo, we are bringing generative AI to the world's enterprise.
79. We're building NVIDIA Omniverse to digitalize and enable the world's multi-trillion-dollar heavy industries to use generative AI to automate how they build and operate physical assets and achieve greater productivity.
80. Generative AI starts in the cloud, but the most significant opportunities are in the world's largest industries where companies can realize trillions of dollars of productivity gains.

## Borderline: automation/robotics without an AI term

1. [Q&A · Jensen Huang, President and Chief Executive Officer] Nvidia's in cloud's enterprise data centers, industrial edge, PCs, workstations, instruments, and robotics.

## Borderline: infrastructure without an AI term

1. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Let me first start with data center.
2. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] China's demand was within the historical range of 20% to 25% of our data center revenue, including compute and networking solutions.
3. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Given the strength of demand for our products worldwide, we do not anticipate that additional export restrictions on our data center GPUs, if adopted, would have an immediate material impact to our financial results.
4. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] However, over the long term, restrictions prohibiting the sale of our data center GPUs to China, if implemented, will result in a permanent loss of an opportunity for the U.S. industry to compete and lead in one of the world's largest markets.
5. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] L40S is not limited by co-op supply and is shipping to the world's leading server system makers.
6. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] It is also shipping to multiple supercomputing customers including Los Alamos National Labs and the Swiss National Computing Centre.
7. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] In addition, only InfiniBand can scale to hundreds of thousands of GPUs.
8. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Growth was fueled by GeForce RTX 40 series GPUs for laptops and desktops, and customer demand was solid and consistent with seasonality.
9. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] We have a large upgrade opportunity ahead of us, just 47% of our installed base have upgraded to RTX, and about 20% of a GPU with an RTX 3060 or higher performance.
10. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Laptop GPUs posted strong growth in the key back-to-school season led by RTX 4060 GPUs.
11. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Nvidia's GPU-powered laptops have gained in popularity, and their shipments are now outpacing desktop GPUs in several regions around the world.
12. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] In desktop, we launched the GeForce RTX 4060 and the GeForce RTX 4060 Ti GPUs, bringing the Ada Lovelace architecture down to price points as low as $299.
13. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] MediaTek will develop automotive SoCs and integrate a new product line of NVIDIA GPU chipsets.
14. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] GAAP gross margins expanded to 70.1% and non-GAAP gross margin to 71.2% driven by higher data center sales.
15. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Our data center products include a significant amount of software and complexity, which is also helping drive our gross margins.
16. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] Additionally, the new L40S GPU will help address the growing demand for many types of workloads from cloud to enterprise.
17. [Prepared remarks · Colette Kress, Executive Vice President, Chief Financial Officer] We expect sequential growth to be driven largely by data center, with gaming and pro vis also contributing.
18. [Q&A · Jensen Huang, President and Chief Executive Officer] The world has something along the lines of about $1 trillion worth of data centers installed in the cloud and enterprise and otherwise.
19. [Q&A · Jensen Huang, President and Chief Executive Officer] One is accelerated computing, and the reason for that is because it's the most cost-effective, most energy-effective, and the most performant way of doing computing now.
20. [Q&A · Jensen Huang, President and Chief Executive Officer] And this incredible application now gives everyone two reasons to transition, to do a platform shift from general purpose computing, the classical way of doing computing, to this new way of doing computing, accelerated computing.
21. [Q&A · Jensen Huang, President and Chief Executive Officer] There's about $1 trillion worth of data centers, call it, a quarter of trillion dollars of -- of capital spend each year.
22. [Q&A · Colette Kress, Executive Vice President, Chief Financial Officer] So, both of these things are the drivers of the revenue inside data center.
23. [Q&A · Colette Kress, Executive Vice President, Chief Financial Officer] The rest of the GPUs, we have new GPUs coming to market that we talk about, the L40S, and they will add continued growth going forward.
24. [Q&A · Jensen Huang, President and Chief Executive Officer] And it takes a supercomputer to test a supercomputer.
25. [Q&A · Jensen Huang, President and Chief Executive Officer] You can do this on any of our GPUs.
26. [Q&A · Jensen Huang, President and Chief Executive Officer] We have hundreds of millions of GPUs in the field and millions of GPUs in the cloud in just about every single cloud.
27. [Q&A · Jensen Huang, President and Chief Executive Officer] And it runs in a single GPU configuration as well as multi-GPU per compute or multi-node.
28. [Q&A · Jensen Huang, President and Chief Executive Officer] It also has multiple -- multiple sessions or multiple -- multiple computing instances per GPU.
29. [Q&A · Jensen Huang, President and Chief Executive Officer] So, from multiple instances per GPU to multiple GPUs, multiple nodes, to entire data center scale.
30. [Q&A · Jensen Huang, President and Chief Executive Officer] And that's just one example of what it would take to get accelerated computing to work that the number of -- of code combinations and type of application combinations is really quite insane.
31. [Q&A · Jensen Huang, President and Chief Executive Officer] You can get multiple GPUs in a -- in a server.
32. [Q&A · Jensen Huang, President and Chief Executive Officer] It's designed for -- for hyperscale scale-out, meaning it's easy to -- to -- to install L40S servers into the world's hyperscale data centers.
33. [Q&A · Jensen Huang, President and Chief Executive Officer] It comes in a standard rack, standard server.
34. [Q&A · Jensen Huang, President and Chief Executive Officer] And we're already planning the next-generation infrastructure with the leading CSPs and data center builders.
35. [Q&A · Jensen Huang, President and Chief Executive Officer] The demand -- the easiest way to think about the demand is the world is transitioning from general-purpose computing to accelerated computing.
36. [Q&A · Jensen Huang, President and Chief Executive Officer] Because by doing that, you're going to offload so much workload off of the CPUs that the available CPUs is -- in your data center will get boosted.
37. [Q&A · Jensen Huang, President and Chief Executive Officer] This isn't a -- a singular application that -- that is driving the demand, but this is a new computing platform, if you will, a new computing transition that's happening, and data centers all over the world are responding to this and shifting, you know, in a broad-based way.
38. [Q&A · Toshi Hari, Goldman Sachs, Analyst] Colette, I think, last quarter, you had said CSPs were about 40% of your data center revenue; consumer internet, 30%; enterprise, 30%.
39. [Q&A · Toshi Hari, Goldman Sachs, Analyst] Curious, you know, if there's enough breadth and depth there to -- to support a sustained increase in your data center business going forward.
40. [Q&A · Colette Kress, Executive Vice President, Chief Financial Officer] So, thank you on the question regarding our types of customers that we have in our data center business, and we look at it in terms of combining our compute as well as our networking together.
41. [Q&A · Jensen Huang, President and Chief Executive Officer] It's called accelerated computing.
42. [Q&A · Jensen Huang, President and Chief Executive Officer] But accelerated computing could be used for all kinds of different applications that's already in the data center.
43. [Q&A · Jensen Huang, President and Chief Executive Officer] And so, I think -- I think the data centers around the world recognize that this is the -- the best way to deploy resources, deploy capital going forward for data centers.
44. [Q&A · Jensen Huang, President and Chief Executive Officer] This is true for the world's clouds, and -- and -- and you're seeing a whole crop of -- of new GPUs -- specialty GPU-specialized cloud service providers.
45. [Q&A · Jensen Huang, President and Chief Executive Officer] But in order for enterprises to do it, you have to support the management system, the operating system, the security, and software -- software-defined data center approach of enterprises, and that's called VMware.
46. [Q&A · Jensen Huang, President and Chief Executive Officer] And we've been working several years with VMware to make it possible for VMware to support, not just the virtualization of CPUs, but the virtualization of GPUs as well as the distributed computing capabilities of GPUs, supporting NVIDIA's BlueField for high-performance networking.
47. [Q&A · Tim Arcuri, UBS, Analyst] Can you talk about the attach rate of your networking solutions to your -- to -- to the compute that you're shipping?
48. [Q&A · Tim Arcuri, UBS, Analyst] In other words, is -- is like half of your compute shipping with your networking solutions, you know, more than half, less than half, and is this something that maybe you can use to prioritize allocation of the -- of -- of the GPUs?
49. [Q&A · Jensen Huang, President and Chief Executive Officer] Well, working backwards, we don't use that to prioritize the allocation of our GPUs.
50. [Q&A · Jensen Huang, President and Chief Executive Officer] And for the customers that are building very large infrastructure, InfiniBand is, you know, I hate to say it, kind of a no-brainer.
51. [Q&A · Jensen Huang, President and Chief Executive Officer] You know, some 10, 15, 20% higher throughput for $1 billion infrastructure translates to enormous savings.
52. [Q&A · Jensen Huang, President and Chief Executive Officer] You know, the amount of infrastructure that we need is quite -- quite significant.
53. [Q&A · Colette Kress, Executive Vice President, Chief Financial Officer] Remember, software is a part of almost all of our products, whether they are data center products, GPUs, systems, or any of our products within gaming and our future automotive products.
54. [Q&A · Jensen Huang, President and Chief Executive Officer] Data centers are making a platform shift from general-purpose to accelerated computing.
55. [Q&A · Jensen Huang, President and Chief Executive Officer] The trillion dollars of global data centers will transition to accelerated computing to achieve an order of magnitude better performance, energy efficiency, and cost.
56. [Q&A · Jensen Huang, President and Chief Executive Officer] The performance and versatility of our architecture translates to the lowest data center TCO, and best energy efficiency.
