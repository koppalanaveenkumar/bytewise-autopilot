# ByteWise daily video playbook

For the scheduled runs. Channel: ByteWise (@heybytewise), YouTube + Instagram, India audience, faceless, English only, voice only (no music, no sound effects).

Never publish, post, upload or schedule anything. Never call vidIQ account, publishing or scheduling tools. Never spend vidIQ or Higgsfield credits. Never print or save the Pixabay key anywhere; it comes in the task prompt and only goes into the PIXABAY_KEY environment variable.

## 0. Setup (every run, fresh workspace)

```bash
git clone --depth 1 https://github.com/koppalanaveenkumar/bytewise-autopilot /tmp/bw
BW=/tmp/bw; bash $BW/setup.sh
W=/tmp/work; mkdir -p $W/out; cd $W
```

Each tool's first lines say how to use it.

## 1. Morning news (7 stories, about 2 minutes, ready by 7:00 IST)

1. **Research.** Search the web for the last 24-36 hours of tech and AI news. Pick 7 stories a beginner cares about. Prefer big names, money, safety, India relevance, and anything with strong visuals. Verify every number and claim in at least one reliable source. Anthropic stories: strictly factual, no opinion. No rumours stated as facts ("reports say" for unconfirmed deals).
2. **Script** (`el_script.txt`, one paragraph per story, blank line between):
   - Paragraph 1, the hook: ONE topic only. Use the most visual story in 1-2 short sentences. Then a bridge: "That's one of seven big tech stories for your <Weekday>."
   - Paragraphs 2-8: one story each, 3-5 short sentences, simple English, zero jargon.
   - Last paragraph: "Which story surprised you most? Tell me in the comments. And follow for simple tech news every morning."
   - No numbering anywhere: no "story one", no "comment one to seven".
   - First person singular only ("me", "I"), never "we"/"us".
   - Put pronunciation fixes in `say.json`, for example {"1859": "eighteen fifty-nine", "FAA": "F A A"}.
3. **Voice + timings:** `python3 $BW/tools/gen.py && python3 $BW/tools/export.py`
4. **Footage:**
   - `PIXABAY_KEY=... python3 $BW/tools/search.py "query" ...`. Use 2 queries per story, plus one for the hook and the ending.
   - Look at the `px/sheet_*.jpg` contact sheets.
   - Pick real, relevant clips. Never put an identifiable person next to accusatory text (hack, scam, cheat, fired). No branded logos you would have to draw.
   - Write `plan.json`. Segments cover 0 to the end of the voice timeline, 1-2 clips per story, with a montage of all stories during the hook's bridge sentence. Then run `python3 $BW/tools/bg.py`.
5. **Scenes:**
   - Copy `$BW/engine/example_news_scenes.js` to `$W/scenes.js` and rewrite `S[0]..S[8]` for today's stories. Keep `TILES` as short headline labels (no numbers), `header`, `hit(...)`, `footage()` and `renderAt` as they are.
   - Use `W("word", para)` to time visuals to the voice. A key visual must not start on a story's last word, and must stay 2+ seconds on screen.
   - Build: `python3 $BW/tools/build_page.py $W $W/scenes.js`
6. **HOOK CHECKLIST.** Check this on stills before the full render: `python3 $BW/tools/rec.py $W 8800 stills 0 1 2.5 4 6 ...` (one per story), then open `/tmp/nw_*.jpg` and look at them.
   - [ ] Frame 0 is full and something is already moving (real footage plus animation). No static text card, no date line, no story grid.
   - [ ] Opening text is 2 short lines at most.
   - [ ] The first 4-5 seconds are about ONE topic only.
   - [ ] No text overlaps, nothing cut off at the edges, captions readable.
   - [ ] No numbers or story counters on screen.
7. **Render:** `bash $BW/tools/render.sh $W $W/out/tech-news-<mon><dd>.mp4`. This takes about 25 minutes on 2 CPUs. Then spot-check 4 frames from the finished file.
8. **Thumbnail:**
   - Base it on `tools/thumbs_example.py`.
   - Use a REAL photo frame from one of today's clips, full-bleed, graded.
   - At most 3 big words, with a TOPIC tag pill, plus the logo badge.
   - Make 2 options for the two strongest stories and recommend one.
9. **Text to paste:**
   - YouTube title that matches the hook and the recommended thumbnail (no date).
   - Description: 2-line summary, then • bullets (no numbering), then "Follow for simple tech news every morning." and #technews #ai #shorts.
   - About 15 tags.
   - Instagram caption ending with: #explorepage #foryou #fyp #viralreels #trendingnow

## 2. Evening explainer Short (about 45-50 seconds, ready by 18:00 IST)

- Pick the hottest tech topic of the day; the user says yesterday's topic got more reach. Title format: "What is X? Explained Simply" (no date, no hashtags in the title).
- Script: hook in the first 2 seconds, one idea, simple English, 5-6 short paragraphs (one per scene). End with "Follow for more simple tech explained".
- Same engine and same steps (voice, footage, scenes, checklist, render). Use about 6 scenes, with the header text "EXPLAINED SIMPLY".
- Thumbnail rules are the same as the news.

## 3. Python for Beginners episode (weekly)

- The next episode number is one after the last delivered episode (Ep11 was "Classes and Objects"). The title format is "Python for Beginners | Episode N - Explained Simply".
- `reference/python_episode/` has the Episode 11 build scripts (1440p widescreen, code windows with typing, output panel, LEARN tag). Adapt their paths to $W.
- Run every code example in Python before it goes in the script.
- Deliver the video, an English .srt and a thumbnail.

## Style rules (all formats)

- Realistic: real stock footage behind everything, darkened at the top and bottom, plus motion graphics on top. No cartoon, anime or voxel characters. No drawn company logos.
- The logo badge is always at the top left. The first frame is always full.
- No music, no transition sounds.
- Don't name subjects like biology, commerce or arts.

## Delivering

- Send the video, the thumbnail options and the pasteable text with SendUserFile and a message, so the user gets a phone notification.
- End with: "Reply 'post it' to publish, or tell me what to change." If the user replies "post it" in that run's chat, publishing still needs their YouTube and Instagram accounts connected in vidIQ and the video at a public URL. If either is missing, say so instead of trying.
