# Progressive Corporation — 2024_Q4 Earnings Call (transcript)

- **Company:** Progressive Corporation (PGR); fiscal year ends December (SEC fiscalYearEnd 1231)
- **Ticker:** PGR
- **CIK:** 0000080661
- **Period:** 2024_Q4 (call held March 4, 2025; date from page date line)
- **Calendar quarter:** 2024 Q4 (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)
- **Source:** third-party transcript, The Motley Fool — https://www.fool.com/earnings/call-transcripts/2025/03/04/progressive-pgr-q4-2024-earnings-call-transcript/
- **Source type:** third_party_transcript_motley_fool
- **Retrieved:** 2026-10-28 (S&P 493 pull, half 1)
- **Source SHA-256:** 2dd5f9f80a6a15358704a5989b8e24224c72ab6726a31901825d8c76c11ac2f7
- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, HTML unescaped, tags stripped (sp493/sp493_pull.py)
- **Note:** official company transcripts were not searched for in this pull. Fool transcripts have speaker labels but are third-party (minor errors possible); fine for private research, check terms before redistributing
- **Filter:** AI-sentence extraction, see FILTER_METHOD.md

---

**26 AI sentences of 584 total**
(Borderline, listed at the end: 3 automation/robotics, 0 infrastructure, none containing an AI term.)

## Prepared remarks

### John Murphy, Claims President
1. In prior presentations, we've discussed our ability to rapidly deploy risk selection and new product models, our segmentation excellence, as well as efficient media and agency compensation each of which has had a positive impact on rate competitiveness. ⚑ uncertain

### Matt White, Business Leader, Claims Data and Analytics
2. In this case, we're using machine vision models, alongside a variety of other technologies, to help us automate parts of the photo estimating process. ⚑ uncertain
3. At a high level, we're using deep learning models or neural networks, alongside more traditional machine learning techniques, to look at customer-submitted photos like the example on the left, identify the correct parts through segmentation masks, and then identify the location and type of damage by part.
4. These models use transformer architectures you may have heard about, quite literally the second T in ChatGPT, but they are trained very differently than some of the models making headlines more recently. ⚑ context-dependent
5. These are supervised models that we train on our photos and our own curated data to ensure accuracy consistent with Progressive's estimating standards. ⚑ uncertain ⚑ context-dependent
6. Such models all benefit from very large, clean, and diverse data sets. ⚑ uncertain
7. You need to be able to distinguish between such things as upper and lower bumper covers depending on the year, make, and model. ⚑ uncertain
8. We continue to iterate and refine our models and approach until such time that we were convinced one of the efficiency gains and, two, that we were able to generate equal or better accuracy results. ⚑ uncertain
9. Beyond our people's efficiency, we also work to make our model training more efficient.
10. This is the practice of training a model on a small set of label data to label the rest of the data. ⚑ context-dependent
11. Our process starts with our original segmentation model capable of identifying major parts such as doors and quarter panels. ⚑ uncertain
12. From this base model trained on subject matter experts labels, pseudo-labels are generated on a much larger data set to create an initial base model that's even better at those major parts. ⚑ uncertain
13. This improved base model is then fine-tuned with even more detailed part labels from a diverse set of vehicles. ⚑ uncertain ⚑ context-dependent
14. This new part segmentation model is a general template model that works reasonably well on all vehicles. ⚑ uncertain ⚑ context-dependent
15. But to ensure the most accurate outcome, we customize the model further for specific vehicle makes and models. ⚑ uncertain
16. For computational efficiency, we then fine-tune the model with a technique called low-rank adaptation or LoRA. ⚑ uncertain
17. LoRA allows us to efficiently adapt large models to specific tasks, enhancing precision without needing as much training data or training time. ⚑ uncertain
18. It allows us to transform two-dimensional images into dynamic three-dimensional models. ⚑ uncertain ⚑ context-dependent
19. Some research scientists have suggested that what large language models are to text, Gaussian Splatting is to graphics and reconstruction.
20. In parallel with understanding camera position, algorithmic techniques such as structure from motion, create a point cloud or mesh of the vehicle. ⚑ uncertain
21. What's ultimately produced is a fully interactive 3D model of the vehicle. ⚑ uncertain

## Q&A

### Susan Patricia Griffith, President and Chief Executive Officer
1. Now, those will ultimately change, and we'll be able to kind of flex our models. ⚑ uncertain
2. We have a bunch of models. ⚑ uncertain
3. We were able to flex those models every time we get a new piece of data or the data changes. ⚑ uncertain

### Susan Patricia Griffith, President and Chief Executive Officer
4. We will build a diverse portfolio of products with partner agents who understand our underwriting strategy and proactively support it. ⚑ uncertain
5. And then really agent alignment, holding our agent partners to volume and quality bundles, and we have very specific expectations for our agents. ⚑ uncertain

## Borderline: automation/robotics without an AI term

1. [Prepared remarks · Matt White, Business Leader, Claims Data and Analytics] While it has been a multiyear journey, the combination of data science and other automation techniques have now doubled the productivity of what, as I mentioned, was already our most efficient means of vehicle inspection and estimating.
2. [Prepared remarks · Matt White, Business Leader, Claims Data and Analytics] To be clear, this is not full automation or straight through processing that you may see referenced across the industry.
3. [Prepared remarks · Matt White, Business Leader, Claims Data and Analytics] We do think full automation is possible at some point, but we won't do that until we're sure we can do it consistent with our guiding principles and, of course, applicable regulations.

## Borderline: infrastructure without an AI term

_None._
